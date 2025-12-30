# tp-probabilidad-y-estadistica

Repositorio destinado al Trabajo de Probabilidad y Estadística desarrollado por Alejo Tomás Mariño en Diciembre 2025

## Estructura del Proyecto

Este proyecto está organizado para realizar experimentos con modelos LLM (específicamente llama-3.1-8b) relacionados con probabilidad y estadística.

```
tp-probabilidad-y-estadistica/
├── api_client/          # Cliente de API para Groq (llama-3.1-8b)
│   ├── __init__.py
│   ├── groq_client.py
│   └── README.md
├── capitulo_1/          # Probabilidad clásica y colisiones
│   ├── experimento.py
│   ├── analisis.py
│   └── README.md
├── capitulo_2/          # Estimación de eventos raros
│   ├── experimento.py
│   ├── analisis.py
│   └── README.md
├── capitulo_3/          # Procesos de Poisson/Exponencial
│   ├── experimento.py
│   ├── analisis.py
│   └── README.md
├── capitulo_4/          # Distribuciones inducidas
│   ├── experimento.py
│   ├── experimento_topp.py
│   ├── analisis.py
│   └── README.md
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

## Configuración

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar API Key de Groq

Obtén tu API key de [Groq Console](https://console.groq.com) y configúrala como variable de entorno:

```bash
export GROQ_API_KEY="tu-api-key-aqui"
```

O crea un archivo `.env` en la raíz del proyecto:

```
GROQ_API_KEY=tu-api-key-aqui
```

## Uso

### Cliente de API

El módulo `api_client` proporciona un cliente simple para interactuar con el modelo llama-3.1-8b:

```python
from api_client import GroqClient

client = GroqClient()
response = client.simple_prompt("¿Qué es probabilidad?")
print(response)
```

Ver [api_client/README.md](api_client/README.md) para más detalles.

### Experimentos por Capítulo

Cada capítulo tiene su propio directorio con scripts que se pueden ejecutar independientemente:

```bash
# Capítulo 1 - Colisiones (Problema del Cumpleaños)
python capitulo_1/experimento.py
python capitulo_1/analisis.py

# Capítulo 2 - Eventos Raros
python capitulo_2/experimento.py
python capitulo_2/analisis.py

# Capítulo 3 - Poisson/Exponencial
python capitulo_3/experimento.py
python capitulo_3/analisis.py

# Capítulo 4 - Distribuciones Inducidas
python capitulo_4/experimento.py
python capitulo_4/analisis.py
```

## Modelo LLM

Este proyecto utiliza el modelo **llama-3.1-8b-instant** a través de la API de Groq.
