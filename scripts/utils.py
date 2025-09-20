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