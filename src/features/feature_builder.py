"""
Módulo para la creación de características (feature engineering).

Este módulo contiene funciones para crear nuevas características a partir
de datos existentes. Sirve como guía para estudiantes sobre cómo realizar
ingeniería de características en problemas de recursos humanos.
"""

from typing import List, Optional

import numpy as np
import pandas as pd


def get_sample_data() -> pd.DataFrame:
    """
    Crea un conjunto de datos de ejemplo para prácticas de feature engineering.

    Returns:
        pd.DataFrame: DataFrame con datos sintéticos de empleados.
    """
    # Crear datos aleatorios para 100 empleados
    np.random.seed(42)
    n = 100

    # Datos básicos
    ids = np.arange(1, n + 1)
    edades = np.random.randint(22, 60, n)
    salarios = np.random.randint(800, 5000, n)
    antiguedad = np.random.randint(0, 20, n)

    # Departamentos y ciudades
    departamentos = np.random.choice(
        ["IT", "RRHH", "Marketing", "Ventas", "Finanzas"], n
    )
    ciudades = np.random.choice(["Lima", "Arequipa", "Trujillo", "Cusco"], n)

    # Niveles de satisfacción (1-5)
    satisfaccion_trabajo = np.random.randint(1, 6, n)
    satisfaccion_ambiente = np.random.randint(1, 6, n)
    satisfaccion_salario = np.random.randint(1, 6, n)

    # Variable objetivo: abandono (binaria)
    abandono = np.random.choice([0, 1], n, p=[0.8, 0.2])

    # Crear DataFrame
    df = pd.DataFrame(
        {
            "id": ids,
            "edad": edades,
            "salario": salarios,
            "antiguedad": antiguedad,
            "departamento": departamentos,
            "ciudad": ciudades,
            "satisfaccion_trabajo": satisfaccion_trabajo,
            "satisfaccion_ambiente": satisfaccion_ambiente,
            "satisfaccion_salario": satisfaccion_salario,
            "abandono": abandono,
        }
    )

    return df


