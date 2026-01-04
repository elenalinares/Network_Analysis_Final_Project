import pickle
import networkx as nx

# 1. Cargar el grafo
path_grafo = "data/processed/graph_europe_unweighted.gpickle"

try:
    with open(path_grafo, "rb") as f:
        G_total = pickle.load(f)
    
    # 2. Filtrar los hubs con grado > 50
    hubs_criticos = [nodo for nodo, grado in G_total.degree() if grado > 50]

    lista_hubs = []
    for nodo in hubs_criticos:
        # 'nodo' suele ser el ID/Abreviatura (MAD, BCN...)
        # 'label' suele ser el nombre largo (Adolfo Suárez Madrid-Barajas...)
        abreviatura = str(nodo) 
        nombre_completo = G_total.nodes[nodo].get('label', 'N/A')
        grado = G_total.degree(nodo)
        lista_hubs.append((abreviatura, nombre_completo, grado))

    # 3. Ordenar por grado
    lista_hubs.sort(key=lambda x: x[2], reverse=True)

    # 4. Imprimir para copiar a Gephi
    print("\n" + "="*60)
    print(f"{'IATA':<10} | {'NOMBRE COMPLETO':<35} | {'GRADO':<6}")
    print("="*60)
    for iata, nombre, grado in lista_hubs:
        print(f"{iata:<10} | {nombre[:33]:<35} | {grado:<6}")
    print("="*60)
    print(f"Total hubs para etiquetar: {len(lista_hubs)}")

except Exception as e:
    print(f"Error: {e}")