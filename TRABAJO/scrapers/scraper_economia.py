import sys
import random

try:
    from client_sender import send_data
except ImportError:
    sys.path.append('.')
    from client_sender import send_data

INE_URL = "https://www.ine.es/"

def get_economic_context():
    """
    Genera Indicadores Económicos para las 52 provincias para permitir Correlación Socioeconómica.
    """
    provinces = [
        'Alava', 'Albacete', 'Alicante', 'Almeria', 'Asturias', 'Avila', 'Badajoz', 'Barcelona', 'Burgos', 'Caceres',
        'Cadiz', 'Cantabria', 'Castellon', 'Ciudad Real', 'Cordoba', 'Coruña', 'Cuenca', 'Girona', 'Granada', 'Guadalajara',
        'Guipuzcoa', 'Huelva', 'Huesca', 'Jaen', 'Leon', 'Lleida', 'Lugo', 'Madrid', 'Malaga', 'Murcia', 'Navarra',
        'Ourense', 'Palencia', 'Las Palmas', 'Pontevedra', 'La Rioja', 'Salamanca', 'Segovia', 'Sevilla', 'Soria',
        'Tarragona', 'Teruel', 'Toledo', 'Valencia', 'Valladolid', 'Vizcaya', 'Zamora', 'Zaragoza', 'Ceuta', 'Melilla'
    ]
    
    data = []
    
    for prov in provinces:
        # Simulate realistic disparities
        # South/Extremadura/Canaries -> Higher Unemployment
        if any(x in prov for x in ['Cadiz', 'Sevilla', 'Huelva', 'Badajoz', 'Palmas', 'Almeria', 'Cordoba', 'Jaen']):
            unemployment = round(random.uniform(18, 25), 2)
            income = round(random.uniform(18000, 22000), 0)
        
        # Norte/Madrid/Cataluña -> Menor Desempleo
        elif any(x in prov for x in ['Madrid', 'Barcelona', 'Alava', 'Guipuzcoa', 'Navarra']):
            unemployment = round(random.uniform(8, 12), 2)
            income = round(random.uniform(28000, 35000), 0)
            
        else: # Promedio España
            unemployment = round(random.uniform(12, 18), 2)
            income = round(random.uniform(22000, 26000), 0)
            
        data.append({
            'province': prov,
            'unemployment_rate': unemployment,
            'avg_income_eur': income
        })
        
    return data

def main():
    print("Generando Contexto Socio-Económico...")
    economic_data = get_economic_context()
    
    # MASIVO: Enviar CADA provincia individualmente (50 registros)
    for record in economic_data:
        send_data(f"ECONOMIC_{record['province'].replace(' ', '_')}", record)
    
    print(f"Datos Económicos Generados: {len(economic_data)} registros provinciales")
    # También enviamos el agregado
    send_data("ECONOMIC_CONTEXT", economic_data)

if __name__ == "__main__":
    main()
