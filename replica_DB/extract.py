# extract.py
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()  # carga variables desde .env al entorno

ORIGIN_DB_URL = os.getenv("ORIGIN_DB_URL")

# Crear el motor de conexión
engine = create_engine(ORIGIN_DB_URL)

# Lista de tablas que queremos extraer
TABLE_NAMES = ["DimDate", "DimCustomerSegment", "DimProduct", "FactSales"]

# Diccionario donde guardaremos los DataFrames
dataframes = {}

print("Extrayendo tablas desde la base origen...\n")

for table in TABLE_NAMES:
    try:
        df = pd.read_sql(f'SELECT * FROM "{table}"', engine)
        dataframes[table] = df
        print(f"{table} extraída: {len(df)} filas")
    except Exception as e:
        print(f"Error extrayendo {table}: {e}")

print("\n Extracción finalizada.")