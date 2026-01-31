# Predicción Electoral España 2027

**Proyecto ATD** - Sistema de predicción electoral usando datos 2019-2026 para proyectar resultados de **2027**

## 📅 Contexto Temporal
- **Fecha actual**: Enero 2026
- **Predicción objetivo**: Elecciones 2027
- **Datos utilizados**: 
  - Históricos: 2019-2023 (elecciones reales)
  - Actuales: 2023-2026 (barómetros CIS)
  - Recientes: Jul 2025 - Ene 2026 (encuestas Electomania)

Este proyecto implementa una
## 🚀 Características Clave

- **Arquitectura Distribuida**: Cliente-Servidor comunicándose vía Sockets TCP.
- **Big Data Realista**: Procesa +250 registros de múltiples fuentes (CIS, INE, Interior, Google).
- **Predicción Inteligente (AI-Like)**:
  - **Regresión Lineal**: Proyecta tendencias a futuro (2027).
  - **Corrección de Sesgos**: Elimina la "cocina" del CIS comparando con datos reales.
  - **Factor Económico**: Pondera el voto según la tasa de paro provincial.
  - **Detección de Voto Oculto**: Cruza datos de encuestas con intensidad de búsqueda en Google.
- **Visualización**: Genera gráficos automáticos con `matplotlib`.

## 🛠️ Tecnologías

- **Python 3.12**: Lenguaje principal.
- **Sockets**: Comunicación de red robusta.
- **JSON Lines**: Formato de intercambio de datos eficiente.
- **Matplotlib**: Generación de dashboards visuales.
- **Selenium** (Opcional): Para scraping dinámico avanzado.
## Contenido de la Carpeta
- `scrapers/`: Scripts de extracción de datos (4 fuentes).
- `server/`: Servidor de Sockets TCP.
- `analysis/`: Scripts de cálculo de sesgos, validación y visualización.
- `data/`: Datos generados (JSON y CSV).
- `docs/`: Documentación + gráfica de resultados.

## Requisitos
El proyecto está diseñado para funcionar en **Linux**.
Se recomienda tener instalado Python 3.

Las librerías ideales son (ver `requirements.txt`):
- `beautifulsoup4`
- `requests`
- `selenium`
- `pandas`
- `matplotlib` (NEW: Para visualización)

*NOTA: Si faltan librerías, el sistema tiene un modo **"Fallo Seguro" (Graceful Degradation)** que permite ejecutar la demostración completa utilizando datos simulados robustos.*

## **Partidos Analizados** (9 totales)
Estadales: **PSOE, PP, VOX, SUMAR, PODEMOS**  
Autonómicos: **ERC, JUNTS, PNV, BILDU**

## **Cómo Ejecutar (DEMO)**

Para lanzar todo el sistema (Servidor + 4 Scrapers + Análisis) automáticamente, ejecuta desde la terminal:

```bash
cd /home/cesar/Documentos/CESAR/ATD/PRACTICAS/TRABAJO
chmod +x run_pipeline.sh
./run_pipeline.sh
```

## Salida Esperada
1. Verás iniciarse el **Servidor** en segundo plano.
2. Verás la ejecución secuencial de los **4 Scrapers** (`CIS`, `InfoElectoral`, `Electomania`, `Trends`) enviando mensajes `ACK`.
3. **VALIDACIÓN**: Avisos de calidad de datos (si existen inconsistencias).
4. **ANÁLISIS DE TENDENCIAS**: Detección de momentum temporal (últimos 6 meses).
5. Verás el **Análisis Final** imprimiendo la tabla de predicción para **4 partidos**.
6. Se genera **gráfica comparativa** en `docs/prediction_chart.png`.
7. Resultado final en `data/final_prediction_2027.csv`.

## 🎯 Predicción Final 2027

Basada en datos Enero 2026 + análisis de tendencias:

```
PP:    33.89%  ↗ (Líder consolidado, +4.5pp momentum)
PSOE:  25.10%  ↘ (Perdiendo apoyo, -4.6pp momentum)
VOX:   19.07%  ↗ (Crecimiento sostenido, +4.2pp momentum)
SUMAR:  6.80%  ↘ (Caída significativa, -4.3pp momentum)
```

**Tendencias clave detectadas**:
- **PP consolida liderazgo** con tendencia alcista
- **PSOE pierde ~6 puntos** respecto a 23J-2023
- **VOX crece fuerte** y podría disputar 2º puesto
- **SUMAR en caída libre** (de 12% a 7%)

## Datos Scrapeados
- **58 registros JSON** (vs ~12 originales)
- **10 Barómetros CIS** (2019-2026)
- **15 encuestas Electomania** (Jul 2025 - Ene 2026)
- **Datos de participación** (3 elecciones)
- **Análisis temporal** de tendencias (6 meses)
- **Resultados oficiales** para 4 partidos
