import json
import os
from datetime import datetime, timedelta

file_path = "public/history.json"
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Wez wszystkie wczorajsze produkty bazujac na dzisiejszych rekordach
    today = list(data.keys())[0]
    yesterday = (datetime.strptime(today, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    two_days_ago = (datetime.strptime(today, "%Y-%m-%d") - timedelta(days=2)).strftime("%Y-%m-%d")
    
    # Skopiuj liste produktów na wczoraj, ale zmien pare cen zeby wymusic trend w gore i w dol
    import copy
    yesterday_products = copy.deepcopy(data[today])
    two_days_products = copy.deepcopy(data[today])
    
    # Zmienmy produkty na indeksie 0 na "spadek" z wczoraj na dzis
    yesterday_products[0]['cena'] = yesterday_products[0]['cena'] + 10.0
    two_days_products[0]['cena'] = two_days_products[0]['cena'] + 15.0
    
    # Zmienmy drugi na "wzrost"
    yesterday_products[1]['cena'] = yesterday_products[1]['cena'] - 5.0
    two_days_products[1]['cena'] = two_days_products[1]['cena'] - 5.0
    
    data[two_days_ago] = two_days_products
    data[yesterday] = yesterday_products
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print("Wygenerowano testowe dane historyczne by pokazac zakladke 'zmiany'")
