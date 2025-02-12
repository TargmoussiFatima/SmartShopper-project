import requests
from bs4 import BeautifulSoup
import statistics
import random
import time

BASE_URL = "https://books.toscrape.com/"
url = BASE_URL + "catalogue/category/books/philosophy_7/index.html"

# Liste de User-Agents pour éviter d’être bloqué
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"
]

def get_headers():
    """Retourne un User-Agent aléatoire"""
    return {"User-Agent": random.choice(USER_AGENTS)}

def fetch_page(url):
    """Télécharge la page avec un délai aléatoire pour éviter les blocages."""
    session = requests.Session()  # Simule un navigateur
    session.headers.update(get_headers())

    try:
        response = session.get(url, timeout=10)  # Timeout pour éviter le blocage
        response.raise_for_status()  # Vérifie si la requête est OK
        return BeautifulSoup(response.text, "lxml")  # Retourne le HTML analysé par BeautifulSoup
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du scraping : {e}")
        return None

# Récupérer le contenu de la page
soup = fetch_page(url)

if soup:
    # Trouver les balises contenant les prix
    price_tags = soup.find_all("p", class_="price_color")

# Extraire les prix en tant que chaînes de caractères
prices = [price.text.strip() for price in price_tags]

# Afficher les prix extraits
print(prices)


    # Attente aléatoire entre 2 et 5 secondes avant de faire d'autres requêtes
sleep_time = random.uniform(2, 5)
print(f"Pause de {sleep_time:.2f} secondes...")
time.sleep(sleep_time)

