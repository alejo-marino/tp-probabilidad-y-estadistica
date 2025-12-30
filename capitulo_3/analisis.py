"""
Análisis del Capítulo 3: Procesos de Poisson y Distribución Exponencial

Procesa 'resultados.csv', calcula métricas y genera gráficos comparando:
- Tiempos de respuesta vs Distribución Exponencial teórica
- Conteos por ventana de tiempo vs Distribución de Poisson teórica

Metodología:
- Se utiliza una "Timeline Virtual" para simular un sistema en saturación
- Se eliminan los delays artificiales entre requests
- Se trunca al último bucket completo para evitar sesgo
"""

import os
import math
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DATA_FILE = os.path.join(os.path.dirname(__file__), "resultados.csv")
DEFAULT_BUCKET_SIZE = 1.0  # Tamaño de ventana en segundos

def analyze_run(filepath, bucket_size=DEFAULT_BUCKET_SIZE):
    print(f"Analizando archivo: {filepath}")
    print(f"Tamaño de bucket: {bucket_size}s")
    
    if not os.path.exists(filepath):
        print("El archivo no existe.")
        return

    df = pd.read_csv(filepath)
    
    # Filtramos solo requests exitosas
    df_ok = df[df['status'] == 'ok'].copy()
    
    if df_ok.empty:
        print("No hay requests exitosas para analizar.")
        return

    n_events = len(df_ok)
    print(f"\nTotal eventos OK: {n_events}")

    # --- 1. Análisis de Tiempos de Respuesta (Distribución Exponencial) ---
    latencies = df_ok['latency_seconds'].values
    mean_latency = np.mean(latencies)
    std_latency = np.std(latencies)
    lambda_hat_1 = 1.0 / mean_latency  # Estimador MLE para λ de la Exponencial
    
    print(f"\n--- Tiempos de Respuesta (n={n_events}) ---")
    print(f"Media (S̄): {mean_latency:.4f} s")
    print(f"Desv. Std: {std_latency:.4f} s")
    print(f"Lambda estimado (1/S̄): {lambda_hat_1:.4f} req/s")
    
    # Gráfico: Histograma vs Curva Exponencial teórica
    plt.figure(figsize=(10, 5))
    count, bins, ignored = plt.hist(latencies, bins=20, density=True, alpha=0.6, color='b', label='Datos Empíricos')
    
    # Curva teórica f(x) = λ * exp(-λx), comenzando desde x=0
    x = np.linspace(0, max(latencies) * 1.1, 100)
    pdf = lambda_hat_1 * np.exp(-lambda_hat_1 * x)
    plt.plot(x, pdf, 'r-', lw=2, label=fr'Exponencial ($\lambda={lambda_hat_1:.2f}$)')
    
    plt.title('Distribución de Tiempos de Respuesta')
    plt.xlabel('Latencia (s)')
    plt.ylabel('Densidad')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plot_file = filepath.replace('.csv', '_latency.png')
    plt.savefig(plot_file)
    print(f"Gráfico de latencia guardado en: {plot_file}")
    plt.close()

    # --- 2. Construcción del Timeline Virtual ---
    # t_virtual[i] = suma de las primeras i latencias
    # Esto simula un sistema en saturación donde cada request comienza inmediatamente
    # después de que la anterior termina
    virtual_completion_times = np.cumsum(latencies)
    
    t_max_raw = virtual_completion_times[-1]
    
    # Truncamos al último bucket completo para evitar sesgo en el conteo
    t_max_usable = math.floor(t_max_raw / bucket_size) * bucket_size
    
    if t_max_usable <= 0:
        print(f"Error: t_max_usable = {t_max_usable}. Aumentar N_REQUESTS o reducir bucket_size.")
        return
    
    # Filtramos eventos que caen dentro del tiempo usable
    mask_usable = virtual_completion_times <= t_max_usable
    n_events_usable = np.sum(mask_usable)
    virtual_times_usable = virtual_completion_times[mask_usable]
    
    print(f"\n--- Timeline Virtual ---")
    print(f"Tiempo total virtual (raw): {t_max_raw:.4f} s")
    print(f"Tiempo usable (truncado): {t_max_usable:.4f} s")
    print(f"Eventos dentro del tiempo usable: {n_events_usable}/{n_events}")

    # --- 3. Conteo de eventos por bucket (Proceso de Poisson) ---
    bins_time = np.arange(0, t_max_usable + bucket_size, bucket_size)
    n_buckets = len(bins_time) - 1
    
    # Contamos cuántos eventos caen en cada ventana de tiempo
    counts, _ = np.histogram(virtual_times_usable, bins=bins_time)
    
    mean_count = np.mean(counts)
    var_count = np.var(counts)
    dispersion_index = var_count / mean_count if mean_count > 0 else 0
    
    # Segundo estimador de λ: basado en conteos
    lambda_hat_2 = n_events_usable / t_max_usable
    
    print(f"\n--- Proceso de Llegada Virtual (Ventana {bucket_size}s) ---")
    print(f"Total buckets completos: {n_buckets}")
    print(f"Conteo Promedio (N̄): {mean_count:.4f}")
    print(f"Varianza Conteos: {var_count:.4f}")
    print(f"Índice de Dispersión (Var/Media): {dispersion_index:.4f} (Poisson ideal = 1.0)")
    print(f"Lambda estimado (N/T): {lambda_hat_2:.4f} req/s")
    
    # Gráfico: Histograma de conteos vs PMF de Poisson
    plt.figure(figsize=(10, 5))
    
    max_count = int(max(counts)) if len(counts) > 0 else 0
    x_counts = np.arange(0, max_count + 2)
    
    plt.hist(counts, bins=np.arange(0, max_count + 3) - 0.5, density=True, 
             alpha=0.6, color='g', rwidth=0.8, label='Empírico')
    
    # PMF de Poisson: P(X=k) = (λΔt)^k * exp(-λΔt) / k!
    lambda_poisson = lambda_hat_2 * bucket_size
    
    def poisson_pmf(k, lam):
        """Función de masa de probabilidad de Poisson."""
        vals = []
        for val in k:
            if val < 0: 
                vals.append(0)
            else:
                try:
                    vals.append((math.exp(-lam) * (lam ** val)) / math.factorial(int(val)))
                except OverflowError:
                    vals.append(0)
        return np.array(vals)

    pmf_vals = poisson_pmf(x_counts, lambda_poisson)
    
    plt.plot(x_counts, pmf_vals, 'mo-', lw=2, label=fr'Poisson ($\lambda \Delta t={lambda_poisson:.2f}$)')
    
    plt.title(f'Distribución de Llegadas por Ventana Virtual ({bucket_size}s)')
    plt.xlabel('Número de Requests completadas')
    plt.ylabel('Probabilidad')
    plt.xticks(x_counts)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plot_file_counts = filepath.replace('.csv', '_counts.png')
    plt.savefig(plot_file_counts)
    print(f"Gráfico de conteos guardado en: {plot_file_counts}")
    plt.close()

    # Guardamos los datos de buckets
    buckets_data = []
    for i in range(n_buckets):
        buckets_data.append({
            "bucket_index": i,
            "bucket_start_virtual": bins_time[i],
            "bucket_end_virtual": bins_time[i+1],
            "count": counts[i]
        })
    buckets_file = filepath.replace('.csv', '_buckets.csv')
    pd.DataFrame(buckets_data).to_csv(buckets_file, index=False)
    print(f"Datos de buckets guardados en: {buckets_file}")
    
    # Guardamos el timeline virtual
    virtual_df = pd.DataFrame({
        "request_id": df_ok['request_id'].values,
        "latency_seconds": latencies,
        "t_virtual_completion": virtual_completion_times,
        "in_usable_range": mask_usable
    })
    virtual_file = filepath.replace('.csv', '_virtual_timeline.csv')
    virtual_df.to_csv(virtual_file, index=False)
    print(f"Timeline virtual guardado en: {virtual_file}")
    
    # Comparación de estimadores
    print("\n=== Comparación de estimadores de Lambda ===")
    print(f"Lambda 1 (1 / LatenciaMedia): {lambda_hat_1:.4f}")
    print(f"Lambda 2 (Eventos / TiempoUsable): {lambda_hat_2:.4f}")
    print(f"Diferencia relativa: {abs(lambda_hat_1 - lambda_hat_2) / lambda_hat_1 * 100:.2f}%")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analizar resultados del experimento Poisson/Exponencial.')
    parser.add_argument("--file", help="Ruta al archivo resultados.csv.")
    parser.add_argument("--bucket", type=float, default=DEFAULT_BUCKET_SIZE, 
                        help="Tamaño de la ventana de tiempo en segundos.")
    args = parser.parse_args()
    
    filepath = args.file if args.file else DATA_FILE
    analyze_run(filepath, bucket_size=args.bucket)
