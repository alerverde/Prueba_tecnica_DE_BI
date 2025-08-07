# load.py
import os
from dotenv import load_dotenv
from schema import DimDate, DimCustomerSegment, DimProduct, FactSales
from schema import get_engine
from sqlalchemy.orm import Session
from sqlalchemy import insert
from sqlalchemy.dialects.postgresql import insert as pg_insert

load_dotenv()
RENDER_DB_URL = os.getenv("ORIGIN_DB_URL")
engine = get_engine(RENDER_DB_URL)

def upsert_from_df(engine, table, df, id_column):
    with engine.begin() as connection:
        for _, row in df.iterrows():
            stmt = pg_insert(table).values(**row.to_dict())
            update_dict = {c.name: stmt.excluded[c.name] for c in table.columns if c.name != id_column}
            stmt = stmt.on_conflict_do_update(index_elements=[id_column], set_=update_dict)
            connection.execute(stmt)

def load_all(dataframes):
    upsert_from_df(engine, DimDate, dataframes["DimDate"], "dateid")
    upsert_from_df(engine, DimCustomerSegment, dataframes["DimCustomerSegment"], "Segmentid")
    upsert_from_df(engine, DimProduct, dataframes["DimProduct"], "Productid")
    upsert_from_df(engine, FactSales, dataframes["FactSales"], "Salesid")
