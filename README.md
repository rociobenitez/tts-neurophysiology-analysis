# Estudio de investigación - Síndrome del túnel del tarso (Clínica Vitruvio)

Este proyecto realiza un análisis estadístico de estudios de **neurofisiología** en pacientes con **Síndrome del Túnel del Tarso** para investigación y publicaciones científicas.

## Alcance y objetivos

- **Diseño del estudio**: Observacional retrospectivo
- **Unidad de análisis**: pie (lado)
- **Mediciones**: pre y post cirugía del túnel del tarso
- **Periodo de estudio**: 2022-2025
- **Muestra actual**: 74 estudios (pies); 49 pacientes
- **Privacidad**: Datos anonimizados, sin información personal identificable

> Nota: revisar los pacientes con `tts=0`. Si `tts=0` y no hay datos neurofisiológicos → ese pie no se estudió en consulta. Si `tts=0` **y** hay datos → se estudió y no tiene TTS.

### Hipótesis principales

1. **H1 — Mejora pre→post** en parámetros neurofisiológicos (pares apareados por pie).
2. **H2 — Falsos negativos:** pies con **velocidad total normal** (≥ 45) y **velocidad segmentaria patológica** (< 45).
3. **H3 — Motora vs sensitiva:** si la **motora total** es normal (≥ 45), ¿hay positividad sensitiva (< 45) por nervio?
4. **H4 — Asociación** entre diagnóstico TTS (por lado) y parámetros neurofisiológicos.

> **Nota de unidades y formatos**
>
> - Fechas: `DD/MM/YYYY` (ej.: `08/03/2023`).
> - Decimales con coma (ej.: `41,5`).
> - Diagnósticos/comorbilidades: `0 = negativo`, `1 = positivo`, `NA` posible.
> - Δ = post − pre. Δ > 0 = mejora (más velocidad tras cirugía).
> - Umbral de normalidad velocidad: **45 m/s**

## Estructura del proyecto

```
tts-neurophysiology-analysis/
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

## Requisitos

- Python 3.12+
- Jupyter Notebook
- Pandas, NumPy, Matplotlib, Seaborn
- SciPy, Pingouin
- (Opcional) Statsmodels

## Cómo reproducir

**Sin datos** no se ejecutarán los notebooks. Coloca el CSV en `data/raw/` con el nombre esperado por `notebooks/01_qa_validacion.ipynb` (variable `CSV_NAME`). Los datos **no** se versionan.

### 1) Crear entorno y dependencias (pip-tools)

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip pip-tools
pip-compile --generate-hashes -o requirements.txt requirements.in
pip-sync requirements.txt
```

### 2) Kernel de Jupyter (opcional si usas Jupyter clásico)

```bash
python -m ipykernel install --user --name=tts-neurophysiology-analysis
```

### 3) Ejecutar notebooks en orden

1. Abre los notebooks en orden:

- `01_qa_validacion.ipynb` → genera `data/processed/estudios_validado.parquet` y `results/summary_qa.md`.
- `02_eda_descriptivo.ipynb` _(pendiente)_
- `03_tests_inferencia.ipynb` _(pendiente)_
- `04_figuras_tablas_publicacion.ipynb` _(pendiente)_

2. Los resultados se guardan en `results/tables/*.csv` y `results/figures/*.png`.

> Si cambias el nombre del fichero en `data/raw/`, actualiza CSV_NAME en `01_qa_validacion.ipynb`.

## Variables principales

- Diagnóstico por lado: `tts_pie_derecho`, `tts_pie_izquierdo` (0/1).
- Comorbilidades por lado: `radiculopatia_s1_dch`, `radiculopatia_s1_izq`, `polineuropatia`, `arcada_del_soleo` (0/1/NA).
- Fechas: `pre_fecha`, `post_fecha`.
- Parámetros neurofisiológicos (prefijos `pre_`/`post_`, lado `dch`/`izq`, tipo `motor`/`sensitivo`):
  - Ej.: `pre_dch_motor_velocidad_total`, `post_izq_sensitivo_amplitud_n_plantar_medial`, etc.

## Plan de análisis

- **QA/Validación:** tipos, fechas (day-first), coma decimal→punto, duplicados, NA, rangos fisiológicos.
- **Descriptivo:** distribución de parámetros por lado y tiempo (pre/post).
- **H1:** mejora pre→post (t pareada o Wilcoxon) + tamaño del efecto (Cohen’s dz); corrección BH-FDR.
- **H2:** flag de “posible falso negativo” por pie; conteos y %.
- **H3:** entre pies con motora total normal (≥ 45), conteos y % de positivos sensoriales (< 45) por nervio.
- **H4:** asociación entre diagnóstico TTS (0/1) y parámetros neurofisiológicos:
- **Múltiples comparaciones:** corrección BH-FDR.
- **Salidas:** tablas CSV y figuras PNG en `results/`.

## Resultados (archivos)

### sumary_qa.md

En `results/summary_qa.md`. Resumen de QA/validación.

### analisis_descriptivo_motor_velocidad.csv

Datos estadísticos descriptivos de velocidad motora (total y segmentaria) por lado (dcho/izq) y tiempo (pre/post). En `results/tables/analisis_descriptivo_motor_velocidad.csv`.

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

Conteos y porcentajes de pies con posible falso negativo (velocidad total normal ≥ 45 y velocidad segmentaria patológica < 45) por lado (dcho/izq) y tiempo (pre/post). En `results/tables/falsos_negativos_vel.csv`.

### motora_neg_vs_sensitiva_pos_pre.csv

Conteos y porcentajes de pies con velocidad motora total PRE ≥ 45 (normal) y velocidad sensorial patológica (< 45) por nervio (n. tibial posterior, n. plantar medial, n. plantar lateral). En `results/tables/motora_neg_vs_sensitiva_pos_pre.csv`.

- `n_eligibles_total`: número de pies TTS+ cuya velocidad motora total PRE ≥ 45 (es decir, TTS clínico/diagnóstico positivo pero motora total normal).
- `n_sens_pos`: número de pies dentro de los elegibles que son positivos sensoriales (< 45) en el nervio.
- `%_sens_pos_sobre_eligibles`: porcentaje de pies positivos sensoriales sobre los elegibles.
- `n_valid_total`: número de pies con datos válidos (no NA) en velocidad sensorial para ese nervio.
- `n_valid_dch`: número de pies con datos válidos (no NA) en velocidad sensorial para el nervio derecho.
- `n_valid_izq`: número de pies con datos válidos (no NA) en velocidad sensorial para el nervio izquierdo.

### paired_summary_prepost.csv

Estadísticos descriptivos (n, media, sd, min, Q1, mediana, Q3, max) de las variables neurofisiológicas (velocidad total y segmentaria, amplitud y latencia) por lado (dcho/izq), tipo (motor/sensitivo) y tiempo (pre/post). En `results/tables/paired_summary_prepost.csv`.

### porcentajes_valores_faltantes.csv

Porcentaje de valores faltantes (NA) por columna en el dataset ordenado de mayor a menor. En `results/tables/porcentajes_valores_faltantes.csv`.

### tts_positivos_umbral_pre.csv

Conteos y porcentajes de pies TTS positivos (diagnóstico clínico) con velocidad motora total PRE ≥ 45 (normal) por lado (dcho/izq). En `results/tables/tts_positivos_umbral_pre.csv`.

## Ética y privacidad

- No se incluyen datos identificables.
- Los datos crudos permanecen locales en data/raw/ (ignorados por git).
- Cualquier compartición externa debe estar autorizada por el comité correspondiente.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.
