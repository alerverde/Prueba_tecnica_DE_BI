# main.py
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine, MetaData, Table, Column, String, Date, NUMERIC, select, func
import pandas as pd
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv

def extract_dolar_bcra():
    print("Extrayendo cotizaciones del BCRA...")

    options = Options()
    options.headless = True
    options.binary_location = "/snap/bin/firefox" 
    driver = webdriver.Firefox(options=options)

    try:
        url = "https://www.bcra.gob.ar/PublicacionesEstadisticas/Principales_variables_datos.asp?serie=7927"
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "fecha_desde"))
        )

        fecha_desde = driver.find_element(By.NAME, "fecha_desde")
        fecha_hasta = driver.find_element(By.NAME, "fecha_hasta")

        fecha_desde.clear()
        fecha_desde.send_keys("2010-06-01")  # Formato YYYY/MM/DD
        fecha_hasta.clear()
        fecha_hasta.send_keys("2025-08-04")

        consultar_btn = driver.find_element(By.NAME, "B1")
        consultar_btn.click()

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table"))
        )

        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", {"class": "table"})

        data = []
        for tbody in table.find_all("tbody"):
            for row in tbody.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) >= 2:
                    fecha = cols[0].text.strip()
                    valor = cols[1].text.strip().replace(".", "").replace(",", ".")
                    try:
                        data.append({"fecha": fecha, "tipo_cambio": float(valor)})
                    except:
                        continue
        print('pase1')
        df = pd.DataFrame(data)
        df["fecha"] = pd.to_datetime(df["fecha"], dayfirst=True)
        print(f"Filas extraídas: {len(df)}")
        return df
        
    finally:
        driver.quit()
    

def load_to_postgres(df):
    print("Cargando datos a PostgreSQL Render...")
    load_dotenv()
    DEST2_DB_URL = os.getenv("ORIGIN_DB_URL")
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
    print('pase2')
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

if __name__ == "__main__":
    try:
        df = extract_dolar_bcra()
        load_to_postgres(df)
    except Exception as e:
        print("Error general en el pipeline:")
        print(e)
