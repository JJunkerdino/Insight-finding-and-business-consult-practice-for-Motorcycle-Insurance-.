"""02 - Exploratory Data Analysis: Motorcycle Insurance

Explore claim frequency and severity by segment, check relationships
between variables, and validate the bonus-malus (no-claims discount)
system before any modeling.

Unlike the notebook version, charts are saved to reports/figures/
instead of shown inline, since a plain script has no notebook cell to
display them in.
"""

import matplotlib

matplotlib.use("Agg")  # save charts to files instead of popping up windows

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pathlib import Path

sns.set_theme(style="whitegrid")

FIGURES_DIR = Path("../reports/figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv("../data/processed/motorcycle_clean.csv")

# frequency/severity need real exposure -> zero-exposure rows would divide by zero
df_exp = df[~df["is_zero_exposure"]].copy()
print(
    f"Full data: {len(df):,} rows | used for frequency/severity: {len(df_exp):,} rows "
    f"({len(df) - len(df_exp):,} zero-exposure rows excluded)"
)

# --- 1. Build readable groups ---
# Bucket the continuous variables (owner_age, vehicle_age) into groups so
# segment comparisons are easier to read and plot.
age_bins = [0, 25, 35, 45, 55, 65, 100]
age_labels = ["<25", "25-34", "35-44", "45-54", "55-64", "65+"]
df_exp["age_group"] = pd.cut(df_exp["owner_age"], bins=age_bins, labels=age_labels, right=False)

veh_bins = [0, 3, 6, 10, 15, 100]
veh_labels = ["0-2", "3-5", "6-9", "10-14", "15+"]
df_exp["vehicle_age_group"] = pd.cut(df_exp["vehicle_age"], bins=veh_bins, labels=veh_labels, right=False)

# --- 2. Overall risk baseline ---
total_exposure = df_exp["duration_years"].sum()
total_claims = df_exp["claim_count"].sum()
total_cost = df_exp["claim_cost"].sum()
claims_only = df_exp[df_exp["claim_count"] > 0]

overall_frequency = total_claims / total_exposure
overall_severity = claims_only["claim_cost"].sum() / claims_only["claim_count"].sum()
overall_pure_premium = total_cost / total_exposure

print(f"Total exposure (policy-years): {total_exposure:,.1f}")
print(f"Total claims: {total_claims:,}")
print(f"Overall claim frequency: {overall_frequency:.4f} claims per policy-year")
print(f"Overall average severity (cost per claim): {overall_severity:,.0f}")
print(f"Overall pure premium (cost per policy-year): {overall_pure_premium:,.1f}")


# --- 3. Claim frequency by segment ---
# Frequency = total claims / total exposure (policy-years) per group -- the
# correct way to compare groups with different amounts of exposure.
def frequency_by(data, group_col):
    g = data.groupby(group_col, observed=True).agg(
        exposure=("duration_years", "sum"),
        claims=("claim_count", "sum"),
    )
    g["frequency"] = g["claims"] / g["exposure"]
    return g.sort_index()


segment_cols = ["gender", "zone", "vehicle_class", "bonus_class", "age_group", "vehicle_age_group"]

fig, axes = plt.subplots(2, 3, figsize=(16, 8))
for ax, col in zip(axes.flat, segment_cols):
    freq_table = frequency_by(df_exp, col)
    freq_table["frequency"].plot(kind="bar", ax=ax, color="steelblue")
    ax.set_title(f"Claim frequency by {col}")
    ax.set_ylabel("claims per policy-year")
    ax.axhline(overall_frequency, color="red", linestyle="--", linewidth=1, label="overall avg")
    ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES_DIR / "frequency_by_segment.png", dpi=150)
plt.close(fig)

# --- 4. Does the bonus-malus (no-claims discount) system work? ---
# If the system works as intended, frequency should generally go down as
# bonus_class goes up.
bonus_freq = frequency_by(df_exp, "bonus_class")
print(bonus_freq)

is_monotonic = bonus_freq["frequency"].is_monotonic_decreasing
print(f"Is frequency strictly decreasing as bonus_class goes up? {is_monotonic}")

print("Average owner_age by bonus_class:")
print(df_exp.groupby("bonus_class", observed=True)["owner_age"].mean())

