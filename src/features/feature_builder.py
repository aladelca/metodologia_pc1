"""
Módulo para la creación de características (guía para estudiantes).

Este módulo contiene funciones genéricas para:
- Creación de nuevas variables derivadas
- Transformación de variables
- Selección de características

NOTA: Este es un módulo de ejemplo. Los estudiantes deben adaptarlo según sus necesidades.
"""

from typing import List, Optional, Union

import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif


def crear_categorias_edad(df: pd.DataFrame, columna: str = "edad") -> pd.DataFrame:
    """
    Crea una variable categórica basada en la edad.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con la columna de edad.
    columna : str, optional
        Nombre de la columna con la edad.
        Por defecto es 'edad'.

    Returns
    -------
    pd.DataFrame
        DataFrame con la nueva columna 'grupo_edad'.

    Examples
    --------
    >>> # Crear datos dummy para demostración
    >>> import pandas as pd
    >>> import numpy as np
    >>> np.random.seed(42)
    >>> df = pd.DataFrame({
    ...     'edad': [25, 32, 45, 18, 60, 15, 50, 38, 72]
    ... })
    >>> # Crear categorías de edad
    >>> df_con_categorias = crear_categorias_edad(df)
    >>> print(df_con_categorias)
    """
    result = df.copy()
    
    if columna not in result.columns:
        raise ValueError(f"Columna {columna} no encontrada en el DataFrame")
    
    # Crear la nueva variable categórica
    conditions = [
        (result[columna] < 18),
        (result[columna] >= 18) & (result[columna] < 30),
        (result[columna] >= 30) & (result[columna] < 50),
        (result[columna] >= 50) & (result[columna] < 65),
        (result[columna] >= 65)
    ]
    
    values = ['Menor', 'Joven', 'Adulto', 'Senior', 'Jubilado']
    
    result['grupo_edad'] = np.select(conditions, values, default='Desconocido')
    
    return result


def calcular_ratio_salario_edad(
    df: pd.DataFrame, 
    columna_salario: str = "salario", 
    columna_edad: str = "edad"
) -> pd.DataFrame:
    """
    Crea una variable que representa el ratio de salario a edad.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con las columnas de salario y edad.
    columna_salario : str, optional
        Nombre de la columna de salario.
        Por defecto es 'salario'.
    columna_edad : str, optional
        Nombre de la columna de edad.
        Por defecto es 'edad'.

    Returns
    -------
    pd.DataFrame
        DataFrame con la nueva columna 'ratio_salario_edad'.

    Examples
    --------
    >>> # Crear datos dummy para demostración
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'salario': [50000, 60000, 75000, 45000],
    ...     'edad': [25, 30, 45, 22]
    ... })
    >>> # Calcular ratio salario/edad
    >>> df_con_ratio = calcular_ratio_salario_edad(df)
    >>> print(df_con_ratio)
    """
    result = df.copy()
    
    if columna_salario not in result.columns:
        raise ValueError(f"Columna {columna_salario} no encontrada en el DataFrame")
    
    if columna_edad not in result.columns:
        raise ValueError(f"Columna {columna_edad} no encontrada en el DataFrame")
    
    # Crear la nueva variable
    result['ratio_salario_edad'] = (result[columna_salario] / result[columna_edad]).round(2)
    
    return result


