# scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_terrenos_posadas():
    url = "https://www.zonaprop.com.ar/terrenos-venta-posadas.html"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    print('pase1')
    terrenos = []
    page = 1

    while len(terrenos) < 20:
        res = requests.get(f"{url}-pagina-{page}", headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        anuncios = soup.find_all("div", class_="posting-card")

        if not anuncios:
            break  # No hay más páginas

        for a in anuncios:
            if len(terrenos) >= 20:
                break
            print('pase2')
            titulo = a.find("h2", class_="posting-title").get_text(strip=True) if a.find("h2", class_="posting-title") else None
            precio = a.find("span", class_="first-price").get_text(strip=True) if a.find("span", class_="first-price") else None
            ubicacion = a.find("span", class_="posting-location").get_text(strip=True) if a.find("span", class_="posting-location") else None

            terrenos.append({
                "titulo": titulo,
                "precio": precio,
                "ubicacion": ubicacion,
                "fuente": res.url
            })

        page += 1
    print('pase3')
    return terrenos