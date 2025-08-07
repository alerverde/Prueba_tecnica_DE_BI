import requests
from bs4 import BeautifulSoup
import pandas as pd

# ⚠️ Advertencia: Desactivar la verificación SSL puede ser un riesgo de seguridad.
# Solo se recomienda si el sitio es confiable y estás en un entorno de prueba.
VERIFY_SSL = False

# URL del formulario
url = "https://www.bcra.gob.ar/PublicacionesEstadisticas/Principales_variables_datos.asp?serie=7927"
# Inicializar sesión para mantener cookies
session = requests.Session()

# Paso 1: GET inicial para obtener cookies y campos ocultos
response_get = session.get(url, verify=VERIFY_SSL)
if response_get.status_code != 200:
    raise Exception(f"Error en GET inicial. Código: {response_get.status_code}")

# Parsear HTML del GET para extraer posibles campos ocultos (__VIEWSTATE, etc.) si fuera necesario
soup = BeautifulSoup(response_get.content, 'html.parser')

# Paso 2: POST con parámetros del formulario
payload = {
    "fecha_desde": "01/01/2024",  # Fecha de inicio (formato dd/mm/yyyy)
    "fecha_hasta": "01/08/2025",  # Fecha de fin
    "B1": "Consultar"
}

response_post = session.post(url, data=payload, verify=VERIFY_SSL)
if response_post.status_code != 200:
    raise Exception(f"Error en POST. Código: {response_post.status_code}")

# Paso 3: Parsear HTML de la respuesta POST
soup = BeautifulSoup(response_post.content, "html.parser")
table = soup.find("table")

# Paso 4: Convertir la tabla a un DataFrame de pandas
if table:
    df = pd.read_html(str(table))[0]
    print(df.head())
else:
    print("❌ No se encontró ninguna tabla en la respuesta HTML.")
