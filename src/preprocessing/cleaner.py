"""
Módulo para la limpieza de datos (guía para estudiantes).

Este módulo contiene funciones genéricas para:
- Manejo de valores faltantes
- Eliminación de duplicados
- Detección y manejo de outliers
- Estandarización de valores

NOTA: Este es un módulo de ejemplo. Los estudiantes deben adaptarlo según necesidades.
"""

from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.impute import SimpleImputer


def fill_missing_values(
    df: pd.DataFrame, strategy: str = "mean", fill_values: Optional[Dict] = None
) -> pd.DataFrame:
    """
    Rellena los valores faltantes en un DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con valores faltantes.
    strategy : str, optional
        Estrategia de imputación para valores numéricos.
        Opciones: 'mean', 'median', 'most_frequent'.
        Por defecto es 'mean'.
    fill_values : Dict, optional
        Diccionario con valores específicos para rellenar por columna.
        Por ejemplo: {'columna1': 0, 'columna2': 'desconocido'}.

    Returns
    -------
    pd.DataFrame
        DataFrame con valores faltantes rellenados.

    Examples
    --------
    >>> # Crear datos dummy para demostración
    >>> import pandas as pd
    >>> import numpy as np
    >>> np.random.seed(42)
    >>> df = pd.DataFrame({
    ...     'edad': [25, np.nan, 34, 28, np.nan],
    ...     'salario': [50000, 60000, np.nan, 55000, 65000],
    ...     'departamento': ['Ventas', 'Marketing', 'Ventas', np.nan, 'IT']
    ... })
    >>> # Llenar valores faltantes
    >>> df_filled = fill_missing_values(
    ...     df,
    ...     strategy='mean',
    ...     fill_values={'departamento': 'Desconocido'}
    ... )
    >>> print(df_filled)
    """
    # Crear una copia para no modificar el original
    df_clean = df.copy()

    # Primero aplicar los valores específicos si se proporcionan
    if fill_values:
        for col, value in fill_values.items():
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].fillna(value)

    # Separar columnas numéricas y categóricas que aún tienen valores faltantes
    remaining_na_cols = df_clean.columns[df_clean.isna().any()]
    numeric_cols = (
        df_clean[remaining_na_cols].select_dtypes(include=[np.number]).columns.tolist()
    )
    categorical_cols = (
        df_clean[remaining_na_cols].select_dtypes(exclude=[np.number]).columns.tolist()
    )

    # Imputar valores numéricos usando SimpleImputer
    if numeric_cols:
        imputer = SimpleImputer(strategy=strategy)
        df_clean[numeric_cols] = imputer.fit_transform(df_clean[numeric_cols])

    # Imputar valores categóricos con la moda
    if categorical_cols:
        cat_imputer = SimpleImputer(strategy="most_frequent")
        df_clean[categorical_cols] = cat_imputer.fit_transform(
            df_clean[categorical_cols]
        )

    return df_clean


