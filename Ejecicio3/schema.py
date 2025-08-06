# schema.py
from sqlalchemy import Table, Column, String, MetaData

metadata = MetaData()

terrenos_table = Table(
    "terrenos_posadas", metadata,
    Column("titulo", String),
    Column("precio", String),
    Column("ubicacion", String),
    Column("fuente", String),
)
