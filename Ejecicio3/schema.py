# schema.py
from sqlalchemy import Table, Column, Integer, String, MetaData
print('pase4')
metadata = MetaData()

terrenos_table = Table(
    "terrenos_posadas", metadata,
    Column("titulo", String),
    Column("precio", Integer),
    Column("ubicacion", String),
    Column("fuente", String),
)
print('pase5')