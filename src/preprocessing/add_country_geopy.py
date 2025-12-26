import pandas as pd
import time
from geopy.geocoders import Nominatim

# -----------------------------
# load cleaned airports
# -----------------------------


airports = pd.read_csv("data/processed/clean_airports.csv")

geolocator = Nominatim(user_agent="network-analysis-project")

countries = []

for i, row in airports.iterrows():
    lat = row["Latitude"]
    lon = row["Longitude"]

    try:
        location = geolocator.reverse((lat, lon), exactly_one=True)
        if location and "country" in location.raw["address"]:
            country = location.raw["address"]["country"]
        else:
            country = None
    except Exception as e:
        country = None

    countries.append(country)

    # Respect rate limits
    if i % 10 == 0:
        time.sleep(1)

    if i % 500 == 0:
        print(f"Processed {i}/{len(airports)} airports")

airports["Country"] = countries

airports.to_csv("data/processed/clean_airports_with_country.csv", index=False)
print("Saved clean_airports_with_country.csv")