"""
Experimento del Capítulo 2: Estimación de Eventos Raros

Este script estima la probabilidad de un fallo de factualidad (error histórico)
en el modelo de lenguaje, utilizando un prompt con conflicto interno.
"""

import sys
import os
import time
import math
import pandas as pd
from tqdm import tqdm

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client.groq_client import GroqClient

# --- CONFIGURACIÓN ---
SYSTEM_MESSAGE = "Sos un asistente útil."

PROMPT = """Respondé con una única frase afirmativa.

¿En qué año Jacob Bernoulli publicó el libro "Ars Conjectandi"?
(Solo respondé con el año)"""

EXPECTED_RESPONSE = "1713"  # Respuesta correcta esperada
N_VALUES = [200]            # Cantidad de ejecuciones
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "resultados.csv")

def calculate_normal_approx_interval(n, p_hat, confidence=0.95):
    """
    Calcula el Intervalo de Confianza por Aproximación Normal para una proporción.
    
    Fórmula: p̂ ± z * √(p̂(1-p̂)/n)
    
    Donde z ≈ 1.96 para 95% de confianza.
    """
    if n == 0:
        return 0.0, 0.0

    z = 1.96
    se = math.sqrt((p_hat * (1 - p_hat)) / n)  # Error estándar
    margin = z * se
    
    lower = max(0.0, p_hat - margin)
    upper = min(1.0, p_hat + margin)
    
    return lower, upper

def run_experiment():
    print(f"=== Capítulo 2 - Estimación de Eventos Raros ===")
    print(f"Evento E: Respuesta != '{EXPECTED_RESPONSE}'")
    
    try:
        client = GroqClient()
    except ValueError as e:
        print(f"Error al inicializar cliente: {e}")
        return

    results = []
    total_runs = N_VALUES[0]
    print(f"Iniciando {total_runs} ejecuciones...")

    success_count = 0
    event_count = 0  # Cuenta de errores (respuestas incorrectas)

    for i in tqdm(range(total_runs), desc="Progreso"):
        run_id = i + 1
        
        try:
            response = client.chat(
                messages=[
                    {"role": "system", "content": SYSTEM_MESSAGE},
                    {"role": "user", "content": PROMPT}
                ],
                temperature=0.8,
                top_p=1.0,
                max_tokens=20
            )
            
            content = response.strip()
            
            # Verificamos si la respuesta es correcta
            if content == EXPECTED_RESPONSE or content == f"{EXPECTED_RESPONSE}.":
                is_event = 0
                success_count += 1
            else:
                is_event = 1
                event_count += 1
                
            results.append({
                "run_id": run_id,
                "response_text": content,
                "event": is_event
            })
            
            time.sleep(0.2)

        except Exception as e:
            print(f"Error en ejecución {run_id}: {e}")
            results.append({
                "run_id": run_id,
                "response_text": "ERROR",
                "event": 0
            })

    # Guardamos los resultados
    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nResultados guardados en {OUTPUT_FILE}")
    
    # Calculamos estadísticas finales
    n = len(df)
    events = df['event'].sum()
    p_hat = events / n if n > 0 else 0
    
    lower, upper = calculate_normal_approx_interval(n, p_hat)
    
    print("\n=== Resultados Finales ===")
    print(f"Total ejecuciones (n): {n}")
    print(f"Eventos observados (E): {events}")
    print(f"Proporción estimada (p̂): {p_hat:.4f}")
    print(f"Intervalo de confianza (95%): [{lower:.4f}, {upper:.4f}]")

if __name__ == "__main__":
    run_experiment()
