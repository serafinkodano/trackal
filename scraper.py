import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- Konfiguracja ---
BASE_URL = "https://www.alensa.pl/soczewki-kontaktowe.html"
DOMAIN = "https://www.alensa.pl"
HISTORY_FILE = "public/history.json"

def fetch_page(url):
    print(f"Pobieranie strony: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def extract_products(soup):
    products_data = []
    products = soup.find_all("a", class_="product")
    
    for p in products:
        name = p.get("data-name")
        price = p.get("data-price")
        link = p.get("href")
        
        if name and price and link:
            # Upewniamy się, że linki są pełne
            if not link.startswith("http"):
                link = DOMAIN + link if link.startswith("/") else DOMAIN + "/" + link
                
            products_data.append({
                "nazwa": name.strip(),
                "cena": float(price),
                "link": link.strip()
            })
            
    return products_data

def get_next_page(soup):
    # Szukamy przycisku "POKAZ WIECEJ PRODUKTOW" ktory laduje ajaxem kolejne strony
    # Alensa ma <a class="ajax btn btn-tercialy btn-uppercase load-more-btn" href="...">
    next_link = soup.find("a", class_="load-more-btn")
    
    if next_link and next_link.get("href"):
        href = next_link.get("href")
        return DOMAIN + href if href.startswith("/") else DOMAIN + "/" + href
        
    return None

def scrape_all_products():
    all_products = {}
    current_url = BASE_URL
    
    while current_url:
        soup = fetch_page(current_url)
        page_products = extract_products(soup)
        
        # Deduplication based on product link
        for p in page_products:
            all_products[p["link"]] = p
            
        print(f"Pobrano {len(page_products)} produktów z tej strony. W sumie unikalnych: {len(all_products)}")
        
        current_url = get_next_page(soup)
        
    return list(all_products.values())

def save_to_local_json(products):
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Utworz katalog public jesli nie istnieje
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    
    # Wczytaj istniejaca historie lub utworz nowa jesli nie ma pliku
    history = {}
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            print("Uwaga: Plik history.json jest uszkodzony, tworzenie nowego.")
            history = {}
            
    # Upewnij sie, ze wezel dzisiejszej daty istnieje
    history[today] = []
    
    # Zapisz produkty pod dzisiejsza data
    for p in products:
        history[today].append({
            "nazwa": p["nazwa"],
            "cena": p["cena"],
            "link": p["link"]
        })
        
    # Zapisz strukture z powrotem do pliku
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
        
    print(f"Dodano {len(products)} produktow do pliku {HISTORY_FILE} na dzien {today}.")

if __name__ == "__main__":
    print("-" * 40)
    print(f"Rozpoczęcie pobierania: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    products = scrape_all_products()
    print(f"Łącznie pobrano {len(products)} produktów. Próba zapisu...")
    save_to_local_json(products)
    print("Zakończono.")
    print("-" * 40)
