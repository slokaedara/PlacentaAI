import numpy as np
import pandas as pd

# Step 1: Load reference dataset
df_source = pd.read_csv("../combined10.csv")

# Step 2: Extract gene features only
gene_columns = [col for col in df_source.columns if col != "Unnamed: 0" and col != "SBNO2"]

# Step 3: Set simulation parameters
np.random.seed(42)
num_samples = 50

# Step 4: Calculate mean and std per feature
gene_means = np.nan_to_num(
    df_source[gene_columns].mean(axis=0).values, nan=10.0
)
gene_stds = np.nan_to_num(df_source[gene_columns].std(axis=0).values, nan=1.0)

# Step 5: Allocate memory matrix
synthetic_matrix = np.zeros((num_samples, len(gene_columns)))

# Step 6: Generate values column by column
for j in range(len(gene_columns)):
    mean_val = gene_means[j]
    std_val = max(gene_stds[j], mean_val * 0.1, 1.0)
    values = np.random.normal(loc=mean_val, scale=std_val, size=num_samples)
    synthetic_matrix[:, j] = np.clip(np.round(values), 0, None)

# Step 7: Export clean matrix
gene_only_df = pd.DataFrame(synthetic_matrix, columns=gene_columns)
row_names = []
i = 0

for j in range(len(gene_only_df)):
    row_names.append(f"Sample_{j + 1}")

col1 = pd.DataFrame(row_names)
final_df = pd.concat([col1, gene_only_df], axis = 1)
final_df.to_csv("maternal_plasma_cfrna_input_final.csv", index=False)