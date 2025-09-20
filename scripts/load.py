import pandas as pd
from .config import DATA_RAW_PATH, DATA_PROCESSED_PATH, DATE_COLS, DATE_DAYFIRST, DECIMAL, BINARY_COLS, ID_COL, NUMERIC_PREFIXES

def read_csv_raw(path: str) -> pd.DataFrame:
    """
    Lee un CSV con detección de separador.
    - Soporta coma decimal
    - Parseo de fechas
    """
    try:
        df = pd.read_csv(
            path,
            decimal=DECIMAL,
            parse_dates=DATE_COLS,
            dayfirst=DATE_DAYFIRST,
            sep=None,  # Detección automática de separador
            engine='python',  # Necesario para sep=None
            dtype={ID_COL: str},  # Asegurar que ID se lee como string
            na_values=['', 'NA', 'NaN', None],  # Manejar valores faltantes comunes
            keep_default_na=True
        )
    except Exception as e:
        df = pd.read_csv(
            path,
            decimal=DECIMAL,
            parse_dates=DATE_COLS,
            dayfirst=DATE_DAYFIRST,
            sep=';',  # Intentar con separador punto y coma
            dtype={ID_COL: str},  # Asegurar que ID se lee como string
            na_values=['', 'NA', 'NaN', None],  # Manejar valores faltantes comunes
            keep_default_na=True
        )

    return df

def read_csv_processed(path: str) -> pd.DataFrame:
    """
    Lee un CSV procesado (punto decimal, UTF-8, coma separador).
    """
    df = pd.read_csv(
        path,
        decimal='.',  # Punto decimal en datos procesados
        sep=',',      # Coma como separador en datos procesados
        dtype={ID_COL: str},  # Asegurar que ID se lee como string
        na_values=['', 'NA', 'NaN', None],  # Manejar valores faltantes comunes
        keep_default_na=True
    )
    return df

def coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Coerce columnas a tipos adecuados.
    - Fechas a datetime
    - Binarios 0/1/NA como Int64
    - Números a float
    - ID como string
    """
    # Fechas
    for col in DATE_COLS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=DATE_DAYFIRST, errors='coerce')

    # Binarios
    for col in BINARY_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

    # Medidas numéricas
    num_cols = [
        col for col in df.columns
        if col not in DATE_COLS and any(col.startswith(prefix) for prefix in NUMERIC_PREFIXES)
    ]
    for col in num_cols:
        if pd.api.types.is_object_dtype(df[col]):
            df[col] = (
                df[col]
                .str.replace(DECIMAL, '.', regex=False) # cambiar coma por punto
                .str.replace(' ', '', regex=False)  # eliminar espacios
            )
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('float64')
    
    # ID como string
    if ID_COL in df.columns:
        df[ID_COL] = df[ID_COL].astype(str).str.strip()

    return df

def load_raw(filename: str) -> pd.DataFrame:
    """
    Carga datos crudos desde data/raw y aplica coerción de tipos.
    """
    path = DATA_RAW_PATH / filename
    df = read_csv_raw(path)
    df = coerce_types(df)
    return df

def load_processed(filename: str) -> pd.DataFrame:
    """
    Carga datos procesados desde data/processed y aplica coerción de tipos.
    """
    path = DATA_PROCESSED_PATH / filename
    df = read_csv_processed(path)
    return df