## Grupo 1 - Unión de Dataset Encuesta de Empelados

El Grupo 1 fue responsable de unir los archivos `employee_survey_data.csv` y `general_data.csv`, los cuales se ubicaron dentro del directorio `data/raw/`.

### Archivos utilizados
- `data/raw/employee_survey_data.csv`
- `data/raw/general_data.csv`

### Módulos desarrollados
Los siguientes scripts fueron desarrollados dentro del directorio `src/preprocessing/` y `src/features/`:

#### 1. `config.py`
Este archivo define:
- Las rutas absolutas hacia los archivos de entrada.
- La columna clave para realizar el merge (`EmployeeID`).
- Las columnas que serán utilizadas para calcular un promedio de satisfacción del empleado.

#### 2. `read_employee_files.py`
Este archivo contiene tres funciones principales:
- `read_file(file: str)`: Lee un archivo CSV desde la ruta especificada.
- `merge_files(file1: str, file2: str, column_join: str)`: Une dos archivos en base a una columna común.
- `mean_columns(df: pd.DataFrame, columnaName: str, columns: list)`: Calcula el promedio por fila de un conjunto de columnas numéricas.

### Ejemplo de uso que se puede aplicar para los otros grupos al momento de leer archivos y unirlos.

```python
import os
os.chdir("..")
from src.preprocessing.config import RUTA_EMPLOYEE_SURVEY, RUTA_GENERAL, MEAN_COLUMNS, COLUMN_AVERAGE_EMPLOYEE_SATISFACTION

from src.preprocessing import read_employee_files as mf

df = mf.merge_files(RUTA_GENERAL, RUTA_EMPLOYEE_SURVEY, "EmployeeID")

ndf = mf.mean_columns(df, COLUMN_AVERAGE_EMPLOYEE_SATISFACTION, MEAN_COLUMNS)
ndf.head(3)
```

#### 3. `encuesta_empleados.py`
Este módulo centraliza el flujo completo de integración de datos, utilizando internamente los métodos definidos en `read_employee_files.py` y las rutas de `config.py`.

Contiene una única función pública:
- `procesar_encuesta_empleados()`: Realiza la lectura, combinación de archivos y cálculo de promedio de satisfacción en un solo paso.

### Resultado
El resultado fue un `DataFrame` enriquecido con información combinada y una nueva columna calculada llamada `average_employee_satisfaction`.

#### 3. `encuesta_empleados.py`
Este módulo centraliza el flujo completo de integración de datos, utilizando internamente los métodos definidos en `read_employee_files.py` y las rutas de `config.py`.

Contiene una única función pública:
- `procesar_encuesta_empleados()`: Realiza la lectura, combinación de archivos y cálculo de promedio de satisfacción en un solo paso.

### Ejemplo alternativo de uso e input para el GRUPO 2

```python
from src.features.encuesta_empleados import procesar_encuesta_empleados

# Ejecutar procesamiento completo
df = procesar_encuesta_empleados()
df.head(3)
```

#### Resultado de la ejecución (head de los primeros 3 registros)

| EmployeeID | Age | Attrition | ... | EnvironmentSatisfaction | JobSatisfaction | WorkLifeBalance | average_employee_satisfaction |
|------------|-----|-----------|-----|--------------------------|------------------|------------------|-------------------------------|
| 1          | 41  | Yes       | ... | 2                        | 4                | 1                | 2.33                          |
| 2          | 49  | No        | ... | 3                        | 2                | 3                | 2.67                          |
| 3          | 37  | No        | ... | 4                        | 3                | 2                | 3.00                          |
