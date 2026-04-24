import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── Data ────────────────────────────────────────────────────────────────────
combined_listing = pd.read_csv("combined_CRMLSListing_202401_to_202603.csv")
#combined_sold = pd.read_csv("combined_CRMLSSold_202401_to_202603.csv")


DATASETS = {
    "Listing": combined_listing,
    #"Sold": combined_sold,
}

# ── Config ───────────────────────────────────────────────────────────────────
# Each column: (price_cap, bins)
# For Sold
# COLUMNS = {
#     "ClosePrice":         (4_995_000, 10),
#     "ListPrice":          (4_999_000, 10),
#     "OriginalListPrice":  (5_298_000, 10),
#     "LivingArea":         (15_464.5,    10),
#     "LotSizeAcres":       (15.8,        10),
#     "BedroomsTotal":      (6,        10),
#     "BathroomsTotalInteger": (6,     10),
#     "DaysOnMarket":       (290,       15),
#     "YearBuilt":          (2025,      10),
# }

# For Listing
COLUMNS = {
    "ClosePrice":         (4_695_000, 10),
    "ListPrice":          (7_150_000, 10),
    "OriginalListPrice":  (7_495_000, 10),
    "LivingArea":         (6_772,    10),
    "LotSizeAcres":       (26.5,        10),
    "BedroomsTotal":      (7,        10),
    "BathroomsTotalInteger": (7,     10),
    "DaysOnMarket":       (147,       15),
    "YearBuilt":          (2025,      10),
}


# # Suggesting Caps
# def suggest_caps(df: pd.DataFrame, columns: list, quantile: float = 0.99):
#     """Print the value at a given quantile to help choose caps."""
#     for col in columns:
#         if col in df.columns:
#             val = df[col].quantile(quantile)
#             print(f"{col:30s} {quantile:.0%} quantile: {val:,.1f}")

# suggest_caps(combined_listing, list(COLUMNS.keys()))

# ── Helpers ───────────────────────────────────────────────────────────────────
def plot_distribution(series: pd.Series, col: str, label: str, cap: float, bins: int):
    """Box + histogram side-by-side for one column/dataset combo."""
    filtered = series[series < cap]

    fig, (ax_box, ax_hist) = plt.subplots(
        1, 2, figsize=(12, 4),
        gridspec_kw={"width_ratios": [1, 2]}
    )
    fig.suptitle(f"{col}  |  {label}  (< {cap:,})", fontsize=13, fontweight="bold")

    # Box plot
    sns.boxplot(y=filtered, ax=ax_box, color="steelblue")
    ax_box.set_ylabel(col)

    # Histogram
    sns.histplot(filtered, bins=bins, ax=ax_hist, color="steelblue", kde=True)
    ax_hist.set_xlabel(col)
    ax_hist.set_ylabel("Count")

    plt.tight_layout()
    plt.show()


def one_percent_rule(df: pd.DataFrame, price_col="ClosePrice", rent_col="MonthlyRent"):
    """Flag properties where monthly rent >= 1% of close price."""
    if rent_col not in df.columns:
        return None
    df = df.copy()
    df["passes_1pct"] = df[rent_col] >= df[price_col] * 0.01
    return df[["passes_1pct", price_col, rent_col]]


# ── Main loop ────────────────────────────────────────────────────────────────
for col, (cap, bins) in COLUMNS.items():
    for label, df in DATASETS.items():
        if col not in df.columns:
            continue
        plot_distribution(df[col], col, label, cap, bins)

# ── 1% Rule (uncomment when rent data is available) ──────────────────────────
# for label, df in DATASETS.items():
#     result = one_percent_rule(df)
#     if result is not None:
#         print(f"\n── 1% Rule ({label}) ──")
#         print(result.value_counts("passes_1pct"))