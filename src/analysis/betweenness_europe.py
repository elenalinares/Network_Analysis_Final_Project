import pickle
import networkx as nx

# Load European unweighted graph
with open("data/processed/graph_europe_unweighted.gpickle", "rb") as f:
    G = pickle.load(f)

# Use undirected version for betweenness
G_undirected = G.to_undirected()

# Compute betweenness centrality
betweenness = nx.betweenness_centrality(
    G_undirected,
    normalized=True
)

# Top 10 airports by betweenness
top_betweenness = sorted(
    betweenness.items(),
    key=lambda x: x[1],
    reverse=True
)[:10]

print("Top 10 airports by betweenness centrality:")
for airport, value in top_betweenness:
    print(airport, round(value, 4))
