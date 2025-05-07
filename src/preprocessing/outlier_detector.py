import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_outliers_isolation_forest(df, features, contamination=0.01, random_state=42):
    """
    Aplica Isolation Forest para detectar outliers en columnas numéricas.
    """
    model = IsolationForest(contamination=contamination, random_state=random_state)
    subset = df[features].dropna()
    preds = model.fit_predict(subset)

    df_result = df.copy()
    df_result['is_outlier'] = 0
    df_result.loc[subset.index, 'is_outlier'] = (preds == -1).astype(int)
    return df_result

 #Eliminar outliers
def remove_outliers(df):
    """
   Elimina los registros detectados como outliers.
    """
    return df[df['is_outlier'] == 0].drop(columns=['is_outlier'])
