# Ejercicio 1 - Replicación de base de datos
El objetivo principal de este ejercicio es replicar datos de una base PostgreSQL local a una base en la nube (Render) mediante un pipeline ETL automatizado.  

### Esquema de la base de datos

- `DimDate`: tabla de fechas con columnas para año, mes, día, etc.  
- `DimCustomerSegment`: segmentos de clientes con ciudades.  
- `DimProduct`: productos y tipos.  
- `FactSales`: tabla de hechos de ventas que referencia a las dimensiones.  

### Datos de origen

Los datos de origen están almacenados en archivos CSV dentro de la carpeta `/tablas`. Estos datos se cargan en la base local inicialmente con `crear_db.py`. El esquema se encuentra en `schema.py` y desde ahi se importa a `crear_db.py` y `load.py`.

### Pipeline ETL

- `extract.py`: se conecta a la base local y extrae los datos de las tablas a pandas DataFrames.  
- `load.py`: realiza el upsert (insert/update) en la base destino en Render para mantener la base espejo sincronizada.  
- `main.py`: orquesta la extracción y carga de datos.  

### Cómo correr localmente

1. Levantar un contenedor PostgreSQL local con Docker.
2. Crear base de datos localmente `python3 crear_db.py` (unica vcez). 
3. Ejecutar pipeline con `python3 main.py` y/o automatizar con Github actions.  

### Cómo acceder a la base espejo