def remove_duplicates(
    df: pd.DataFrame, subset: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Elimina filas duplicadas de un DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con posibles duplicados.
    subset : List[str], optional
        Lista de columnas a considerar para determinar duplicados.
        Si es None, se utilizan todas las columnas.

    Returns
    -------
    pd.DataFrame
        DataFrame sin filas duplicadas.

    Examples
    --------
    >>> # Crear datos dummy para demostración
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'id': [1, 2, 2, 3, 4],
    ...     'nombre': ['Juan', 'María', 'María', 'Pedro', 'Ana'],
    ...     'departamento': ['Ventas', 'Marketing', 'Marketing', 'IT', 'Ventas']
    ... })
    >>> # Eliminar duplicados basados en nombre y departamento
    >>> df_no_duplicates = remove_duplicates(df, subset=['nombre', 'departamento'])
    >>> print(df_no_duplicates)
    """
    return df.drop_duplicates(subset=subset, keep="first")


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


def detect_outliers(
    df: pd.DataFrame, column: str, method: str = "iqr", threshold: float = 1.5
) -> pd.Series:
    """
    Detecta outliers en una columna numérica.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame que contiene la columna a analizar.
    column : str
        Nombre de la columna numérica.
    method : str, optional
        Método para detectar outliers ('iqr', 'zscore').
        Por defecto es 'iqr'.
    threshold : float, optional
        Umbral para considerar un valor como outlier.
        Para IQR, valores típicos son 1.5 o 3.
        Para Z-score, valores típicos son 3 o 2.5.

    Returns
    -------
    pd.Series
        Serie booleana que indica si cada valor es un outlier (True) o no (False).

    Examples
    --------
    >>> # Crear datos dummy para demostración
    >>> import pandas as pd
    >>> import numpy as np
    >>> np.random.seed(42)
    >>> df = pd.DataFrame({
    ...     'salario': [50000, 55000, 52000, 51000, 53000, 120000, 48000]
    ... })
    >>> # Detectar outliers en salario
    >>> outliers = detect_outliers(df, 'salario', method='iqr', threshold=1.5)
    >>> print(df[outliers])  # Muestra las filas con outliers
    """
    if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column {column} must be numeric")

    if method == "iqr":
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR

        return (df[column] < lower_bound) | (df[column] > upper_bound)

    elif method == "zscore":
        z_scores = np.abs(stats.zscore(df[column].dropna()))
        outliers = pd.Series(False, index=df.index)

        # Aplicar los z-scores a los índices correspondientes
        non_na_idx = df[~df[column].isna()].index
        outliers.loc[non_na_idx] = pd.Series(z_scores > threshold, index=non_na_idx)

        return outliers

    else:
        raise ValueError("Method must be 'iqr' or 'zscore'")


def handle_outliers(
    df: pd.DataFrame, column: str, method: str = "clip", **kwargs
) -> pd.DataFrame:
    """
    Maneja outliers en una columna numérica.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame que contiene la columna a procesar.
    column : str
        Nombre de la columna numérica.
    method : str, optional
        Método para manejar outliers ('clip', 'remove', 'replace').
        Por defecto es 'clip'.
    **kwargs
        Argumentos adicionales para detect_outliers() o para el método específico.

    Returns
    -------
    pd.DataFrame
        DataFrame con outliers tratados.

    Examples
    --------
    >>> # Crear datos dummy para demostración
    >>> import pandas as pd
    >>> import numpy as np
    >>> np.random.seed(42)
    >>> df = pd.DataFrame({
    ...     'salario': [50000, 55000, 52000, 51000, 53000, 120000, 48000]
    ... })
    >>> # Manejar outliers en salario (recortando a los límites)
    >>> df_clean = handle_outliers(df, 'salario', method='clip')
    >>> print(df_clean)
    >>>
    >>> # Manejar outliers en salario (eliminando filas)
    >>> df_clean = handle_outliers(df, 'salario', method='remove')
    >>> print(df_clean)
    >>>
    >>> # Manejar outliers en salario (reemplazando con la mediana)
    >>> df_clean = handle_outliers(df, 'salario', method='replace')
    >>> print(df_clean)
    """
    df_result = df.copy()

    # Obtener los outliers
    outlier_method = kwargs.pop("outlier_method", "iqr")
    threshold = kwargs.pop("threshold", 1.5)
    outliers = detect_outliers(df, column, method=outlier_method, threshold=threshold)

    if method == "clip":
        # Recortar valores a los límites definidos por el IQR
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR

        df_result[column] = df_result[column].clip(lower=lower_bound, upper=upper_bound)

    elif method == "remove":
        # Eliminar filas con outliers
        df_result = df_result[~outliers]

    elif method == "replace":
        # Reemplazar outliers con un valor específico o la mediana
        replacement_value = kwargs.get("replacement_value", df[column].median())
        df_result.loc[outliers, column] = replacement_value

    else:
        raise ValueError("Method must be 'clip', 'remove', or 'replace'")

    return df_result


# Datos de ejemplo para que los estudiantes puedan probar rápidamente
def get_sample_data() -> pd.DataFrame:
    """
    Crea un DataFrame de ejemplo para realizar pruebas de limpieza.

    Returns
    -------
    pd.DataFrame
        DataFrame con datos de ejemplo incluyendo valores faltantes,
        duplicados y outliers.

    Examples
    --------
    >>> # Obtener datos de ejemplo
    >>> df_sample = get_sample_data()
    >>> print(df_sample.head())
    """
    np.random.seed(42)

    # Crear un DataFrame con datos de ejemplo
    data = {
        "id": list(range(1, 16)) + [3, 5],  # Incluye duplicados
        "edad": [
            25,
            30,
            np.nan,
            28,
            40,
            35,
            42,
            np.nan,
            38,
            29,
            45,
            33,
            36,
            31,
            27,
            38,
            40,
        ],
        "salario": [
            50000,
            55000,
            60000,
            np.nan,
            70000,
            52000,
            90000,
            54000,
            120000,
            51000,
            53000,
            np.nan,
            59000,
            48000,
            56000,
            54000,
            70000,
        ],
        "departamento": [
            "Ventas",
            "Marketing",
            "Ventas",
            np.nan,
            "IT",
            "Marketing",
            "IT",
            "Ventas",
            "Marketing",
            "Ventas",
            "IT",
            np.nan,
            "Marketing",
            "Ventas",
            "IT",
            "Ventas",
            "IT",
        ],
        "genero": [
            "M",
            "F",
            "m",
            "F",
            "M",
            "f",
            "M",
            "F",
            "M",
            "F",
            "M",
            "F",
            "M",
            "F",
            "m",
            "F",
            "M",
        ],
    }

    return pd.DataFrame(data)
