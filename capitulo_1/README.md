# Capítulo 1 — Probabilidad clásica y colisiones en modelos generativos

## Objetivo

Estudiar la aparición de **colisiones** (respuestas idénticas) en un modelo de lenguaje generativo (Llama 3.1 8B) cuando se ejecuta múltiples veces el mismo prompt. Se busca verificar si la probabilidad de colisión sigue la distribución predicha por el **problema del cumpleaños**.

## Estructura del Capítulo

- `experimento.py`: Script principal que ejecuta las pruebas contra la API de Groq.
- `analisis.py`: Script que procesa los resultados, calcula probabilidades y genera gráficos.
- `resultados.csv`: Archivo generado automáticamente con los datos crudos del experimento.
- `probabilidad_colision.png`: Gráfico generado comparando la teórica vs empírica.

## Cómo reproducir

### 1. Configuración de entorno

Asegurate de tener las dependencias instaladas y tu API Key de Groq configurada.

```bash
# En Windows
$env:GROQ_API_KEY = "tu_api_key_aqui"

# Instalar dependencias (si no las tenés)
pip install pandas matplotlib tqdm groq numpy python-dotenv
```

### 2. Ejecutar experimento

Esto realizará múltiples llamadas a la API. Puede tomar unos minutos.

```bash
python experimento.py
```

_Se generará el archivo `resultados.csv`_

### 3. Analizar resultados

Una vez finalizado el experimento:

```bash
python analisis.py
```

_Se mostrarán métricas en consola y se guardará el gráfico `probabilidad_colision.png`_

## Detalles del Experimento

- **Prompt**: "Elegí un número entero del 1 al 30 inclusive. Respondé únicamente con el número, sin texto adicional."
- **Modelo**: Llama 3.1 8B (via Groq)
- **Parámetros**: Temperature 0.8, Top-P 1.0.
- **Hipótesis**: La probabilidad de colisión seguirá la aproximación del problema del cumpleaños para $M=30$:
  $$ P(A_N) \approx 1 - \exp\left(-\frac{N(N-1)}{2 \times 30}\right) $$
