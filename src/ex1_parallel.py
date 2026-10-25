import multiprocessing as mp
import time
import matplotlib.pyplot as plt

def estimate_pi_worker(samples):
    import random
    inside = 0
    for _ in range(samples):
        x, y = random.random(), random.random()
        if x*x + y*y <= 1.0:
            inside += 1
    return inside

def run_parallel_pi(total_samples, num_processes):
    samples_per_process = total_samples // num_processes
    pool = mp.Pool(processes=num_processes)
    
    start_time = time.time()
    results = pool.map(estimate_pi_worker, [samples_per_process] * num_processes)
    pool.close()
    pool.join()
    
    total_inside = sum(results)
    pi_estimate = (4.0 * total_inside) / total_samples
    return time.time() - start_time

if __name__ == '__main__':
    samples = 10_000_000
    processes = [1, 2, 4, 8]
    times = []
    
    for p in processes:
        t = run_parallel_pi(samples, p)
        times.append(t)
        
    speedups = [times[0] / t for t in times]
    
    plt.plot(processes, speedups, marker='o', label='Speedup Obtenido')
    plt.plot(processes, processes, linestyle='--', color='gray', label='Speedup Ideal')
    plt.xlabel('Número de Procesos')
    plt.ylabel('Speedup')
    plt.title('Aceleración Paralela vs. N° de Procesos')
    plt.legend()
    plt.grid(True)
    plt.show()