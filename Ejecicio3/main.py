# main.py
from scraper import scrape_terrenos_posadas
from load import save_to_postgres

if __name__ == "__main__":
    print("Iniciando scraping...")
    print('pase8')
    terrenos = scrape_terrenos_posadas()
    print(f"Scrapeados {len(terrenos)} terrenos")
    print('pase9')
    db_url = "postgresql+psycopg2://usuario:password@host:puerto/db"
    save_to_postgres(terrenos, db_url)
    print("Datos guardados en PostgreSQL")
    print('pase9')