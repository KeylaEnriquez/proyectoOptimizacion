import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations

N_CIUDADES = 9
N_INSTANCIAS = 100

def calcular_matriz_distancias(coords):
    return np.sqrt(np.sum((coords[:, np.newaxis] - coords) ** 2, axis=2))

def costo_ruta(ruta, dist_matrix):
    return sum(dist_matrix[ruta[i], ruta[(i + 1) % len(ruta)]] for i in range(len(ruta)))

def two_opt(ruta, dist_matrix):
    mejor_ruta = ruta.copy()
    mejora = True
    while mejora:
        mejora = False
        for i in range(1, len(ruta) - 1):
            for j in range(i + 1, len(ruta)):
                if j - i == 1: continue
                nueva_ruta = mejor_ruta[:i] + mejor_ruta[i:j][::-1] + mejor_ruta[j:]
                if costo_ruta(nueva_ruta, dist_matrix) < costo_ruta(mejor_ruta, dist_matrix):
                    mejor_ruta = nueva_ruta
                    mejora = True
    return mejor_ruta

ratios = []
costos_opt = []
costos_mst = []
costos_mst_2opt = []

print(f"Evaluando {N_INSTANCIAS} instancias... esto puede tomar un par de segundos.")

for _ in range(N_INSTANCIAS):
    coords = np.random.rand(N_CIUDADES, 2)
    dist_matrix = calcular_matriz_distancias(coords)
    
    mejor_costo_opt = float('inf')
    for perm in permutations(range(1, N_CIUDADES)):
        ruta_actual = [0] + list(perm)
        costo = costo_ruta(ruta_actual, dist_matrix)
        if costo < mejor_costo_opt:
            mejor_costo_opt = costo
            
    G = nx.Graph()
    for i in range(N_CIUDADES):
        for j in range(i+1, N_CIUDADES):
            G.add_edge(i, j, weight=dist_matrix[i, j])
            
    arbol_mst = nx.minimum_spanning_tree(G)
    ruta_mst = list(nx.dfs_preorder_nodes(arbol_mst, source=0))
    costo_mst = costo_ruta(ruta_mst, dist_matrix)
    
    ruta_mst_2opt = two_opt(ruta_mst, dist_matrix)
    costo_mst_2opt = costo_ruta(ruta_mst_2opt, dist_matrix)
    
    ratios.append(costo_mst / mejor_costo_opt)
    costos_opt.append(mejor_costo_opt)
    costos_mst.append(costo_mst)
    costos_mst_2opt.append(costo_mst_2opt)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.hist(ratios, bins=15, color='#9b59b6', alpha=0.8, edgecolor='black')
ax1.axvline(x=2.0, color='red', linestyle='dashed', linewidth=2, label='Límite Teórico (2.0)')
ax1.axvline(x=np.mean(ratios), color='orange', linestyle='dashed', linewidth=2, label=f'Media Observada: {np.mean(ratios):.2f}')
ax1.set_title('Razón de Aproximación (MST / Óptimo)')
ax1.set_xlabel('Costo MST / Costo Óptimo')
ax1.set_ylabel('Frecuencia (Instancias)')
ax1.legend()

ax2.boxplot([costos_opt, costos_mst, costos_mst_2opt], labels=['Óptimo Exacto', 'MST Puro', 'MST + 2-opt'])
ax2.set_title('Comparación de Calidad (Costos)')
ax2.set_ylabel('Costo Total del Recorrido')

plt.tight_layout()
plt.show()