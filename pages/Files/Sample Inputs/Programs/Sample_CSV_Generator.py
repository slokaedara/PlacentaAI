import numpy as np
import pandas as pd

# Set random seed for consistent results
np.random.seed(42)

num_samples = 1000
num_features = 500

feature_columns = [f"ENSG{10000000000 + i}" for i in range(1, num_features + 1)]

conditions = ["Normal", "Preeclampsia", "GDM", "Placental_Abruption"]
probabilities = [0.70, 0.10, 0.10, 0.10]

# Generate conditions based on target 70/10/10/10 ratio
sample_conditions = np.random.choice(
    conditions, size=num_samples, p=probabilities
)

data = []

for condition in sample_conditions:
    expr = np.random.exponential(scale=50, size=num_features)

    if condition == "Preeclampsia":
        expr[:20] *= np.random.uniform(8.0, 15.0, size=20)
        expr[20:100] *= np.random.uniform(2.0, 4.0, size=80)

    elif condition == "GDM":
        expr[200:220] *= np.random.uniform(6.0, 12.0, size=20)
        expr[220:280] *= np.random.uniform(1.8, 3.5, size=60)

    elif condition == "Placental_Abruption":
        expr[400:420] *= np.random.uniform(7.0, 14.0, size=20)
        expr[420:480] *= np.random.uniform(2.0, 4.0, size=60)

    data.append(np.round(expr, 1))

sample_ids = [f"Sample_{i+1:03d}" for i in range(num_samples)]

# 1. Feature DataFrame (Model Input ONLY - No Condition)
df_features = pd.DataFrame(data, columns=feature_columns)
df_features.insert(0, "Sample_ID", sample_ids)

# 2. Ground Truth DataFrame (Labels ONLY)
df_labels = pd.DataFrame(
    {"Sample_ID": sample_ids, "True_Condition": sample_conditions}
)

# Save unlabelled feature matrix for model input
with open("../eval_features.csv", "w") as f:
    f.write("!Project=Placenta Health Assessment\n")
    f.write("!Technology=Cell-Free RNA Sequencing (cfRNA-seq) Evaluation Set\n")
    df_features.to_csv(f, index=False)

# Save ground truth labels separately
df_labels.to_csv("ground_truth_labels.csv", index=False)

print("Generated 'eval_features.csv' (500 features, unlabeled input)")
print("Generated 'ground_truth_labels.csv' (Actual target conditions)")