# src/analyze_cph.py
"""
Analyze the derived graph and produce centrality outputs focused on CPH.

Outputs (data/derived/):
 - centralities_all.csv
 - cph_summary.csv
 - cph_neighbors.csv
 - (optional) cph_link_prediction.csv
"""

import networkx as nx
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DERIVED.mkdir(parents=True, exist_ok=True)

GRAPH_GEXF = DERIVED / "graph.gexf"

# Toggle whether to run link prediction (set to True if you want candidates)
RUN_LINK_PREDICTION = True

def load_graph():
    # Load graph from the saved GEXF file.
    G = nx.read_gexf(GRAPH_GEXF)
    # Ensure weight attribute is numeric
    for u, v, d in G.edges(data=True):
        if "weight" in d:
            try:
                d["weight"] = float(d["weight"])
            except Exception:
                d["weight"] = 1.0
        else:
            d["weight"] = 1.0
    return G

def compute_centralities(G):
    # Weighted in/out degree
    in_deg = dict(G.in_degree(weight='weight'))
    out_deg = dict(G.out_degree(weight='weight'))

    # Convert to undirected for betweenness/closeness/eigenvector
    Gu = G.to_undirected(reciprocal=False)

    # Betweenness (unweighted for speed). If you want weighted betweenness,
    # consider using weight as inverse distance; that will be slower and needs careful handling.
    print("Computing betweenness (unweighted)...")
    bet = nx.betweenness_centrality(Gu, weight=None)

    print("Computing closeness (unweighted)...")
    clos = nx.closeness_centrality(Gu)

    # Eigenvector on largest connected component for stability
    print("Computing eigenvector centrality on largest connected component...")
    try:
        largest_cc = max(nx.connected_components(Gu), key=len)
        sub = Gu.subgraph(largest_cc)
        eig_sub = nx.eigenvector_centrality_numpy(sub)
        eig = {n: eig_sub.get(n, 0.0) for n in Gu.nodes()}
    except Exception:
        eig = {n: 0.0 for n in Gu.nodes()}

    # Build dataframe
    rows = []
    for n in G.nodes():
        rows.append({
            "ID": n,
            "Label": G.nodes[n].get("label", ""),
            "Weighted_InDegree": in_deg.get(n, 0.0),
            "Weighted_OutDegree": out_deg.get(n, 0.0),
            "Betweenness": bet.get(n, 0.0),
            "Closeness": clos.get(n, 0.0),
            "Eigenvector": eig.get(n, 0.0)
        })
    df = pd.DataFrame(rows)
    return df

def cph_outputs(G, central_df, cph_id="CPH"):
    if cph_id not in G:
        raise KeyError(f"{cph_id} not present in graph nodes.")

    # Save CPH centrality row
    cph_row = central_df[central_df["ID"] == cph_id]
    cph_row.to_csv(DERIVED / "cph_summary.csv", index=False)

    # Collect neighbors: predecessors and successors
    preds = set(G.predecessors(cph_id))
    succs = set(G.successors(cph_id))
    neighbors = sorted(list(preds | succs))

    neighbor_rows = []
    for nb in neighbors:
        neighbor_rows.append({
            "ID": nb,
            "Label": G.nodes[nb].get("label", ""),
            "Edge_to_CPH_weight": G[nb][cph_id]["weight"] if G.has_edge(nb, cph_id) else 0.0,
            "Edge_from_CPH_weight": G[cph_id][nb]["weight"] if G.has_edge(cph_id, nb) else 0.0
        })
    neigh_df = pd.DataFrame(neighbor_rows)
    neigh_df.to_csv(DERIVED / "cph_neighbors.csv", index=False)

    return cph_row, neigh_df

def link_prediction(G, cph_id="CPH", top_k=50):
    # Convert to undirected simple graph for neighborhood-based predictors
    Gu = nx.Graph()
    for u, v, d in G.edges(data=True):
        w = d.get("weight", 1.0)
        if Gu.has_edge(u, v):
            Gu[u][v]["weight"] += w
        else:
            Gu.add_edge(u, v, weight=w)

    if cph_id not in Gu:
        raise KeyError(f"{cph_id} not present in undirected graph for link prediction.")

    # Candidates: nodes that are not current neighbors nor the node itself
    neighbors = set(Gu.neighbors(cph_id))
    candidates = [n for n in Gu.nodes() if n != cph_id and n not in neighbors]

    pairs = [(cph_id, cand) for cand in candidates]

    # Compute scores
    print("Computing Adamic-Adar scores...")
    aa = {v: p for _, v, p in nx.adamic_adar_index(Gu, pairs)}
    print("Computing Jaccard scores...")
    ja = {v: p for _, v, p in nx.jaccard_coefficient(Gu, pairs)}
    print("Computing Preferential Attachment scores...")
    pa = {v: p for _, v, p in nx.preferential_attachment(Gu, pairs)}

    # Compose dataframe
    rows = []
    for cand in candidates:
        rows.append({
            "ID": cand,
            "Label": Gu.nodes[cand].get("label", "") if "label" in Gu.nodes[cand] else "",
            "AdamicAdar": aa.get(cand, 0.0),
            "Jaccard": ja.get(cand, 0.0),
            "PrefAttach": pa.get(cand, 0.0)
        })
    df = pd.DataFrame(rows)
    # Simple combined score: AA + Jaccard + small-normalized PA
    df["Score"] = df["AdamicAdar"] + df["Jaccard"] + (df["PrefAttach"] / (df["PrefAttach"].max() if df["PrefAttach"].max() > 0 else 1))
    df = df.sort_values("Score", ascending=False).head(top_k)
    df.to_csv(DERIVED / "cph_link_prediction.csv", index=False)
    return df

def main():
    G = load_graph()
    print("Graph loaded:", G.number_of_nodes(), "nodes;", G.number_of_edges(), "edges")

    central_df = compute_centralities(G)
    central_df.to_csv(DERIVED / "centralities_all.csv", index=False)
    print("Saved centralities_all.csv")

    # CPH outputs
    try:
        cph_row, neigh_df = cph_outputs(G, central_df, cph_id="CPH")
        print("Saved cph_summary.csv and cph_neighbors.csv")
    except KeyError as e:
        print("Warning:", e)
        return

    if RUN_LINK_PREDICTION:
        try:
            lp_df = link_prediction(G, cph_id="CPH", top_k=100)
            print("Saved cph_link_prediction.csv (top candidates)")
        except Exception as e:
            print("Link prediction failed:", e)

if __name__ == "__main__":
    main()
