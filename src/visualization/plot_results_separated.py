import pickle
import matplotlib.pyplot as plt
from pathlib import Path

FIG_DIR = Path("data/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

with open("data/processed/final_comparison_data.pkl", "rb") as f:
    res = pickle.load(f)

# ESTE ES EL ZOOM QUE FUNCIONA: Ni muy lejos ni muy cerca
Y_LIM_MIN = 0.82 
Y_LIM_MAX = 1.02

def apply_style(title):
    plt.ylim(Y_LIM_MIN, Y_LIM_MAX)
    plt.title(title, fontsize=13, fontweight='bold')
    plt.xlabel("Airports Removed ($n$)", fontsize=11)
    plt.ylabel("LCC Size ($S/S_0$)", fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend(loc="lower left")

# --- GRÁFICA CONJUNTA (Las 3 líneas juntas) ---
plt.figure(figsize=(10, 6))
plt.plot(res["spain"], color="#c0392b", linewidth=3, label="Spain Shutdown")
plt.plot(res["real_random"], color="#7f8c8d", linewidth=3, label="Random Shutdown")
plt.plot(res["theory_random"], color="#27ae60", linewidth=3, label="Waxman Spatial Benchmark")

# Tu texto original en la roja
plt.text(len(res["spain"])-1, res["spain"][-1], f'  {len(res["spain"])-1} airports closed', 
         color="#c0392b", fontweight='bold', va='center')

apply_style("Network Robustness: Comparative Analysis")
plt.tight_layout()
plt.savefig(FIG_DIR / "4_combined_analysis.png", dpi=300)

# --- GRÁFICAS SEPARADAS (Una por una) ---
tasks = [("spain", "Spain Shutdown", "#c0392b", "1_spain"),
         ("real_random", "European Random Shutdown", "#7f8c8d", "2_random"),
         ("theory_random", "Waxman Spatial Benchmark", "#27ae60", "3_theory")]

for key, name, col, fname in tasks:
    plt.figure(figsize=(8, 5))
    plt.plot(res[key], color=col, linewidth=3, label=name)
    apply_style(name)
    plt.tight_layout()
    plt.savefig(FIG_DIR / f"{fname}.png", dpi=300)
    plt.close()

print("Hecho. Se han generado las 3 individuales y la conjunta (4 imágenes en total).")

# --- EXTRACCIÓN DE DATOS PARA LA TABLA DE RESULTADOS ---
print("\n" + "="*30)
print("DATOS EXACTOS PARA LAS SLIDES")
print("="*30)

# LCC Inicial siempre es 1.0
start_val = 1.0

for key, name in [("spain", "Spain Blackout"), 
                  ("real_random", "Random Europe"), 
                  ("theory_random", "Waxman Model")]:
    
    final_val = res[key][-1]  # El último valor de la lista
    drop_percentage = (start_val - final_val) * 100
    
    print(f"{name}:")
    print(f"  - Final LCC: {final_val:.4f}")
    print(f"  - Total Drop: {drop_percentage:.2f}%")
    print("-" * 20)