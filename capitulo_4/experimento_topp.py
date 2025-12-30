"""
Experimento del Capítulo 4 - Parte 2: Variación de Top-P

Objetivo:
Analizar cómo el parámetro Top-P afecta la distribución de respuestas de un modelo generativo
manteniendo la temperatura fija.
"""

import sys
import os
import time
import pandas as pd
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import GroqClient

# --- CONFIGURACIÓN ---
MODEL = "llama-3.1-8b-instant"
PROMPT = "Elegí una de las siguientes opciones y respondé únicamente con la opción elegida: A, B, C o D."
N_REQUESTS_PER_CONFIG = 500
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "resultados_topp.csv")

FIXED_TEMP = 0.7  # Temperatura fija

# Configuraciones a probar: variamos Top-P
CONFIGS = [
    {"name": "Top-P 1.0 (Base)", "temperature": FIXED_TEMP, "top_p": 1.0},
    {"name": "Top-P 0.9", "temperature": FIXED_TEMP, "top_p": 0.9},
    {"name": "Top-P 0.6", "temperature": FIXED_TEMP, "top_p": 0.6},
]

def run_experiment():
    print("=== Capítulo 4 - Experimento 2: Top-P ===")
    print(f"Modelo: {MODEL}")
    print(f"Temp Fija: {FIXED_TEMP}")
    print(f"Configs: {len(CONFIGS)}")
    print(f"Requests por config: {N_REQUESTS_PER_CONFIG}")
    
    try:
        client = GroqClient()
    except ValueError as e:
        print(f"Error inicializando cliente: {e}")
        return

    results = []
    total_start = time.time()

    for config in CONFIGS:
        print(f"\nEjecutando configuración: {config['name']} (Top-P={config['top_p']})")
        
        for i in range(1, N_REQUESTS_PER_CONFIG + 1):
            print(f"  Req {i}/{N_REQUESTS_PER_CONFIG}...", end="", flush=True)
            
            try:
                response = client.chat(
                    messages=[{"role": "user", "content": PROMPT}],
                    temperature=config["temperature"],
                    top_p=config["top_p"],
                    max_tokens=10
                )
                print(f" OK [{response.strip()}]")
                
                results.append({
                    "config_name": config["name"],
                    "temperature": config["temperature"],
                    "top_p": config["top_p"],
                    "response": response,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                print(f" ERROR: {e}")
                results.append({
                    "config_name": config["name"],
                    "temperature": config["temperature"],
                    "top_p": config["top_p"],
                    "response": "ERROR",
                    "timestamp": datetime.now().isoformat()
                })
            
            time.sleep(0.05)
        print("")

    total_duration = time.time() - total_start
    print(f"\nExperimento finalizado en {total_duration:.2f}s")
    
    # Guardamos los resultados
    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Resultados guardados en: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_experiment()
