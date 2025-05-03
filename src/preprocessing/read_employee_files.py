import pandas as pd
from pathlib import Path

def read_file(file: str) -> pd.DataFrame:
    """
    Lee un archivo CSV y retorna un DataFrame.

    Parámetros:
    ----------
    file : str
        Ruta al archivo CSV.

    Retorna:
    -------
    pd.DataFrame
        DataFrame con el contenido del archivo.
    """
    if not Path(file).exists():
        raise FileNotFoundError(f"El archivo {file} no existe.")
    return pd.read_csv(file)


def merge_files(file1: str, file2: str, column_join: str) -> pd.DataFrame:
    """
    Une dos archivos CSV en un único DataFrame usando una columna común.

    Parámetros:
    ----------
    file1 : str
        Ruta al primer archivo CSV.
    file2 : str
        Ruta al segundo archivo CSV.
    column_join : str
        Nombre de la columna común para unir ambos archivos.

    Retorna:
    -------
    pd.DataFrame
        DataFrame resultante de la unión.
    """
    ds1 = read_file(file1)
    ds2 = read_file(file2)

    if column_join not in ds1.columns or column_join not in ds2.columns:
        raise KeyError(f"La columna '{column_join}' no se encuentra en ambos archivos.")

    return pd.merge(ds1, ds2, on=column_join, how="inner")

def mean_columns(df: pd.DataFrame, columnaName: str, columns: list) -> pd.DataFrame:
    """
    Calcula el promedio por fila de columnas específicas y lo guarda en una nueva columna.

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame que contiene los datos.
    columnaName : str
        Nombre de la nueva columna que almacenará el promedio.
    columns : list
        Lista de nombres de columnas numéricas para calcular el promedio.

    Retorna:
    -------
    pd.DataFrame
        DataFrame con la nueva columna agregada.
    """
    if not columns:
        raise ValueError("La lista de columnas no debe estar vacía.")

    missing_cols = [col for col in columns if col not in df.columns]
    if missing_cols:
        raise KeyError(f"Las siguientes columnas no están en el DataFrame: {missing_cols}")

    df[columnaName] = df[columns].mean(axis=1)
    return df