"""Config file para el preprocesamiento."""
from pathlib import Path

# Obtener la ruta absoluta del directorio del proyecto
ROOT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = ROOT_DIR / "data" / "raw"

# Ruta absoluta para el archivo AFP
RUTA_EMPLOYEE_SURVEY = str(DATA_DIR / "employee_survey_data.csv")
RUTA_GENERAL = str(DATA_DIR / "general_data.csv")

# Columna de unión
EMPLOYEE_COLUMN_JOIN = str("EmployeeID")
MEAN_COLUMNS = [
    "EnvironmentSatisfaction",
    "JobSatisfaction",
    "WorkLifeBalance",
]
COLUMN_AVERAGE_EMPLOYEE_SATISFACTION = "average_employee_satisfaction"