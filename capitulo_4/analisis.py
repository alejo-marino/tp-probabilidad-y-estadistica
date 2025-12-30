"""
Análisis del Capítulo 4: Distribuciones Inducidas

Procesa los resultados de los experimentos de temperatura y top-p,
calcula métricas de dispersión (Entropía de Shannon) y genera
gráficos comparativos de las distribuciones.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

DATA_FILE = os.path.join(os.path.dirname(__file__), "resultados.csv")
CATEGORIES = ['A', 'B', 'C', 'D']  # Espacio muestral fijo

def clean_response(text):
    """
    Extrae la categoría (A, B, C, D) de la respuesta del modelo.
    Devuelve 'INVALID' si no encuentra ninguna o hay ambigüedad.
    """
    if pd.isna(text) or text == "ERROR":
        return "INVALID"
    
    text = str(text).upper().strip()
    
    # Caso ideal: una sola letra
    if text in CATEGORIES:
        return text
    
    # Buscar patrones como "Opción A", "La respuesta es B", etc.
    matches = re.findall(r'\b([ABCD])\b', text)
    if len(matches) == 1:
        return matches[0]
    
    return "INVALID"

def analyze_experiment(filepath=DATA_FILE):
    print(f"Analizando archivo: {filepath}")
    
    if not os.path.exists(filepath):
        print("El archivo no existe.")
        return

    df = pd.read_csv(filepath)
    print(f"Total de registros: {len(df)}")
    
    # Limpiamos las respuestas
    df['category'] = df['response'].apply(clean_response)
    
    print("\n--- Distribución Global de Categorías ---")
    print(df['category'].value_counts())
    
    # Análisis por configuración
    configs = df['config_name'].unique()
    results_by_config = {}
    
    for config_name in configs:
        subset = df[df['config_name'] == config_name]
        total_n = len(subset)
        
        # Conteo de categorías
        counts = subset['category'].value_counts()
        
        # Aseguramos que todas las categorías existan
        for cat in CATEGORIES:
            if cat not in counts:
                counts[cat] = 0
                
        # Probabilidades empíricas
        probs = {cat: counts.get(cat, 0) / total_n for cat in CATEGORIES}
        
        # Entropía de Shannon: H(X) = -Σ p(x) * log₂(p(x))
        # Máximo = log₂(4) = 2 bits para distribución uniforme
        entropy = 0
        for p in probs.values():
            if p > 0:
                entropy -= p * np.log2(p)
                
        results_by_config[config_name] = {
            "counts": counts,
            "probs": probs,
            "entropy": entropy,
            "n": total_n,
            "invalid_count": counts.get("INVALID", 0)
        }
        
        print(f"\nConfiguración: {config_name} (N={total_n})")
        print(f"  Entropía: {entropy:.4f} bits")
        print(f"  Inválidos: {counts.get('INVALID', 0)}")
        print("  Distribución:")
        for cat in CATEGORIES:
            print(f"    {cat}: {probs[cat]:.4f} ({counts.get(cat, 0)})")

    plot_distributions(results_by_config, filepath)

def plot_distributions(results, filepath):
    """Genera gráfico de barras comparando las distribuciones por configuración."""
    configs = list(results.keys())
    categories = CATEGORIES
    
    x = np.arange(len(categories))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    offsets = [-width, 0, width]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    for i, config_name in enumerate(configs):
        offset = offsets[i] if i < len(offsets) else 0
        probs = [results[config_name]['probs'][cat] for cat in categories]
        ax.bar(x + offset, probs, width, label=config_name, 
               color=colors[i % len(colors)], alpha=0.8)

    ax.set_ylabel('Probabilidad Empírica')
    ax.set_title('Distribución de Respuestas por Configuración de Temperatura')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # Mostramos la entropía de cada configuración
    info_text = "Entropía (bits):\n"
    for conf in configs:
        info_text += f"{conf}: {results[conf]['entropy']:.2f}\n"
        
    plt.text(0.02, 0.95, info_text, transform=ax.transAxes, verticalalignment='top', 
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plot_path = filepath.replace('.csv', '_distribucion.png')
    plt.savefig(plot_path)
    print(f"\nGráfico guardado en: {plot_path}")
    plt.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Analizar resultados del experimento de distribuciones.')
    parser.add_argument('file', nargs='?', default=DATA_FILE, help='Archivo CSV a analizar')
    args = parser.parse_args()
    
    analyze_experiment(args.file)
