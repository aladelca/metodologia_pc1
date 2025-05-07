import pandas as pd
import numpy as np


from src.preprocessing.outlier_detector import detect_outliers_isolation_forest, remove_outliers

# Dataset de ejemplo para pruebas
def sample_data():
    return pd.DataFrame({
        'feature1': [10, 11, 12, 13, 200],
        'feature2': [100, 101, 102, 103, 1000]
    })

# Test 1: Verifica que se agregue la columna 'is_outlier' al DataFrame
def test_detect_outliers_column_added():
    df = sample_data()
    result = detect_outliers_isolation_forest(df, ['feature1', 'feature2'], contamination=0.2)
    assert 'is_outlier' in result.columns, "No se agregó la columna 'is_outlier'"

# Test 2: Verifica que la cantidad de outliers detectados sea aproximadamente igual a la proporción especificada
def test_outlier_count_matches_contamination():
    df = sample_data()
    contamination = 0.2
    result = detect_outliers_isolation_forest(df, ['feature1', 'feature2'], contamination=contamination)
    num_outliers = result['is_outlier'].sum()
    expected = int(len(df) * contamination)
    assert abs(num_outliers - expected) <= 1, f"Se esperaban aprox. {expected} outliers, pero se detectaron {num_outliers}"

# Test 3: Verifica que la función remove_outliers elimine correctamente las filas marcadas y borre la columna 'is_outlier'
def test_remove_outliers_functionality():
    df = pd.DataFrame({
        'A': [1, 2, 3, 4],
        'is_outlier': [0, 1, 0, 1]
    })
    cleaned = remove_outliers(df)
    assert len(cleaned) == 2, "No eliminó correctamente los outliers"
    assert 'is_outlier' not in cleaned.columns, "La columna 'is_outlier' no fue eliminada"

# Test 4: Verifica que el algoritmo funcione correctamente incluso cuando hay valores faltantes
def test_detect_outliers_with_missing_values():
    df = pd.DataFrame({
        'feature1': [10, 11, np.nan, 13, 200],
        'feature2': [100, np.nan, 102, 103, 1000]
    })
    result = detect_outliers_isolation_forest(df, ['feature1', 'feature2'], contamination=0.2)
    assert 'is_outlier' in result.columns, "No se agregó la columna 'is_outlier'"
    assert result['is_outlier'].isnull().sum() == 0, "Hay valores nulos en la columna 'is_outlier'"

# Test 5: Verifica que si no hay outliers esperados (contamination=0), no se marquen como tales ni se eliminen filas
def test_no_false_modification():
    df = pd.DataFrame({
        'feature1': [1, 2, 3],
        'feature2': [4, 5, 6]
    })
    original_shape = df.shape
    result = detect_outliers_isolation_forest(df, ['feature1', 'feature2'], contamination=0)
    assert result.shape[0] == original_shape[0], "Se modificaron filas cuando no debería"
    assert result['is_outlier'].sum() == 0, "Se detectaron outliers con contamination=0"
