"""
Tests para el módulo cleaner de preprocesamiento.

Este archivo contiene pruebas unitarias para las funciones del módulo cleaner.py.
Los estudiantes pueden usarlo como base para crear sus propias pruebas.
"""

import numpy as np
import pandas as pd
import pytest
from src.preprocessing.cleaner import (
    detect_outliers,
    fill_missing_values,
    get_sample_data,
    handle_outliers,
    remove_duplicates,
    standardize_column_values,
)


@pytest.fixture
def sample_df():
    """Crear un DataFrame de muestra con datos faltantes."""
    return pd.DataFrame({
        "edad": [30, 40, None, 25, 50],
        "salario": [5000, None, 4500, 5500, 6000],
        "departamento": ["Ventas", "IT", "IT", "Ventas", None],
        "genero": ["M", "F", "M", "F", "M"],
    })


@pytest.fixture
def outlier_df():
    """Crear un DataFrame de muestra con outliers."""
    return pd.DataFrame({
        "edad": [30, 40, 35, 25, 80],
        "salario": [5000, 5200, 4500, 5500, 20000],
    })


def test_get_sample_data():
    """Probar la función get_sample_data."""
    df = get_sample_data()
    
    # Verificar que el DataFrame no está vacío
    assert not df.empty
    
    # Verificar que tiene las columnas esperadas
    expected_columns = ['id', 'edad', 'salario', 'departamento', 'genero']
    assert all(col in df.columns for col in expected_columns)
    
    # Verificar que hay valores nulos
    assert df.isna().any().any()
    
    # Verificar que hay duplicados en 'id'
    assert df['id'].duplicated().any()


def test_fill_missing_values_with_mean(sample_df):
    """Probar la función fill_missing_values con estrategia 'mean'."""
    # También proporcionar un valor de llenado para la columna departamento
    result = fill_missing_values(sample_df, strategy="mean", fill_values={"departamento": "Desconocido"})
    
    # Verificar que no hay valores faltantes
    assert result.isna().sum().sum() == 0
    
    # Verificar que el valor faltante en 'edad' se rellenó con la media
    expected_age_mean = sample_df["edad"].mean()
    assert result["edad"].iloc[2] == pytest.approx(expected_age_mean)
    
    # Verificar que el valor faltante en 'salario' se rellenó con la media
    expected_salary_mean = sample_df["salario"].mean()
    assert result["salario"].iloc[1] == pytest.approx(expected_salary_mean)
    
    # Verificar que el valor faltante en 'departamento' se rellenó con el valor especificado
    assert result["departamento"].iloc[4] == "Desconocido"


def test_fill_missing_values_with_custom_values(sample_df):
    """Probar la función fill_missing_values con valores personalizados."""
    fill_values = {"edad": 99, "departamento": "Desconocido"}
    result = fill_missing_values(sample_df, fill_values=fill_values)
    
    # Verificar que los valores se rellenaron según lo esperado
    assert result["edad"].iloc[2] == 99
    assert result["departamento"].iloc[4] == "Desconocido"
    
    # El valor de 'salario' debería rellenarse con la media
    expected_salary_mean = sample_df["salario"].mean()
    assert result["salario"].iloc[1] == pytest.approx(expected_salary_mean)


def test_remove_duplicates():
    """Probar la función remove_duplicates."""
    # Crear DataFrame con duplicados
    df = pd.DataFrame({
        "id": [1, 2, 2, 3, 4],
        "nombre": ["Juan", "María", "María", "Pedro", "Ana"],
        "departamento": ["Ventas", "Marketing", "Marketing", "IT", "Ventas"],
    })
    
    # Eliminar duplicados completos
    result = remove_duplicates(df)
    assert len(result) == 4  # Debería eliminar una fila
    
    # Eliminar duplicados basados en las columnas 'nombre' y 'departamento'
    result = remove_duplicates(df, subset=["nombre", "departamento"])
    assert len(result) == 4  # Debería eliminar una fila


def test_standardize_column_values(sample_df):
    """Probar la función standardize_column_values."""
    mapping = {"M": "Masculino", "F": "Femenino"}
    result = standardize_column_values(sample_df, "genero", mapping)
    
    # Verificar que los valores se estandarizaron
    assert result["genero"].iloc[0] == "Masculino"
    assert result["genero"].iloc[1] == "Femenino"
    
    # El DataFrame original no debe modificarse
    assert sample_df["genero"].iloc[0] == "M"


