"""
Experimento del Capítulo 1
"""

import sys
import os

# Añadir el directorio raíz al path para importar api_client
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_client import GroqClient


def run_experiment():
    """
    Ejecuta el experimento del capítulo 1.
    
    Implementa aquí tu experimento específico usando el cliente de Groq.
    """
    print("=== Capítulo 1 - Experimento ===")
    
    # Ejemplo de uso del cliente
    try:
        client = GroqClient()
        
        # Aquí va tu experimento
        prompt = "Este es un experimento de ejemplo para el capítulo 1."
        response = client.simple_prompt(prompt)
        
        print(f"Prompt: {prompt}")
        print(f"Respuesta: {response}")
        
    except ValueError as e:
        print(f"Error: {e}")
        print("Asegúrate de configurar la variable de entorno GROQ_API_KEY")


if __name__ == "__main__":
    run_experiment()
