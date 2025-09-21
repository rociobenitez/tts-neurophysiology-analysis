import pandas as pd
import numpy as np
from scipy import stats
import pingouin as pg

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from config import TIMES, SIDES, NERVES, MOTOR_VELOCIDAD_TOTAL, MOTOR_VELOCIDAD_SEG, MOTOR_AMPLITUD_TOTAL, MOTOR_AMPLITUD_SEG, SENSITIVO_VELOCIDAD, SENSITIVO_AMPLITUD

# Helpers para recuperar listas rápidas
def cols_motor_velocidad_total(side=None, time=None):
    if side and time: return [MOTOR_VELOCIDAD_TOTAL[side][time]]
    if side:          return [MOTOR_VELOCIDAD_TOTAL[side][t] for t in TIMES]
    if time:          return [MOTOR_VELOCIDAD_TOTAL[s][time] for s in SIDES]
    return [MOTOR_VELOCIDAD_TOTAL[s][t] for s in SIDES for t in TIMES]

def cols_motor_velocidad_segmentario(side=None, time=None):
    if side and time: return [MOTOR_VELOCIDAD_SEG[side][time]]
    if side:          return [MOTOR_VELOCIDAD_SEG[side][t] for t in TIMES]
    if time:          return [MOTOR_VELOCIDAD_SEG[s][time] for s in SIDES]
    return [MOTOR_VELOCIDAD_SEG[s][t] for s in SIDES for t in TIMES]

def cols_sensitivo(tipo="velocidad", nerve=None, side=None, time=None):
    base = SENSITIVO_VELOCIDAD if tipo=="velocidad" else SENSITIVO_AMPLITUD
    nerves = [nerve] if nerve else NERVES
    sides = [side] if side else SIDES
    times = [time] if time else TIMES
    out = []
    for n in nerves:
        for s in sides:
            for t in times:
                out.append(base[n][s][t])
    return out

# Para validaciones/EDA
def all_measure_cols():
    cols = []
    cols += cols_motor_velocidad_total()
    cols += cols_motor_velocidad_segmentario()
    for tipo in ("velocidad", "amplitud"):
        cols += cols_sensitivo(tipo=tipo)
    # Añade motor amplitud si quieres tratarlas igual:
    cols += [MOTOR_AMPLITUD_TOTAL[s][t] for s in SIDES for t in TIMES]
    cols += [MOTOR_AMPLITUD_SEG[s][t] for s in SIDES for t in TIMES]
    return cols

# Formateo de estadísticas descriptivas
def _fmt(x, nd=2):
    """
    Formatea número x con nd decimales, o "NA" si es NaN.
    """
    return ("{0:." + str(nd) + "f}").format(x) if pd.notna(x) else "NA"

def motor_stat_row_joint(df, cols, label):
    """
    Une columnas de ambos pies (cols) y devuelve una fila con:
    Variable, n, media, sd, min, max
    """
    s = pd.concat([df[c] for c in cols], ignore_index=True).dropna()
    n = int(s.size)
    mean = s.mean() if n else np.nan
    sd   = s.std(ddof=1) if n >= 2 else np.nan
    vmin = s.min() if n else np.nan
    vmax = s.max() if n else np.nan
    return {
        "Variable": label,
        "n": n,
        "media": _fmt(mean),
        "sd": _fmt(sd),
        "min": _fmt(vmin),
        "max": _fmt(vmax),
    }

# Estadísticos descriptivos de delta (post - pre)
def summarize_delta(delta: pd.Series) -> pd.Series:
    '''
    Resume una serie de deltas (post - pre).
    - n pares válidos
    - media, sd, mediana, q1, q3
    - IC95% de la media (t de Student)
    - % de casos con mejoría (delta > 0)
    '''
    delta = delta.dropna()
    n = int(delta.size)
    mean = float(delta.mean()) if n else np.nan
    sd = float(delta.std(ddof=1)) if n > 1 else np.nan
    median = float(delta.median()) if n else np.nan
    q1, q3 = delta.quantile([0.25, 0.75])

    # IC95% de la media (t de Student; si hay n>=3 y sd finita)
    if n >= 3 and np.isfinite(sd):  # evitar NaN
        se = sd / np.sqrt(n)
        tcrit = stats.t.ppf(0.975, df=n-1)  # 97.5% para IC bilateral 95%
        ci_low, ci_high = mean - tcrit*se, mean + tcrit*se
    else:
        ci_low = ci_high = np.nan
    pct_improved = (delta > 0).mean() * 100
    return pd.Series({
        "n": n,
        "mean": mean,
        "sd": sd,
        "median": median,
        "q1": q1,
        "q3": q3,
        "ci95_low": ci_low,
        "ci95_high": ci_high,
        "pct_improved": pct_improved
    })


