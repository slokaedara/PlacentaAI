import streamlit as st

st.header("Placenta_AI")
st.write("Mission: To create an open-access site that medical labs can use to translate maternal blood samples "
         "into precise risk percentages for three major placenta-associated syndromes, giving physicians a more\n"
         "specific idea of how severe their patients condition is and, by extension, what treatments should be\n"
         "carried out.")
st.space("medium")

st.subheader(f"⚠️ Accuracy Disclaimer ⚠️\n")
st.write(
    "\nKeep the following information on accuracy in mind when utilizing this model:\n"
    "- Placenta_AI has an accuracy percentage of roughly 80.42%.\n"
    "- All training data is sourced from the NIH's GEO (Gene Expression Omnibus)\n"
    "- However, data on placental abruption is sourced from a maternal chemical exposure dataset. The\n"
    "  dataset analyzes gene expression in those exposed to certain chemicals versus those who were not.\n"
    "  Placental abruption can be a result of this, but this study was not specific to abruption."
    "  Consider this when you receive your abruption risk assessment.\n"
    "- Your risk assessments for GDM and preeclampsia are specific to the conditions themselves.\n"
    "- Only the 500 most informative genes from the CSV you input into the model will be considered for risk\n"
    "  assessment. This is in the interest of model efficiency and alignment with the training data.\n"
    "  Additionally, if any of your genes were not found in the training data, the model will not recognize\n"
    "  them. To prevent confusion, such genes will be dropped. Any genes not present in your data that\n"
    "  were present in the model's training data will be added with expression values of 0.")
st.space("small")

st.subheader("🛠 ️Workings of the Model 🛠\n")
st.write(
    "\nWhen you input your data into this model, it first examines its own training data and then your\n"
    "upload. After making some modifications to align your data with the data it was trained on, it generates\n"
    "your susceptibility to each individual condition as well as perfect health based on this.")