def test_detect_outliers_iqr(outlier_df):
    """Probar la función detect_outliers con método IQR."""
    outliers = detect_outliers(outlier_df, "salario", method="iqr", threshold=1.5)
    
    # Verificar que detecta el outlier en la última fila
    assert outliers.iloc[4]
    
    # Verificar que las demás filas no son outliers
    assert not any(outliers.iloc[:4])


def test_detect_outliers_zscore(outlier_df):
    """Probar la función detect_outliers con método Z-Score."""
    # Usar un umbral más bajo para detectar el outlier con Z-score
    outliers = detect_outliers(outlier_df, "salario", method="zscore", threshold=1.2)
    
    # Verificar que detecta el outlier en la última fila
    assert outliers.iloc[4]
    
    # Verificar que las demás filas no son outliers (dependiendo del umbral, esto podría no cumplirse)
    assert sum(outliers.iloc[:4]) == 0


def test_detect_outliers_invalid_column(outlier_df):
    """Probar que detect_outliers lanza error con columna inválida."""
    with pytest.raises(ValueError):
        detect_outliers(outlier_df, "columna_inexistente")


def test_detect_outliers_invalid_method(outlier_df):
    """Probar que detect_outliers lanza error con método inválido."""
    with pytest.raises(ValueError):
        detect_outliers(outlier_df, "salario", method="metodo_inexistente")


def test_handle_outliers_clip(outlier_df):
    """Probar la función handle_outliers con método 'clip'."""
    result = handle_outliers(outlier_df, "salario", method="clip")
    
    # El valor original era 20000, debería estar recortado
    original_value = outlier_df["salario"].iloc[4]
    clipped_value = result["salario"].iloc[4]
    
    assert clipped_value < original_value
    
    # Verificar que todos los demás valores se mantienen igual
    for i in range(4):
        assert result["salario"].iloc[i] == outlier_df["salario"].iloc[i]


def test_handle_outliers_remove(outlier_df):
    """Probar la función handle_outliers con método 'remove'."""
    result = handle_outliers(outlier_df, "salario", method="remove")
    
    # Debería tener una fila menos
    assert len(result) == len(outlier_df) - 1
    
    # La fila con el outlier debería haberse eliminado
    assert 20000 not in result["salario"].values


def test_handle_outliers_replace(outlier_df):
    """Probar la función handle_outliers con método 'replace'."""
    # Usar la mediana como valor de reemplazo
    result = handle_outliers(outlier_df, "salario", method="replace")
    
    # El valor del outlier debería ser la mediana
    median = outlier_df["salario"].median()
    assert result["salario"].iloc[4] == median
    
    # Probar con un valor personalizado
    result = handle_outliers(
        outlier_df, "salario", method="replace", replacement_value=9999
    )
    assert result["salario"].iloc[4] == 9999


def test_handle_outliers_invalid_method(outlier_df):
    """Probar que handle_outliers lanza error con método inválido."""
    with pytest.raises(ValueError):
        handle_outliers(outlier_df, "salario", method="metodo_inexistente")


def test_complete_workflow():
    """Probar un flujo de trabajo completo con todas las funciones."""
    # Obtener datos de ejemplo
    df = get_sample_data()
    
    # 1. Eliminar duplicados
    df_no_duplicates = remove_duplicates(df, subset=['id'])
    assert len(df_no_duplicates) < len(df)
    
    # 2. Estandarizar valores de género
    mapping = {'M': 'Masculino', 'm': 'Masculino', 'F': 'Femenino', 'f': 'Femenino'}
    df_std = standardize_column_values(df_no_duplicates, 'genero', mapping)
    assert set(df_std['genero'].unique()).issubset({'Masculino', 'Femenino'})
    
    # 3. Detectar y manejar outliers
    outliers = detect_outliers(df_std, 'salario', method='iqr')
    df_no_outliers = handle_outliers(df_std, 'salario', method='clip')
    
    # 4. Llenar valores faltantes
    df_clean = fill_missing_values(
        df_no_outliers, 
        strategy='median', 
        fill_values={'departamento': 'Desconocido'}
    )
    
    # Verificar que el resultado no tiene valores faltantes
    assert not df_clean.isna().any().any()
    
    # Si había valores NaN en 'departamento', verificar que se rellenaron con 'Desconocido'
    if df_no_outliers['departamento'].isna().any():
        assert 'Desconocido' in df_clean['departamento'].values 