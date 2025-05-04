"""Este módulo contiene un método generar el dataset de feedback de los jefes."""

from src.features.encuesta_empleados import procesar_encuesta_empleados
from src.preprocessing import read_employee_files, read_feedback_files
from src.preprocessing.config import (
    COLUMN_AVERAGE_MANAGER_FEEDBACK,
    EMPLOYEE_COLUMN_JOIN,
    MEAN_COLUMNS_FEEDBACK,
    RUTA_MANAGER_SURVEY_PATH,
)


def procesar_feedback_jefes():
    """
    Carga los datos del dataset generado por el grupo 1.

    Luego lo combina con los datos de manager_survey_data.

    Realiza los siguientes pasos:
    1. Llama al método final del grupo 1
    2. Carga el dataset de manager_survey_data.
    3. Hace merge con el dataset de manager_survey_data.
    4. Calcula una nueva columna de promedio de feedback del jefe
    a partir de columnas definidas.
    5. Devuelve el DataFrame combinado.

    Returns:
        df_average_manag_fb: DataFrame combinado con la data de manager_survey_data.
    """
    # Paso 1
    df_encuesta_empleados = procesar_encuesta_empleados()

    # Paso 2
    df_manager_survey_data = read_employee_files.read_file(RUTA_MANAGER_SURVEY_PATH)

    # Paso 3
    df_merge_employee_manager = read_feedback_files.merge_dataframe(
        df_encuesta_empleados, df_manager_survey_data, EMPLOYEE_COLUMN_JOIN
    )

    # Paso 4
    df_average_manag_fb = read_employee_files.mean_columns(
        df_merge_employee_manager,
        COLUMN_AVERAGE_MANAGER_FEEDBACK,
        MEAN_COLUMNS_FEEDBACK,
    )

    # Paso 5
    return df_average_manag_fb
