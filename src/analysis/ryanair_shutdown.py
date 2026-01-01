import pickle
import networkx as nx

# -----------------------------
# Load European graph
# -----------------------------
with open("data/processed/graph_europe.gpickle", "rb") as f:
    G = pickle.load(f)

print("European graph loaded")
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

# -----------------------------
# Helper: compute basic metrics
# -----------------------------
def compute_metrics(G):
    G_undirected = G.to_undirected()

    lcc_nodes = max(nx.connected_components(G_undirected), key=len)
    G_lcc = G_undirected.subgraph(lcc_nodes)

    metrics = {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "lcc_size": len(lcc_nodes),
        "avg_degree": sum(dict(G.degree()).values()) / G.number_of_nodes(),
        "diameter": nx.diameter(G_lcc)
    }
    return metrics

# -----------------------------
# Baseline metrics
# -----------------------------
baseline = compute_metrics(G)

print("\n--- Baseline (before Ryanair shutdown) ---")
for k, v in baseline.items():
    print(f"{k}: {v}")

# -----------------------------
# Ryanair shutdown (remove edges)
# -----------------------------
G_no_FR = G.copy()

edges_to_remove = [
    (u, v) for u, v, d in G_no_FR.edges(data=True)
    if "FR" in d.get("Airline ID", [])
]

print("\nRyanair edges to remove:", len(edges_to_remove))

G_no_FR.remove_edges_from(edges_to_remove)

# -----------------------------
# After-shutdown metrics
# -----------------------------
after = compute_metrics(G_no_FR)

print("\n--- After Ryanair shutdown ---")
for k, v in after.items():
    print(f"{k}: {v}")

# -----------------------------
# Simple comparison
# -----------------------------
print("\n--- Change (After - Before) ---")
for k in baseline:
    print(f"{k}: {after[k] - baseline[k]}")