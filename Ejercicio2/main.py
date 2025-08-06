# main.py
from sqlalchemy import create_engine, MetaData, Table, Column, String, Date, NUMERIC, select, func
import pandas as pd
from bs4 import BeautifulSoup
import os

import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract_dolar_bcra():
    print("Extrayendo cotizaciones del BCRA...")

    # Paso 1: URL del formulario
    url = "https://www.bcra.gob.ar/PublicacionesEstadisticas/Principales_variables_datos.asp"

    # Paso 2: Datos que se enviarían desde el formulario
    payload = {
        "serie": "7927",
        "fecha_desde": "01/06/2010",  # formato día/mes/año
        "fecha_hasta": "04/08/2025",
        "B1": "Consultar"
    }

    # Paso 3: Hacemos el POST
    response = requests.post(url, data=payload)

    # Paso 4: Parseamos el HTML para extraer la tabla
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"class": "table"})

    # Paso 5: Convertimos a DataFrame
    data = []
    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) >= 2:
            fecha = cols[0].text.strip()
            valor = cols[1].text.strip().replace(".", "").replace(",", ".")
            try:
                data.append({"fecha": fecha, "tipo_cambio": float(valor)})
            except:
                continue

    df = pd.DataFrame(data)
    df["fecha"] = pd.to_datetime(df["fecha"], dayfirst=True)
    print(df.head())
    return df

def load_to_postgres(df):
    print("Cargando datos a PostgreSQL en Render...")
    DEST2_DB_URL = os.getenv("DEST2_DB_URL")
    engine = create_engine(DEST2_DB_URL, connect_args={"sslmode": "require"})
    metadata = MetaData()

    cotizaciones = Table(
        "cotizaciones", metadata,
        Column("fecha", Date, nullable=False),
        Column("moneda", String(50), nullable=False),
        Column("tipo_cambio", NUMERIC(10,4), nullable=False),
        Column("fuente", String(50), nullable=False)
    )

    metadata.create_all(engine)
    print('pase5')
    df["moneda"] = "Dólar"
    df["fuente"] = "BCRA"
    df = df[["fecha", "moneda", "tipo_cambio", "fuente"]]

    with engine.connect() as conn:
        result = conn.execute(select(func.max(cotizaciones.c.fecha)))
        max_fecha = result.scalar()

    if max_fecha:
        df = df[df["fecha"] > max_fecha]
        print(f"Ingestando incremental desde: {max_fecha.date() + pd.Timedelta(days=1)}")
    else:
        print("Ingesta completa inicial.")

    if not df.empty:
        with engine.begin() as conn:
            conn.execute(cotizaciones.insert(), df.to_dict(orient="records"))
        print(f"{len(df)} filas insertadas en 'cotizaciones'.")
    else:
        print("No hay nuevas filas para insertar.")
    print('pase6')

if __name__ == "__main__":
    try:
        df = extract_dolar_bcra()
        load_to_postgres(df)
    except Exception as e:
        print("Error general en el pipeline:")
        print(e)
