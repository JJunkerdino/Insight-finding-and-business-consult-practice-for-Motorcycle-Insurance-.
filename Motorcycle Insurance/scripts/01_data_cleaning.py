"""01 - Data Cleaning: Motorcycle Insurance

Load the raw data, rename columns to clear English names, check data
quality, and save a cleaned version for the next scripts.
"""

from pathlib import Path

import pandas as pd

RAW_PATH = Path("../data/raw/Motorcycle Insurance.xlsx")
PROCESSED_DIR = Path("../data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

df_raw = pd.read_excel(RAW_PATH)
print(df_raw.shape)
print(df_raw.head())

# --- 1. Look at the original columns ---
# The raw file uses short Swedish variable codes. Check the shape, types,
# and summary stats before touching anything.
print("Columns:", list(df_raw.columns))
print(df_raw.dtypes)
print(df_raw.describe(include="all").T)

# --- 2. Rename columns to clear English names ---
# The original column names are short Swedish codes (agarald, kon,
# skadkost, ...). Renaming them makes the analysis readable for anyone,
# without needing the data dictionary open next to it.
rename_map = {
    "rownames": "policy_id",
    "agarald": "owner_age",
    "kon": "gender",
    "zon": "zone",
    "mcklass": "vehicle_class",
    "fordald": "vehicle_age",
    "bonuskl": "bonus_class",
    "duration": "duration_years",
    "antskad": "claim_count",
    "skadkost": "claim_cost",
}

df = df_raw.rename(columns=rename_map)

# M = "Man", K = "Kvinna" (Swedish for woman) -> spell them out for readability
df["gender"] = df["gender"].map({"M": "Male", "K": "Female"})

print(df.head())

# --- 3. Data quality checks ---
# Before trusting this data, check for missing values, duplicates, and any
# values outside the expected ranges from the data description.
print("Missing values per column:")
print(df.isnull().sum())
print("Duplicate rows (ignoring policy_id):", df.drop(columns=["policy_id"]).duplicated().sum())
print("gender counts:\n", df["gender"].value_counts())
for col in ["zone", "vehicle_class", "bonus_class"]:
    print(f"{col} unique values:", sorted(df[col].unique()))
print("owner_age range:", df["owner_age"].min(), "-", df["owner_age"].max())
print("vehicle_age range:", df["vehicle_age"].min(), "-", df["vehicle_age"].max())
print("claim_count value counts:\n", df["claim_count"].value_counts())

# --- 4. Known data issues to flag ---
# - duration_years == 0 for 2,074 policies (~3.2%) -- zero-exposure
#   policies. They can't be used in a frequency/severity model since
#   exposure can't be zero in the denominator.
# - Of those zero-exposure rows, 4 still have a claim recorded
#   (claim_count = 1). Kept and flagged with a column rather than
#   deleted, so nothing is silently thrown away.
# - owner_age == 0 for exactly 1 policy -- a single outlier, not worth
#   dropping, just noted here.
# - No missing values, no duplicate rows, and zone/vehicle_class/
#   bonus_class are exactly the 1-7 categories from the data description.
df["is_zero_exposure"] = df["duration_years"] == 0

print("Zero-exposure policies:", df["is_zero_exposure"].sum())
print(
    "Zero-exposure policies that still have a claim recorded:",
    ((df["is_zero_exposure"]) & (df["claim_count"] > 0)).sum(),
)

# --- 5. Save the cleaned data ---
# Save the renamed, flagged dataset to data/processed/ so the next
# script (EDA) can load it directly without repeating this cleaning step.
output_path = PROCESSED_DIR / "motorcycle_clean.csv"
df.to_csv(output_path, index=False)

print(f"Saved cleaned data to: {output_path.resolve()}")
print(f"Final shape: {df.shape}")
