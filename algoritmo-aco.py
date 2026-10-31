import math
import random
import numpy as np

# Coordenadas de los 12 clientes
clientes = {
    1: (0, 0),   2: (5, 3),   3: (8, 6),   4: (2, 7),
    5: (-3, 4),  6: (6, -2),  7: (10, 8),  8: (-5, -3),
    9: (4, -5), 10: (9, 2), 11: (-2, 6), 12: (7, -4)
}

# Calcular distancia entre dos puntos
def calcular_distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Crear matriz de distancias
n = len(clientes)
distancias = np.zeros((n + 1, n + 1))
for i in range(1, n + 1):
    for j in range(1, n + 1):
        if i != j:
            distancias[i][j] = calcular_distancia(clientes[i], clientes[j])

print("✅ Matriz de distancias creada")
print(distancias)

# Parámetros del algoritmo ACO
numero_hormigas = 12
iteraciones = 50
alfa = 1.0    # Importancia de la feromona
beta = 2.0    # Importancia de la distancia
evaporacion = 0.1

# Inicializar feromonas
feromona = np.ones((n + 1, n + 1))

# Ejecutar el algoritmo
mejor_ruta = []
mejor_distancia = float('inf')

for it in range(iteraciones):
    rutas = []
    distancias_rutas = []
    
    for hormiga in range(numero_hormigas):
        actual = random.randint(1, n)
        ruta = [actual]
        visitado = set([actual])
        
        while len(ruta) < n:
            siguiente = [c for c in range(1, n + 1) if c not in visitado]
            probabilidades = []
            for c in siguiente:
                tau = feromona[actual][c] ** alfa
                eta = (1.0 / distancias[actual][c]) ** beta
                probabilidades.append(tau * eta)
            suma = sum(probabilidades)
            probabilidades = [p / suma for p in probabilidades]
            actual = random.choices(siguiente, weights=probabilidades)[0]
            ruta.append(actual)
            visitado.add(actual)
        
        ruta.append(ruta[0])
        rutas.append(ruta)
        d = sum(distancias[ruta[i]][ruta[i+1]] for i in range(len(ruta)-1))
        distancias_rutas.append(d)
        
        if d < mejor_distancia:
            mejor_distancia = d
            mejor_ruta = ruta
    
    # Evaporación de feromonas
    feromona *= (1 - evaporacion)
    # Depositar feromonas en las rutas
    for ruta, d in zip(rutas, distancias_rutas):
        for i in range(len(ruta) - 1):
            feromona[ruta[i]][ruta[i+1]] += 1.0 / d
            feromona[ruta[i+1]][ruta[i]] += 1.0 / d

# Mostrar resultados
print("\n" + "="*50)
print("🏆 MEJOR RUTA ENCONTRADA:")
print(" → ".join(f"C{c}" for c in mejor_ruta))
print(f"📏 Distancia total: {mejor_distancia:.2f} km")
print("="*50)
