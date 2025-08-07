import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL del formulario
url = "https://www.bcra.gob.ar/PublicacionesEstadisticas/Principales_variables_datos.asp"

# Inicializar sesión para mantener cookies
session = requests.Session()

# Paso 1: GET inicial para obtener cookies y mantener la sesión
response_get = session.get(url)
if response_get.status_code != 200:
    raise Exception(f"Error en GET inicial. Código: {response_get.status_code}")

# Paso 2: POST con parámetros del formulario
payload = {
    "serie": "7927",  # Dólar tipo vendedor
    "fecha_desde": "01/01/2024",  # Puedes modificar esto
    "fecha_hasta": "01/08/2025",
    "B1": "Consultar"
}

response_post = session.post(url, data=payload)
if response_post.status_code != 200:
    raise Exception(f"Error en POST. Código: {response_post.status_code}")

# Paso 3: Parsear HTML con BeautifulSoup
soup = BeautifulSoup(response_post.content, "html.parser")
table = soup.find("table")

# Paso 4: Convertir tabla a DataFrame
if table:
    df = pd.read_html(str(table))[0]
    print(df.head())
else:
    print("❌ No se encontró ninguna tabla en la respuesta HTML.")

