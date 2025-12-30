"""
Análisis del Capítulo 2: Convergencia y Distribución de Errores

Genera gráficos de convergencia del intervalo de confianza y
distribución de las respuestas del modelo.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# --- CONFIGURACIÓN ---
RESULTS_FILE = os.path.join(os.path.dirname(__file__), "resultados.csv")
CONVERGENCE_PLOT = os.path.join(os.path.dirname(__file__), "convergencia_probabilidad.png")
DISTRIBUTION_PLOT = os.path.join(os.path.dirname(__file__), "distribucion_respuestas.png")
CONFIDENCE_LEVEL = 1.96  # z para 95% de confianza

def calculate_normal_approx_interval_vectorized(n_series, p_hat_series, z=1.96):
    """
    Calcula el Intervalo de Confianza por Aproximación Normal de forma vectorizada.
    Utilizado para graficar la evolución del IC a medida que aumenta n.
    """
    n = n_series.replace(0, 1)
    se = (p_hat_series * (1 - p_hat_series) / n) ** 0.5  # Error estándar
    margin = z * se
    
    lower = (p_hat_series - margin).clip(lower=0.0)
    upper = (p_hat_series + margin).clip(upper=1.0)
    
    return lower, upper

def main():
    if not os.path.exists(RESULTS_FILE):
        print(f"No se encontró {RESULTS_FILE}. Ejecutá primero experimento.py")
        return

    df = pd.read_csv(RESULTS_FILE)
    
    # --- 1. Gráfico de Convergencia del Intervalo de Confianza ---
    # Calculamos estadísticas acumulativas
    df['cumulative_n'] = df['run_id']
    df['cumulative_events'] = df['event'].cumsum()
    df['p_hat'] = df['cumulative_events'] / df['cumulative_n']
    
    df['ci_lower'], df['ci_upper'] = calculate_normal_approx_interval_vectorized(
        df['cumulative_n'], df['p_hat']
    )
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['cumulative_n'], df['p_hat'], label='Estimación P(E)', color='#2563eb', linewidth=2)
    plt.fill_between(df['cumulative_n'], df['ci_lower'], df['ci_upper'], 
                     color='#2563eb', alpha=0.2, label='IC 95% (Normal Aprox)')
    
    plt.title('Convergencia de la Estimación de Probabilidad de Error', fontsize=14)
    plt.xlabel('Número de Ejecuciones (n)', fontsize=12)
    plt.ylabel('Probabilidad Estimada', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(CONVERGENCE_PLOT)
    print(f"Gráfico guardado: {CONVERGENCE_PLOT}")
    
    # --- 2. Gráfico de Distribución de Respuestas ---
    plt.figure(figsize=(10, 6))
    
    # Top 5 respuestas más frecuentes
    counts = df['response_text'].value_counts().head(5)
    
    # Verde para respuestas correctas, Rojo para incorrectas
    colors = []
    for resp in counts.index:
        resp_clean = str(resp).strip()
        if resp_clean == "1713" or resp_clean == "1713.":
            colors.append('#22c55e')
        else:
            colors.append('#ef4444')
            
    counts.plot(kind='bar', color=colors, edgecolor='black', rot=45)
    
    plt.title('Distribución de Respuestas (Top 5)', fontsize=14)
    plt.xlabel('Respuesta del Modelo', fontsize=12)
    plt.ylabel('Frecuencia', fontsize=12)
    plt.tight_layout()
    plt.savefig(DISTRIBUTION_PLOT)
    print(f"Gráfico guardado: {DISTRIBUTION_PLOT}")

if __name__ == "__main__":
    main()
