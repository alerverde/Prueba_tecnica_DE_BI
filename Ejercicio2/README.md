# Ejercicio 1 -Extracción incremental desde API externa (BCRA)

En este ejercicio se automatiza la extracción de cotizaciones del dólar tipo vendedor desde la página oficial del Banco Central de la República Argentina (BCRA) mediante web scraping con Selenium, y carga los datos en una base de datos PostgreSQL alojada en Render.
Contenido

### Ingesta incremental 

main.py

Este script realiza un pipeline ETL automatizado para extraer la cotización del dólar (tipo vendedor) desde el sitio del BCRA, procesar los datos y cargarlos en una base de datos PostgreSQL alojada en Render.

El proceso consta de:
1. Extracción mediante Selenium de la tabla HTML de cotizaciones desde el sitio web oficial del BCRA.
2. Transformación de los datos en un DataFrame de Pandas con formato limpio.
3. Carga incremental en la tabla `cotizaciones` en la base espejo en la nube (Render), evitando duplicados.


### Automatización

NOTA: En este caso la opción de preferencia hubiese sido Github Actions, pero la configuración de los drives de Firefox y el acceso a la web desde el running de Github no la pude configurar a pesar de varios intentos. Seria una opcion pasar a Chrome.
El .yml se ve as


Por lo detallado anteriormente opté por un cronjob configurado es:

0 0 * * * /usr/bin/python3 /ruta/completa/a/Ejercicio2/main.py >> /ruta/completa/a/Ejercicio2/logs/bnra_update.log 2>&1