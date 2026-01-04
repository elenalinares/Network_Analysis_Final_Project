import pickle
import matplotlib.pyplot as plt
from pathlib import Path

FIG_DIR = Path("data/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

# 1. Cargar los datos
with open("data/processed/final_comparison_data.pkl", "rb") as f:
    curves = pickle.load(f)

lcc_spain = curves["spain"]
lcc_random = curves["real_random"]
n_airports = len(lcc_spain) - 1

plt.figure(figsize=(10, 6))

# 2. Dibujar curvas (AMBAS CONTINUAS)
plt.plot(lcc_spain, color="#c0392b", linewidth=3, label="Spain Shutdown")
plt.plot(lcc_random, color="#7f8c8d", linewidth=3, label="Random Shutdown") 

# 3. Texto al final de la línea roja
plt.text(n_airports, lcc_spain[-1], f'  {n_airports} airports closed', 
         color="#c0392b", fontweight='bold', va='center')

# --- ZOOM CORREGIDO (IGUAL AL DE LAS SEPARADAS) ---
# Usamos un margen muy pequeño (0.02) para que la curva destaque
min_val = min(min(lcc_spain), min(lcc_random))
plt.ylim(min_val - 0.02, 1.02) # Este es el zoom "apretado" que pedías

# Formato de Network Analysis
plt.xlabel("Number of Airports Closed ($n$)", fontsize=12)
plt.ylabel("Relative LCC Size ($S/S_0$)", fontsize=12)
plt.title("Network Robustness Analysis", fontsize=14)

plt.grid(alpha=0.2, linestyle='--')
plt.axhline(y=1.0, color='black', linewidth=0.8, alpha=0.3)
plt.legend(loc="lower left", frameon=True)

plt.tight_layout()
plt.savefig(FIG_DIR / "network_robustness_analysis.png", dpi=300)
plt.show()

print(f"Graph saved with enhanced zoom in: {FIG_DIR / 'network_robustness_analysis.png'}")