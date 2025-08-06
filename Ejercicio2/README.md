# Ejercicio 1 -Extracción incremental desde API externa (BCRA)

En este ejercicio se automatiza la extracción de cotizaciones del dólar tipo vendedor desde la página oficial del Banco Central de la República Argentina (BCRA) mediante web scraping con Selenium, y carga los datos en una base de datos PostgreSQL alojada en Render.
Contenido

### Webscapring 

El script navega a la página del BCRA con cotizaciones del dólar.Extrae datos desde la fecha 2010-06-01 hasta la fecha 2025-08-04. Limpia y procesa los datos en un DataFrame de pandas. Carga los datos nuevos incrementalmente en la tabla cotizaciones en PostgreSQL
    (la tabla se crea automáticamente si no existe)

    main.py : Script principal que realiza la extracción y carga incremental de datos.


    Asegurate que Firefox y geckodriver estén instalados y accesibles.

    Configurá el archivo .env con la URL de conexión a PostgreSQL:

DEST2_DB_URL=postgresql://usuario:password@host:puerto/base_de_datos

Uso

Ejecutar el script principal:

python main.py


Usando correctamente Selenium con Firefox en modo headless
✅ Extrayendo la serie 7927 desde la web del BCRA
✅ Parseando correctamente los valores tipo_cambio
✅ Obteniendo todas las filas, incluso con valores mayores a 1.000
✅ Mostrando el DataFrame completo y su longitud