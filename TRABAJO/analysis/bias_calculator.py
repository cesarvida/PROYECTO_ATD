"""
Analizador de Sesgos y Predicción Electoral 2027
Proyecto ATD - Universidad

Desarrollado por: César
Este script analiza los sesgos históricos del CIS y proyecta
los resultados para las elecciones de 2027.
"""

import json
import os
from datetime import datetime

# Rutas de archivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DATOS = os.path.join(BASE_DIR, '../data/raw_data.jsonl')
ARCHIVO_SALIDA = os.path.join(BASE_DIR, '../data/final_prediction_2027.csv')

def cargar_datos():
    """Carga todos los datos scrapeados del JSON Lines"""
    datos = []
    with open(ARCHIVO_DATOS, 'r', encoding='utf-8') as f:
        for linea in f:
            try:
                datos.append(json.loads(linea))
            except:
                pass  # Ignora líneas mal formadas
    return datos

def analizar():
    """Función principal que realiza todo el análisis"""
    datos = cargar_datos()
    
    # Extraemos los diferentes conjuntos de datos
    cis_historico = next((item['data'] for item in datos if item['source'] == 'CIS_HISTORICAL_MULTI'), [])
    oficial = next((item['data'] for item in datos if item['source'] == 'OFFICIAL_MULTI'), {})
    cis_actual = next((item['data'] for item in datos if item['source'] == 'CIS_CURRENT'), {})
    electomania = next((item['data'] for item in datos if item['source'] == 'ELECTOMANIA'), {})
    tendencias = next((item['data'] for item in datos if item['source'] == 'GOOGLE_TRENDS'), {})
    economia = next((item['data'] for item in datos if item['source'] == 'ECONOMIC_CONTEXT'), [])
    
    print("\n" + "="*50)
    print("   SISTEMA DE PREDICCIÓN ELECTORAL 2027   ")
    print("="*50 + "\n")

    # Trabajamos con los 4 partidos principales
    partidos = ['PSOE', 'PP', 'VOX', 'SUMAR']
    
    # Mapeo para Google Trends
    candidatos = {
        'PSOE': 'Sanchez_Interest',
        'PP': 'Feijoo_Interest',
        'VOX': 'Abascal_Interest',
        'SUMAR': 'Diaz_Interest'
    }

    # PASO 0: Contexto Económico (Factor de Corrección)
    print("--- 0. ANÁLISIS DE CONTEXTO ECONÓMICO ---")
    factor_malestar = 0.0
    if economia:
        paro_medio = sum(p['unemployment_rate'] for p in economia) / len(economia)
        print(f"  Tasa de Paro Media (Provincial): {paro_medio:.2f}%")
        
        # Si el paro es alto (>15%), históricamente favorece a la oposición (PP/VOX)
        if paro_medio > 15.0:
            factor_malestar = (paro_medio - 15.0) * 0.2  # 0.2 puntos por cada % extra
            print(f"  ⚠️ ALERTA: Malestar económico detectado (+{factor_malestar:.2f}pp bonificación oposición)")
        else:
            print("  Situación económica estable (sin corrección significativa)")
    else:
        print("  No hay datos económicos disponibles.")


    # PASO 1: Calcular el sesgo histórico del CIS
    print("--- 1. ANÁLISIS DEL SESGO HISTÓRICO DEL CIS ---")
    sesgo = {p: 0.0 for p in partidos}
    contador = 0
    
    # Comparamos predicciones CIS vs resultados reales
    for barometro in cis_historico:
        eleccion = barometro.get('election_id')
        if eleccion in oficial:
            print(f"\nComprobando Elección {eleccion}:")
            datos_cis = barometro['data']
            datos_reales = oficial[eleccion]
            
            for p in partidos:
                pred_cis = datos_cis.get(p, 0)
                real = datos_reales.get(p, 0)
                error = pred_cis - real
                sesgo[p] += error
                print(f"  > {p}: CIS predijo {pred_cis}% vs Real {real}% (Error: {error:+.2f}%)")
            contador += 1
    
    # Calculamos el sesgo promedio
    if contador > 0:
        for p in partidos:
            sesgo[p] /= contador
            print(f"  => SESGO PROMEDIO {p}: {sesgo[p]:+.2f}%")

    # PASO 2: Proyección a 2027 usando regresión lineal
    print("\n--- 2. PROYECCIÓN DE TENDENCIAS → 2027 ---")
    electo_hist = next((item['data'] for item in datos if item['source'] == 'ELECTOMANIA_HISTORICAL'), [])
    
    proyeccion_2027 = {p: 0.0 for p in partidos}
    
    if electo_hist and len(electo_hist) >= 5:
        print(f"Analizando {len(electo_hist)} encuestas históricas...")
        print("Periodo: Julio 2025 → Enero 2026 (6 meses)")
        print("Proyectando a: Enero 2027 (12 meses adelante)\n")
        
        for p in partidos:
            # Convertimos fechas a números (meses desde julio 2025)
            meses = []
            valores = []
            for encuesta in electo_hist:
                fecha = datetime.strptime(encuesta['date'], '%Y-%m-%d')
                # Julio 2025 = mes 0
                mes = (fecha.year - 2025) * 12 + fecha.month - 7
                meses.append(mes)
                valores.append(encuesta['data'].get(p, 0))
            
            # Regresión lineal: y = m*x + b
            # donde m es la tendencia (cuánto sube/baja por mes)
            n = len(meses)
            suma_x = sum(meses)
            suma_y = sum(valores)
            suma_xy = sum(x*y for x,y in zip(meses, valores))
            suma_x2 = sum(x*x for x in meses)
            
            # Calculamos la pendiente
            denom = (n * suma_x2 - suma_x * suma_x)
            if denom != 0:
                m = (n * suma_xy - suma_x * suma_y) / denom
                b = (suma_y - m * suma_x) / n
            else:
                m = 0
                b = suma_y / n if n > 0 else 0
            
            # Valor actual (enero 2026 = mes 6)
            valor_ahora = m * 6 + b
            
            # Proyección a enero 2027 (= mes 18)
            valor_2027 = m * 18 + b
            
            proyeccion_2027[p] = valor_2027
            
            # Mostramos
            flecha = "↗" if m > 0 else "↘"
            print(f"  {flecha} {p}:")
            print(f"      Tendencia: {m:+.3f}pp/mes")
            print(f"      Enero 2026 (hoy): {valor_ahora:.1f}%")
            print(f"      → Enero 2027 (proyección): {valor_2027:.1f}% ({valor_2027-valor_ahora:+.1f}pp)")
    else:
        print("  Datos insuficientes para proyección")

    # PASO 2.5: Detección de Voto Oculto (Google Trends)
    print("\n--- 2.5. DETECCIÓN DE VOTO OCULTO (Google Trends) ---")
    ajuste_voto_oculto = {p: 0.0 for p in partidos}
    
    if tendencias:
        for p in partidos:
            key_trend = candidatos.get(p)
            volumen_busqueda = tendencias.get(key_trend, 0)
            intencion_directa = cis_actual.get(p, 1) # Evitar div/0
            
            # Ratio: Si buscan mucho al candidato pero la intención es baja => Voto Oculto
            ratio = volumen_busqueda / intencion_directa if intencion_directa > 0 else 0
            
            # Umbral empírico: ratio > 3.0 indica anomalía
            if ratio > 5.0 and intencion_directa > 2.0:
                print(f"  ⚠️ {p}: Detectado posible voto oculto (Ratio {ratio:.1f})")
                ajuste_voto_oculto[p] = 1.5 # Sumamos 1.5 puntos conservadores
            else:
                print(f"  {p}: Tendencias normales (Ratio {ratio:.1f})")
    else:
        print("  Sin datos de Google Trends para análisis cruzado")

    # PASO 3: Predicción final combinada
    print("\n--- 3. PREDICCIÓN FINAL 2027 ---")
    prediccion = {}
    
    for p in partidos:
        # Empezamos con la proyección de tendencias (que ya mira a 2027)
        base = proyeccion_2027.get(p, 0)
        
        # 1. Corregimos el sesgo del CIS (50% de corrección)
        corregida = base - (sesgo.get(p, 0) * 0.5)
        
        # 2. Aplicamos corrección por malestar económico (Bonifica oposición: PP/VOX)
        if p in ['PP', 'VOX'] and factor_malestar > 0:
            corregida += (factor_malestar * 0.5) # Repartimos el malestar
        elif p in ['PSOE', 'SUMAR'] and factor_malestar > 0:
            corregida -= (factor_malestar * 0.5) # Penalizamos gobierno
            
        # 3. Sumamos voto oculto específico
        corregida += ajuste_voto_oculto.get(p, 0)
        
        # 4. Mezclamos con Electomania actual para suavizar (70% proyección, 30% actual)
        electo_val = electomania.get(p, base)
        final = corregida * 0.7 + electo_val * 0.3
        
        # Aseguramos valor mínimo razonable
        if final < 0.5 and base > 0:
            final = base * 0.5
        
        prediccion[p] = max(0, final)
        
        print(f"{p}:")
        print(f"  Proyección 2027: {base:.2f}%")
        print(f"  - Sesgo CIS: {sesgo.get(p, 0)*0.5:+.2f}pp")
        if factor_malestar > 0:
            signo = "+" if p in ['PP', 'VOX'] else "-"
            print(f"  {signo} Factor Económico: {factor_malestar*0.5:.2f}pp")
        if ajuste_voto_oculto.get(p, 0) > 0:
            print(f"  + Voto Oculto: {ajuste_voto_oculto[p]:+.2f}pp")
        print(f"  → FINAL: {final:.2f}%")

    # Mostramos el resultado final
    print("\n" + "="*30)
    print("   ESTIMACIÓN 2027   ")
    print("="*30)
    # Ordenamos de mayor a menor
    ordenado = sorted(prediccion.items(), key=lambda x: x[1], reverse=True)
    for partido, porcentaje in ordenado:
        print(f"{partido:10} | {porcentaje:.2f}%")

    # Guardamos a CSV
    print(f"\nGuardando resultados en {ARCHIVO_SALIDA}")
    with open(ARCHIVO_SALIDA, 'w') as f:
        f.write("Party,Estimated %\n")
        for partido, porcentaje in ordenado:
            f.write(f"{partido},{porcentaje:.2f}\n")

if __name__ == "__main__":
    analizar()
