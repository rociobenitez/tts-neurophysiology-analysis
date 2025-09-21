# Estudio de investigación - Síndrome del túnel del tarso (Clínica Vitruvio)

Este proyecto tiene como objetivo realizar un análisis estadístico de los estudios de neurofisiología de pacientes con Síndrome del túnel del tarso de la Clínica Vitruvio en Madrid para estudios de investigación y publicaciones científicas.

## Alcance y objetivos

- **Diseño del estudio**: Observacional retrospectivo
- **Unidad de análisis**: pie (lado)
- **Mediciones**: pre y post cirugía del túnel del tarso
- **Periodo de estudio**: 2022-2025
- **Muestra actual**: 74 estudios (pies); 49 pacientes
- **Privacidad**: Datos anonimizados, sin información personal identificable

Nota: revisar los pacientes con tts 0: si el paciente tiene 0 pero no tiene datos neurofisiológicos es porque no se ha estudiado ese pie en consulta, pero si tiene 0 y datos neurofisiológicos es porque se ha estudiado y no tiene tts.

### Hipótesis principales

1. **H1 — Mejora pre→post** en parámetros neurofisiológicos (pares apareados por pie).
2. **H2 — Falsos negativos:** pies con **velocidad total normal** (≥ 45) y **velocidad segmentaria patológica** (< 45).
3. **H3 - Motora vs sensitiva:** Si es negativa (>= 45) en motora, ¿cómo es la velocidad en sensitiva? Si la velocidad sensitiva es positiva, tiene un TTS.
4. **H4 — Asociación** entre diagnóstico TTS (por lado) y parámetros neurofisiológicos.

> **Nota de unidades y formatos**
>
> - Fechas: `DD/MM/YYYY` (ej.: `08/03/2023`).
> - Decimales con coma (ej.: `41,5`).
> - Diagnósticos/comorbilidades: `0 = negativo`, `1 = positivo`, `NA` posible.
> - Δ = post − pre. Δ > 0 = mejora (más velocidad tras cirugía).

## Estructura del proyecto

```
clinical_study_vitruvio/
├─ data/
│  ├─ raw/        # CSV original (privado)
│  └─ processed/  # Datos limpios/derivados para análisis
├─ notebooks/
│  ├─ 01_qa_validacion.ipynb
│  ├─ 02_eda_descriptivo.ipynb
│  ├─ 03_tests_inferencia.ipynb
│  └─ 04_figuras_tablas_publicacion.ipynb
├─ scripts/
│  ├─ config.py           # rutas, constantes, diccionario columnas
│  ├─ load.py             # lectura tipada + validación
│  ├─ preprocess.py       # limpieza, imputación, derivadas
│  ├─ stats.py            # tests y efectos
│  ├─ viz.py              # gráficas estándar
│  └─ report.py           # genera tablas/figuras a results/
├─ results/
├─ requirements.txt  # dependencias
├─ .gitignore        # ignorar data/raw y outputs pesados
└─ README.md
```

## Variables principales

- Diagnóstico por lado: `tts_pie_derecho`, `tts_pie_izquierdo` (0/1).
- Comorbilidades por lado: `radiculopatia_s1_dch`, `radiculopatia_s1_izq`, `polineuropatia`, `arcada_del_soleo` (0/1/NA).
- Fechas: `pre_fecha`, `post_fecha`.
- Parámetros neurofisiológicos (prefijos `pre_`/`post_`, lado `dch`/`izq`, tipo `motor`/`sensitivo`):
  - Ej.: `pre_dch_motor_velocidad_total`, `post_izq_sensitivo_amplitud_n_plantar_medial`, etc.

## Plan de análisis

- **QA/Validación:** tipos, fechas (day-first), coma decimal→punto, duplicados, NA, rangos fisiológicos.
- **Descriptivo:** distribución de parámetros por lado y tiempo (pre/post).
- **H1:** demostrar estadísticamente si, en promedio, hay mejoría tras la cirugía en cada métrica (velocidad total y segmentaria, pie dcho/izq).
  - Pruebas pareadas (t pareada o Wilcoxon)
  - Cuantificar tamaño del efecto (Cohen’s d o r de Wilcoxon)
- **H2:** flag de “posible falso negativo” por pie; conteos y %.
- **H3:** asociación TTS (0/1) con parámetros (comparaciones y/o regresión logística simple si procede).
- **Múltiples comparaciones:** corrección BH-FDR.
- **Salidas:** tablas CSV y figuras PNG en `results/`.

## Requisitos

- Python 3.12+
- Jupyter Notebook
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy
- Pingouin
- Statsmodels

## Documentación de cada archivo

### analisis_descriptivo_motor_velocidad.csv

Datos estadísticos descriptivos de velocidad motora (total y segmentaria) por lado (dcho/izq) y tiempo (pre/post).

- count: número de observaciones
- mean: media
- std: desviación estándar
- min: valor mínimo
- 25%: primer cuartil (Q1)
- 50%: mediana (Q2)
- 75%: tercer cuartil (Q3)
- max: valor máximo

- En el archivo `summary_qa.md` se incluye un resumen con **pre/post total** y **pre/post segmentario** uniendo ambos pies (derecho e izquierdo).

### falsos_negativos_vel.csv

Conteos y porcentajes de pies con posible falso negativo (velocidad total normal ≥ 45 y velocidad segmentaria patológica < 45) por lado (dcho/izq) y tiempo (pre/post).

### motora_neg_vs_sensitiva_pos_pre.csv

- `n_eligibles_total`: número de pies TTS+ cuya velocidad motora total PRE ≥ 45 (es decir, TTS clínico/diagnóstico positivo pero motora total normal).
- `n_sens_pos`: número de pies dentro de los elegibles que son positivos sensoriales (< 45) en el nervio.
- `%_sens_pos_sobre_eligibles`: porcentaje de pies positivos sensoriales sobre los elegibles.
- `n_valid_total`: número de pies con datos válidos (no NA) en velocidad sensorial para ese nervio.
- `n_valid_dch`: número de pies con datos válidos (no NA) en velocidad sensorial para el nervio derecho.
- `n_valid_izq`: número de pies con datos válidos (no NA) en velocidad sensorial para el nervio izquierdo.

### paired_summary_prepost.csv

Estadísticos descriptivos (n, media, sd, min, Q1, mediana, Q3, max) de las variables neurofisiológicas (velocidad total y segmentaria, amplitud y latencia) por lado (dcho/izq), tipo (motor/sensitivo) y tiempo (pre/post).

### porcentajes_valores_faltantes.csv

Porcentaje de valores faltantes (NA) por columna en el dataset ordenado de mayor a menor.

### tts_positivos_umbral_pre.csv

Conteos y porcentajes de pies TTS positivos (diagnóstico clínico) con velocidad motora total PRE ≥ 45 (normal) por lado (dcho/izq).

## Dudas

- ¿amplitud vs velocidad?
- ¿misma importancia sensitivo y motor?
- refinir valores fisiológicos amplitud/velocidad (en config.py)
