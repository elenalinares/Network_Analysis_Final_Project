# src/clean_data.py
"""
Simple cleaning pipeline for the airports/routes raw CSVs.

What this script does:
- Loads raw CSVs from data/raw/
- Cleans airports and routes (basic validation and filtering)
- Aggregates routes into unique directed pairs with a weight:
    Weight_NumAirlines = number of distinct airlines operating that route
- Saves cleaned files to data/processed/:
    - airports_clean.csv
    - routes_clean.csv
    - routes_weighted.csv
- Writes a small cleaning report to data/processed/:
    - cleaning_report.json (machine readable)
    - cleaning_report.md (human readable)

This file is meant to be straightforward and reproducible: run it, inspect the outputs,
and use the processed CSVs for graph building and analysis.
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime, UTC

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)


def load_raw():
    # Read the raw CSV files and return two DataFrames.
    airports = pd.read_csv(RAW / "airports.csv")
    routes = pd.read_csv(RAW / "routes.csv")
    return airports, routes


def clean_airports(airports: pd.DataFrame):
    # Keep track of counts for the report.
    stats = {}
    stats["raw_airports_rows"] = len(airports)

    # Normalize column names and ensure ID is a string.
    airports = airports.rename(columns=lambda c: c.strip())
    airports["ID"] = airports["ID"].astype(str)

    # Count and remove duplicate airport IDs (keep first occurrence).
    dup_mask = airports.duplicated(subset=["ID"], keep=False)
    stats["airport_duplicate_id_rows"] = int(dup_mask.sum())
    airports = airports.drop_duplicates(subset=["ID"], keep="first")

    # Remove airports with invalid latitude/longitude values.
    valid_coords_mask = airports["Latitude"].between(-90, 90) & airports["Longitude"].between(-180, 180)
    stats["airport_invalid_coord_rows_removed"] = int((~valid_coords_mask).sum())
    airports = airports[valid_coords_mask].copy()

    # Save cleaned airports and return stats.
    airports.to_csv(PROCESSED / "airports_clean.csv", index=False)
    stats["cleaned_airports_rows"] = len(airports)
    return airports, stats


def clean_routes(airports: pd.DataFrame, routes: pd.DataFrame):
    # Stats for routes cleaning.
    stats = {}
    stats["raw_routes_rows"] = len(routes)

    # Normalize column names and enforce string types for key columns.
    routes = routes.rename(columns=lambda c: c.strip())
    routes["Departure"] = routes["Departure"].astype(str)
    routes["Destination"] = routes["Destination"].astype(str)

    # Make sure Airline ID exists and replace missing with "UNKNOWN".
    if "Airline ID" in routes.columns:
        routes["Airline ID"] = routes["Airline ID"].fillna("UNKNOWN").astype(str)
    else:
        routes["Airline ID"] = "UNKNOWN"

    # Drop rows with missing or empty Departure/Destination values.
    before = len(routes)
    missing_mask = (
        routes["Departure"].isna()
        | routes["Destination"].isna()
        | (routes["Departure"].str.strip() == "")
        | (routes["Destination"].str.strip() == "")
        | (routes["Departure"].str.lower() == "nan")
        | (routes["Destination"].str.lower() == "nan")
    )
    routes = routes[~missing_mask].copy()
    stats["routes_rows_dropped_missing_ids"] = int(before - len(routes))

    # Keep only routes where both endpoints exist in the cleaned airports list.
    valid_ids = set(airports["ID"])
    before = len(routes)
    valid_mask = routes["Departure"].isin(valid_ids) & routes["Destination"].isin(valid_ids)
    stats["routes_rows_removed_invalid_airport_refs"] = int((~valid_mask).sum())
    invalid_sample = routes[~valid_mask].head(10).to_dict(orient="records")
    routes = routes[valid_mask].copy()

    # Remove self-loops where Departure == Destination.
    before_self = len(routes)
    selfloop_mask = routes["Departure"] == routes["Destination"]
    stats["routes_self_loops_removed"] = int(selfloop_mask.sum())
    selfloop_sample = routes[selfloop_mask].head(10).to_dict(orient="records")
    routes = routes[~selfloop_mask].copy()

    # Save cleaned routes and include samples in stats for inspection.
    routes.to_csv(PROCESSED / "routes_clean.csv", index=False)
    stats["cleaned_routes_rows"] = len(routes)
    stats["routes_invalid_sample"] = invalid_sample
    stats["routes_selfloop_sample"] = selfloop_sample
    return routes, stats


def aggregate_routes(routes: pd.DataFrame):
    # Group by (Departure, Destination) and count distinct Airline IDs.
    routes_weighted = (
        routes.groupby(["Departure", "Destination"])["Airline ID"]
        .nunique()
        .reset_index(name="Weight_NumAirlines")
    )
    # Record how many unique directed route pairs we have and save to CSV.
    stats = {"unique_route_pairs": len(routes_weighted)}
    routes_weighted.to_csv(PROCESSED / "routes_weighted.csv", index=False)
    return routes_weighted, stats


def write_report(report: dict):
    # Add a timestamp and save both JSON and a simple markdown summary.
    ts = datetime.now(UTC).isoformat()
    report["generated_at_utc"] = ts
    with open(PROCESSED / "cleaning_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Build a short, readable markdown summary that lists counts and examples.
    md_lines = [
        f"# Cleaning report ({ts})\n",
        "## Summary counts\n",
        f"- Raw airports rows: {report['airports_stats']['raw_airports_rows']}",
        f"- Cleaned airports rows: {report['airports_stats']['cleaned_airports_rows']}",
        f"- Airport duplicate-ID rows removed: {report['airports_stats']['airport_duplicate_id_rows']}",
        f"- Airport invalid-coord rows removed: {report['airports_stats']['airport_invalid_coord_rows_removed']}\n",
        f"- Raw routes rows: {report['routes_stats']['raw_routes_rows']}",
        f"- Routes dropped (missing departure/destination): {report['routes_stats']['routes_rows_dropped_missing_ids']}",
        f"- Routes removed (invalid airport references): {report['routes_stats']['routes_rows_removed_invalid_airport_refs']}",
        f"- Routes self-loops removed: {report['routes_stats']['routes_self_loops_removed']}",
        f"- Cleaned routes rows: {report['routes_stats']['cleaned_routes_rows']}",
        f"- Unique route pairs (weighted): {report['agg_stats']['unique_route_pairs']}\n",
        "## Examples of removed route rows (invalid airport refs)\n",
    ]
    if report['routes_stats'].get('routes_invalid_sample'):
        for r in report['routes_stats']['routes_invalid_sample']:
            md_lines.append(f"- {r}\n")
    else:
        md_lines.append("- (none)\n")
    md_lines.append("\n## Examples of removed self-loop rows\n")
    if report['routes_stats'].get('routes_selfloop_sample'):
        for r in report['routes_stats']['routes_selfloop_sample']:
            md_lines.append(f"- {r}\n")
    else:
        md_lines.append("- (none)\n")

    with open(PROCESSED / "cleaning_report.md", "w", encoding="utf-8") as f:
        f.writelines([line + "\n" if not line.endswith("\n") else line for line in md_lines])

    print(f"Cleaning report saved to: {PROCESSED / 'cleaning_report.json'} and .md")


def main():
    print("Loading raw data...")
    airports_raw, routes_raw = load_raw()

    print("Cleaning airports...")
    airports_clean, airports_stats = clean_airports(airports_raw)

    print("Cleaning routes...")
    routes_clean, routes_stats = clean_routes(airports_clean, routes_raw)

    print("Aggregating by unique airlines per route...")
    routes_weighted, agg_stats = aggregate_routes(routes_clean)

    # Combine stats and write the report.
    report = {
        "airports_stats": airports_stats,
        "routes_stats": routes_stats,
        "agg_stats": agg_stats
    }
    write_report(report)

    # Console summary for quick verification.
    print("\n--- Quick summary ---")
    print(f"Airports: raw={airports_stats['raw_airports_rows']}, cleaned={airports_stats['cleaned_airports_rows']}")
    print(f"Routes: raw={routes_stats['raw_routes_rows']}, cleaned={routes_stats['cleaned_routes_rows']}, unique_pairs={agg_stats['unique_route_pairs']}")
    print("Done.")

if __name__ == "__main__":
    main()
