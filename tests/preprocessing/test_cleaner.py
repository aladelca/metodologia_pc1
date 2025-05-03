"""
Tests para el módulo cleaner de preprocesamiento.

Este archivo contiene pruebas unitarias para las funciones del módulo cleaner.py.
Los estudiantes pueden usarlo como base para crear sus propias pruebas.
"""

import pandas as pd
import pytest

from src.preprocessing.cleaner import get_sample_data, standardize_column_values


@pytest.fixture
def sample_df():
    """Crear un DataFrame de muestra para estandarización."""
    return pd.DataFrame(
        {
            "genero": ["M", "F", "m", "F", "m"],
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
    )


def test_get_sample_data():
    """Probar la función get_sample_data."""
    df = get_sample_data()

    # Verificar que el DataFrame no está vacío
    assert not df.empty

    # Verificar que tiene las columnas esperadas
    expected_columns = [
        "id",
        "genero",
        "estado_civil",
        "nivel_educativo",
        "departamento",
    ]
    assert all(col in df.columns for col in expected_columns)

    # Verificar que hay registros suficientes
    assert len(df) == 5

    # Verificar que contiene valores en mayúsculas, minúsculas y mezclados
    assert any(df["genero"].str.islower())
    assert any(df["genero"].str.isupper())


def test_standardize_column_values_genero(sample_df):
    """Probar la función standardize_column_values con la columna genero."""
    mapping = {"M": "Masculino", "m": "Masculino", "F": "Femenino", "f": "Femenino"}
    result = standardize_column_values(sample_df, "genero", mapping)

    # Verificar que los valores se estandarizaron correctamente
    assert result["genero"].iloc[0] == "Masculino"
    assert result["genero"].iloc[1] == "Femenino"
    assert result["genero"].iloc[2] == "Masculino"

    # El DataFrame original no debe modificarse
    assert sample_df["genero"].iloc[0] == "M"

    # Verificar valores únicos después de la estandarización
    assert set(result["genero"].unique()) == {"Masculino", "Femenino"}


def test_standardize_column_values_estado_civil(sample_df):
    """Probar la función standardize_column_values con la columna estado_civil."""
    mapping = {
        "Soltero": "Soltero/a",
        "soltero": "Soltero/a",
        "CASADO": "Casado/a",
        "Casado": "Casado/a",
        "viudo": "Viudo/a",
    }
    result = standardize_column_values(sample_df, "estado_civil", mapping)

    # Verificar que los valores se estandarizaron correctamente
    assert result["estado_civil"].iloc[0] == "Soltero/a"
    assert result["estado_civil"].iloc[1] == "Soltero/a"
    assert result["estado_civil"].iloc[2] == "Casado/a"
    assert result["estado_civil"].iloc[3] == "Casado/a"
    assert result["estado_civil"].iloc[4] == "Viudo/a"

    # Verificar valores únicos después de la estandarización
    assert set(result["estado_civil"].unique()) == {"Soltero/a", "Casado/a", "Viudo/a"}


def test_standardize_column_values_nivel_educativo(sample_df):
    """Probar la función standardize_column_values con la columna nivel_educativo."""
    mapping = {
        "universitario": "Universitario",
        "UNIVERSITARIO": "Universitario",
        "Técnico": "Técnico",
        "técnico": "Técnico",
        "Secundaria": "Secundaria",
    }
    result = standardize_column_values(sample_df, "nivel_educativo", mapping)

    # Verificar que los valores se estandarizaron correctamente
    assert result["nivel_educativo"].iloc[0] == "Universitario"
    assert result["nivel_educativo"].iloc[1] == "Universitario"
    assert result["nivel_educativo"].iloc[2] == "Técnico"
    assert result["nivel_educativo"].iloc[3] == "Secundaria"
    assert result["nivel_educativo"].iloc[4] == "Técnico"

    # Verificar valores únicos después de la estandarización
    assert set(result["nivel_educativo"].unique()) == {
        "Universitario",
        "Técnico",
        "Secundaria",
    }


def test_standardize_column_values_departamento(sample_df):
    """Probar la función standardize_column_values con la columna departamento."""
    mapping = {
        "Ventas": "VENTAS",
        "ventas": "VENTAS",
        "Marketing": "MARKETING",
        "MARKETING": "MARKETING",
        "IT": "IT",
    }
    result = standardize_column_values(sample_df, "departamento", mapping)

    # Verificar que los valores se estandarizaron correctamente
    assert result["departamento"].iloc[0] == "VENTAS"
    assert result["departamento"].iloc[1] == "MARKETING"
    assert result["departamento"].iloc[2] == "VENTAS"
    assert result["departamento"].iloc[3] == "MARKETING"
    assert result["departamento"].iloc[4] == "IT"

    # Verificar valores únicos después de la estandarización
    assert set(result["departamento"].unique()) == {"VENTAS", "MARKETING", "IT"}


def test_standardize_column_values_nonexistent_column(sample_df):
    """Probar la función standardize_column_values con una columna que no existe."""
    mapping = {"A": "Valor A", "B": "Valor B"}
    result = standardize_column_values(sample_df, "columna_inexistente", mapping)

    # Verificar que el DataFrame no se modificó
    assert result.equals(sample_df)


def test_standardize_column_values_empty_mapping(sample_df):
    """Probar la función standardize_column_values con un mapeo vacío."""
    mapping = {}
    result = standardize_column_values(sample_df, "genero", mapping)

    # Verificar que el DataFrame no se modificó
    assert result["genero"].equals(sample_df["genero"])


def test_standardize_multiple_columns(sample_df):
    """Probar la estandarización de múltiples columnas en secuencia."""
    # Mapeo para género
    genero_mapping = {
        "M": "Masculino",
        "m": "Masculino",
        "F": "Femenino",
        "f": "Femenino",
    }

    # Mapeo para departamento
    departamento_mapping = {
        "Ventas": "VENTAS",
        "ventas": "VENTAS",
        "Marketing": "MARKETING",
        "MARKETING": "MARKETING",
    }

    # Aplicar estandarizaciones en secuencia
    result = standardize_column_values(sample_df, "genero", genero_mapping)
    result = standardize_column_values(result, "departamento", departamento_mapping)

    # Verificar que ambas columnas se estandarizaron correctamente
    assert result["genero"].iloc[0] == "Masculino"
    assert result["genero"].iloc[1] == "Femenino"

    assert result["departamento"].iloc[0] == "VENTAS"
    assert result["departamento"].iloc[1] == "MARKETING"

    # Verificar valores únicos después de la estandarización
    assert set(result["genero"].unique()) == {"Masculino", "Femenino"}
    assert set(result["departamento"].unique()) == {"VENTAS", "MARKETING", "IT"}
