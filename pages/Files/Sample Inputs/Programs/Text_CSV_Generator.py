import pandas as pd

# 1. Load the original file
df = pd.read_csv("../maternal_plasma_cfrna_results2.csv")

# 2. Fix the sample column header from '0' to 'Sample_ID'
if "0" in df.columns:
    df = df.rename(columns={"0": "Sample_ID"})

# 3. Convert the ENTIRE table (all 50 rows & 13,577 columns) into plain text CSV
full_csv_plain_text = df.to_csv(index=False)

# 4. Save the full plain text directly to a .txt or .csv file
with open("../maternal_plasma_cfrna_FULL_PLAIN_TEXT.txt", "w") as f:
    f.write(full_csv_plain_text)

print("Successfully converted the entire dataset into plain text!")
print(f"Total Rows: {len(df)}")
print(f"Total Columns: {len(df.columns)}")