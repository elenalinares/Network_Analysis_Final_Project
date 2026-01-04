#just some nice a silly data cleaning - ensure consistency between aiports and routes before building the network

import pandas as pd
from pathlib import Path

Path("data").mkdir(exist_ok=True)
# minimal cleaning step to ensure consistency between airports and routes
# removing missing values, invalid iata codes, selfloops, 
# and routes pointing to inexistent airports.

# ---------- Airports ----------
airports = pd.read_csv("data/raw/airports.csv")
print("Raw airports:", len(airports))

airports_clean = airports[
    airports["ID"].notna() &
    airports["Latitude"].notna() &
    airports["Longitude"].notna() &
    (airports["ID"].astype(str).str.len() == 3)
].copy()

airports_clean = airports_clean.drop_duplicates(subset=["ID"])
airports_clean = airports_clean.rename(columns={"ID": "IATA"})

airports_clean.to_csv("data/processed/clean_airports.csv", index=False)
print("Clean airports:", len(airports_clean))

# ---------- Routes ----------
routes = pd.read_csv("data/raw/routes.csv")
print("Raw routes:", len(routes))

routes_clean = routes[
    routes["Departure"].notna() &
    routes["Destination"].notna() &
    (routes["Departure"] != routes["Destination"])
].copy()

valid_iata = set(airports_clean["IATA"])

routes_clean = routes_clean[
    routes_clean["Departure"].isin(valid_iata) &
    routes_clean["Destination"].isin(valid_iata)
]

routes_clean.to_csv("data/processed/clean_routes.csv", index=False)
print("Clean routes:", len(routes_clean))
