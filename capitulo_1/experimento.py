"""
Experimento del Capítulo 1: Colisiones en Modelos Generativos

Este script ejecuta múltiples consultas al modelo de lenguaje para observar
colisiones (respuestas idénticas) y compararlas con el Problema del Cumpleaños.
"""

import os
import sys
import time
import pandas as pd
from tqdm import tqdm
import groq

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client.groq_client import GroqClient

# --- CONFIGURACIÓN ---
PROMPT = """Elegí un número entero del 1 al 30 inclusive.
Respondé únicamente con el número, sin texto adicional."""

SYSTEM_MESSAGE = "Sos un asistente útil que responde de manera concisa."

N_VALUES = [5, 10, 20, 30]  # Cantidad de respuestas a generar por ensayo
TRIALS_PER_N = 6            # Cantidad de ensayos por cada valor de N
OUTPUT_FILE = "resultados.csv"

def run_experiment():
    print("Iniciando experimento del Capítulo 1 (Colisiones)...")
    
    try:
        client = GroqClient()
    except ValueError as e:
        print(f"Error al inicializar el cliente: {e}")
        print("Asegurate de tener la variable de entorno GROQ_API_KEY configurada.")
        return

    results = []
    completed_trials = set()

    # Reanudación: si existe un archivo previo, continuar desde donde quedó
    if os.path.exists(OUTPUT_FILE):
        try:
            print(f"Archivo {OUTPUT_FILE} encontrado. Intentando resumir...")
            df = pd.read_csv(OUTPUT_FILE)
            results = df.to_dict('records')
            for _, row in df.iterrows():
                completed_trials.add((row['N'], row['trial']))
            print(f"Se encontraron {len(completed_trials)} pruebas completadas.")
        except pd.errors.EmptyDataError:
            print("El archivo está vacío. Iniciando desde cero.")
        except Exception as e:
            print(f"Error leyendo archivo existente: {e}. Iniciando desde cero.")

    # Iteramos sobre cada valor de N (cantidad de respuestas por ensayo)
    for n in tqdm(N_VALUES, desc="Progreso General (N)"):
        # Ejecutamos T ensayos para cada N
        for t in range(TRIALS_PER_N):
            current_trial = t + 1
            if (n, current_trial) in completed_trials:
                continue

            responses = []
            
            # Generamos N respuestas del modelo
            for _ in range(n):
                try:
                    response = client.chat(
                        messages=[
                            {"role": "system", "content": SYSTEM_MESSAGE},
                            {"role": "user", "content": PROMPT}
                        ],
                        temperature=0.8,
                        top_p=1.0,
                        max_tokens=10
                    )
                    content = response.strip()
                    if content.isdigit():
                        responses.append(content)
                    else:
                        print(f"Respuesta inválida recibida: '{content}'")
                        responses.append("INVALID")
                except groq.RateLimitError:
                    print(f"\n[CRÍTICO] Rate Limit alcanzado durante N={n}, trial={current_trial}.")
                    print("Guardando progreso y deteniendo ejecución.")
                    print("Podés volver a ejecutar el script más tarde para continuar.")
                    sys.exit(0)
                except Exception as e:
                    print(f"Error en llamada API: {e}")
                    responses.append("ERROR")
                
                time.sleep(0.1)

            # Analizamos el ensayo: verificamos si hubo colisión
            unique_responses = set(responses)
            num_unique = len(unique_responses)
            has_collision = num_unique < n  # Colisión = menos únicos que respuestas
            
            results.append({
                "N": n,
                "trial": current_trial,
                "unique_count": num_unique,
                "collision": has_collision,
                "responses": str(responses)
            })
            
            # Guardado incremental para no perder datos
            df = pd.DataFrame(results)
            df.to_csv(OUTPUT_FILE, index=False)

    print(f"Experimento finalizado. Resultados guardados en {OUTPUT_FILE}")

if __name__ == "__main__":
    run_experiment()
