import requests
from bs4 import BeautifulSoup
import random
import time

# URL eBay pour rechercher les iPhone (peut être modifiée selon les besoins)
EBAY_URL = "https://www.ebay.com/sch/i.html?_nkw=iphone"

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
    session = requests.Session()
    session.headers.update(get_headers())

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()  # Vérifie si la requête a réussi
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du scraping : {e}")
        return None

# Scraper la page eBay
soup = fetch_page(EBAY_URL)

if soup:
    # Trouver les annonces d'iPhone
    listings = soup.find_all("li", class_="s-item")

    iphone_data = []
    for listing in listings:
        title = listing.find("div", class_="s-item__title")
        price = listing.find("span", class_="s-item__price")

        if title and price:
            iphone_data.append((title.text.strip(), price.text.strip()))

    # Afficher les résultats
    print("\n📱 **Liste des iPhones trouvés sur eBay** 📱\n")
    for title, price in iphone_data:
        print(f"{title} - {price}")

    # Attente aléatoire entre 2 et 5 secondes avant de refaire une requête
    sleep_time = random.uniform(2, 5)
    print(f"\nPause de {sleep_time:.2f} secondes...")
    time.sleep(sleep_time)

    print("\n Scraping terminé avec succès ! 🎉")
    print("we just nailed it !!!!!!!!")

else:
    print(" Impossible d'obtenir les données.")
