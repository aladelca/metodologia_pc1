"""Este módulo contiene un método para realizar la unión de 2 DataFrame."""

import pandas as pd


def merge_dataframe(
    df1: pd.DataFrame, df2: pd.DataFrame, column_join: str
) -> pd.DataFrame:
    """
    Une dos dataframes en un único dataframe usando una columna común.

    Parámetros:
    ----------
    df1 : pd.DataFrame
        Primer DataFrame.
    df2 : pd.DataFrame
        Segundo DataFrame.
    column_join : str
        Nombre de la columna común para unir ambos archivos.

    Retorna:
    -------
    pd.DataFrame
        DataFrame resultante de la unión.
    """
    if column_join not in df1.columns or column_join not in df2.columns:
        raise KeyError(f"La columna '{column_join}' no se encuentra en ambos archivos.")

    return pd.merge(df1, df2, on=column_join, how="inner")
