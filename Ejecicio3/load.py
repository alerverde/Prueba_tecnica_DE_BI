# load.py
from sqlalchemy import create_engine
from schema import terrenos_table, metadata

def save_to_postgres(terrenos, db_url):
    engine = create_engine(db_url)
    metadata.create_all(engine)
    print('pase6')
    with engine.begin() as conn:
        conn.execute(terrenos_table.insert(), terrenos)
    print('pase7')