"""
Experimento del Capítulo 3: Procesos de Poisson/Exponencial

Este script realiza múltiples llamadas a la API de Groq para medir los tiempos de respuesta.
Los resultados se guardan en 'resultados.csv' para su posterior análisis.
"""

import sys
import os
import time
import statistics
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import GroqClient

# --- CONFIGURACIÓN ---
MODEL = "llama-3.1-8b-instant"
PROMPT = "Respondé con un solo número aleatorio entre 1 y 100."
INFERENCE_PARAMS = {
    "temperature": 1.0,
    "top_p": 1.0,
    "max_tokens": 10
}
N_REQUESTS = 300       # Cantidad de requests a realizar
SLEEP_SECONDS = 5.0    # Delay entre requests (para evitar rate limits)
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "resultados.csv")

def run_experiment():
    print(f"=== Capítulo 3 - Experimento Poisson/Exponencial ===")
    print(f"Modelo: {MODEL}")
    print(f"N Requests: {N_REQUESTS}")
    print(f"Delay entre requests: {SLEEP_SECONDS}s")
    
    try:
        client = GroqClient()
    except ValueError as e:
        print(f"Error inicializando cliente: {e}")
        return

    results = []
    latencies = []
    
    print(f"Iniciando recolección de datos...")
    t_run_start = time.time()
    
    count_ok = 0
    count_error = 0
    
    try:
        for i in range(1, N_REQUESTS + 1):
            request_id = i
            print(f"Request {i}/{N_REQUESTS}...", end="", flush=True)
            
            t_start = time.time()
            status = "ok"
            error_type = None
            
            try:
                client.chat(
                    messages=[{"role": "user", "content": PROMPT}],
                    temperature=INFERENCE_PARAMS["temperature"],
                    top_p=INFERENCE_PARAMS["top_p"],
                    max_tokens=INFERENCE_PARAMS["max_tokens"]
                )
            except Exception as e:
                status = "error"
                error_type = type(e).__name__
                print(f" Error: {e}")
            
            t_end = time.time()
            latency = t_end - t_start
            
            # Registramos los datos de cada request
            row = {
                "request_id": request_id,
                "t_start": t_start,
                "t_end": t_end,
                "latency_seconds": latency,
                "status": status,
                "error_type": error_type if status == "error" else ""
            }
            results.append(row)
            
            if status == "ok":
                count_ok += 1
                latencies.append(latency)
                print(f" OK ({latency:.3f}s)")
            else:
                count_error += 1
            
            # Guardado incremental
            df = pd.DataFrame(results)
            df.to_csv(OUTPUT_FILE, index=False)
            
            # Delay fijo entre requests
            if i < N_REQUESTS:
                time.sleep(SLEEP_SECONDS)
                    
    except KeyboardInterrupt:
        print("\nExperimento interrumpido por usuario.")
    
    print("\n=== Resumen ===")
    print(f"Total Requests: {len(results)}")
    print(f"OK: {count_ok}")
    print(f"Error: {count_error}")
    
    if latencies:
        mean_latency = statistics.mean(latencies)
        print(f"Latencia Media: {mean_latency:.4f}s")
    
    print(f"Resultados guardados en: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_experiment()
