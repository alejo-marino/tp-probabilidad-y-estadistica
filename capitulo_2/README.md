# Capítulo 2 – Estimación de eventos raros en modelos generativos

## Objetivo

Estimar la probabilidad de ocurrencia de un **fallo de factualidad inducido** (alucinación específica) en un modelo de lenguaje, bajo condiciones de prompt adversas o confusas.

## Definición del Evento (Confusión Histórica)

Utilizamos una pregunta sobre un dato histórico específico que suele causar confusión en los modelos debido a la similitud entre miembros de la familia Bernoulli.

- **Prompt**:

  > "Respondé con una única frase afirmativa.
  >
  > ¿En qué año Jacob Bernoulli publicó el libro "Ars Conjectandi"?
  > (Solo respondé con el año)"

- **Dato Real**: _Ars Conjectandi_ fue publicado póstumamente en **1713**.
- **Posible Confusión**: Daniel Bernoulli publicó _Hydrodynamica_ en **1738**. Los modelos a menudo confunden estas fechas.

- **Respuesta Esperada**: `"1713"` (se acepta `"1713."` con punto final).
- **Evento $E$ (Fallo)**: Cualquier respuesta que **no** sea `"1713"` o `"1713."`.
  - El error más común observado es `"1738"`.

## Estructura

- `experimento.py`: Ejecuta las $N$ tiradas del experimento.
- `analisis.py`: Genera gráficos de convergencia y distribución de respuestas.
- `resultados.csv`: Datos crudos.

## Cómo reproducir

### 1. Ejecutar experimento

```bash
python capitulo_2/experimento.py
```

Esto generará `resultados.csv`.

### 2. Generar gráficos

```bash
python capitulo_2/analisis.py
```

Esto generará `convergencia_probabilidad.png` y `distribucion_respuestas.png`.

## Resultados Esperados

El script `analisis.py` mostrará cómo la estimación de la probabilidad de error converge a medida que aumenta $N$. También verás un gráfico de barras destacando la frecuencia de la alucinación "1738" frente a la respuesta correcta "1713".