def analyze_paired(pre: pd.Series, post: pd.Series, label: str) -> pd.Series:
    """
    Contraste pareado para una métrica (mismo pie pre/post).
    Devuelve:
    - n_pairs, mean_delta, sd_delta, ci95_low/high, pct_improved
    - t_stat, p_t  (t pareada)
    - w_stat, p_w  (Wilcoxon)
    - cohen_dz     (tamaño del efecto pareado)
    """
    # Pares válidos (ambos no-NA)
    valid = pre.notna() & post.notna()
    pre_v, post_v = pre[valid], post[valid]
    delta = post_v - pre_v
    n = int(valid.sum())

    # Descriptivos del delta
    desc = summarize_delta(delta)

    # t pareada (media Δ = 0)
    t_stat, p_t = (np.nan, np.nan)
    if n >= 2:
        t_stat, p_t = stats.ttest_rel(post_v, pre_v, nan_policy="omit")

    # Wilcoxon (mediana Δ = 0)
    try:
        w_stat, p_w = stats.wilcoxon(post_v, pre_v, zero_method="wilcox", correction=False, alternative="two-sided")
    except ValueError:
        w_stat, p_w = (np.nan, np.nan)

    # Tamaño del efecto (Cohen's dz)
    try:
        cohen_dz = pg.compute_effsize(post_v, pre_v, paired=True, eftype="cohen")
    except Exception:
        cohen_dz = np.nan

    return pd.Series({
        "var": label,
        "n_pairs": n,
        "mean_delta": desc["mean"],
        "sd_delta": desc["sd"],
        "ci95_low": desc["ci95_low"],
        "ci95_high": desc["ci95_high"],
        "pct_improved": desc["pct_improved"],
        "t_stat": t_stat, "p_t": p_t,
        "w_stat": w_stat, "p_w": p_w,
        "cohen_dz": cohen_dz
    })

def run_paired_suite(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ejecuta analyze_paired para las 4 métricas (total/segmentario × dch/izq)
    y aplica corrección FDR a p_t y p_w.
    """
    pairs = [
        ("vel_total_dch",  df["pre_dch_motor_velocidad_total"], df["post_dch_motor_velocidad_total"]),
        ("vel_total_izq",  df["pre_izq_motor_velocidad_total"], df["post_izq_motor_velocidad_total"]),
        ("vel_seg_dch",    df["pre_dch_motor_velocidad_segmentario"], df["post_dch_motor_velocidad_segmentario"]),
        ("vel_seg_izq",    df["pre_izq_motor_velocidad_segmentario"], df["post_izq_motor_velocidad_segmentario"]),
    ]

    rows = [analyze_paired(pre, post, label) for label, pre, post in pairs]
    out = pd.DataFrame(rows)

    # Corrección FDR (aplícalo a la familia de tests que reportes como principal)
    rej_t, p_t_fdr = pg.multicomp(out["p_t"].values, method="fdr_bh")
    rej_w, p_w_fdr = pg.multicomp(out["p_w"].values, method="fdr_bh")
    out["p_t_fdr"] = p_t_fdr
    out["p_w_fdr"] = p_w_fdr

    # Orden de columnas y redondeo
    cols = ["var","n_pairs","mean_delta","sd_delta","ci95_low","ci95_high",
            "pct_improved","t_stat","p_t","p_t_fdr","w_stat","p_w","p_w_fdr","cohen_dz"]
    return out[cols].round(4)


# Función auxiliar de conteo contra umbral (porcentaje sobre total_pies_pos)
def summarize_against_threshold(series: pd.Series, denom: int, umbral: float) -> pd.Series:
    """
    Resume una serie numérica contra un umbral, con denominador fijo.
    Devuelve:
    - total_tts_pos: total de pies con TTS positivo (denom)
    - n_validos: número de valores válidos (no NA)
    - n_faltantes: número de valores NA
    - n_positivos_<umbral: número de valores por debajo del umbral
    - n_negativos_≥umbral: número de valores por encima o igual al umbral
    - %_pos_sobre_tts_pos: % de valores por debajo del umbral sobre denom
    - %_neg_sobre_tts_pos: % de valores por encima o igual al umbral sobre denom
    - %_faltantes_sobre_tts_pos: % de valores NA sobre denom
    """
    n_valid = int(series.notna().sum())
    n_missing = int(denom - n_valid)
    n_below = int((series < umbral).sum(skipna=True))       # “positivos” al test
    n_aboveeq = int((series >= umbral).sum(skipna=True))    # “negativos” al test
    return pd.Series({
        "total_tts_pos": denom,
        "n_validos": n_valid,
        "n_faltantes": n_missing,
        "n_positivos_<umbral": n_below,
        "n_negativos_≥umbral": n_aboveeq,
        "%_pos_sobre_tts_pos": round(n_below / denom * 100, 2) if denom else np.nan,
        "%_neg_sobre_tts_pos": round(n_aboveeq / denom * 100, 2) if denom else np.nan,
        "%_faltantes_sobre_tts_pos":   round(n_missing / denom * 100, 2) if denom else np.nan,
    })
