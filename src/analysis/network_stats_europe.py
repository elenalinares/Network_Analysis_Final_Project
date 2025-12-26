import pickle
import networkx as nx
import pandas as pd


# -----------------------------
# Load European graph
# -----------------------------
with open("data/processed/graph_europe.gpickle", "rb") as f:
    G = pickle.load(f)

print("European graph loaded")

# Load datasets
routes = pd.read_csv("data/processed/clean_routes.csv")
airports = pd.read_csv("data/processed/clean_airports_with_country_std.csv")

# -----------------------------
# size metrics
# -----------------------------
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
density = nx.density(G)

# -----------------------------
# Degree and strength
# -----------------------------
degrees = dict(G.degree())
avg_degree = sum(degrees.values()) / num_nodes

# Weighted degree (strength)
strengths = dict(G.degree(weight="weight"))
avg_strength = sum(strengths.values()) / num_nodes

# -----------------------------
# GCC
# (weakly connected, since graph is directed)
# -----------------------------
gcc = max(nx.weakly_connected_components(G), key=len)
gcc_size = len(gcc)

# -----------------------------
# Diameter (undirected GCC)
# -----------------------------
G_undirected = G.subgraph(gcc).to_undirected()
diameter = nx.diameter(G_undirected)


# -----------------------------
# Count total European routes (airline level)
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
print("\n--- European Network Statistics ---")
print(f"Number of nodes: {num_nodes}")
print(f"Number of edges: {num_edges}")
print("Total routes (with airlines):", total_routes_europe)
print(f"Density: {density:.5f}")
print(f"Average degree: {avg_degree:.2f}")
print(f"Average weighted degree (strength): {avg_strength:.2f}")
print(f"GCC size: {gcc_size} ({100 * gcc_size / num_nodes:.2f}% of nodes)")
print(f"Diameter (undirected GCC): {diameter}")