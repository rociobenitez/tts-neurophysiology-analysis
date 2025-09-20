# Resumen QA — data-neuro-tts.csv

- **Shape**: 49 filas × 63 columnas
- **Pacientes únicos (id)**: 49
- **IDs duplicados**: 0 (filas afectadas: 0)

## Top-20 columnas con más missing
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

## H2 — Posibles falsos negativos

### Pre cirugía
- derecho: n=31 (63.27%)
- izquierdo: n=26 (53.06%)

## Post cirugía
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