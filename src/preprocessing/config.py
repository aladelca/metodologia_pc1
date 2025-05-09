"""Configuración para el preprocesamiento de datos.

Este módulo define rutas importantes y configuraciones clave.
Estas son necesarias para la carga y manipulación de datos.
Incluyendo la unión de archivos y el cálculo de variables agregadas.
"""

from pathlib import Path

# Obtener la ruta absoluta del directorio del proyecto.
# Usado como base para construir rutas a los datos crudos.
ROOT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = ROOT_DIR / "data" / "raw"
CLEAN_DATA_DIR = ROOT_DIR / "data" / "clean"

# Rutas absolutas para los archivos de datos.
# RUTA_EMPLOYEE_SURVEY_PATH: Ruta al archivo de la encuesta a empleados.
# RUTA_GENERAL_PATH: Ruta al archivo de datos generales.
# RUTA_MANAGER_SURVEY_PATH: Ruta al archivo de feedback de los jefes.
RUTA_EMPLOYEE_SURVEY_PATH = DATA_DIR / "employee_survey_data.csv"
RUTA_GENERAL_PATH = DATA_DIR / "general_data.csv"
RUTA_MANAGER_SURVEY_PATH = DATA_DIR / "manager_survey_data.csv"

# Validar existencia de archivos antes de asignar las rutas.
if not RUTA_EMPLOYEE_SURVEY_PATH.exists():
    raise FileNotFoundError(f"No se encontró el archivo: {RUTA_EMPLOYEE_SURVEY_PATH}")
if not RUTA_GENERAL_PATH.exists():
    raise FileNotFoundError(f"No se encontró el archivo: {RUTA_GENERAL_PATH}")

# Convertir rutas a string para uso posterior (por ejemplo, en pandas).
RUTA_EMPLOYEE_SURVEY = str(RUTA_EMPLOYEE_SURVEY_PATH)
RUTA_GENERAL = str(RUTA_GENERAL_PATH)
RUTA_ENCODED_DATA = str(CLEAN_DATA_DIR / "encoded_data.csv")

# Columna clave para la unión de datasets.
# EMPLOYEE_COLUMN_JOIN: Usada como clave primaria para unir los archivos de datos.
EMPLOYEE_COLUMN_JOIN = "EmployeeID"

# Columnas de las cuales se calculará el promedio
# de satisfacción del empleado.
# MEAN_COLUMNS: Lista de columnas de satisfacción que
# serán promediadas para crear una nueva variable.
MEAN_COLUMNS = [
    "EnvironmentSatisfaction",
    "JobSatisfaction",
    "WorkLifeBalance",
]

# Columnas de las cuales se calculará el promedio de
# feedback de los jefes.
# MEAN_COLUMNS_FEEDBACK: Lista de columnas de feedback
# que serán promediadas para crear una nueva variable.
MEAN_COLUMNS_FEEDBACK = ["JobInvolvement", "PerformanceRating"]

# Validación: asegurar que MEAN_COLUMNS no esté vacía.
if not MEAN_COLUMNS:
    raise ValueError("La lista MEAN_COLUMNS no debe estar vacía.")

# Nombre de la columna resultante del promedio de satisfacción.
# COLUMN_AVERAGE_EMPLOYEE_SATISFACTION: Nombre asignado a la
# nueva variable agregada en el paso 1.
COLUMN_AVERAGE_EMPLOYEE_SATISFACTION = "average_employee_satisfaction"

# Nombre de la columna resultante del promedio de feedback.
# COLUMN_AVERAGE_MANAGER_FEEDBACK: Nombre asignado a la
# nueva variable agregada en el paso 2
COLUMN_AVERAGE_MANAGER_FEEDBACK = "average_manager_feedback"