def crear_categorias_edad(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea categorías de edad a partir de la columna 'edad'.

    Ejemplo:
    ```python
    import pandas as pd

    # Crear DataFrame de ejemplo
    df = pd.DataFrame({
        'edad': [25, 35, 45, 55, 65]
    })

    # Aplicar función
    df_result = crear_categorias_edad(df)
    print(df_result)
    ```

    Args:
        df (pd.DataFrame): DataFrame con la columna 'edad'.

    Returns:
        pd.DataFrame: DataFrame con la nueva columna 'grupo_edad'.
    """
    # Crear una copia para no modificar el original
    result = df.copy()

    # Crear la columna de categorías
    bins = [0, 18, 30, 50, 65, 100]
    labels = ["Menor", "Joven", "Adulto", "Senior", "Jubilado"]

    result["grupo_edad"] = pd.cut(result["edad"], bins=bins, labels=labels, right=False)

    return result


def calcular_ratio_salario_edad(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula el ratio entre salario y edad.

    Ejemplo:
    ```python
    import pandas as pd

    # Crear DataFrame de ejemplo
    df = pd.DataFrame({
        'edad': [25, 30, 35, 40, 45],
        'salario': [2500, 3000, 3500, 4000, 4500]
    })

    # Aplicar función
    df_result = calcular_ratio_salario_edad(df)
    print(df_result)
    ```

    Args:
        df (pd.DataFrame): DataFrame con las columnas 'salario' y 'edad'.

    Returns:
        pd.DataFrame: DataFrame con la nueva columna 'ratio_salario_edad'.
    """
    # Crear una copia para no modificar el original
    result = df.copy()

    # Asegurar que los valores son numéricos
    result["salario"] = pd.to_numeric(result["salario"], errors="coerce")
    result["edad"] = pd.to_numeric(result["edad"], errors="coerce")

    # Calcular el ratio
    result["ratio_salario_edad"] = (result["salario"] / result["edad"]).round(2)

    return result


def crear_indice_satisfaccion(
    df: pd.DataFrame,
    columnas_satisfaccion: Optional[List[str]] = None,
    pesos: Optional[List[float]] = None,
) -> pd.DataFrame:
    """
    Crea un índice de satisfacción a partir de múltiples columnas.

    Ejemplo:
    ```python
    import pandas as pd

    # Crear DataFrame de ejemplo
    df = pd.DataFrame({
        'satisfaccion_trabajo': [4, 3, 5, 2, 1],
        'satisfaccion_ambiente': [3, 4, 5, 3, 2],
        'satisfaccion_salario': [2, 3, 4, 2, 1]
    })

    # Aplicar función con pesos personalizados
    cols = ['satisfaccion_trabajo', 'satisfaccion_ambiente', 'satisfaccion_salario']
    pesos = [0.5, 0.3, 0.2]
    df_result = crear_indice_satisfaccion(df, columnas_satisfaccion=cols, pesos=pesos)
    print(df_result)
    ```

    Args:
        df (pd.DataFrame): DataFrame con columnas de satisfacción.
        columnas_satisfaccion (Optional[List[str]], optional):
            Lista de columnas a incluir en el índice.
            Por defecto: ['satisfaccion_trabajo', 'satisfaccion_ambiente'].
        pesos (Optional[List[float]], optional):
            Lista de pesos para cada columna.
            Por defecto: pesos iguales para todas las columnas.

    Returns:
        pd.DataFrame: DataFrame con la nueva columna 'indice_satisfaccion'.
    """
    # Crear una copia para no modificar el original
    result = df.copy()

    # Valores por defecto
    if columnas_satisfaccion is None:
        columnas_satisfaccion = [
            "satisfaccion_trabajo",
            "satisfaccion_ambiente",
            "satisfaccion_salario",
        ]

    # Verificar que las columnas existen
    columnas_existentes = [
        col for col in columnas_satisfaccion if col in result.columns
    ]

    if not columnas_existentes:
        raise ValueError(
            f"Ninguna de las columnas {columnas_satisfaccion} existe en el DataFrame"
        )

    # Pesos por defecto (iguales para todas las columnas)
    if pesos is None:
        pesos = [1 / len(columnas_existentes)] * len(columnas_existentes)

    # Ajustar los pesos si hay menos columnas existentes que las solicitadas
    if len(columnas_existentes) < len(columnas_satisfaccion):
        # Obtener índices de las columnas existentes
        indices = [columnas_satisfaccion.index(col) for col in columnas_existentes]
        # Filtrar los pesos
        pesos = [pesos[i] for i in indices]
        # Normalizar para que sumen 1
        pesos = [p / sum(pesos) for p in pesos]

    # Convertir las columnas a numéricas
    for col in columnas_existentes:
        result[col] = pd.to_numeric(result[col], errors="coerce")

    # Calcular el índice de satisfacción ponderado
    indice = pd.Series(0.0, index=result.index)
    for col, peso in zip(columnas_existentes, pesos):
        indice += result[col] * peso

    result["indice_satisfaccion"] = indice.round(2)

    return result


def crear_variables_dummy(
    df: pd.DataFrame, columnas: Optional[List[str]] = None, drop_first: bool = True
) -> pd.DataFrame:
    """
    Crea variables dummy a partir de variables categóricas.

    Ejemplo:
    ```python
    import pandas as pd

    # Crear DataFrame de ejemplo
    df = pd.DataFrame({
        'departamento': ['IT', 'RRHH', 'Marketing', 'IT', 'Ventas'],
        'ciudad': ['Lima', 'Arequipa', 'Lima', 'Cusco', 'Lima']
    })

    # Aplicar función
    df_result = crear_variables_dummy(df, columnas=['departamento', 'ciudad'])
    print(df_result)
    ```

    Args:
        df (pd.DataFrame): DataFrame con variables categóricas.
        columnas (Optional[List[str]], optional):
            Lista de columnas categóricas para convertir a dummy.
            Por defecto: ['departamento', 'ciudad'].
        drop_first (bool, optional): Si es True, elimina la primera categoría.

    Returns:
        pd.DataFrame: DataFrame con nuevas columnas dummy.
    """
    # Crear una copia para no modificar el original
    result = df.copy()

    # Valores por defecto
    if columnas is None:
        columnas = ["departamento", "ciudad"]

    # Verificar que las columnas existen
    columnas_existentes = [col for col in columnas if col in result.columns]

    if not columnas_existentes:
        raise ValueError(f"Ninguna de las columnas {columnas} existe en el DataFrame")

    # Crear variables dummy para cada columna
    for col in columnas_existentes:
        # Crear dummies
        dummies = pd.get_dummies(result[col], prefix=col, drop_first=drop_first)
        # Concatenar con el DataFrame original
        result = pd.concat([result, dummies], axis=1)

    return result


def crear_flags_riesgo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea flags de riesgo y un score global de riesgo.

    Ejemplo:
    ```python
    import pandas as pd

    # Crear DataFrame de ejemplo
    df = pd.DataFrame({
        'satisfaccion_trabajo': [2, 4, 3, 1, 5],
        'salario': [1200, 3500, 2000, 1000, 4000],
        'antiguedad': [0, 5, 2, 1, 10]
    })

    # Aplicar función
    df_result = crear_flags_riesgo(df)
    print(df_result)
    ```

    Args:
        df (pd.DataFrame): DataFrame con las columnas necesarias.

    Returns:
        pd.DataFrame: DataFrame con nuevas columnas de flags y score de riesgo.
    """
    # Crear una copia para no modificar el original
    result = df.copy()

    # Flag 1: Baja satisfacción (menor a 3 en satisfacción trabajo)
    if "satisfaccion_trabajo" in result.columns:
        # Convertir a numérico
        result["satisfaccion_trabajo"] = pd.to_numeric(
            result["satisfaccion_trabajo"], errors="coerce"
        )
        result["flag_baja_satisfaccion"] = (result["satisfaccion_trabajo"] < 3).astype(
            int
        )
    else:
        result["flag_baja_satisfaccion"] = 0

    # Flag 2: Salario bajo (menor a 1500)
    if "salario" in result.columns:
        # Convertir a numérico
        result["salario"] = pd.to_numeric(result["salario"], errors="coerce")
        result["flag_salario_bajo"] = (result["salario"] < 1500).astype(int)
    else:
        result["flag_salario_bajo"] = 0

    # Flag 3: Empleado nuevo (menos de 1 año de antigüedad)
    if "antiguedad" in result.columns:
        # Convertir a numérico
        result["antiguedad"] = pd.to_numeric(result["antiguedad"], errors="coerce")
        result["flag_empleado_nuevo"] = (result["antiguedad"] < 1).astype(int)
    else:
        result["flag_empleado_nuevo"] = 0

    # Calcular score global de riesgo (suma de flags)
    result["score_riesgo"] = (
        result["flag_baja_satisfaccion"]
        + result["flag_salario_bajo"]
        + result["flag_empleado_nuevo"]
    )

    return result


def seleccionar_mejores_caracteristicas(
    df: pd.DataFrame, columna_objetivo: str = "abandono", k: int = 5
) -> pd.DataFrame:
    """
    Selecciona las k mejores características para predecir la columna objetivo.

    Ejemplo:
    ```python
    import pandas as pd
    import numpy as np

    # Crear DataFrame de ejemplo con múltiples columnas
    np.random.seed(42)
    df = pd.DataFrame({
        'feature1': np.random.rand(100),
        'feature2': np.random.rand(100),
        'feature3': np.random.rand(100),
        'feature4': np.random.rand(100),
        'feature5': np.random.rand(100),
        'abandono': np.random.choice([0, 1], 100)
    })

    # Seleccionar las 3 mejores características
    df_result = seleccionar_mejores_caracteristicas(
        df, columna_objetivo='abandono', k=3
    )
    print(df_result.columns)
    ```

    Args:
        df (pd.DataFrame): DataFrame con características y columna objetivo.
        columna_objetivo (str, optional): Nombre de la columna objetivo.
        k (int, optional): Número de características a seleccionar.

    Returns:
        pd.DataFrame: DataFrame con las k mejores características y la columna objetivo.
    """
    # Importar dentro de la función para no depender de scikit-learn en todo el módulo
    from sklearn.feature_selection import SelectKBest, f_classif

    # Crear una copia para no modificar el original
    result = df.copy()

    # Verificar que la columna objetivo existe
    if columna_objetivo not in result.columns:
        raise ValueError(
            f"La columna objetivo '{columna_objetivo}' no existe en el DataFrame"
        )

    # Separar características y objetivo
    X = result.drop(columns=[columna_objetivo])
    y = result[columna_objetivo]

    # Eliminar columnas no numéricas y manejar valores faltantes
    X = X.select_dtypes(include=["number"]).fillna(0)

    if X.empty:
        raise ValueError("No hay columnas numéricas en el DataFrame")

    # Ajustar k si es mayor que el número de columnas disponibles
    k = min(k, X.shape[1])

    # Seleccionar las mejores características
    selector = SelectKBest(f_classif, k=k)
    selector.fit_transform(X, y)

    # Obtener los nombres de las columnas seleccionadas
    mask = selector.get_support()
    selected_features = X.columns[mask].tolist()

    # Crear DataFrame con las columnas seleccionadas y la columna objetivo
    return result[selected_features + [columna_objetivo]]
