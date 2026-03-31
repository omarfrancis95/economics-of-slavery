from pathlib import Path
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import numpy as np
# ---------------------------------
# 1. File paths
# ---------------------------------
project_root = Path.cwd()
file_1860 = project_root / "1860 census data on slavery.csv"
file_1900 = project_root / "1900 census data.csv"

# ---------------------------------
# 2. Load data
# ---------------------------------
df1860 = pd.read_csv(file_1860)
df1900 = pd.read_csv(file_1900)

# ---------------------------------
# 3. Chose needed columns
# ---------------------------------
df1860 = df1860[
    ["STATE", "total_enslaved", "farms_per_capita", "state_population", "slaves_per_capita"]
].copy()

df1900 = df1900[
    ["STATE", "state_population", "total_capital_invested_manufacturing", "manufacture_k_per_capita"]
].copy()

# Renamed population columns
df1860 = df1860.rename(columns={"state_population": "state_population_1860"})
df1900 = df1900.rename(columns={"state_population": "state_population_1900"})

# ---------------------------------
# 4. Clean state names
# ---------------------------------
df1860["STATE"] = df1860["STATE"].astype(str).str.strip()
df1900["STATE"] = df1900["STATE"].astype(str).str.strip()

# ---------------------------------
# 5. Filled missing enslaved with 0
# ---------------------------------
df1860["total_enslaved"] = df1860["total_enslaved"].fillna(0)

# ---------------------------------
# 6. Merged datasets
# ---------------------------------
df = pd.merge(df1860, df1900, on="STATE", how="inner")

# ---------------------------------
# 7. Regression dataset
# ---------------------------------
df_model = df[
    [
        "STATE",
        "slaves_per_capita",
        "farms_per_capita",
        "manufacture_k_per_capita"
    ]
].dropna().copy()

print("Number of observations:", len(df_model))
print(df_model.head())

# ---------------------------------
# 8. Ran regression
# ---------------------------------
model = smf.ols(
    formula="manufacture_k_per_capita ~ slaves_per_capita + farms_per_capita",
    data=df_model
).fit()

print("\nOLS RESULTS")
print(model.summary())

# ---------------------------------
# 9. Robust standard errors
# ---------------------------------
robust_model = model.get_robustcov_results(cov_type="HC1")

print("\nROBUST STANDARD ERRORS")
print(robust_model.summary())

# ---------------------------------
# 10. Save outputs
# ---------------------------------
output_dir = project_root / "output"
output_dir.mkdir(exist_ok=True)

df_model.to_csv(output_dir / "merged_regression_data.csv", index=False)

with open(output_dir / "python_results.txt", "w") as f:
    f.write(model.summary().as_text())
    f.write("\n\nROBUST:\n")
    f.write(robust_model.summary().as_text())

print("\nSaved results to /output folder")




# LOAD FILE (adjust path if needed)
df = pd.read_csv("output/merged_regression_data.csv")

# CHECK COLUMN NAMES (VERY IMPORTANT)
print(df.columns)

# SCATTER PLOT
plt.figure()
plt.scatter(df["slaves_per_capita"], df["manufacture_k_per_capita"])

# TREND LINE
m, b = np.polyfit(df["slaves_per_capita"], df["manufacture_k_per_capita"], 1)
plt.plot(df["slaves_per_capita"], m * df["slaves_per_capita"] + b)

# LABELS
plt.xlabel("Slaves per Capita")
plt.ylabel("Manufacturing Capital per Capita")
plt.title("Slavery vs Industrial Development")

plt.show()