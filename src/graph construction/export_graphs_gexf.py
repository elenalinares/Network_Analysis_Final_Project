import networkx as nx
import pickle

with open("data/processed/graph_europe.gpickle", "rb") as f:
    G = pickle.load(f)

nx.write_gexf(G, "data/processed/graph_europe.gexf")
print("Graph exported to graph_europe.gexf")