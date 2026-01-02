#silly code to get a visualilzation on gephi

import networkx as nx
import pickle

# -----------------------------
# Load European UNWEIGHTED graph
# -----------------------------
with open("data/processed/graph_europe_unweighted.gpickle", "rb") as f:
    G = pickle.load(f)

print("European unweighted graph loaded")
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

# -----------------------------
# Export to GEXF for Gephi
# -----------------------------
nx.write_gexf(G, "data/processed/graph_europe_unweighted.gexf")

print("Graph exported to data/processed/graph_europe_unweighted.gexf")

