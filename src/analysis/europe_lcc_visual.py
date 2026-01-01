import pickle
import networkx as nx
import matplotlib.pyplot as plt
import math

# -----------------------------
# Load European graph
# -----------------------------
with open("data/processed/graph_europe.gpickle", "rb") as f:
    G = pickle.load(f)

print("European graph loaded")
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

# -----------------------------
# Extract LCC (Largest Connected Component)
# -----------------------------
G_undirected = G.to_undirected()
lcc_nodes = max(nx.connected_components(G_undirected), key=len)
G_lcc = G_undirected.subgraph(lcc_nodes).copy()

print("LCC nodes:", G_lcc.number_of_nodes())
print("LCC edges:", G_lcc.number_of_edges())

# -----------------------------
# Node sizes (degree-based, smooth)
# -----------------------------
degrees = dict(G_lcc.degree())
node_sizes = [math.sqrt(degrees[n]) * 15 for n in G_lcc.nodes()]

# -----------------------------
# Layout
# -----------------------------
pos = nx.spring_layout(
    G_lcc,
    seed=42,
    k=0.12,
    iterations=50
)

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(12, 12))

# Edges (thicker)
nx.draw_networkx_edges(
    G_lcc,
    pos,
    edge_color="#ffbd59",
    alpha=0.18,
    width=1.2
)

# Nodes (with black border)
nx.draw_networkx_nodes(
    G_lcc,
    pos,
    node_size=node_sizes,
    node_color="#e2a9f1",
    edgecolors="black",
    linewidths=0.8,
    alpha=0.9
)

plt.title("LCC Europe Subgraph", fontsize=14)
plt.axis("off")
plt.tight_layout()

plt.savefig("data/figures/europe_lcc.png", dpi=300)
plt.show()