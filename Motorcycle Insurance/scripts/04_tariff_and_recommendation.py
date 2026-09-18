"""04 - Tariff Table & Business Recommendation: Motorcycle Insurance

Load the saved frequency and severity models, build a full pricing
tariff (base rate grid + modifier factors), and print the final
business recommendation.
"""

import itertools
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

MODELS_DIR = Path("../models")
PROCESSED_DIR = Path("../data/processed")

freq_model = sm.load(MODELS_DIR / "frequency_glm.pickle")
sev_model = sm.load(MODELS_DIR / "severity_glm.pickle")

df = pd.read_csv("../data/processed/motorcycle_clean.csv")
df_exp = df[~df["is_zero_exposure"]].copy()

age_bins = [0, 25, 35, 45, 55, 65, 100]
age_labels = ["<25", "25-34", "35-44", "45-54", "55-64", "65+"]
df_exp["age_group"] = pd.cut(df_exp["owner_age"], bins=age_bins, labels=age_labels, right=False)

veh_bins = [0, 3, 6, 10, 15, 100]
veh_labels = ["0-2", "3-5", "6-9", "10-14", "15+"]
df_exp["vehicle_age_group"] = pd.cut(df_exp["vehicle_age"], bins=veh_bins, labels=veh_labels, right=False).astype(str)

for col in ["gender", "zone", "vehicle_class", "bonus_class", "age_group"]:
    df_exp[col] = df_exp[col].astype(str)

print("Models loaded from disk (not refit).")
print(f"Frequency model params: {len(freq_model.params)} | Severity model params: {len(sev_model.params)}")

# --- 1. Build the base tariff grid ---
# A real motor tariff is built as a base rate grid for the strongest
# factors, plus modifier multipliers for the rest -- not one giant table
# with every factor crossed together (that would be 6 x 7 x 7 x 7 x 2 x 5
# = 20,580 rows, unusable).
#
# Base grid: age_group x zone x vehicle_class (the 3 strongest, most
# reliable factors), priced at a reference profile: bonus_class = 1,
# gender = Female, vehicle_age_group = 0-2 (a brand-new rider/bike/
# no-claims baseline).
base_bonus = "1"
base_gender = "Female"
base_vehicle_age_group = "0-2"

zones = [str(z) for z in range(1, 8)]
vehicle_classes = [str(c) for c in range(1, 8)]

grid_rows = list(itertools.product(age_labels, zones, vehicle_classes))
tariff = pd.DataFrame(grid_rows, columns=["age_group", "zone", "vehicle_class"])
tariff["bonus_class"] = base_bonus
tariff["gender"] = base_gender
tariff["vehicle_age_group"] = base_vehicle_age_group

tariff["predicted_frequency"] = freq_model.predict(tariff, offset=np.zeros(len(tariff)))
tariff["predicted_severity"] = sev_model.predict(tariff)
tariff["base_pure_premium"] = tariff["predicted_frequency"] * tariff["predicted_severity"]

print(f"Base tariff grid: {len(tariff)} combinations (age_group x zone x vehicle_class)")
print("Top 10 highest base rates:")
print(tariff.sort_values("base_pure_premium", ascending=False).head(10))


# --- 2. Build the modifier tables ---
# For bonus_class, gender, and vehicle_age_group, compute the combined
# (frequency x severity) relativity for every level relative to the
# reference profile above.
def build_modifier_table(factor_col, levels, ref_level):
    rows = pd.DataFrame(
        {
            "age_group": "25-34",
            "zone": "1",
            "vehicle_class": "1",
            "bonus_class": base_bonus,
            "gender": base_gender,
            "vehicle_age_group": base_vehicle_age_group,
        },
        index=levels,
    )
    rows[factor_col] = levels

    freq = freq_model.predict(rows, offset=np.zeros(len(rows)))
    sev = sev_model.predict(rows)
    pure_premium = freq * sev

    return pd.DataFrame(
        {
            "predicted_frequency": freq,
            "predicted_severity": sev,
            "pure_premium": pure_premium,
            "modifier": pure_premium / pure_premium.loc[ref_level],
        }
    )


bonus_table = build_modifier_table("bonus_class", [str(i) for i in range(1, 8)], base_bonus)
gender_table = build_modifier_table("gender", ["Female", "Male"], base_gender)
vehicle_age_table = build_modifier_table("vehicle_age_group", veh_labels, base_vehicle_age_group)

