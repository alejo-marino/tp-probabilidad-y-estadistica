# Capítulo 3 — Procesos de llegada (Poisson/Exponencial) sobre tiempos de respuesta

## Objetivo

Analizar si los tiempos de respuesta de un modelo de lenguaje generativo (Llama 3.1 8B) siguen una distribución **Exponencial** y si el proceso de llegadas (completación de requests) se aproxima a un **proceso de Poisson**.

## Definición del Experimento

- **Evento**: Finalización de una request (recepción de la respuesta completa).
- **Variable de interés**: Tiempo de respuesta (latencia) $S_i$.
- **Análisis Poisson**: Conteo de eventos en ventanas de tiempo fijo $\Delta t$.

> **Nota importante**: Por limitaciones de rate limit, se introduce un delay fijo (5s) entre requests. Este delay **no forma parte del fenómeno** y se elimina mediante una **Timeline Virtual** en el análisis.

## Estructura

- `experimento.py`: Ejecuta las $N$ requests y registra latencias en `resultados.csv`.
- `analisis.py`: Procesa los datos, construye la Timeline Virtual y genera gráficos.
- `resultados.csv`: Datos crudos (latencias, timestamps).
- `resultados_latency.png`: Histograma de latencias vs curva Exponencial teórica.
- `resultados_counts.png`: Histograma de conteos por ventana vs PMF Poisson.
- `resultados_buckets.csv`: Conteos por bucket en la timeline virtual.
- `resultados_virtual_timeline.csv`: Timeline virtual calculada.

## Cómo reproducir

### 1. Ejecutar experimento

```bash
python capitulo_3/experimento.py
```

Esto generará `resultados.csv`.

### 2. Generar gráficos y análisis

```bash
python capitulo_3/analisis.py
```

El script mostrará métricas en consola y generará los gráficos.

## Metodología: Timeline Virtual

Para evaluar correctamente el proceso de Poisson, se construye una **línea de tiempo virtual** que simula un sistema en saturación (sin tiempos muertos):

1. Se ordenan las latencias $S_i$ de las requests exitosas.
2. Se calcula el tiempo de completación virtual:
   $$ t*{virtual}^{(i)} = \sum*{k=1}^{i} S_k $$
3. Se trunca al último bucket completo para evitar sesgo.
4. Se cuentan eventos en ventanas de 1.0s sobre esta timeline.

## Estimadores de $\lambda$

- **Estimador 1 (tiempos)**: $\hat{\lambda}_1 = 1 / \overline{S}$
- **Estimador 2 (conteos)**: $\hat{\lambda}_2 = N_{eventos} / T_{usable}$

Ambos estimadores se comparan para verificar consistencia.

## Resultados Esperados

El ajuste Poisson/Exponencial puede **no ser bueno**. Esto es aceptable y esperado dado que los tiempos de respuesta de una API tienen baja varianza y no son memoryless. Las conclusiones deben reflejar las desviaciones respecto al modelo teórico ideal.
