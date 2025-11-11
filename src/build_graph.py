# src/build_graph.py
"""
Build a directed, weighted NetworkX graph from the cleaned data.

Inputs (from data/processed/):
 - airports_clean.csv
 - routes_weighted.csv   (contains Weight_NumAirlines)

Outputs (saved to data/derived/):
 - graph.gexf      for Gephi and visualization tools
 - graph.graphml   portable XML version

No pickle files are created. Reload later from either .gexf or .graphml.
"""

import networkx as nx
import pandas as pd
from pathlib import Path

# Define directories
ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
DERIVED = ROOT / "data" / "derived"
DERIVED.mkdir(parents=True, exist_ok=True)


def load_processed():
    """Load cleaned airport and route files from data/processed/."""
    airports = pd.read_csv(PROCESSED / "airports_clean.csv", dtype={"ID": str})
    routes = pd.read_csv(PROCESSED / "routes_weighted.csv", dtype={"Departure": str, "Destination": str})
    return airports, routes


def build_graph(airports: pd.DataFrame, routes: pd.DataFrame):
    """Create a directed graph where airports are nodes and routes are edges."""
    G = nx.DiGraph()

    # Add airports as nodes
    for _, row in airports.iterrows():
        node_id = str(row["ID"])
        G.add_node(
            node_id,
            label=row.get("Label", ""),
            lat=row.get("Latitude"),
            lon=row.get("Longitude"),
        )

    # Add routes as directed edges with weight = number of airlines
    weight_col = "Weight_NumAirlines" if "Weight_NumAirlines" in routes.columns else "weight"
    for _, row in routes.iterrows():
        u = str(row["Departure"])
        v = str(row["Destination"])
        try:
            w = int(row[weight_col])
        except Exception:
            w = 1
        G.add_edge(u, v, weight=w)

    return G


def main():
    airports, routes = load_processed()
    G = build_graph(airports, routes)

    # Save the graph in common formats
    nx.write_gexf(G, DERIVED / "graph.gexf")
    nx.write_graphml(G, DERIVED / "graph.graphml")

    print("Graph built and saved to:", DERIVED)
    print("Nodes:", G.number_of_nodes(), "Edges:", G.number_of_edges())


if __name__ == "__main__":
    main()
