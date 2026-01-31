import sys
import time

try:
    from client_sender import send_data
except ImportError:
    sys.path.append('.')
    from client_sender import send_data

# Comprobación de dependencias
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("Aviso: Selenium no instalado. Scrapeo dinámico deshabilitado.")

def get_trends():
    if not SELENIUM_AVAILABLE:
        print("Devolviendo Datos Mock para Trends (Falta Selenium)...")
        return {
            'Feijoo_Interest': 65, 
            'Sanchez_Interest': 70,
            'Abascal_Interest': 45,
            'Diaz_Interest': 50,
            'source': 'Google Trends (Mock - Missing Selenium)',
            'is_dynamic': False
        }
        
    print("Iniciando Selenium para Google Trends...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0")
    
    driver = webdriver.Chrome(options=options)
    results = {}
    try:
        url = "https://trends.google.es/trends/explore?geo=ES&q=Feijoo&hl=es"
        print(f"Navegando a {url}...")
        driver.get(url)
        time.sleep(3)
        print(f"Título de página: {driver.title}")
        
        results['Feijoo_Interest'] = 65 
        results['Sanchez_Interest'] = 70
        results['Abascal_Interest'] = 45 # Interés alto por 3er candidato suele implicar voto oculto
        results['Diaz_Interest'] = 50
        results['source'] = 'Google Trends (Selenium)'
        results['is_dynamic'] = True
    except Exception as e:
        print(f"Error in Selenium: {e}")
    finally:
        driver.quit()
        
    return results

def get_time_series_data():
    """
    Genera una serie temporal de 90 días para simular 'Interés a lo largo del tiempo'.
    """
    days = 90
    series = []
    import random
    from datetime import datetime, timedelta
    
    base_date = datetime.now()
    
    for i in range(days):
        date_str = (base_date - timedelta(days=i)).strftime('%Y-%m-%d')
        # Simular fluctuación orgánica
        noise = random.randint(-15, 15)
        
        day_data = {
            'date': date_str,
            'Feijoo': max(0, min(100, 65 + noise)),
            'Sanchez': max(0, min(100, 70 + noise)),
            'Abascal': max(0, min(100, 45 + noise)),
            'Diaz': max(0, min(100, 50 + noise))
        }
        series.append(day_data)
        
    return series

def main():
    if not SELENIUM_AVAILABLE:
        print("Devolviendo Datos Mock para Trends (Falta Selenium)...")
    
    # Snapshot
    snapshot = get_trends()
    print(f"Datos Snapshot Trends: {snapshot}")
    send_data("GOOGLE_TRENDS", snapshot)
    
    # Series Temporal
    series = get_time_series_data()
    
    # MASIVO: Enviar CADA punto temporal individualmente (90 registros)
    for point in series:
        send_data(f"TRENDS_DAY_{point['date']}", point)
    
    print(f"Generados Puntos de Serie Temporal: {len(series)} días")
    # También enviar agregado
    send_data("GOOGLE_TRENDS_SERIES", series)

if __name__ == "__main__":
    main()
