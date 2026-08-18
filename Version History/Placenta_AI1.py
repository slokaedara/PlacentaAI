import pickle
import streamlit as st
import pandas as pd
from streamlit.web.bootstrap import run
from io import StringIO

with open("../placenta_model.pkl", "rb") as file:
    model = pickle.load(file)

#Actual Thing
text_enter = st.chat_input("Enter the text-based results of your cfRNA-seq test here.")
upload_enter = st.file_uploader("Upload CSV or TSV cfRNA-seq test results here", type=["csv", "tsv"])

user_data = None
#find out a way to keep the screen blank until the if statements bc otherwise we get an error thrown bc none
if text_enter:
    user_data = pd.read_csv(StringIO(text_enter), sep=',', comment='!', header=0, index_col=0)
    print("reading done")
elif upload_enter:
    if upload_enter.type == "text/csv":
        user_data = pd.read_csv(upload_enter, sep=',', comment='!', header=0, index_col=0, low_memory=False)
        print("reading done")
    elif upload_enter.type == "text/tsv":
        user_data = pd.read_csv(upload_enter, sep='\t', comment='!', header=0, index_col=0, low_memory=False)
        print("reading done")
    else:
        exit("Error: unsupported file type")

print("running prediction on input")
prediction = model.predict(user_data)
st.subheader("Prediction Results")
st.write(prediction)

print("done prediction")