def crear_indice_satisfaccion(
    df: pd.DataFrame,
    columnas_satisfaccion: List[str] = ["satisfaccion_trabajo", "satisfaccion_ambiente"],
    pesos: Optional[List[float]] = None
) -> pd.DataFrame:
    """
    Crea un índice de satisfacción basado en varias medidas.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con las columnas necesarias.
    columnas_satisfaccion : List[str], optional
        Lista de columnas que miden satisfacción.
    pesos : List[float], optional
        Lista de pesos para cada columna de satisfacción.
        Si es None, todas las columnas tendrán el mismo peso.

    Returns
    -------
    pd.DataFrame
        DataFrame con la nueva columna 'indice_satisfaccion'.

    Examples
    --------
    >>> # Crear datos dummy para demostración
    >>> import pandas as pd
    >>> import numpy as np
    >>> np.random.seed(42)
    >>> df = pd.DataFrame({
    ...     'satisfaccion_trabajo': [3, 4, 2, 5, 1],
    ...     'satisfaccion_ambiente': [4, 3, 2, 4, 3],
    ...     'satisfaccion_salario': [2, 3, 1, 4, 2]
    ... })
    >>> # Crear índice de satisfacción
    >>> df_con_indice = crear_indice_satisfaccion(
    ...     df, 
    ...     columnas_satisfaccion=['satisfaccion_trabajo', 'satisfaccion_ambiente', 'satisfaccion_salario'],
    ...     pesos=[0.5, 0.3, 0.2]
    ... )
    >>> print(df_con_indice)
    """
    result = df.copy()
    
    # Verificar que las columnas existen
    for col in columnas_satisfaccion:
        if col not in result.columns:
            raise ValueError(f"Columna {col} no encontrada en el DataFrame")
    
    # Si no se proporcionan pesos, asignar el mismo peso a cada columna
    if pesos is None:
        pesos = [1.0 / len(columnas_satisfaccion)] * len(columnas_satisfaccion)
    
    # Verificar que hay tantos pesos como columnas
    if len(pesos) != len(columnas_satisfaccion):
        raise ValueError("La cantidad de pesos debe ser igual a la cantidad de columnas")
    
    # Verificar que los pesos suman 1
    if abs(sum(pesos) - 1.0) > 1e-10:
        raise ValueError("La suma de los pesos debe ser 1")
    
    # Calcular el índice ponderado
    result['indice_satisfaccion'] = 0
    
    for col, peso in zip(columnas_satisfaccion, pesos):
        result['indice_satisfaccion'] += result[col] * peso
    
    # Redondear a 2 decimales
    result['indice_satisfaccion'] = result['indice_satisfaccion'].round(2)
    
    return result


def crear_variables_dummy(
    df: pd.DataFrame, columnas: List[str], drop_first: bool = True
) -> pd.DataFrame:
    """
    Crea variables dummy a partir de variables categóricas.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con las columnas a convertir.
    columnas : List[str]
        Lista de columnas categóricas.
    drop_first : bool, optional
        Si es True, elimina la primera categoría para evitar multicolinealidad.
        Por defecto es True.

    Returns
    -------
    pd.DataFrame
        DataFrame con las nuevas columnas dummy.

    Examples
    --------
    >>> # Crear datos dummy para demostración
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'departamento': ['Ventas', 'Marketing', 'IT', 'Ventas', 'IT'],
    ...     'ciudad': ['Madrid', 'Barcelona', 'Madrid', 'Valencia', 'Barcelona']
    ... })
    >>> # Crear variables dummy
    >>> df_con_dummies = crear_variables_dummy(
    ...     df, columnas=['departamento', 'ciudad']
    ... )
    >>> print(df_con_dummies)
    """
    result = df.copy()
    
    # Verificar que las columnas existen
    for col in columnas:
        if col not in result.columns:
            raise ValueError(f"Columna {col} no encontrada en el DataFrame")
    
    # Crear variables dummy para cada columna
    for col in columnas:
        # Crear dummies
        dummies = pd.get_dummies(result[col], prefix=col, drop_first=drop_first)
        
        # Añadir al DataFrame
        result = pd.concat([result, dummies], axis=1)
    
    return result


