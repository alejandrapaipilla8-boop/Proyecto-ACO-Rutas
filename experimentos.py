"""Ejecuta ACO N veces (más Manual y Vecino más cercano) y guarda cada corrida en SQL Server.

Uso:  python experimentos.py --corridas 30
"""
import argparse
import json
import time
import uuid

from sqlalchemy.orm import Session

from algoritmos import aco, distancia_ruta, matriz_distancias, ruta_manual, vecino_mas_cercano
from models import Base, Cliente, Ejecucion
from sql_auth import engine

PARAMS_ACO = dict(numero_hormigas=12, iteraciones=50, alfa=1.0, beta=2.0, evaporacion=0.1)


def cargar_clientes():
    with Session(engine) as s:
        regs = s.query(Cliente).order_by(Cliente.id_cliente).all()
    if not regs:
        raise SystemExit("No hay clientes. Ejecuta init_db.py y escribir.py primero.")
    ids = [c.id_cliente for c in regs]
    puntos = [(float(c.coordenada_x), float(c.coordenada_y)) for c in regs]
    return ids, puntos


def cronometrar(fn, *args, **kwargs):
    t0 = time.perf_counter()
    res = fn(*args, **kwargs)
    return res, (time.perf_counter() - t0) * 1000


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corridas", type=int, default=30)
    args = ap.parse_args()

    Base.metadata.create_all(engine)  # crea Ejecuciones si no existe
    ids, puntos = cargar_clientes()
    d = matriz_distancias(puntos)
    lote = str(uuid.uuid4())
    a_ids = lambda ruta: "-".join(str(ids[i]) for i in ruta)
    registros = []

    for k in range(1, args.corridas + 1):
        semilla = 1000 + k
        (ruta, dist, conv), ms = cronometrar(aco, d, semilla=semilla, **PARAMS_ACO)
        registros.append(Ejecucion(lote=lote, metodo="ACO", corrida=k, semilla=semilla,
                                   distancia=dist, tiempo_ms=ms, ruta=a_ids(ruta),
                                   convergencia=json.dumps([round(x, 4) for x in conv]),
                                   parametros=json.dumps(PARAMS_ACO)))

        for nombre, fn in (("Vecino mas cercano", vecino_mas_cercano), ("Manual", ruta_manual)):
            ruta, ms = cronometrar(fn, d)
            registros.append(Ejecucion(lote=lote, metodo=nombre, corrida=k, distancia=distancia_ruta(ruta, d),
                                       tiempo_ms=ms, ruta=a_ids(ruta)))
        print(f"corrida {k:>3}/{args.corridas}  ACO={registros[-3].distancia:.3f}")

    with Session(engine) as s:
        s.add_all(registros)
        s.commit()
    print(f"\nLote {lote} guardado: {len(registros)} filas en dbo.Ejecuciones")


if __name__ == "__main__":
    main()
