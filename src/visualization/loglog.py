import pickle
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Cargar Grafo
with open("data/processed/graph_europe_unweighted.gpickle", "rb") as f:
    G_total = pickle.load(f)

degrees = [d for _, d in G_total.degree()]
avg_degree = sum(degrees) / len(degrees)

# 2. Definir Categorías (Bins)
bins = {
    "Small / Local\n(1-5)": [d for d in degrees if 1 <= d <= 5],
    "Regional\n(6-20)": [d for d in degrees if 6 <= d <= 20],
    "Medium Hubs\n(21-50)": [d for d in degrees if 21 <= d <= 50],
    "Large Hubs\n(51-100)": [d for d in degrees if 51 <= d <= 100],
    "Super Hubs\n(>100)": [d for d in degrees if d > 100]
}

labels = list(bins.keys())
counts = [len(v) for v in bins.values()]
total_nodes = sum(counts)

# ---------------------------------------------------------
# 3. CÁLCULO DE DATOS PARA LAS SLIDES (Texto para copiar)
# ---------------------------------------------------------
percentages = [(count / total_nodes) * 100 for count in counts]

# Encontrar índices de la más y menos común
idx_max = counts.index(max(counts))
idx_min = counts.index(min(counts))

print("\n" + "="*50)
print("DATOS PARA TU SLIDE (COPIA ESTO):")
print("="*50)
print(f"1. Categoria mas comun: {labels[idx_max].replace('\\n', ' ')}")
print(f"   Porcentaje: {percentages[idx_max]:.2f}% de los nodos")
print(f"   Numero de aeropuertos: {counts[idx_max]}")
print("-" * 30)
print(f"2. Categoria menos comun (Infraestructura Critica): {labels[idx_min].replace('\\n', ' ')}")
print(f"   Porcentaje: {percentages[idx_min]:.2f}% de los nodos")
print(f"   Numero de aeropuertos: {counts[idx_min]}")
print("-" * 30)
print(f"3. Grado Medio (Average Degree): {avg_degree:.2f} conexiones")
print("="*50 + "\n")

# 4. Generar la Gráfica
plt.figure(figsize=(12, 8))
colors = ['#d7ccc8', '#a1887f', '#795548', '#5d4037', '#3e2723']
bars = plt.bar(labels, counts, color=colors, edgecolor="black", alpha=0.9)

# Añadir etiquetas con número y % sobre las barras
for i, bar in enumerate(bars):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 1,
             f'{int(height)}\n({percentages[i]:.1f}%)', 
             ha='center', va='bottom', fontsize=10, fontweight='bold')

# Línea vertical de la media
if avg_degree <= 5: pos = 0
elif avg_degree <= 20: pos = 1
elif avg_degree <= 50: pos = 2
elif avg_degree <= 100: pos = 3
else: pos = 4

plt.axvline(x=pos, color="#e74c3c", linestyle="--", linewidth=2.5, 
            label=f"Avg Degree ({avg_degree:.2f})")

plt.title("Degree Distribution", fontsize=18, fontweight='bold', pad=25)
plt.xlabel("Categories (Number of direct connections per airport)", fontsize=12, labelpad=15)
plt.ylabel("Number of Airports", fontsize=12)
plt.legend()
plt.grid(axis='y', linestyle=':', alpha=0.5)

plt.tight_layout()
plt.show()