print("Bonus class modifier (relative to bonus_class = 1):")
print(bonus_table["modifier"])
print("Gender modifier (relative to Female):")
print(gender_table["modifier"])
print("Vehicle age modifier (relative to 0-2 years):")
print(vehicle_age_table["modifier"])


# --- 3. Verify the decomposition is exact ---
def quote(age_group, zone, vehicle_class, bonus_class, gender, vehicle_age_group):
    row = pd.DataFrame(
        [
            {
                "age_group": age_group,
                "zone": zone,
                "vehicle_class": vehicle_class,
                "bonus_class": bonus_class,
                "gender": gender,
                "vehicle_age_group": vehicle_age_group,
            }
        ]
    )
    freq = freq_model.predict(row, offset=np.zeros(len(row))).iloc[0]
    sev = sev_model.predict(row).iloc[0]
    return freq * sev


def quote_from_table(age_group, zone, vehicle_class, bonus_class, gender, vehicle_age_group):
    base_row = tariff[
        (tariff["age_group"] == age_group) & (tariff["zone"] == zone) & (tariff["vehicle_class"] == vehicle_class)
    ]
    base_rate = base_row["base_pure_premium"].iloc[0]
    return (
        base_rate
        * bonus_table.loc[bonus_class, "modifier"]
        * gender_table.loc[gender, "modifier"]
        * vehicle_age_table.loc[vehicle_age_group, "modifier"]
    )


test_cases = [
    ("<25", "2", "6", "7", "Male", "15+"),
    ("45-54", "3", "2", "4", "Female", "6-9"),
    ("65+", "1", "6", "1", "Male", "0-2"),
]

for case in test_cases:
    direct = quote(*case)
    from_table = quote_from_table(*case)
    print(f"{case}: direct model = {direct:,.1f} | base x modifiers = {from_table:,.1f} | match: {np.isclose(direct, from_table)}")

# --- 4. Lowest-risk vs highest-risk example quotes ---
# NOTE: stacking multiple extreme modifiers together compounds their
# uncertainty into unrealistic ratios (see the caution below). Real
# insurers cap combined discounts/loadings for this reason.
higher_risk_profile = ("<25", "2", "6", "1", "Male", "0-2")  # young rider, risky zone, high-power new bike
lower_risk_profile = ("45-54", "4", "1", "7", "Female", "15+")  # mature rider, low-power old bike, max bonus

higher_risk_quote = quote(*higher_risk_profile)
lower_risk_quote = quote(*lower_risk_profile)

print(f"Higher-risk profile {higher_risk_profile}: {higher_risk_quote:,.0f} per policy-year")
print(f"Lower-risk profile  {lower_risk_profile}: {lower_risk_quote:,.0f} per policy-year")
print(f"Realistic price ratio: {higher_risk_quote / lower_risk_quote:,.0f}x")
print(
    "Caution: this ratio is far more extreme than what real insurers charge between best/worst "
    "customers -- a known effect of multiplicative rating with no interaction terms or caps. "
    "The EDA's directly observed 17.7x (age<25/zone2/vehicle_class6, 75 real policy-years) is the "
    "safer, data-backed number to quote to a business stakeholder."
)

# --- 5. Save the tariff outputs ---
tariff.to_csv(PROCESSED_DIR / "tariff_base_rates.csv", index=False)
bonus_table.to_csv(PROCESSED_DIR / "tariff_modifier_bonus_class.csv")
gender_table.to_csv(PROCESSED_DIR / "tariff_modifier_gender.csv")
vehicle_age_table.to_csv(PROCESSED_DIR / "tariff_modifier_vehicle_age.csv")
print(f"Saved tariff outputs to: {PROCESSED_DIR.resolve()}")

# --- Business recommendation ---
print(
    """
BUSINESS RECOMMENDATION
========================
1. Reprice the confirmed high-risk segment: riders under 25, zone 2,
   vehicle class 6 cost ~17.7x the average policy (75 real policy-years,
   8 claims) -- likely under-priced today.
2. Stop relying on bonus_class as a standalone rating signal -- not
   statistically significant once age/zone/vehicle class are controlled
   for. Keep it as a loyalty/retention tool, not a risk indicator.
3. Cap combined discounts/loadings in production -- the multiplicative
   tariff can compound into unrealistic extremes (>1,000x) when several
   "best" or "worst" factor levels stack together.
4. Treat zone 7 and other thin segments with caution -- zone 7 has
   exactly 1 claim on record; apply credibility weighting or merge with
   a similar zone until more data accumulates.
"""
)
