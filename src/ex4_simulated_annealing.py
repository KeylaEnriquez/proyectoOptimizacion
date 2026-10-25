import numpy as np
import matplotlib.pyplot as plt
import time
import math

N_CIUDADES = 20
np.random.seed(42)
coords = np.random.rand(N_CIUDADES, 2)
dist_matrix = np.sqrt(np.sum((coords[:, np.newaxis] - coords) ** 2, axis=2))

def costo_ruta(ruta):
    return sum(dist_matrix[ruta[i], ruta[(i + 1) % N_CIUDADES]] for i in range(N_CIUDADES))

def simulated_annealing(temp_inicial, temp_final, enfriamiento_tipo, alpha, max_iter):
    ruta_actual = np.random.permutation(N_CIUDADES).tolist()
    mejor_ruta = ruta_actual.copy()
    costo_actual = costo_ruta(ruta_actual)
    mejor_costo = costo_actual
    
    T = temp_inicial
    historial_costos = [costo_actual]
    start_time = time.time()
    
    for iteracion in range(max_iter):
        if T <= temp_final:
            break
            
        i, j = sorted(np.random.choice(range(N_CIUDADES), 2, replace=False))
        if j - i == 1: continue
        ruta_vecina = ruta_actual[:i] + ruta_actual[i:j][::-1] + ruta_actual[j:]
        costo_vecino = costo_ruta(ruta_vecina)
        
        delta_costo = costo_vecino - costo_actual
        if delta_costo < 0 or np.random.rand() < math.exp(-delta_costo / T):
            ruta_actual = ruta_vecina
            costo_actual = costo_vecino
            if costo_actual < mejor_costo:
                mejor_costo = costo_actual
                
        historial_costos.append(costo_actual)
        
        if enfriamiento_tipo == 'exponencial':
            T *= alpha
        elif enfriamiento_tipo == 'lineal':
            T -= alpha
            
    tiempo_exec = time.time() - start_time
    return historial_costos, mejor_costo, tiempo_exec

T0 = 100
Tf = 0.1
max_iteraciones = 1500

hist_exp, costo_exp, tiempo_exp = simulated_annealing(T0, Tf, 'exponencial', 0.99, max_iteraciones)

alpha_lin = (T0 - Tf) / 500
hist_lin, costo_lin, tiempo_lin = simulated_annealing(T0, Tf, 'lineal', alpha_lin, max_iteraciones)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(hist_exp, label='Exponencial', color='blue')
ax1.plot(hist_lin, label='Lineal', color='orange')
ax1.set_title('Convergencia: Costo vs Iteraciones')
ax1.set_xlabel('Iteraciones')
ax1.set_ylabel('Costo de la Ruta')
ax1.legend()

ax2_2 = ax2.twinx()
ax2.bar([0, 1], [tiempo_exp, tiempo_lin], width=0.4, color='lightblue', label='Tiempo (s)')
ax2_2.plot([0, 1], [costo_exp, costo_lin], color='red', marker='o', linewidth=2, label='Costo Final')

ax2.set_xticks([0, 1])
ax2.set_xticklabels(['Exponencial', 'Lineal'])
ax2.set_ylabel('Tiempo de Ejecución (segundos)', color='blue')
ax2_2.set_ylabel('Costo Final (menor es mejor)', color='red')
ax2.set_title('Tiempo de Cómputo vs Calidad')

plt.tight_layout()
plt.show()