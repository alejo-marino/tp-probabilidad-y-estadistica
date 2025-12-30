# Capítulo 4 — Distribuciones inducidas en modelos generativos

## Objetivo

Analizar cómo los parámetros de muestreo de un modelo de lenguaje (Temperatura y Top-P) inducen transformaciones sistemáticas en la distribución de probabilidad de su salida, manteniendo fijo el espacio muestral.

## Definición del Experimento

- **Prompt Fijo**: "Elegí una de las siguientes opciones y respondé únicamente con la opción elegida: A, B, C o D."
- **Variable Aleatoria**: Elección categórica $X \in \{A, B, C, D\}$.
- **Parámetros**:
  - **Experimento 1**: Variación de Temperatura ($T = 0.2, 0.7, 1.2$).
  - **Experimento 2**: Variación de Top-P ($P = 1.0, 0.9, 0.6$) con Temperatura fija ($T=0.7$).

## Estructura

- `experimento.py`: Ejecuta el Experimento 1 (Temperatura) y guarda en `resultados.csv`.
- `experimento_topp.py`: Ejecuta el Experimento 2 (Top-P) y guarda en `resultados_topp.csv`.
- `analisis.py`: Script unificado para procesar los datos, categorizar respuestas y generar gráficos de barras.
- `resultados.csv` / `resultados_topp.csv`: Datos crudos del modelo.
- `resultados_distribucion.png`: Gráfico comparativo de distribuciones (Experimento 1).
- `resultados_topp_distribucion.png`: Gráfico comparativo de distribuciones (Experimento 2).

## Cómo reproducir

### 1. Ejecutar experimentos

Para la variación de Temperatura:

```bash
python capitulo_4/experimento.py
```

Para la variación de Top-P:

```bash
python capitulo_4/experimento_topp.py
```

### 2. Generar análisis y gráficos

Para analizar temperatura:

```bash
python capitulo_4/analisis.py
```

Para analizar top-p:

```bash
python capitulo_4/analisis.py capitulo_4/resultados_topp.csv
```

## Métricas de Dispersión

Se utiliza la **Entropía de Shannon** ($H$) como medida de dispersión de la distribución inducida:
$$ H(X) = - \sum\_{x \in \mathcal{X}} p(x) \log_2 p(x) $$

Se espera que:

- A mayor Temperatura, mayor Entropía (distribución más uniforme).
- A menor Top-P, menor Entropía (distribución más concentrada en la masa principal).

## Resultados Esperados

El experimento debe mostrar visualmente cómo la "creatividad" o "aleatoriedad" del modelo se traduce físicamente en un desplazamiento de la masa de probabilidad entre las categorías disponibles.
