from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy import Integer, Float, String, DateTime, Text

class Base(DeclarativeBase):
    pass

class Cliente(Base):
    __tablename__ = "Clientes"
    id_cliente: Mapped[int] = mapped_column(Integer, primary_key=True)
    coordenada_x: Mapped[float] = mapped_column(Float)
    coordenada_y: Mapped[float] = mapped_column(Float)


class Ejecucion(Base):
    """Una corrida de un método de ruteo dentro de un lote experimental."""
    __tablename__ = "Ejecuciones"
    id_ejecucion: Mapped[int] = mapped_column(Integer, primary_key=True)
    lote: Mapped[str] = mapped_column(String(36), index=True)
    metodo: Mapped[str] = mapped_column(String(30))       # ACO | Vecino mas cercano | Manual
    corrida: Mapped[int] = mapped_column(Integer)
    semilla: Mapped[int | None] = mapped_column(Integer, nullable=True)
    distancia: Mapped[float] = mapped_column(Float)
    tiempo_ms: Mapped[float] = mapped_column(Float)
    ruta: Mapped[str] = mapped_column(String(500))        # ids de cliente separados por '-'
    convergencia: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON (solo ACO)
    parametros: Mapped[str | None] = mapped_column(String(300), nullable=True)
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)