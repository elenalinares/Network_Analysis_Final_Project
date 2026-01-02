#basic properties for the eurpoean air transport network + LCC
#we get a baseline to evaluate large-scale disruptios --> research question

import pickle
import networkx as nx
import pandas as pd

# -----------------------------
# Load European UNWEIGHTED graph
# -----------------------------
with open("data/processed/graph_europe_unweighted.gpickle", "rb") as f:
    G = pickle.load(f)

print("European graph loaded")

# -----------------------------
# Basics
# -----------------------------
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
density = nx.density(G)

degrees = dict(G.degree())
avg_degree = sum(degrees.values()) / num_nodes

# -----------------------------
# LCC stuff
# -----------------------------
G_undirected = G.to_undirected()
lcc_nodes = max(nx.connected_components(G_undirected), key=len)
G_lcc = G_undirected.subgraph(lcc_nodes).copy()

lcc_size = G_lcc.number_of_nodes()
lcc_fraction = 100 * lcc_size / num_nodes
lcc_avg_degree = sum(dict(G_lcc.degree()).values()) / lcc_size
lcc_diameter = nx.diameter(G_lcc)

# -----------------------------
# Count total European airline routes
# -----------------------------
routes = pd.read_csv("data/processed/clean_routes.csv")
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

europe_iata = set(
    airports.loc[
        airports["Country_std"].isin(EUROPE_COUNTRIES),
        "IATA"
    ]
)

routes_europe = routes[
    routes["Departure"].isin(europe_iata) &
    routes["Destination"].isin(europe_iata)
]

total_routes_europe = len(routes_europe)

# -----------------------------
# Print results
# -----------------------------
print("\n--- European Network Statistics (unweighted) ---")
print("Number of nodes:", num_nodes)
print("Number of edges:", num_edges)
print("Total airline routes (edge-level):", total_routes_europe)
print(f"Density: {density:.5f}")
print(f"Average degree: {avg_degree:.2f}")

print("\n--- Largest Connected Component (LCC) ---")
print(f"LCC size: {lcc_size} ({lcc_fraction:.2f}% of nodes)")
print(f"Average degree (LCC): {lcc_avg_degree:.2f}")
print(f"Diameter (LCC): {lcc_diameter}")