import pickle
import networkx as nx
import pandas as pd

# -----------------------------
# Load European UNWEIGHTED graph
# -----------------------------
with open("data/processed/graph_europe_unweighted.gpickle", "rb") as f:
    G = pickle.load(f)

print("European graph loaded")
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

# -----------------------------
# Load airports with country info
# -----------------------------
airports = pd.read_csv("data/processed/clean_airports_with_country_std.csv")

# -----------------------------
# Helper function to compute stats
# -----------------------------
def compute_stats(G):
    G_undirected = G.to_undirected()
    lcc_nodes = max(nx.connected_components(G_undirected), key=len)
    G_lcc = G_undirected.subgraph(lcc_nodes)

    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    avg_degree = sum(dict(G.degree()).values()) / num_nodes

    lcc_size = G_lcc.number_of_nodes()
    lcc_fraction = 100 * lcc_size / num_nodes
    diameter = nx.diameter(G_lcc)

    return {
        "nodes": num_nodes,
        "edges": num_edges,
        "avg_degree": avg_degree,
        "lcc_size": lcc_size,
        "lcc_fraction": lcc_fraction,
        "diameter": diameter
    }

# -----------------------------
# Baseline statistics
# -----------------------------
baseline_stats = compute_stats(G)

print("\n--- Baseline (before shutdown) ---")
for k, v in baseline_stats.items():
    print(f"{k}: {v}")

# -----------------------------
# Identify Spanish airports
# -----------------------------
spain_airports = airports.loc[
    airports["Country_std"] == "Spain",
    "IATA"
]

spain_airports = set(spain_airports)

print("\nSpanish airports:", len(spain_airports))

# -----------------------------
# Simulate Spain blackout (node removal)
# -----------------------------
G_spain_blackout = G.copy()
G_spain_blackout.remove_nodes_from(spain_airports)

print("After Spain blackout")
print("Nodes:", G_spain_blackout.number_of_nodes())
print("Edges:", G_spain_blackout.number_of_edges())

# -----------------------------
# Statistics after shutdown
# -----------------------------
after_stats = compute_stats(G_spain_blackout)

print("\n--- After Spain blackout ---")
for k, v in after_stats.items():
    print(f"{k}: {v}")

# -----------------------------
# Differences
# -----------------------------
print("\n--- Change (After - Before) ---")
for k in baseline_stats:
    print(f"{k}: {after_stats[k] - baseline_stats[k]}")