def crear_flags_riesgo(
    df: pd.DataFrame,
    columnas_satisfaccion: List[str] = ["satisfaccion_trabajo", "satisfaccion_ambiente"],
    columna_salario: str = "salario",
    columna_antiguedad: str = "antiguedad"
) -> pd.DataFrame:
    """
    Crea flags binarios que indican riesgo de abandono.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con las columnas necesarias.
    columnas_satisfaccion : List[str], optional
        Lista de columnas de satisfacción.
    columna_salario : str, optional
        Nombre de la columna de salario.
    columna_antiguedad : str, optional
        Nombre de la columna de antigüedad en la empresa.

    Returns
    -------
    pd.DataFrame
        DataFrame con nuevas columnas de flags de riesgo.

    Examples
    --------
    >>> # Crear datos dummy para demostración
    >>> import pandas as pd
    >>> import numpy as np
    >>> np.random.seed(42)
    >>> df = pd.DataFrame({
    ...     'satisfaccion_trabajo': [3, 4, 2, 5, 1],
    ...     'satisfaccion_ambiente': [4, 3, 2, 4, 3],
    ...     'salario': [50000, 60000, 45000, 70000, 48000],
    ...     'antiguedad': [1, 5, 2, 7, 1]
    ... })
    >>> # Crear flags de riesgo
    >>> df_con_flags = crear_flags_riesgo(df)
    >>> print(df_con_flags)
    """
    result = df.copy()
    
    # Verificar que las columnas existen
    required_columns = columnas_satisfaccion + [columna_salario, columna_antiguedad]
    for col in required_columns:
        if col not in result.columns:
            raise ValueError(f"Columna {col} no encontrada en el DataFrame")
    
    # 1. Crear flag de baja satisfacción
    result['satisfaccion_promedio'] = result[columnas_satisfaccion].mean(axis=1)
    result['flag_baja_satisfaccion'] = np.where(result['satisfaccion_promedio'] < 3, 1, 0)
    
    # 2. Crear flag de salario bajo
    salario_promedio = result[columna_salario].mean()
    result['flag_salario_bajo'] = np.where(result[columna_salario] < salario_promedio, 1, 0)
    
    # 3. Crear flag de empleado nuevo (menos de 2 años)
    result['flag_empleado_nuevo'] = np.where(result[columna_antiguedad] < 2, 1, 0)
    
    # 4. Crear score de riesgo como suma de flags
    result['score_riesgo'] = (
        result['flag_baja_satisfaccion'] + 
        result['flag_salario_bajo'] + 
        result['flag_empleado_nuevo']
    )
    
    return result


