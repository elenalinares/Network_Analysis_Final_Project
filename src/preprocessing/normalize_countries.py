COUNTRY_NORMALIZATION = {
    # Norway
    "Norge": "Norway",
    "Noruega": "Norway",
    "Norway": "Norway",

    # Spain
    "España": "Spain",
    "Spain": "Spain",

    # Germany
    "Deutschland": "Germany",
    "Germany": "Germany",

    # France
    "France": "France",
    "Francia": "France",

    # Italy
    "Italia": "Italy",
    "Italy": "Italy",

    # Sweden
    "Sverige": "Sweden",
    "Sweden": "Sweden",

    # Finland
    "Suomi": "Finland",
    "Finland": "Finland",

    # Denmark
    "Danmark": "Denmark",
    "Denmark": "Denmark",

    # Poland
    "Polska": "Poland",
    "Poland": "Poland",

    # United Kingdom
    "United Kingdom": "United Kingdom",
    "UK": "United Kingdom",
    "Great Britain": "United Kingdom",

    # Netherlands
    "Nederland": "Netherlands",
    "Netherlands": "Netherlands",

    # Czech Republic
    "Czech Republic": "Czechia",
    "Czechia": "Czechia"
}

import pandas as pd

airports = pd.read_csv("data/processed/clean_airports_with_country.csv")

airports["Country_std"] = (
    airports["Country"]
    .map(COUNTRY_NORMALIZATION)
    .fillna(airports["Country"])
)

airports.to_csv(
    "data/processed/clean_airports_with_country_std.csv",
    index=False
)

print("Saved clean_airports_with_country_std.csv")
print("Unique standardized countries:",
      airports["Country_std"].nunique())