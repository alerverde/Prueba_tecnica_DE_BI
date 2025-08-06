# Ejercicio 1 -Extracción incremental desde API externa (BCRA)

En este ejercicio se automatiza la extracción de cotizaciones del dólar tipo vendedor desde la página oficial del Banco Central de la República Argentina (BCRA) mediante web scraping con Selenium, y carga los datos en una base de datos PostgreSQL alojada en Render.
Contenido

### Ingesta incremental 

El script `main.py` tiene dos funciones: extract_dolar_bcra y load_to_postgres. La función extract_dolar_brca navega a la página del BCRA con cotizaciones del dólar. Extrae datos desde la fecha 2010-06-01 hasta la fecha 2025-08-04. Limpia y procesa los datos en un DataFrame de pandas. La función load_to_postgres carga los datos nuevos incrementalmente en la tabla cotizaciones en PostgreSQL.
