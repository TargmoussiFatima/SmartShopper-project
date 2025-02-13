import requests
from bs4 import BeautifulSoup
import random
import time
import json

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
START_PAGE = 1  # On commence à la première page

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"
]

def get_headers():
    return {"User-Agent": random.choice(USER_AGENTS)}

def fetch_page(url):
    session = requests.Session()
    session.headers.update(get_headers())
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "lxml")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du scraping : {e}")
        return None

def extract_products(soup):
    products = []
    for product in soup.find_all("article", class_="product_pod"):
        title = product.h3.a["title"].strip()
        price = product.find("p", class_="price_color").text.strip()
        stock = product.find("p", class_="instock availability").text.replace("\n", "").strip()
        rating = product.find("p", class_="star-rating")["class"][1] if product.find("p", class_="star-rating") else "No rating"
        
        products.append({
            "title": title,
            "price": price,
            "stock": stock,
            "rating": rating
        })
    return products

def save_to_json(data, filename="products.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Données enregistrées dans {filename}")

def scrape_all_pages():
    all_products = []
    page_number = START_PAGE

    while True:
        url = BASE_URL.format(page_number)
        print(f"Scraping : {url}")
        soup = fetch_page(url)

        if soup and soup.find_all("article", class_="product_pod"):
            all_products.extend(extract_products(soup))
            page_number += 1  # Passer à la page suivante

            sleep_time = random.uniform(2, 5)
            print(f"Pause de {sleep_time:.2f} secondes avant la page {page_number}...")
            time.sleep(sleep_time)
        else:
            print("Aucune nouvelle page trouvée. Fin du scraping.")
            break
    
    save_to_json(all_products)
    print("Scraping terminé avec succès !")

scrape_all_pages()

