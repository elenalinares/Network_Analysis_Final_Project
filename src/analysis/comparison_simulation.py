import pickle
import networkx as nx
import random
import pandas as pd
import numpy as np

# 1. Semilla para estabilidad total
random.seed(10)
np.random.seed(10) # Necesario también para Waxman

with open("data/processed/graph_europe_unweighted.gpickle", "rb") as f:
    G_real = pickle.load(f).to_undirected()

airports = pd.read_csv("data/processed/clean_airports_with_country_std.csv")
spain_nodes = [a for a in airports.loc[airports["Country_std"] == "Spain", "IATA"].tolist() if a in G_real.nodes()]
n_removals = len(spain_nodes)
N = G_real.number_of_nodes()
initial_lcc_real = len(max(nx.connected_components(G_real), key=len))

def get_lcc_curve(G, nodes_to_remove, baseline_size):
    G_temp = G.copy()
    curve = [1.0]
    for node in nodes_to_remove:
        if node in G_temp:
            G_temp.remove_node(node)
        components = list(nx.connected_components(G_temp))
        size = len(max(components, key=len)) if components else 0
        curve.append(size / baseline_size)
    return curve

# --- SIMULACIÓN 1: ESPAÑA (Estratégico) ---
spain_sorted = sorted(spain_nodes, key=lambda x: G_real.degree(x), reverse=True)
curve_spain = get_lcc_curve(G_real, spain_sorted, initial_lcc_real)

# --- SIMULACIÓN 2: ALEATORIO EUROPA ---
random_nodes_europe = random.sample(list(G_real.nodes()), n_removals)
curve_real_random = get_lcc_curve(G_real, random_nodes_europe, initial_lcc_real)

# --- SIMULACIÓN 3: WAXMAN GRAPH (Benchmark Espacial) ---
# Este es el equivalente avanzado al Planar Graph de Chicago
# alpha: probabilidad de aristas cortas. beta: controla la longitud de aristas.
G_theory = nx.waxman_graph(N, alpha=0.15, beta=0.1, seed=10)
theory_lcc_init = len(max(nx.connected_components(G_theory), key=len))

# Ataque aleatorio sobre la red espacial
random_nodes_theory = random.sample(list(G_theory.nodes()), n_removals)
curve_theory_random = get_lcc_curve(G_theory, random_nodes_theory, theory_lcc_init)

# 4. Guardar resultados
results = {
    "spain": curve_spain, 
    "real_random": curve_real_random, 
    "theory_random": curve_theory_random
}

with open("data/processed/final_comparison_data.pkl", "wb") as f:
    pickle.dump(results, f)

print("Datos generados con éxito usando el modelo Waxman (Espacial).")