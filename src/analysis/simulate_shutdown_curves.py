import pickle
import networkx as nx
import pandas as pd
import random

# -----------------------------
# Load European graph
# -----------------------------
with open("data/processed/graph_europe_unweighted.gpickle", "rb") as f:
    G = pickle.load(f)

# Work with undirected graph for LCC analysis
G_base = G.to_undirected()

# -----------------------------
# CALCULATE BASELINE LCC SIZE (The Fix)
# -----------------------------
# We identify the core connected network (e.g., your 369 nodes)
initial_components = list(nx.connected_components(G_base))
initial_lcc_nodes = max(initial_components, key=len)
LCC_SIZE_BASELINE = len(initial_lcc_nodes) 

print(f"Baseline LCC size: {LCC_SIZE_BASELINE} nodes")

# -----------------------------
# Load airports and identify Spanish nodes
# -----------------------------
airports = pd.read_csv("data/processed/clean_airports_with_country_std.csv")

spain_iata_list = airports.loc[airports["Country_std"] == "Spain", "IATA"].tolist()
spain_in_graph = [a for a in spain_iata_list if a in G_base.nodes()]

# STRATEGIC STEP: Sort Spanish airports by degree (hubs first)
# This makes the attack "targeted" instead of random
spain_airports_sorted = sorted(spain_in_graph, key=lambda x: G_base.degree(x), reverse=True)
n_remove = len(spain_airports_sorted)

# -----------------------------
# Helper: Normalized LCC fraction
# -----------------------------
def lcc_fraction_normalized(graph):
    if graph.number_of_nodes() == 0:
        return 0
    components = list(nx.connected_components(graph))
    if not components:
        return 0
    current_lcc_size = len(max(components, key=len))
    # Normalized by the 369 nodes, so it starts at 1.0 (100%)
    return current_lcc_size / LCC_SIZE_BASELINE

# -----------------------------
# Strategic Spain shutdown (Progressive)
# -----------------------------
G_spain = G_base.copy()
lcc_spain_curve = [lcc_fraction_normalized(G_spain)]

for airport in spain_airports_sorted:
    if airport in G_spain:
        G_spain.remove_node(airport)
        lcc_spain_curve.append(lcc_fraction_normalized(G_spain))

# -----------------------------
# Random shutdown (Europe-wide)
# -----------------------------
all_nodes = list(G_base.nodes())
random_airports = random.sample(all_nodes, n_remove)

G_random = G_base.copy()
lcc_random_curve = [lcc_fraction_normalized(G_random)]

for airport in random_airports:
    if airport in G_random:
        G_random.remove_node(airport)
        lcc_random_curve.append(lcc_fraction_normalized(G_random))

# -----------------------------
# Save results
# -----------------------------
results = {
    "spain": lcc_spain_curve,
    "random": lcc_random_curve
}

with open("data/processed/shutdown_curves.pkl", "wb") as f:
    pickle.dump(results, f)

print("Simulation finished. Data saved to data/processed/shutdown_curves.pkl")

