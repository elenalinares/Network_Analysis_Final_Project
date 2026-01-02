import pickle #para descargar fotos
import networkx as nx #báisca, para network analysis
import matplotlib.pyplot as plt #graphs
from pathlib import Path #file routes

# -----------------------------
# Paths - create a folder
# -----------------------------
FIG_DIR = Path("data/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Load European UNWEIGHTED graph
# -----------------------------
with open("data/processed/graph_europe_unweighted.gpickle", "rb") as f:
    G_europe = pickle.load(f) #basic af graph loading

print("European graph loaded")
print("Nodes:", G_europe.number_of_nodes())
print("Edges:", G_europe.number_of_edges())

# -----------------------------
# Extract Largest Connected Component (LCC)  --  basic info
# -----------------------------
G_undirected = G_europe.to_undirected()
lcc_nodes = max(nx.connected_components(G_undirected), key=len)
G_lcc = G_europe.subgraph(lcc_nodes).copy()

print("LCC nodes:", G_lcc.number_of_nodes())
print("LCC edges:", G_lcc.number_of_edges())

# -----------------------------
# Degree distribution + ploting it
# -----------------------------
degrees = [d for _, d in G_lcc.degree()]
avg_degree = sum(degrees) / len(degrees)

plt.figure(figsize=(8, 5))

plt.hist(
    degrees,
    bins=40,
    color="#ada090",      # brown
    edgecolor="black",
    alpha=0.85
)

plt.axvline(
    avg_degree,
    color="black",
    linestyle="--",
    linewidth=1,
    label=f"Average degree = {avg_degree:.2f}"
)

plt.xlabel("Degree (number of direct connections per airport)")
plt.ylabel("Number of airports")
plt.title("Degree Distribution of Airports (European LCC)")
plt.legend()

plt.tight_layout()

# -----------------------------
# Save figure
# -----------------------------
output_path = FIG_DIR / "degree_distribution_europe_lcc.png"
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Figure saved to {output_path}")
