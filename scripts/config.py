from pathlib import Path

# Rutas
ROOT = Path(__file__).resolve().parents[1]
DATA_RAW_PATH = ROOT / 'data' / 'raw'
DATA_PROCESSED_PATH = ROOT / 'data' / 'processed'
RESULTS_PATH = ROOT / 'results'
RESULTS_FIGURES = RESULTS_PATH / 'figures'
RESULTS_TABLES = RESULTS_PATH / 'tables'

# Parámetros de parsing
DATE_COLS = ['pre_fecha', 'post_fecha']
DATE_DAYFIRST = True   # Formato DD/MM/YYYY
DECIMAL = ','          # Coma decimal en CSV

# Prefijos de columnas de parámetros neurofisiológicos
NUMERIC_PREFIXES = ['pre_', 'post_']

# Columna ID único por paciente (DNI)
ID_COL = 'id'

# Umbrales fisiológicos
VEL_NORMAL_UMBRAL = 45.0  # (m/s) normalidad velocidad total >= 45; segmentaria patológica < 45
AMP_NORMAL_UMBRAL = 5.0   # (mV) normalidad amplitud >= 5; patológica < 5 (pendiente de definir)
VEL_MIN = 10.0            # (m/s) velocidad mínima fisiológica
VEL_MAX = 80.0            # (m/s) velocidad máxima fisiológica

# Columnas de diagnóstico/comorbilidad (0/1/NA)
BINARY_COLS = [
    "tts_pie_derecho", "tts_pie_izquierdo",
    "radiculopatia_s1_dch", "radiculopatia_s1_izq",
    "polineuropatia", "arcada_del_soleo",
]

# Config de gráficos Matplotlib
FIG_DPI = 160
FIG_SIZE = (8, 5)

# Utilidades
SIDES = ['dch', 'izq']
TIMES = ['pre', 'post']
NERVES = ["n_plantar_medial", "n_plantar_lateral", "n_baxter", "n_calcaneo_medial"]

# Grupos de columnas - Motor total/segmentario por lado y tiempo
MOTOR_VELOCIDAD_TOTAL = {
    side: {
        "pre":  f"pre_{side}_motor_velocidad_total",
        "post": f"post_{side}_motor_velocidad_total",
    } for side in SIDES
}
MOTOR_VELOCIDAD_SEG = {
    side: {
        "pre":  f"pre_{side}_motor_velocidad_segmentario",
        "post": f"post_{side}_motor_velocidad_segmentario",
    } for side in SIDES
}
MOTOR_AMPLITUD_TOTAL = {
    side: {
        "pre":  f"pre_{side}_motor_amplitud_total",
        "post": f"post_{side}_motor_amplitud_total",
    } for side in SIDES
}
MOTOR_AMPLITUD_SEG = {
    side: {
        "pre":  f"pre_{side}_motor_amplitud_segmentario",
        "post": f"post_{side}_motor_amplitud_segmentario",
    } for side in SIDES
}

# Grupos de columnas (sensitivo) por nervio, lado y tiempo
SENSITIVO_VELOCIDAD = {
    nerve: {
        side: {
            "pre":  f"pre_{side}_sensitivo_velocidad_{nerve}",
            "post": f"post_{side}_sensitivo_velocidad_{nerve}",
        } for side in SIDES
    } for nerve in NERVES
}
SENSITIVO_AMPLITUD = {
    nerve: {
        side: {
            "pre":  f"pre_{side}_sensitivo_amplitud_{nerve}",
            "post": f"post_{side}_sensitivo_amplitud_{nerve}",
        } for side in SIDES
    } for nerve in NERVES
}