def seleccionar_mejores_caracteristicas(
    df: pd.DataFrame, 
    columna_objetivo: str, 
    k: int = 5, 
    excluir_columnas: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Selecciona las k mejores características usando ANOVA F-value.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con las características y la variable objetivo.
    columna_objetivo : str
        Nombre de la columna objetivo.
    k : int, optional
        Número de características a seleccionar.
        Por defecto es 5.
    excluir_columnas : List[str], optional
        Lista de columnas a excluir de la selección.

    Returns
    -------
    pd.DataFrame
        DataFrame con las k mejores características y la columna objetivo.

    Examples
    --------
    >>> # Crear datos dummy para demostración
    >>> import pandas as pd
    >>> import numpy as np
    >>> np.random.seed(42)
    >>> df = pd.DataFrame({
    ...     'var1': np.random.rand(100),
    ...     'var2': np.random.rand(100),
    ...     'var3': np.random.rand(100),
    ...     'var4': np.random.rand(100),
    ...     'var5': np.random.rand(100),
    ...     'objetivo': np.random.randint(0, 2, 100)
    ... })
    >>> # Seleccionar mejores características
    >>> df_seleccionado = seleccionar_mejores_caracteristicas(
    ...     df, columna_objetivo='objetivo', k=3
    ... )
    >>> print(df_seleccionado.columns)
    """
    # Verificar que la columna objetivo existe
    if columna_objetivo not in df.columns:
        raise ValueError(f"Columna objetivo {columna_objetivo} no encontrada en el DataFrame")
    
    # Crear copia para no modificar el original
    result = df.copy()
    
    # Determinar columnas a excluir
    if excluir_columnas is None:
        excluir_columnas = []
    
    # Añadir la columna objetivo a las columnas a excluir
    excluir_columnas = excluir_columnas + [columna_objetivo]
    
    # Seleccionar las columnas para el análisis
    columnas_caracteristicas = [col for col in result.columns if col not in excluir_columnas]
    
    # Verificar que hay suficientes columnas
    if len(columnas_caracteristicas) <= k:
        return result[columnas_caracteristicas + [columna_objetivo]]
    
    # Preparar X e y
    X = result[columnas_caracteristicas]
    y = result[columna_objetivo]
    
    # Convertir todas las columnas a numéricas para el algoritmo
    X_numeric = X.copy()
    
    for col in X.columns:
        if not pd.api.types.is_numeric_dtype(X[col]):
            # Para columnas categóricas, las convertimos a códigos numéricos
            X_numeric[col] = pd.Categorical(X[col]).codes
    
    # Aplicar selección de características
    selector = SelectKBest(f_classif, k=k)
    _ = selector.fit_transform(X_numeric, y)
    
    # Obtener las columnas seleccionadas
    selected_indices = selector.get_support(indices=True)
    selected_columns = [columnas_caracteristicas[i] for i in selected_indices]
    
    # Devolver el DataFrame con las características seleccionadas y la columna objetivo
    return result[selected_columns + [columna_objetivo]]


# Datos de ejemplo para que los estudiantes puedan probar rápidamente
def get_sample_data() -> pd.DataFrame:
    """
    Crea un DataFrame de ejemplo para realizar pruebas de feature engineering.
    
    Returns
    -------
    pd.DataFrame
        DataFrame con datos de ejemplo adecuados para feature engineering.
        
    Examples
    --------
    >>> # Obtener datos de ejemplo
    >>> df_sample = get_sample_data()
    >>> print(df_sample.head())
    """
    np.random.seed(42)
    
    # Crear un DataFrame con datos de ejemplo
    n_samples = 100
    
    data = {
        'id': list(range(1, n_samples + 1)),
        'edad': np.random.randint(18, 65, n_samples),
        'salario': np.random.randint(30000, 80000, n_samples),
        'antiguedad': np.random.randint(0, 15, n_samples),
        'departamento': np.random.choice(['Ventas', 'Marketing', 'IT', 'RRHH', 'Finanzas'], n_samples),
        'ciudad': np.random.choice(['Madrid', 'Barcelona', 'Valencia', 'Sevilla'], n_samples),
        'satisfaccion_trabajo': np.random.randint(1, 6, n_samples),
        'satisfaccion_ambiente': np.random.randint(1, 6, n_samples),
        'satisfaccion_salario': np.random.randint(1, 6, n_samples),
        'abandono': np.random.choice([0, 1], n_samples, p=[0.8, 0.2])  # Variable objetivo: 0=No abandono, 1=Abandono
    }
    
    # Correlación artificial con la variable objetivo
    # Las personas con baja satisfacción tienen mayor probabilidad de abandono
    df = pd.DataFrame(data)
    
    # Ajustar la probabilidad de abandono basada en la satisfacción
    for i in range(n_samples):
        # Si la satisfacción promedio es baja (< 3) y el abandono era 0, hay 50% de cambiar a 1
        if (df.loc[i, 'satisfaccion_trabajo'] + df.loc[i, 'satisfaccion_ambiente'] + df.loc[i, 'satisfaccion_salario'])/3 < 3:
            if df.loc[i, 'abandono'] == 0 and np.random.random() < 0.5:
                df.loc[i, 'abandono'] = 1
        
        # Si el salario es bajo y el abandono era 0, hay 40% de cambiar a 1
        if df.loc[i, 'salario'] < 45000:
            if df.loc[i, 'abandono'] == 0 and np.random.random() < 0.4:
                df.loc[i, 'abandono'] = 1
                
        # Si la antigüedad es baja y el abandono era 0, hay 30% de cambiar a 1
        if df.loc[i, 'antiguedad'] < 2:
            if df.loc[i, 'abandono'] == 0 and np.random.random() < 0.3:
                df.loc[i, 'abandono'] = 1
    
    return df 