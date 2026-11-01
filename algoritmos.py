"""Algoritmos de ruteo: ruta manual, vecino más cercano y colonia de hormigas (ACO).

Todas las rutas son ciclos cerrados que inician y terminan en el índice 0
(el primer cliente, coordenada (0,0), se trata como depósito).
"""
import math
import random

import numpy as np

EPS = 1e-9  # evita división por cero si dos clientes comparten coordenadas


def matriz_distancias(puntos):
    n = len(puntos)
    d = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                d[i][j] = math.dist(puntos[i], puntos[j])
    return d


def distancia_ruta(ruta, d):
    return float(sum(d[ruta[i]][ruta[i + 1]] for i in range(len(ruta) - 1)))


def rotar_a_deposito(ciclo, deposito=0):
    """Rota un ciclo cerrado para que empiece/termine en el depósito."""
    abierto = ciclo[:-1]
    k = abierto.index(deposito)
    abierto = abierto[k:] + abierto[:k]
    return abierto + [deposito]


def ruta_manual(d):
    """Línea base: visitar en el orden de registro (como lo haría un despachador sin optimizar)."""
    n = len(d)
    return list(range(n)) + [0]


def vecino_mas_cercano(d, inicio=0):
    n = len(d)
    ruta, visitado = [inicio], {inicio}
    actual = inicio
    while len(ruta) < n:
        siguiente = min((c for c in range(n) if c not in visitado), key=lambda c: d[actual][c])
        ruta.append(siguiente)
        visitado.add(siguiente)
        actual = siguiente
    return ruta + [inicio]


def aco(d, numero_hormigas=12, iteraciones=50, alfa=1.0, beta=2.0, evaporacion=0.1, semilla=None):
    """Devuelve (mejor_ruta, mejor_distancia, convergencia[mejor distancia por iteración])."""
    rng = random.Random(semilla)
    n = len(d)
    eta = 1.0 / (d + EPS)
    feromona = np.ones((n, n))
    mejor_ruta, mejor_dist = None, float("inf")
    convergencia = []

    for _ in range(iteraciones):
        rutas, dists = [], []
        for _ in range(numero_hormigas):
            actual = rng.randrange(n)
            ruta, visitado = [actual], {actual}
            while len(ruta) < n:
                cand = [c for c in range(n) if c not in visitado]
                pesos = [(feromona[actual][c] ** alfa) * (eta[actual][c] ** beta) for c in cand]
                actual = rng.choices(cand, weights=pesos)[0]
                ruta.append(actual)
                visitado.add(actual)
            ruta.append(ruta[0])
            dist = distancia_ruta(ruta, d)
            rutas.append(ruta)
            dists.append(dist)
            if dist < mejor_dist:
                mejor_dist, mejor_ruta = dist, ruta

        feromona *= (1 - evaporacion)
        for ruta, dist in zip(rutas, dists):
            for i in range(len(ruta) - 1):
                a, b = ruta[i], ruta[i + 1]
                feromona[a][b] += 1.0 / dist
                feromona[b][a] += 1.0 / dist
        convergencia.append(mejor_dist)

    return rotar_a_deposito(mejor_ruta), mejor_dist, convergencia
