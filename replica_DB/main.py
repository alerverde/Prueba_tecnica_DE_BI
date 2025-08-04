# main.py
from extract import dataframes
from load import load_all

def main():
    print("\nIniciando pipeline ETL...\n")
    load_all(dataframes)
    print("\nPipeline ETL completado exitosamente.")

if __name__ == "__main__":
    main()
