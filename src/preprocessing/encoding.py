import pandas as pd
from sklearn.preprocessing import LabelEncoder

def apply_label_encoding(df, columns):
    """
    Aplica Label Encoding a columnas binarias.
    
    Parámetros:
    ----------
      df (pd.DataFrame): DataFrame original.
      columns (list): Lista de nombres de columnas a codificar.
    
    Retorna:
    -------
      df_encoded (pd.DataFrame): DataFrame con columnas codificadas.
      encoders (dict): Diccionario con los LabelEncoders por columna.
    """
    df_encoded = df.copy()
    encoders = {}

    for col in columns:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df_encoded[col])
        encoders[col] = le
    
    return df_encoded, encoders

def apply_one_hot_encoding(df, columns):
    """
    Aplica One Hot Encoding usando pandas.get_dummies.
    
    Parámetros:
    ----------
      df (pd.DataFrame): DataFrame original.
      columns (list): Lista de nombres de columnas a codificar.
    
    Retorna:
    -------
      df_encoded (pd.DataFrame): DataFrame con columnas codificadas.
    """
    df_encoded = pd.get_dummies(df, columns=columns, drop_first=False)
    return df_encoded