fig = bonus_freq["frequency"].plot(marker="o", figsize=(6, 4), title="Claim frequency by bonus class").get_figure()
plt.ylabel("claims per policy-year")
plt.xlabel("bonus_class")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "bonus_class_frequency.png", dpi=150)
plt.close(fig)


# --- 5. Claim severity by segment ---
# Severity = average cost per claim, so this only uses policies where
# claim_count > 0.
def severity_by(data, group_col):
    claims = data[data["claim_count"] > 0]
    g = claims.groupby(group_col, observed=True).agg(
        n_claims=("claim_count", "sum"),
        total_cost=("claim_cost", "sum"),
    )
    g["avg_severity"] = g["total_cost"] / g["n_claims"]
    return g.sort_index()


fig, axes = plt.subplots(2, 3, figsize=(16, 8))
for ax, col in zip(axes.flat, segment_cols):
    sev_table = severity_by(df_exp, col)
    sev_table["avg_severity"].plot(kind="bar", ax=ax, color="darkorange")
    ax.set_title(f"Avg claim severity by {col}")
    ax.set_ylabel("avg cost per claim")
    ax.axhline(overall_severity, color="red", linestyle="--", linewidth=1, label="overall avg")
    ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES_DIR / "severity_by_segment.png", dpi=150)
plt.close(fig)

# check sample size behind each severity number -- some segments have very few claims
print("Severity by zone, with claim count (n_claims) for reliability check:")
print(severity_by(df_exp, "zone"))

# --- 6. Distribution of claim cost ---
# Insurance claim costs are almost always right-skewed: most claims are
# small, a few are very expensive.
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
sns.histplot(claims_only["claim_cost"], bins=40, ax=axes[0])
axes[0].set_title("Claim cost distribution")
sns.histplot(claims_only["claim_cost"], bins=40, log_scale=True, ax=axes[1])
axes[1].set_title("Claim cost distribution (log scale)")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "claim_cost_distribution.png", dpi=150)
plt.close(fig)

sorted_costs = claims_only["claim_cost"].sort_values(ascending=False)
top_1pct_n = max(1, int(len(sorted_costs) * 0.01))
top_1pct_share = sorted_costs.head(top_1pct_n).sum() / sorted_costs.sum()
print(f"Top 1% most expensive claims ({top_1pct_n} claims) = {top_1pct_share:.1%} of total claim cost")
print(f"Largest single claim: {sorted_costs.iloc[0]:,.0f}")
print(f"Median claim: {sorted_costs.median():,.0f}")

# --- 7. Relationships between numeric variables ---
numeric_cols = ["owner_age", "vehicle_age", "bonus_class", "duration_years", "claim_count", "claim_cost"]
corr = df_exp[numeric_cols].corr()

fig = plt.figure(figsize=(6, 5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Correlation matrix")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "correlation_matrix.png", dpi=150)
plt.close(fig)

# Note: the correlations above look weak (e.g. owner_age vs claim_count is
# only -0.06), which seems to contradict the strong age pattern seen in
# section 3. This is expected -- plain linear correlation is a poor measure
# here because claim_count is a rare, mostly-zero count and the true
# relationship is non-linear. The grouped frequency/severity tables are far
# more informative for this kind of data than a correlation matrix.

# --- 8. Combined risk ranking ---
# Which combination of age group x zone x vehicle class has the highest
# pure premium (expected cost per policy-year)? Only groups with enough
# exposure are shown, so the ranking isn't driven by a couple of lucky or
# unlucky policies.
combo = df_exp.groupby(["age_group", "zone", "vehicle_class"], observed=True).agg(
    exposure=("duration_years", "sum"),
    claims=("claim_count", "sum"),
    total_cost=("claim_cost", "sum"),
)
combo = combo[combo["exposure"] >= 50]  # keep only groups with enough data to trust
combo["frequency"] = combo["claims"] / combo["exposure"]
combo["pure_premium"] = combo["total_cost"] / combo["exposure"]

print(f"Groups with at least 50 policy-years of exposure: {len(combo)}")
print(f"Overall pure premium for comparison: {overall_pure_premium:,.1f}")
print("Top 10 riskiest combinations (highest pure premium):")
print(combo.sort_values("pure_premium", ascending=False).head(10))

print(f"\nCharts saved to: {FIGURES_DIR.resolve()}")
