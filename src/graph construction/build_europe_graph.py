import pickle
import pandas as pd
import networkx as nx

# -----------------------------
# Load global UNWEIGHTED graph
# -----------------------------
with open("data/processed/graph_global_unweighted.gpickle", "rb") as f:
    G = pickle.load(f)

print("Global graph loaded")
print("Global nodes:", G.number_of_nodes())
print("Global edges:", G.number_of_edges())

# -----------------------------
# Load airports with countries
# -----------------------------
airports = pd.read_csv("data/processed/clean_airports_with_country_std.csv")

EUROPE_COUNTRIES = [
    "Portugal", "Spain", "France", "Belgium", "Netherlands",
    "Luxembourg", "Germany", "Switzerland", "Austria",
    "United Kingdom", "Ireland", "Norway", "Sweden",
    "Finland", "Denmark", "Iceland",
    "Italy", "Greece", "Malta", "Cyprus",
    "Poland", "Czechia", "Slovakia", "Hungary",
    "Slovenia", "Croatia", "Bosnia and Herzegovina",
    "Serbia", "Montenegro", "North Macedonia",
    "Albania", "Romania", "Bulgaria",
    "Estonia", "Latvia", "Lithuania"
]

# -----------------------------
# Select European airports
# -----------------------------
europe_airports = airports[
    airports["Country_std"].isin(EUROPE_COUNTRIES)
]

europe_iata = set(europe_airports["IATA"])

print("European airports:", len(europe_iata))

# -----------------------------
# Build European subgraph
# -----------------------------
G_europe = G.subgraph(europe_iata).copy()

print("European graph nodes:", G_europe.number_of_nodes())
print("European graph edges:", G_europe.number_of_edges())

# -----------------------------
# Save European graph
# -----------------------------
with open("data/processed/graph_europe_unweighted.gpickle", "wb") as f:
    pickle.dump(G_europe, f)

print("European graph saved to data/processed/graph_europe_unweighted.gpickle")