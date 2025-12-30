"""
Análisis del Capítulo 1: Probabilidad de Colisiones

Compara las probabilidades empíricas de colisión observadas en el experimento
con la probabilidad teórica del Problema del Cumpleaños.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- CONFIGURACIÓN ---
INPUT_FILE = "resultados.csv"
PLOT_FILE = "probabilidad_colision.png"
THEORETICAL_M = 30  # Tamaño del espacio muestral (enteros del 1 al 30)

def calculate_theoretical_prob(n, m):
    """
    Calcula la probabilidad teórica de al menos una colisión (Problema del Cumpleaños).
    
    Fórmula: P(colisión) ≈ 1 - exp(-N(N-1) / 2M)
    
    Donde:
        N = cantidad de muestras tomadas
        M = tamaño del espacio muestral
    """
    exponent = - (n * (n - 1)) / (2 * m)
    return 1 - np.exp(exponent)

def run_analysis():
    if not os.path.exists(INPUT_FILE):
        print(f"No se encontró el archivo {INPUT_FILE}. Ejecutá primero experimento.py")
        return

    print("Analizando resultados...")
    df = pd.read_csv(INPUT_FILE)
    
    # Calculamos la probabilidad empírica para cada N
    # Agrupamos por N y promediamos la columna 'collision' (True=1, False=0)
    stats = df.groupby('N')['collision'].agg(['mean', 'count']).reset_index()
    stats.rename(columns={'mean': 'prob_empirica', 'count': 'trials'}, inplace=True)
    
    print("Probabilidades empíricas calculadas:")
    print(stats)

    n_values = stats['N'].values
    prob_empirica = stats['prob_empirica'].values
    
    # Generamos la curva teórica para un rango continuo de N
    n_dense = np.linspace(min(n_values), max(n_values), 100)
    prob_teorica = calculate_theoretical_prob(n_dense, THEORETICAL_M)

    # Graficamos: curva teórica vs puntos empíricos
    plt.figure(figsize=(10, 6))
    plt.plot(n_dense, prob_teorica, 'r--', label=f'Teórico (M={THEORETICAL_M})')
    plt.plot(n_values, prob_empirica, 'bo-', label='Empírico (Groq Llama 3.1)')
    
    plt.xlabel('Número de ejecuciones (N)')
    plt.ylabel('Probabilidad de colisión P(A_N)')
    plt.title('Probabilidad de Colisiones vs N')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig(PLOT_FILE)
    print(f"Gráfico guardado en {PLOT_FILE}")

if __name__ == "__main__":
    run_analysis()
