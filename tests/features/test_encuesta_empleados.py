import pytest
import pandas as pd

from src.features.encuesta_empleados import procesar_encuesta_empleados
from src.preprocessing.config import (
    COLUMN_AVERAGE_EMPLOYEE_SATISFACTION,
    MEAN_COLUMNS,
    RUTA_EMPLOYEE_SURVEY,
    RUTA_GENERAL,
    EMPLOYEE_COLUMN_JOIN
)
from src.preprocessing.read_employee_files import merge_files


def test_procesar_devuelve_dataframe():
    """Verifica que la función retorna un objeto de tipo DataFrame."""
    df = procesar_encuesta_empleados()
    assert isinstance(df, pd.DataFrame)


def test_procesar_agrega_columna_promedio():
    """
    Verifica que la función agrega una nueva columna al DataFrame original.
    Se espera que la nueva columna sea 'average_employee_satisfaction'.
    """
    df = procesar_encuesta_empleados()
    assert COLUMN_AVERAGE_EMPLOYEE_SATISFACTION in df.columns


def test_columna_promedio_es_numerica():
    """Verifica que los valores en la columna de promedio sean numéricos."""
    df = procesar_encuesta_empleados()
    assert pd.api.types.is_numeric_dtype(df[COLUMN_AVERAGE_EMPLOYEE_SATISFACTION])


def test_incremento_columnas_por_uno():
    """
    Verifica que el número de columnas en el DataFrame final sea igual
    al original más una columna adicional.
    """
    df_original = merge_files(RUTA_GENERAL, RUTA_EMPLOYEE_SURVEY, EMPLOYEE_COLUMN_JOIN)
    df_procesado = procesar_encuesta_empleados()
    assert df_procesado.shape[1] == df_original.shape[1] + 1


def test_columnas_base_estan_presentes():
    """Verifica que las columnas base requeridas para el promedio estén presentes en el DataFrame resultante."""
    df = procesar_encuesta_empleados()
    for col in MEAN_COLUMNS:
        assert col in df.columns