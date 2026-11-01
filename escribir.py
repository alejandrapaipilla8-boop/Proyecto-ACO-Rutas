from sql_auth import engine
from sqlalchemy.orm import Session
from models import Cliente


coordenadas = [
    (0, 0),
    (5, 3),
    (8, 6),
    (2, 7),
    (-3, 4),
    (6, -2),
    (10, 8),
    (-5, -3),
    (4, -5),
    (9, 2),
    (-2, 6),
    (7, -4)
]



clientes = [
    Cliente(
    coordenada_x=x,
    coordenada_y=y
    )
for x, y in coordenadas
]



with Session(engine) as session:
    session.add_all(clientes)
    session.commit()

print(f'Se insertaron {len(clientes)} clientes correctamente.')