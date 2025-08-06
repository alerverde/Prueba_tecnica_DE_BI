from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, Float, Date, ForeignKey
)
import pandas as pd
from sqlalchemy import insert
from sqlalchemy.dialects.postgresql import insert as pg_insert  # para ON CONFLICT
from sqlalchemy.orm import Session

engine = create_engine("postgresql://admin:admin123@localhost:5432/ventas_db")
metadata = MetaData()

fechas = Table(
    "DimDate", metadata,
    Column("dateid", Integer, primary_key=True),
    Column("date", Date, nullable=False),
    Column("Year", Integer, nullable=False),
    Column("Quarter", Integer, nullable=False),
    Column("QuarterName", String(50), nullable=False),
    Column("Month", Integer, nullable=False),
    Column("Monthname", String(50), nullable=False),    
    Column("Day", Integer, nullable=False),
    Column("Weekday", Integer, nullable=False),
    Column("WeekdayName", String(50), nullable=False)
)

customer_segment = Table(
    "DimCustomerSegment", metadata,
    Column("Segmentid", Integer, primary_key=True),
    Column("City", String(50), nullable=False)
)

productos = Table(
    "DimProduct", metadata,
    Column("Productid", Integer, primary_key=True),
    Column("Producttype", String(100), nullable=False)
)

ventas = Table(
    "FactSales", metadata,
    Column("Salesid", String(100), primary_key=True),
    Column("Dateid", Integer, ForeignKey("DimDate.dateid"), nullable=False),
    Column("Productid", Integer, ForeignKey("DimProduct.Productid"), nullable=False),
    Column("Segmentid", Integer, ForeignKey("DimCustomerSegment.Segmentid"), nullable=False),
    Column("Price_PerUnit", Float, nullable=False),
    Column("QuantitySold", Integer, nullable=False),
)

try:
    metadata.create_all(engine)
    print("Tablas creadas correctamente.")
except Exception as e:
    print(f"Error creando las tablas: {e}")

def upsert_from_csv(engine, table, csv_path, pk_column):
    try:
        df = pd.read_csv(csv_path)
        df = df.where(pd.notnull(df), None)

        table_columns = set(c.name for c in table.columns)
        df = df[[col for col in df.columns if col in table_columns]]

        with Session(engine) as session:
            for _, row in df.iterrows():
                stmt = pg_insert(table).values(**row.to_dict())

                update_cols = {
                    c.name: stmt.excluded[c.name]
                    for c in table.columns
                    if c.name != pk_column
                }

                stmt = stmt.on_conflict_do_update(
                    index_elements=[pk_column],
                    set_=update_cols
                )

                session.execute(stmt)
            session.commit()
            print(f"Datos insertados o actualizados en {table.name}")
    except Exception as e:
        print(f"Error al cargar datos en la tabla {table.name} desde {csv_path}: {e}")

tables_info = [
    (fechas, "tablas/DimDate.csv", "dateid"),
    (customer_segment, "tablas/DimCustomerSegment.csv", "Segmentid"),
    (productos, "tablas/DimProduct.csv", "Productid"),
    (ventas, "tablas/FactSales.csv", "Salesid"),
]

for table, csv_path, pk in tables_info:
    try:
        upsert_from_csv(engine, table, csv_path, pk)
    except Exception as e:
        print(f"Falló la carga para la tabla {table.name}: {e}")

print("Proceso terminado.")



