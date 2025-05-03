"""Configuración para el preprocesamiento de datos del proyecto de metodología para Data Science.

Este módulo define rutas importantes y configuraciones clave necesarias para la carga y manipulación
de datos, incluyendo la unión de archivos y el cálculo de variables agregadas.
"""
from pathlib import Path

# Obtener la ruta absoluta del directorio del proyecto.
# Usado como base para construir rutas a los datos crudos.
ROOT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = ROOT_DIR / "data" / "raw"

# Rutas absolutas para los archivos de datos.
# RUTA_EMPLOYEE_SURVEY: Ruta al archivo de la encuesta a empleados, usado para cargar datos de satisfacción.
# RUTA_GENERAL: Ruta al archivo de datos generales, usado para cargar información general de empleados.
RUTA_EMPLOYEE_SURVEY = DATA_DIR / "employee_survey_data.csv"
RUTA_GENERAL = DATA_DIR / "general_data.csv"

# Validar existencia de archivos antes de asignar las rutas.
if not RUTA_EMPLOYEE_SURVEY.exists():
    raise FileNotFoundError(f"No se encontró el archivo: {RUTA_EMPLOYEE_SURVEY}")
if not RUTA_GENERAL.exists():
    raise FileNotFoundError(f"No se encontró el archivo: {RUTA_GENERAL}")

# Convertir rutas a string para uso posterior (por ejemplo, en pandas).
RUTA_EMPLOYEE_SURVEY = str(RUTA_EMPLOYEE_SURVEY)
RUTA_GENERAL = str(RUTA_GENERAL)

# Columna clave para la unión de datasets.
# EMPLOYEE_COLUMN_JOIN: Usada como clave primaria para unir los archivos de datos.
EMPLOYEE_COLUMN_JOIN = "EmployeeID"

# Columnas de las cuales se calculará el promedio de satisfacción del empleado.
# MEAN_COLUMNS: Lista de columnas de satisfacción que serán promediadas para crear una nueva variable.
MEAN_COLUMNS = [
    "EnvironmentSatisfaction",
    "JobSatisfaction",
    "WorkLifeBalance",
]

# Validación: asegurar que MEAN_COLUMNS no esté vacía.
if not MEAN_COLUMNS:
    raise ValueError("La lista MEAN_COLUMNS no debe estar vacía.")

# Nombre de la columna resultante del promedio de satisfacción.
# COLUMN_AVERAGE_EMPLOYEE_SATISFACTION: Nombre asignado a la nueva variable agregada.
COLUMN_AVERAGE_EMPLOYEE_SATISFACTION = "average_employee_satisfaction"