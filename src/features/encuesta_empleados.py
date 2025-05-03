

from src.preprocessing.config import (
    RUTA_EMPLOYEE_SURVEY,
    RUTA_GENERAL,
    MEAN_COLUMNS,
    COLUMN_AVERAGE_EMPLOYEE_SATISFACTION,
    EMPLOYEE_COLUMN_JOIN,
)
from src.preprocessing import read_employee_files as mf

def procesar_encuesta_empleados():
    """
    Carga y combina los datos de los archivos de encuesta y datos generales de empleados.

    Realiza los siguientes pasos:
    1. Lee ambos archivos CSV usando rutas definidas en `config.py`.
    2. Une los DataFrames por la columna `EmployeeID`.
    3. Calcula una nueva columna de promedio de satisfacción del empleado a partir de columnas definidas.

    Returns:
        pd.DataFrame: DataFrame combinado y enriquecido con la nueva columna de satisfacción.
    """
    df = mf.merge_files(RUTA_GENERAL, RUTA_EMPLOYEE_SURVEY, EMPLOYEE_COLUMN_JOIN)
    df = mf.mean_columns(df, COLUMN_AVERAGE_EMPLOYEE_SATISFACTION, MEAN_COLUMNS)
    return df