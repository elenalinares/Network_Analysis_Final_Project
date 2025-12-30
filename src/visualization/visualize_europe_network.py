import pickle
import networkx as nx
import matplotlib.pyplot as plt

with open("data/processed/graph_europe.gpickle", "rb") as f:
    G = pickle.load(f)

print("European graph loaded")

G_undirected = G.to_undirected()
gcc_nodes = max(nx.connected_components(G_undirected), key=len)
G_gcc = G_undirected.subgraph(gcc_nodes)

print("GCC nodes:", G_gcc.number_of_nodes())
print("GCC edges:", G_gcc.number_of_edges())

degrees = dict(G_gcc.degree())
node_sizes = [degrees[n] * 10 for n in G_gcc.nodes()]

pos = nx.spring_layout(G_gcc, seed=42, k=0.15)

plt.figure(figsize=(12, 12))

nx.draw_networkx_nodes(
    G_gcc,
    pos,
    node_size=node_sizes,
    node_color="steelblue",
    alpha=0.7
)

nx.draw_networkx_edges(
    G_gcc,
    pos,
    alpha=0.2,
    width=0.5
)

plt.title("European Air Transport Network (GCC)")
plt.axis("off")
plt.tight_layout()
plt.show()
