import pandas as pd
import networkx as nx
import pickle

# Load cleaned data
airports = pd.read_csv("data/processed/clean_airports.csv")
routes = pd.read_csv("data/processed/clean_routes.csv")

print("Clean airports:", len(airports))
print("Clean routes:", len(routes))

# ---- Aggregate routes to create weights ----
edges_df = (
    routes
    .groupby(["Departure", "Destination"])["Airline ID"]
    .nunique()
    .reset_index(name="weight")
)

print("Unique routes (weighted edges):", len(edges_df))

# ---- Create directed weighted graph ----
G = nx.DiGraph()

# Add nodes
for _, row in airports.iterrows():
    G.add_node(
        row["IATA"],
        label=row["Label"],
        latitude=row["Latitude"],
        longitude=row["Longitude"]
    )

# Add weighted edges
for _, row in edges_df.iterrows():
    G.add_edge(
        row["Departure"],
        row["Destination"],
        weight=row["weight"]
    )

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

# Save graph
with open("data/processed/graph_global.gpickle", "wb") as f:
    pickle.dump(G, f)

print("Weighted global graph saved")
