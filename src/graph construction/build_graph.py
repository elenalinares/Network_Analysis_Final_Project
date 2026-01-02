#really important code -
#it builds the global unweighted air trasport network
#airports = nodes
#airlines = directed edges

import pandas as pd
import networkx as nx
import pickle

# -----------------------------
# Load cleaned data
# -----------------------------
airports = pd.read_csv("data/processed/clean_airports.csv")
routes = pd.read_csv("data/processed/clean_routes.csv")

print("Clean airports:", len(airports))
print("Clean routes:", len(routes))

# -----------------------------
# Create unweighted graph
# -----------------------------
G = nx.DiGraph()

# Add nodes
for _, row in airports.iterrows():
    G.add_node(
        row["IATA"],
        label=row["Label"],
        latitude=row["Latitude"],
        longitude=row["Longitude"]
    )

# Add edges (ONE per airline route)
for _, row in routes.iterrows():
    G.add_edge(
        row["Departure"],
        row["Destination"],
        airline_id=row["Airline ID"]
    )

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

# -----------------------------
# Save graph
# -----------------------------
with open("data/processed/graph_global_unweighted.gpickle", "wb") as f:
    pickle.dump(G, f)

print("Unweighted global graph saved")