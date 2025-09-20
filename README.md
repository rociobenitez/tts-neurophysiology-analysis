# Estudio de investigación - Síndrome del túnel del tarso (Clínica Vitruvio)

Este proyecto tiene como objetivo realizar un análisis estadístico de los estudios de neurofisiología de pacientes con Síndrome del túnel del tarso de la Clínica Vitruvio en Madrid para estudios de investigación y publicaciones científicas.

## Alcance y objetivos

- **Diseño del estudio**: Observacional retrospectivo
- **Unidad de análisis**: pie (lado)
- **Mediciones**: pre y post cirugía del túnel del tarso
- **Periodo de estudio**: 2022-2025
- **Muestra actual**: 50 estudios (irá aumentando); un paciente puede tener >1 estudio
- **Privacidad**: Datos anonimizados, sin información personal identificable

### Hipótesis principales

1. **H1 — Mejora pre→post** en parámetros neurofisiológicos (pares apareados por pie).
2. **H2 — Falsos negativos:** pies con **velocidad total normal** (≥ 45) y **velocidad segmentaria patológica** (< 45).
3. **H3 — Asociación** entre diagnóstico TTS (por lado) y parámetros neurofisiológicos.

> **Nota de unidades y formatos**
>
> - Fechas: `DD/MM/YYYY` (ej.: `08/03/2023`).
> - Decimales con coma (ej.: `41,5`).
> - Diagnósticos/comorbilidades: `0 = negativo`, `1 = positivo`, `NA` posible.

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
- **H1:** pruebas pareadas (t pareada o Wilcoxon) + tamaños de efecto.
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

## Dudas

- ¿amplitud vs velocidad?
- ¿misma importancia sensitivo y motor?
- refinir valores fisiológicos amplitud/velocidad (en config.py)
