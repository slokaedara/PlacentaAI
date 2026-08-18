import joblib
import pandas as pd
import numpy as np
import streamlit as st
import io

# 1. Load ALL required components (not just the model)
# These must match the files saved during training
model = joblib.load('/content/drive/MyDrive/Placenta_AI/model/placenta_model.pkl')
scaler = joblib.load('/content/drive/MyDrive/Placenta_AI/model/scaler.pkl')
selector = joblib.load('/content/drive/MyDrive/Placenta_AI/model/selector.pkl')
encoder = joblib.load('/content/drive/MyDrive/Placenta_AI/model/label_encoder.pkl')
all_genes = joblib.load('/content/drive/MyDrive/Placenta_AI/model/selected_genes.pkl') # Or gene_columns.pkl

def run_inference(user_df):
    try:
        # Step A: Ensure columns match training (fill missing with 0, drop others)
        # Note: 'X.columns' from your training state is required here
        existing_genes = [col for col in X.columns if col in user_df.columns]
        processed_df = pd.DataFrame(index=user_df.index, columns=X.columns).fillna(0)
        processed_df[existing_genes] = user_df[existing_genes]

        # Step B: Log2 Transformation (Crucial for gene expression data)
        processed_df = np.log2(processed_df.astype(float) + 1)

        # Step C: Scaling
        scaled_data = scaler.transform(processed_df)

        # Step D: Feature Selection (Reducing to the top 500)
        selected_data = selector.transform(scaled_data)

        # Step E: Prediction
        probs = model.predict_proba(selected_data)[0]
        prediction_idx = np.argmax(probs)
        label = encoder.inverse_transform([prediction_idx])[0]

        return label, probs
    except Exception as e:
        return f"Error during preprocessing: {e}", None


#Actual Thing
text_enter = st.chat_input("Enter the text-based results of your cfRNA-seq test here.")
upload_enter = st.file_uploader("Upload CSV or TSV cfRNA-seq test results here", type=["csv", "tsv"])

print("running prediction on input")
prediction = model.predict(user_data)
st.subheader("Prediction Results")
st.write(prediction)
