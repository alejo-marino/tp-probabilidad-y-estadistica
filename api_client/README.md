# API Client

Este módulo contiene el cliente de API para interactuar con Groq y el modelo llama-3.1-8b.

## Configuración

1. Obtén tu API key de [Groq](https://console.groq.com)
2. Configura la variable de entorno `GROQ_API_KEY` o pásala directamente al cliente

## Uso

```python
from api_client import GroqClient

# Inicializar el cliente
client = GroqClient()  # Usa GROQ_API_KEY del entorno
# o
client = GroqClient(api_key="tu-api-key-aqui")

# Prompt simple
response = client.simple_prompt("¿Qué es probabilidad?")
print(response)

# Chat con mensajes múltiples
messages = [
    {"role": "system", "content": "Eres un experto en estadística."},
    {"role": "user", "content": "Explica la distribución normal."}
]
response = client.chat(messages)
print(response)
```

## Modelo

El cliente usa el modelo `llama-3.1-8b-instant` por defecto.
