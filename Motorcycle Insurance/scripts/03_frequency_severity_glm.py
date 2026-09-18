"""03 - Frequency & Severity GLM: Motorcycle Insurance

Build the two models actuaries actually use to price a policy: a Poisson
GLM for how often a policy claims, and a Gamma GLM for how expensive a
claim is when one happens. Combine them into a risk premium, check it
against reality, and save both fitted models to disk.
"""

import matplotlib

matplotlib.use("Agg")  # save charts to files instead of popping up windows

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from pathlib import Path

FIGURES_DIR = Path("../reports/figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR = Path("../models")
MODELS_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv("../data/processed/motorcycle_clean.csv")
df_exp = df[~df["is_zero_exposure"]].copy()

age_bins = [0, 25, 35, 45, 55, 65, 100]
age_labels = ["<25", "25-34", "35-44", "45-54", "55-64", "65+"]
df_exp["age_group"] = pd.cut(df_exp["owner_age"], bins=age_bins, labels=age_labels, right=False)

veh_bins = [0, 3, 6, 10, 15, 100]
veh_labels = ["0-2", "3-5", "6-9", "10-14", "15+"]
df_exp["vehicle_age_group"] = pd.cut(df_exp["vehicle_age"], bins=veh_bins, labels=veh_labels, right=False).astype(str)

# GLM needs plain categorical columns (not pandas "category" dtype quirks)
for col in ["gender", "zone", "vehicle_class", "bonus_class", "age_group"]:
    df_exp[col] = df_exp[col].astype(str)

# --- 1. Frequency model ---
# Target: claim_count. Exposure: duration_years goes in as an offset
# (log(duration_years)), not as a regular feature. First check whether a
# plain Poisson GLM is appropriate, or whether the data is overdispersed
# (variance > mean), which would call for a Negative Binomial instead.
mean_claims = df_exp["claim_count"].mean()
var_claims = df_exp["claim_count"].var()
print(f"Mean of claim_count: {mean_claims:.5f}")
print(f"Variance of claim_count: {var_claims:.5f}")
print(f"Variance / Mean ratio: {var_claims / mean_claims:.3f} (close to 1.0 -> Poisson is fine)")

rating_factors = ["age_group", "zone", "vehicle_class", "bonus_class", "gender", "vehicle_age_group"]
freq_formula = "claim_count ~ " + " + ".join(f"C({col})" for col in rating_factors)

freq_model = smf.glm(
    formula=freq_formula,
    data=df_exp,
    family=sm.families.Poisson(),
    offset=np.log(df_exp["duration_years"]),
).fit()

print(freq_model.summary())


# --- 2. Turn coefficients into relativities ---
# Raw GLM coefficients are on the log scale. Apply exp() to turn each one
# into a relativity: "this group claims X times more/less often than the
# reference group."
def relativities_table(model):
    out = pd.DataFrame({"relativity": np.exp(model.params), "p_value": model.pvalues})
    out = out.drop("Intercept")
    out["significant_at_5pct"] = out["p_value"] < 0.05
    return out.sort_values("relativity", ascending=False)


freq_relativities = relativities_table(freq_model)
print(freq_relativities)

# --- 3. Severity model ---
# Target: claim_cost, but only for rows where a claim happened
# (claim_count > 0). Gamma GLM with a log link is the standard choice for
# insurance cost data (always positive, right-skewed).
claims_only = df_exp[df_exp["claim_count"] > 0].copy()

# 27 policies have 2 claims recorded as one combined claim_cost -> use
# average cost per claim as the target
claims_only["avg_claim_cost"] = claims_only["claim_cost"] / claims_only["claim_count"]

sev_formula = "avg_claim_cost ~ " + " + ".join(f"C({col})" for col in rating_factors)

sev_model = smf.glm(
    formula=sev_formula,
    data=claims_only,
    family=sm.families.Gamma(link=sm.families.links.Log()),
    var_weights=claims_only["claim_count"],  # policies with 2 claims carry more weight
).fit()

print(f"Number of claims used: {int(claims_only['claim_count'].sum())}")
print(sev_model.summary())

sev_relativities = relativities_table(sev_model)
print(sev_relativities)

# --- 4. Combine into a risk premium and validate ---
# Multiply the two models together: predicted risk premium = predicted
# frequency x predicted severity. Then check the combined model against
# reality before using it for pricing.
predicted_frequency = freq_model.predict(df_exp, offset=np.zeros(len(df_exp)))
predicted_severity = sev_model.predict(df_exp)

df_exp["predicted_pure_premium"] = predicted_frequency * predicted_severity
df_exp["predicted_cost"] = df_exp["predicted_pure_premium"] * df_exp["duration_years"]

total_predicted = df_exp["predicted_cost"].sum()
total_actual = df_exp["claim_cost"].sum()

print(f"Total actual claim cost: {total_actual:,.0f}")
print(f"Total predicted claim cost: {total_predicted:,.0f}")
print(f"Ratio (predicted / actual): {total_predicted / total_actual:.3f}")

validation = df_exp.groupby("age_group", observed=True).agg(
    exposure=("duration_years", "sum"),
    actual_cost=("claim_cost", "sum"),
    predicted_cost=("predicted_cost", "sum"),
)
validation["actual_pure_premium"] = validation["actual_cost"] / validation["exposure"]
validation["predicted_pure_premium"] = validation["predicted_cost"] / validation["exposure"]
validation = validation.reindex(age_labels)
print(validation)

fig, ax = plt.subplots(figsize=(8, 4))
validation[["actual_pure_premium", "predicted_pure_premium"]].plot(
    kind="bar", ax=ax, title="Actual vs predicted pure premium by age group"
)
ax.set_ylabel("pure premium (cost per policy-year)")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "actual_vs_predicted_by_age.png", dpi=150)
plt.close(fig)

# --- 5. Price the riskiest segment found in the EDA ---
overall_pure_premium = total_actual / df_exp["duration_years"].sum()
riskiest_segment = df_exp[
    (df_exp["age_group"] == "<25") & (df_exp["zone"] == "2") & (df_exp["vehicle_class"] == "6")
]
exposure = riskiest_segment["duration_years"].sum()
actual_pure_premium = riskiest_segment["claim_cost"].sum() / exposure
predicted_pure_premium = riskiest_segment["predicted_cost"].sum() / exposure

print(f"Riskiest segment: age <25, zone 2, vehicle_class 6 ({len(riskiest_segment)} policies, {exposure:.1f} policy-years)")
print(f"Actual pure premium: {actual_pure_premium:,.0f} per policy-year")
print(f"Model's predicted pure premium: {predicted_pure_premium:,.0f} per policy-year")
print(f"Model says this segment is {predicted_pure_premium / overall_pure_premium:.1f}x the average risk")

# --- 6. Save the fitted models ---
# Save both GLMs to models/ so the next script (pricing table) can load
# them directly instead of re-fitting.
freq_model.save(MODELS_DIR / "frequency_glm.pickle")
sev_model.save(MODELS_DIR / "severity_glm.pickle")
print(f"Saved models to: {MODELS_DIR.resolve()}")
print(f"Charts saved to: {FIGURES_DIR.resolve()}")
