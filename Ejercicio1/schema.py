# schema.py
from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, Float, Date, ForeignKey
)
import os
from dotenv import load_dotenv

load_dotenv()
DEST_DB_URL = os.getenv("DEST_DB_URL")

try:
    engine = create_engine(DEST_DB_URL, connect_args={"sslmode": "require"})
    metadata = MetaData()

    DimDate = Table(
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

    DimCustomerSegment = Table(
        "DimCustomerSegment", metadata,
        Column("Segmentid", Integer, primary_key=True),
        Column("City", String(50), nullable=False)
    )

    DimProduct = Table(
        "DimProduct", metadata,
        Column("Productid", Integer, primary_key=True),
        Column("Producttype", String(100), nullable=False)
    )

    FactSales = Table(
        "FactSales", metadata,
        Column("Salesid", String(100), primary_key=True),
        Column("Dateid", Integer, ForeignKey("DimDate.dateid"), nullable=False),
        Column("Productid", Integer, ForeignKey("DimProduct.Productid"), nullable=False),
        Column("Segmentid", Integer, ForeignKey("DimCustomerSegment.Segmentid"), nullable=False),
        Column("Price_PerUnit", Float, nullable=False),
        Column("QuantitySold", Integer, nullable=False),
    )

except Exception as e:
    print("Error inicializando metadata o engine:")
    print(e)

def recreate_schema():
    try:
        print("Recreando esquema...")
        metadata.drop_all(engine)
        metadata.create_all(engine)
        print("Esquema recreado.")
    except Exception as e:
        print("Error al recrear el esquema:")
        print(e)

if __name__ == "__main__":
    recreate_schema()