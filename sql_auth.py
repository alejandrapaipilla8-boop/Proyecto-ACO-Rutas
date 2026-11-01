import os

from sqlalchemy import create_engine, text

from urllib.parse import quote_plus

# Configurable por variables de entorno; los valores por defecto mantienen el entorno local actual.
usuario = os.getenv("DB_USER", "sa")
password = quote_plus(os.getenv("DB_PASSWORD", "Password123!Aa"))
host = os.getenv("DB_HOST", "localhost:1433")
base = os.getenv("DB_NAME", "master")

connection_string = (

    f"mssql+pyodbc://{usuario}:{password}@{host}/{base}"

    "?driver=ODBC+Driver+18+for+SQL+Server"

    "&TrustServerCertificate=yes"

)

engine = create_engine(connection_string, echo=os.getenv("DB_ECHO", "0") == "1")
