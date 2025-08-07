from extract import dataframes
from load import load_all
from schema import metadata, get_engine
from schema import DimDate, DimCustomerSegment, DimProduct, FactSales

def main():
    print("\nIniciando pipeline ETL...\n")
    
    # Crear el esquema si no existe
    engine = get_engine()
    metadata.create_all(engine)
    print("Esquema en la base espejo creado o verificado.\n")

    # Ejecutar la carga
    load_all(dataframes)

    print("\nPipeline ETL completado exitosamente.")

if __name__ == "__main__":
    main()