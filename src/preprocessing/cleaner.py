"""
Módulo para la limpieza de datos (guía para estudiantes).

Este módulo contiene funciones genéricas para:
- Estandarización de valores

NOTA: Este es un módulo de ejemplo. Los estudiantes deben adaptarlo según necesidades.
"""

from typing import Dict

import pandas as pd


def standardize_column_values(
    df: pd.DataFrame, column: str, mapping: Dict
) -> pd.DataFrame:
    """
    Estandariza los valores en una columna de acuerdo a un mapeo.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con la columna a estandarizar.
    column : str
        Nombre de la columna a estandarizar.
    mapping : Dict
        Diccionario con el mapeo de valores.
        Por ejemplo: {'M': 'Masculino', 'F': 'Femenino'}.

    Returns
    -------
    pd.DataFrame
        DataFrame con valores estandarizados.

    Examples
    --------
    >>> # Crear datos dummy para demostración
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'genero': ['M', 'F', 'm', 'F', 'f'],
    ...     'edad': [25, 30, 35, 28, 40]
    ... })
    >>> # Estandarizar valores de género
    >>> mapping = {'M': 'Masculino', 'm': 'Masculino', 'F': 'Femenino', 'f': 'Femenino'}
    >>> df_std = standardize_column_values(df, 'genero', mapping)
    >>> print(df_std)
    """
    df_std = df.copy()

    if column in df_std.columns:
        df_std[column] = df_std[column].replace(mapping)

    return df_std


# Datos de ejemplo para que los estudiantes puedan probar rápidamente
def get_sample_data() -> pd.DataFrame:
    """
    Crea un DataFrame de ejemplo para realizar pruebas de estandarización.

    Returns
    -------
    pd.DataFrame
        DataFrame con datos de ejemplo para estandarización de valores.

    Examples
    --------
    >>> # Obtener datos de ejemplo
    >>> df_sample = get_sample_data()
    >>> print(df_sample.head())
    """
    # Crear un DataFrame con datos de ejemplo
    data = {
        "id": list(range(1, 6)),
        "genero": ["M", "F", "m", "F", "f"],
        "estado_civil": ["Soltero", "soltero", "CASADO", "Casado", "viudo"],
        "nivel_educativo": [
            "universitario",
            "UNIVERSITARIO",
            "Técnico",
            "Secundaria",
            "técnico",
        ],
        "departamento": ["Ventas", "Marketing", "ventas", "MARKETING", "IT"],
    }

    return pd.DataFrame(data)
