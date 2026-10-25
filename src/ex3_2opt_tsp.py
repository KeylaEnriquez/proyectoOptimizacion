import numpy as np
import matplotlib.pyplot as plt

N_CIUDADES = 30
N_EXPERIMENTOS = 20

np.random.seed(42)
coords = np.random.rand(N_CIUDADES, 2)
dist_matrix = np.sqrt(np.sum((coords[:, np.newaxis] - coords) ** 2, axis=2))

def costo_ruta(ruta):
    return sum(dist_matrix[ruta[i], ruta[(i + 1) % N_CIUDADES]] for i in range(N_CIUDADES))

def vecino_mas_cercano(nodo_inicial):
    no_visitados = set(range(N_CIUDADES))
    no_visitados.remove(nodo_inicial)
    ruta = [nodo_inicial]
    actual = nodo_inicial
    while no_visitados:
        siguiente = min(no_visitados, key=lambda ciudad: dist_matrix[actual, ciudad])
        ruta.append(siguiente)
        no_visitados.remove(siguiente)
        actual = siguiente
    return ruta

def two_opt(ruta):
    mejor_ruta = ruta.copy()
    mejora = True
    num_mejoras = 0
    while mejora:
        mejora = False
        for i in range(1, N_CIUDADES - 1):
            for j in range(i + 1, N_CIUDADES):
                if j - i == 1: continue
                nueva_ruta = mejor_ruta[:i] + mejor_ruta[i:j][::-1] + mejor_ruta[j:]
                if costo_ruta(nueva_ruta) < costo_ruta(mejor_ruta):
                    mejor_ruta = nueva_ruta
                    num_mejoras += 1
                    mejora = True
    return mejor_ruta, num_mejoras, costo_ruta(mejor_ruta)

mejoras_random, costos_random = [], []
mejoras_nn, costos_nn = [], []

for _ in range(N_EXPERIMENTOS):

    ruta_random = np.random.permutation(N_CIUDADES).tolist()
    _, imp_rand, costo_rand = two_opt(ruta_random)
    mejoras_random.append(imp_rand)
    costos_random.append(costo_rand)
    
    nodo_inicial = np.random.randint(0, N_CIUDADES)
    ruta_nn = vecino_mas_cercano(nodo_inicial)
    _, imp_nn, costo_nn = two_opt(ruta_nn)
    mejoras_nn.append(imp_nn)
    costos_nn.append(costo_nn)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.boxplot([mejoras_random, mejoras_nn], labels=['Inicio Aleatorio', 'Vecino Más Cercano'])
ax1.set_title('Número de Mejoras necesarias (2-opt)')
ax1.set_ylabel('Cantidad de intercambios aceptados')

ax2.boxplot([costos_random, costos_nn], labels=['Inicio Aleatorio', 'Vecino Más Cercano'])
ax2.set_title('Calidad de la Solución (Costo Final)')
ax2.set_ylabel('Distancia Total Recorrida')

plt.tight_layout()
plt.show()