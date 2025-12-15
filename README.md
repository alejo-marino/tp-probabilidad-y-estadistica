# tp-probabilidad-y-estadistica
Repositorio destinado al Trabajo de Probabilidad y Estadistica desarrollado por Alejo Tomás Mariño en Diciembre 2025

## Estructura del Proyecto

Este proyecto está organizado para realizar experimentos con modelos LLM (específicamente llama-3.1-8b) relacionados con probabilidad y estadística.

```
tp-probabilidad-y-estadistica/
├── api_client/          # Cliente de API para Groq (llama-3.1-8b)
│   ├── __init__.py
│   ├── groq_client.py
│   └── README.md
├── capitulo_1/          # Experimentos del capítulo 1
│   ├── __init__.py
│   ├── experimento.py
│   └── README.md
├── capitulo_2/          # Experimentos del capítulo 2
│   ├── __init__.py
│   ├── experimento.py
│   └── README.md
├── capitulo_3/          # Experimentos del capítulo 3
│   ├── __init__.py
│   ├── experimento.py
│   └── README.md
├── capitulo_4/          # Experimentos del capítulo 4
│   ├── __init__.py
│   ├── experimento.py
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

Cada capítulo tiene su propio directorio con un archivo `experimento.py` que se puede ejecutar independientemente:

```bash
# Capítulo 1
cd capitulo_1
python experimento.py

# Capítulo 2
cd capitulo_2
python experimento.py

# Y así sucesivamente...
```

## Modelo LLM

Este proyecto utiliza el modelo **llama-3.1-8b-instant** a través de la API de Groq.

## Notas

- Este es un proyecto académico para un curso de Probabilidad y Estadística
- La calidad del código no es el foco principal, sino los experimentos y resultados
- Cada capítulo es independiente y puede tener diferentes tipos de experimentos
