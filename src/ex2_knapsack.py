import matplotlib.pyplot as plt

items = [
    {'id': 1, 'v': 100, 'w': 10},
    {'id': 2, 'v': 2, 'w': 1},
    {'id': 3, 'v': 2, 'w': 1}
]
capacity = 10

def greedy_knapsack(items, capacity, sort_key):
    sorted_items = sorted(items, key=sort_key)
    total_val, total_weight, selected = 0, 0, []
    
    for item in sorted_items:
        if total_weight + item['w'] <= capacity:
            total_weight += item['w']
            total_val += item['v']
            selected.append(item['id'])
            
    return total_val, total_weight

val_weight, w_weight = greedy_knapsack(items, capacity, lambda x: x['w'])

val_ratio, w_ratio = greedy_knapsack(items, capacity, lambda x: -(x['v']/x['w']))

labels = ['Menor Peso Primero', 'Mayor Valor/Peso Primero']
valores = [val_weight, val_ratio]

plt.bar(labels, valores, color=['#E63946', '#2A9D8F'])
plt.ylabel('Valor Total en la Mochila')
plt.title('Comparación de Heurísticas (Greedy Knapsack)')

for i, v in enumerate(valores):
    plt.text(i, v + 2, str(v), ha='center', fontweight='bold')

plt.ylim(0, max(valores) + 15)
plt.show()