#!/bin/bash
echo "--- STARTING PIPELINE ---"

# 1. Start Server
echo "[1/6] Starting Server..."
python3 server/server.py > server_log.txt 2>&1 &
SERVER_PID=$!
sleep 2

# 2. Run Scrapers
echo "[2/6] Running CIS Scraper..."
python3 scrapers/cis_scraper.py

echo "[3/6] Running InfoElectoral Scraper..."
python3 scrapers/resultados_scraper.py

echo "[4/6] Running Electomania Scraper..."
python3 scrapers/electomania_scraper.py

echo "[5/7] Running Google Trends Scraper..."
python3 scrapers/trends_selenium.py

echo "[6/7] Running Economic Context Scraper..."
python3 scrapers/scraper_economia.py

# 3. Kill Server
echo "[7/7] Stopping Server..."
kill $SERVER_PID

# 4. Run Analysis
echo ""
echo "--- RUNNING ANALYSIS ---"
python3 analysis/bias_calculator.py

# 5. Generate Visualization
echo ""
echo "--- GENERATING VISUALIZATION ---"
python3 analysis/visualizer.py 2>/dev/null || echo "⚠️  Skipped: matplotlib not installed (pip3 install matplotlib)"

echo ""
echo "✅ PIPELINE COMPLETE!"
echo "   📊 Prediction: data/final_prediction_2027.csv"
echo "   📈 Chart: docs/prediction_chart.png (if matplotlib installed)"
