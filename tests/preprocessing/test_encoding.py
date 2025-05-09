import pandas as pd
import pytest
from src.preprocessing.encoding import apply_label_encoding, apply_one_hot_encoding

def test_apply_label_encoding():
    """Valida la codificación correcta de las columnas binarias."""
    df = pd.DataFrame({
        'Attrition': ['Yes', 'No', 'Yes', 'No'],
        'Gender': ['Male', 'Female', 'Female', 'Male']
    })

    encoded_df, encoders = apply_label_encoding(df, ['Attrition', 'Gender'])

    # Verifica que las columnas se codificaron correctamente
    assert set(encoded_df['Attrition'].unique()) <= {0, 1}
    assert set(encoded_df['Gender'].unique()) <= {0, 1}
    # Verifica que se devolvieron los encoders
    assert 'Attrition' in encoders and 'Gender' in encoders

def test_apply_one_hot_encoding():
    """Valida la codificación correcta de las columnas nominales."""
    df = pd.DataFrame({
        'Department': ['Sales', 'HR', 'Sales', 'IT'],
        'MaritalStatus': ['Single', 'Married', 'Single', 'Divorced']
    })

    encoded_df = apply_one_hot_encoding(df, ['Department', 'MaritalStatus'])

    # Verifica que las nuevas columnas fueron creadas
    expected_columns = {'Department_Sales', 'Department_HR', 'Department_IT',
                        'MaritalStatus_Single', 'MaritalStatus_Married', 'MaritalStatus_Divorced'}
    assert expected_columns.issubset(set(encoded_df.columns))

    # Verifica que las columnas originales ya no están
    assert 'Department' not in encoded_df.columns
    assert 'MaritalStatus' not in encoded_df.columns
