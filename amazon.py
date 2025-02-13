import requests
from bs4 import BeautifulSoup
import random
import time

# URL Amazon pour rechercher les iPhones (modifie selon le pays)
AMAZON_URL = "https://www.amazon.com/s?k=iphone&crid=49OGAGRFJLMM&sprefix=iphone%2Caps%2C237&ref=nb_sb_noss_1"

# Liste de User-Agents pour éviter d’être détecté
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"
]

def get_headers():
    """Retourne un User-Agent aléatoire"""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.5",
    }

def fetch_page(url):
    """Télécharge la page avec un délai aléatoire pour éviter les blocages."""
    session = requests.Session()
    session.headers.update(get_headers())

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()  # Vérifie si la requête est OK
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Erreur lors du scraping : {e}")
        return None

# Scraper la page Amazon
soup = fetch_page(AMAZON_URL)

if soup:
    # Trouver les annonces d'iPhone
    iphone_data = []
    listings = soup.find_all("div", class_="a-container")

    for listing in listings:
        title = listing.find("span", class_="product-title-word-break")
        price_whole = listing.find("input", class_="a-button-input")

        if title and price_whole:
            full_price = f"${price_whole.text.strip()}"
            iphone_data.append((title.text.strip(), full_price))

    # Afficher les résultats
    print("\n📱 **Liste des iPhones trouvés sur Amazon** 📱\n")
    for title, price in iphone_data:
        print(f"{title} - {price}")

    # Attente aléatoire entre 2 et 5 secondes pour éviter d’être bloqué
    sleep_time = random.uniform(2, 5)
    print(f"\nPause de {sleep_time:.2f} secondes...")
    time.sleep(sleep_time)

    print("\n✅ Scraping terminé avec succès ! 🎉")

else:
    print("⚠️ Impossible d'obtenir les données (Amazon bloque souvent le scraping).")
