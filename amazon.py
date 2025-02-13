from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Configuration de Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Exécute Chrome en mode invisible
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Lancer le navigateur avec WebDriver Manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL Amazon
AMAZON_URL = "https://www.amazon.com/b?node=283155"

try:
    driver.get(AMAZON_URL)
    time.sleep(5)  # Laisser le temps à la page de charger

    # Récupérer les titres des livres
    titles = driver.find_elements(By.CSS_SELECTOR, "div.p13n-sc-truncate-desktop-type2")
    
    # Récupérer les prix
    prices = driver.find_elements(By.CSS_SELECTOR, "span._cDEzb_p13n-sc-price_3mJ9Z")

    print("\n📚 **Livres trouvés sur Amazon** 📚\n")
    for i in range(len(titles)):
        title = titles[i].get_attribute("title")
        price = prices[i].text if i < len(prices) else "Prix non disponible"
        print(f"{title} - {price}")

finally:
    driver.quit()  # Fermer le navigateur

print("\n✅ Scraping terminé avec succès ! 🎉")
