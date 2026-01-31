import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import csv
import os
import numpy as np

# Resolve paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, '../data/final_prediction_2027.csv')
OUTPUT_IMAGE = os.path.join(BASE_DIR, '../docs/prediction_chart.png')

def visualize_results():
    """
    Generates a modern bar chart comparing predicted 2027 results with actual 2023 results.
    """
    # Load prediction
    if not os.path.exists(DATA_FILE):
        print("Prediction file not found. Run bias_calculator.py first.")
        return
    
    parties = []
    predictions = []
    
    with open(DATA_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            parties.append(row['Party'])
            predictions.append(float(row['Estimated %']))
    
    # Historical results 23J-2023 (for comparison) - 4 main parties
    results_2023 = {
        'PP': 33.06,
        'PSOE': 31.68,
        'VOX': 12.38,
        'SUMAR': 12.31
    }
    
    actual_2023 = [results_2023.get(p, 0) for p in parties]
    
    # Color Palette Mapping (Official Party Colors)
    party_colors = {
        'PP': '#0055a7',    # Blue
        'PSOE': '#ef1c1e',  # Red
        'VOX': '#63be21',   # Green
        'SUMAR': '#e51c55'  # Pink
    }
    
    # Assign colors based on party list order
    colors_2023_mapped = [party_colors.get(p, '#888888') for p in parties]
    # Prediction bars slightly darker or same
    colors_2027_mapped = [party_colors.get(p, '#888888') for p in parties]
    
    # Create modern chart
    fig, ax = plt.subplots(figsize=(14, 7), facecolor='#f8f9fa')
    ax.set_facecolor('#ffffff')
    
    x = np.arange(len(parties))
    width = 0.38
    
    # Bars with party-specific colors
    bars1 = ax.bar([i - width/2 for i in x], actual_2023, width, 
                    label='23J-2023 (Real)', alpha=0.6, 
                    color=colors_2023_mapped, edgecolor='#2c3e50', linewidth=1.0)
    bars2 = ax.bar([i + width/2 for i in x], predictions, width, 
                    label='2027 (Predicción)', alpha=1.0, 
                    color=colors_2027_mapped, edgecolor='#2c3e50', linewidth=1.5)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Styling
    ax.set_xlabel('Partidos Políticos', fontsize=14, fontweight='bold', color='#2c3e50')
    ax.set_ylabel('Porcentaje de Voto (%)', fontsize=14, fontweight='bold', color='#2c3e50')
    ax.set_title('Predicción Electoral 2027 vs Resultados 23J-2023\nSistema de Análisis ATD - España', 
                 fontsize=16, fontweight='bold', color='#2c3e50', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(parties, fontsize=12, fontweight='bold')
    ax.legend(fontsize=11, loc='upper right', framealpha=0.95)
    ax.grid(axis='y', alpha=0.25, linestyle='--', linewidth=0.8)
    ax.set_ylim(0, max(max(actual_2023), max(predictions)) * 1.15)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#95a5a6')
    ax.spines['bottom'].set_color('#95a5a6')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE, dpi=200, facecolor='#f8f9fa')
    print(f"✅ Modern chart saved to {OUTPUT_IMAGE}")

if __name__ == "__main__":
    try:
        visualize_results()
    except Exception as e:
        print(f"❌ Visualization failed: {e}")
        print("   (Install matplotlib with: pip3 install matplotlib)")
