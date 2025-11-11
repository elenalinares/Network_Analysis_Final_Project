# src/compare_cph_europe.py
"""
Compare Copenhagen (CPH) with Nordic peers and with a selection of major European hubs.

Produces:
 - data/derived/compare_nordic.csv
 - data/derived/compare_europe.csv
 - data/derived/compare_nordic.png
 - data/derived/compare_europe.png

Reads:
 - data/derived/centralities_all.csv (produced by analyze_cph.py)
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DERIVED.mkdir(parents=True, exist_ok=True)

CENTRAL_FILE = DERIVED / "centralities_all.csv"

# Lists to compare: edit if you want different airports
NORDIC_IDS = ["CPH", "ARN", "OSL", "HEL", "BGO", "SVG", "TLL"]
EUROPE_IDS = [
    "CPH", "LHR", "CDG", "FRA", "AMS", "MAD", "BCN", "ZRH", "MXP",
    "DUB", "VIE", "IST", "BRU", "ARN", "OSL", "HEL"
]

# Centrality columns to present and plot
CENT_COLUMNS = [
    "Weighted_InDegree",
    "Weighted_OutDegree",
    "Betweenness",
    "Closeness",
    "Eigenvector"
]

# Colors (pink / lilac theme)
PINK = "#FF69B4"         # bright pink — used to highlight CPH
PINK_FADE = "#FFB6C1"    # light pink — used for other in-degree bars
LILAC = "#C8A2C8"        # lilac — used for other out-degree bars
LILAC_FADE = "#E6D7E9"   # pale lilac — lighter variant

HIGHLIGHT_ID = "CPH"     # airport to emphasize in plots

def load_centralities(path):
    if not path.exists():
        raise FileNotFoundError(f"Centralities file not found: {path}")
    df = pd.read_csv(path)
    # Ensure ID column is string
    df["ID"] = df["ID"].astype(str)
    for col in CENT_COLUMNS:
        if col not in df.columns:
            df[col] = 0.0
    return df

def filter_and_export(df, ids, out_csv, title):
    present = [i for i in ids if i in set(df["ID"])]
    missing = [i for i in ids if i not in set(df["ID"])]
    if missing:
        print(f"Warning: the following requested IDs were not found and will be skipped: {missing}")

    sub = df[df["ID"].isin(present)].copy()
    # compute total degree for sorting
    sub["TotalDegree"] = sub["Weighted_InDegree"].astype(float) + sub["Weighted_OutDegree"].astype(float)
    sub = sub.sort_values("TotalDegree", ascending=False)
    # Keep only needed columns and set index
    sub = sub.set_index("ID")[["Label"] + CENT_COLUMNS + ["TotalDegree"]].copy()

    # Save CSV for later use
    sub.to_csv(out_csv)
    print(f"Saved {out_csv} ({len(sub)} rows)")

    # Print table to console
    print(f"\n=== {title} ===")
    print(sub.round(6).to_string())

    return sub

def plot_comparison(subdf, out_png, title, figsize=(12,6)):
    if subdf.empty:
        print(f"No data to plot for {title}.")
        return

    labels_idx = list(subdf.index)
    labels_text = [lbl if isinstance(lbl, str) and lbl.strip() != "" else idx for idx, lbl in zip(subdf.index, subdf["Label"])]

    x = np.arange(len(subdf))
    width = 0.35

    in_vals = subdf["Weighted_InDegree"].astype(float).values
    out_vals = subdf["Weighted_OutDegree"].astype(float).values

    # Colors: highlight CPH
    in_colors = [PINK if idx == HIGHLIGHT_ID else PINK_FADE for idx in labels_idx]
    out_colors = [PINK if idx == HIGHLIGHT_ID else LILAC for idx in labels_idx]

    fig, ax = plt.subplots(figsize=figsize)
    bars_in = ax.bar(x - width/2, in_vals, width, label="Weighted InDegree", color=in_colors, edgecolor="k", linewidth=0.3)
    bars_out = ax.bar(x + width/2, out_vals, width, label="Weighted OutDegree", color=out_colors, edgecolor="k", linewidth=0.3)

    # Add numeric labels above bars
    def annotate_bars(bars):
        for b in bars:
            h = b.get_height()
            if np.isnan(h):
                h = 0.0
            ax.annotate(
                f"{int(h)}",
                xy=(b.get_x() + b.get_width() / 2, h),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8
            )

    annotate_bars(bars_in)
    annotate_bars(bars_out)

    ax.set_xticks(x)
    ax.set_xticklabels(labels_text, rotation=45, ha="right")
    ax.set_ylabel("Weighted degree (sum of airlines)")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    fig.savefig(out_png, dpi=200)
    plt.close(fig)
    print(f"Saved plot {out_png}")

def main():
    central = load_centralities(CENTRAL_FILE)

    # Nordic comparison
    nordic_csv = DERIVED / "compare_nordic.csv"
    nordic_png = DERIVED / "compare_nordic.png"
    nordic_df = filter_and_export(central, NORDIC_IDS, nordic_csv, "Nordic Airports Comparison")
    plot_comparison(nordic_df, nordic_png, "CPH vs Nordic Airports (pink/lilac theme)")

    # Europe comparison
    europe_csv = DERIVED / "compare_europe.csv"
    europe_png = DERIVED / "compare_europe.png"
    europe_df = filter_and_export(central, EUROPE_IDS, europe_csv, "European Airports Comparison")
    plot_comparison(europe_df, europe_png, "CPH vs Selected European Hubs (pink/lilac theme)")

    print("\nFinished comparisons. Check the CSVs and PNGs in data/derived/")

if __name__ == "__main__":
    main()
