# Resumen QA — data-neuro-tts.csv

- **Shape**: 49 filas × 63 columnas
- **Pacientes únicos (id)**: 49
- **Muestra total (pies disponibles)**: 98 (derechos: 49, izquierdos: 49)
- **Pies con TTS positivo**: 74 (75.5%) (derechos: 42 (56.8%), izquierdos: 32 (43.2%))
- **Pies con TTS negativo**: 24 (24.5%) (derechos: 7 (29.2%), izquierdos: 17 (70.8%))
- **IDs duplicados**: 0 (filas afectadas: 0)

## Top-20 columnas con más valores faltantes

- post_dch_sensitivo_amplitud_n_calcaneo_medial: 100.0%
- post_dch_sensitivo_velocidad_n_calcaneo_medial: 100.0%
- post_izq_sensitivo_amplitud_n_calcaneo_medial: 97.96%
- post_dch_sensitivo_velocidad_n_baxter: 97.96%
- post_dch_sensitivo_amplitud_n_baxter: 97.96%
- post_izq_sensitivo_velocidad_n_baxter: 97.96%
- post_izq_sensitivo_amplitud_n_baxter: 97.96%
- post_izq_sensitivo_velocidad_n_calcaneo_medial: 97.96%
- pre_dch_sensitivo_velocidad_n_calcaneo_medial: 95.92%
- post_dch_sensitivo_velocidad_n_plantar_medial: 95.92%
- pre_dch_sensitivo_amplitud_n_calcaneo_medial: 95.92%
- pre_izq_sensitivo_velocidad_n_calcaneo_medial: 95.92%
- pre_izq_sensitivo_amplitud_n_calcaneo_medial: 95.92%
- post_dch_sensitivo_amplitud_n_plantar_medial: 95.92%
- pre_dch_sensitivo_amplitud_n_baxter: 91.84%
- pre_dch_sensitivo_velocidad_n_baxter: 91.84%
- post_izq_sensitivo_amplitud_n_plantar_lateral: 91.84%
- post_izq_sensitivo_velocidad_n_plantar_lateral: 91.84%
- post_dch_sensitivo_amplitud_n_plantar_lateral: 91.84%
- post_dch_sensitivo_velocidad_n_plantar_lateral: 91.84%

## Análisis descriptivo de velocidad motora (por lado)

| Variable             |   n |   media |   sd |   min |   max |
|:---------------------|----:|--------:|-----:|------:|------:|
| motor_vel_total_pre  |  70 |   49.69 | 4.11 |  42.2 |  61.2 |
| motor_vel_total_post |  23 |   50.53 | 5.63 |  35.7 |  64.5 |
| motor_vel_seg_pre    |  77 |   39.52 | 5.19 |  27.1 |  53.6 |
| motor_vel_seg_post   |  40 |   46.53 | 4.69 |  36.8 |  57.1 |

## Total pies TTS+ y motor total normal (>= 45.0) en PRE

- Total: 62 (83.78% del total de positivos)
    - Derecho: 35 (56.45%)
    - Izquierdo: 27 (43.55%)

## H2 — Posibles falsos negativos

### Pre cirugía
- derecho: n=31 (63.27%)
- izquierdo: n=26 (53.06%)

### Post cirugía
- derecho: n=5 (10.2%)
- izquierdo: n=2 (4.08%)

## Outliers en velocidad (rango usado: 10.0–80.0 m/s; ajustable)

- No se detectaron outliers.

## Consistencia de binarios

- OK (solo {0,1,NA})

## Fechas

- Días entre pre y post: n=27, mediana=328.0, IQR≈(310.5, 349.0)
- Semanas entre pre y post: n=27, mediana=46.86, IQR≈(44.36, 49.86)
- Casos con post < pre: 0