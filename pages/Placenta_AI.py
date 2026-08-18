import pickle
import random
import streamlit as st
import pandas as pd
from io import StringIO
import numpy as np
import joblib
from sklearn.feature_selection import SelectKBest, f_classif

VALID_SAMPLE_FRACTION = 0.5

#Setting decimal default as 2 places
pd.options.display.float_format = "{:.2f}".format

#Creating list of columns in training data
training = pd.read_csv("pages/Files/Sample Inputs/combined_dataset_final.csv")
training_cols = [col for col in training.columns if col != training.columns[0] and col != "Disease"]
    #We know it has a header, so we omit the first column

#Loading Files:
with open("pages/Files/Pkl_Pickle_Files/placenta_model4.pkl", "rb") as file:
    model = joblib.load(file)

with open("pages/Files/Pkl_Pickle_Files/scaler4.pkl", "rb") as file:
    scaler = joblib.load(file)

with open("pages/Files/Pkl_Pickle_Files/selector4.pkl", "rb") as file:
    selector = joblib.load(file)

with open("pages/Files/Pkl_Pickle_Files/label_encoder4.pkl", "rb") as file:
    labels = joblib.load(file)

#Actual Thing
text_enter = st.chat_input("Enter the text-based CSV or space-separated results of your cfRNA-seq test here.")
upload_enter = st.file_uploader("Upload CSV or TSV cfRNA-seq test results here", type=["csv", "tsv"])

user_data = None

if text_enter:
    user_data = pd.read_csv(StringIO(text_enter), sep=r'[,\s]', comment='!', header=0, index_col=0)
    print("reading done")
    file_name = f"Placenta_AI_Results_{random.randint(1, 100)}"
elif upload_enter:
    if upload_enter.type == "text/csv":
        user_data = pd.read_csv(upload_enter, sep=',', comment='!', header=0, index_col=0, low_memory=False)
        print("reading done")
    elif upload_enter.type == "text/tsv":
        user_data = pd.read_csv(upload_enter, sep='\t', comment='!', header=0, index_col=0, low_memory=False)
        print("reading done")
    else:
        exit("Error: unsupported file type")
    file_name = f"Results_{upload_enter.name}"



selected_mask = selector.get_support()
best_500_cols = pd.Index(training_cols)[selected_mask]

print(f"Successfully retrieved {len(best_500_cols)} columns.")
print("Top 10 columns:", best_500_cols[:10])

if user_data is not None:
    if len(user_data) < 1:
        st.write(f":red[Expected at least 1 sample in the input data aside from header, found only 0. Please try again\n"
                 f"with at least 1 sample and a header row.]")
    else:
        original_user_cols = set(user_data.columns)
        common_col_count = len(original_user_cols.intersection(best_500_cols))
        if common_col_count < 1/2 * len(best_500_cols):
            st.write(f":red[Expected at least 250 relevant genes, found only {common_col_count}. Please try again with\n"
                 f"relevant genes.]")
        else:
            #Reindexing columns of user data as per training data columns
            #Reordering occurs
            #If the user_data is missing certain columns, they are added and listed as NaN
            #If the user_data has extra columns not present in the training data, they are dropped
            user_data = user_data.reindex(columns=training_cols)
            #NaN is replaced with 0 (the neutral value for this model)
            user_data = user_data.fillna(0)

            #Change User Data:
            user_data = np.log2(user_data + 1)
            user_data_scaled = scaler.fit_transform(user_data)
            user_data_selected = selector.transform(user_data_scaled)

            print("running prediction on input")
            all_sample_probabilities = model.predict_proba(
                user_data_selected
            )

            st.subheader("Prediction Results")
            all_results = []
            for probabilities in all_sample_probabilities:
                results = {}

                for disease, probability in zip(
                        labels.classes_,
                        probabilities
                ):
                    results[disease] = round(
                        probability * 100,
                        2
                    )

                # Sort highest probability first
                results = dict(
                    sorted(
                        results.items(),
                        key=lambda x: x[1],
                        reverse=True
                    )
                )
                all_results.append(results)
            results_df = pd.DataFrame(all_results)
            #how does the dict —> list —> df sequence work
            results_df.index = user_data.index
            results_df.index.name = "Sample Names"
            proper_names = ["GDM", "Placental_Abruption", "Preeclampsia", "Healthy"]
            results_df = results_df.reindex(columns = proper_names)
            #is the header just the column that we omitted initially
            st.table(results_df.style.format("{:.2f}%"))
            def convert_to_csv(results_df):
                return results_df.to_csv(index = True).encode("utf-8-sig")
            csv_results = convert_to_csv(results_df)
            st.download_button(
                label = "Download Results",
                data = csv_results,
                file_name = file_name,
                mime = "text/csv"
            )
            print("done predictions")

            st.space("medium")
            st.subheader("Result Explanation")
            st.write("- Each percentage represents the probability of that condition for the corresponding sample\n"
                     "- Your percentage for 'GDM' represents the likelihood that you have Gestational Diabetes Mellitus,\n"
                     "  a high blood sugar condition originating during pregnancy. For more information, please visit this\n"
                     "  [link](https://www.hopkinsmedicine.org/health/conditions-and-diseases/diabetes/gestational-diabetes).\n"
                     "- Your percentage for 'Placental_Abruption' represents your likelihood of experiencing a condition in which\n"
                     "  the placenta peels away prematurely, restricting nutrient flow to the fetus. This may require urgent\n"
                     "  medical intervention. For more information, please visit this [link](https://www.mayoclinic.org/diseases-conditions/placental-abruption/symptoms-causes/syc-20376458).\n"
                     "- Your percentage for 'Preeclampsia' represents your likelihood of a high blood pressure condition that\n"
                     "  can restrict blood flow to the placenta, weakening nutrient flow to the fetus. For more information, \n"
                     "  please visit this [link](https://www.mayoclinic.org/diseases-conditions/preeclampsia/symptoms-causes/syc-20355745).\n"
                     "- Your percentage for 'Healthy' represents the likelihood that you have none of the three conditions\n"
                     "  listed above but does not necessarily mean that you do not have others.\n")