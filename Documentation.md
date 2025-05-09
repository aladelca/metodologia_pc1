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

## ------------------------------------------------------------------------------------------------
## ------------------------------------------------------------------------------------------------
## ------------------------------------------------------------------------------------------------
## Grupo 2 - Unir datasets con datos de feedback de jefes

El Grupo 2 fue responsable de unir el dataset procesado por el Grupo 1 con la data del archivo `manager_survey_data.csv`, que se ubica dentro del directorio `data/raw/`. Adicionalmente, agregamos una columna llamada `average_manager_feedback` con el promedio de las columnas de feedback.

### Archivos utilizados
- `data/raw/manager_survey_data.csv`

### Módulos modificados
Los siguientes módulos fueron modificados dentro del directorio `src/preprocessing/` y `src/features/`:

#### 1. `config.py`
En este archivo agregamos lo siguiente:
- La ruta absoluta hacia el archivo `manager_survey_data.csv`.
- Lista de columnas de feedback que serán promediadas para crear una nueva variable.
- Nombre asignado a la nueva variable `average_manager_feedback`.

#### 2. `read_feedback_files.py`
Creamos este archivo para crear un método adicional que se requería para hacer merge.
- `merge_dataframe(df1: pd.DataFrame, df2: pd.DataFrame, column_join: str)`: Une dos DataFrame en base a una columna común.

#### 3. `read_feedback_files_test.py`
Creamos este archivo para agregar tests y validar el método creado.
- `test_merge_dataframe_success`: Verifica que la función une correctamente los archivos cuando la columna de unión existe.
- `test_merge_dataframe_missing_column`: Verifica que se lanza un error si la columna de unión no existe en los archivos.
- `test_merge_dataframe_empty_files`: Verifica que la función maneje archivos vacíos correctamente.
- `test_merge_dataframe_different_columns`: Verifica que se lanza un error si las columnas de unión no coinciden entre los archivos.
- `test_merge_dataframe_no_common_rows`: Verifica que la función maneje correctamente el caso en que no hay filas comunes entre los archivos.

#### 4. `feedback_jefes.py`
Creamos este archivo para definir el método final con el que generar el dataset final con los datos del archivo `manager_survey_data.csv` y la columna solicitada `average_manager_feedback`.
- `procesar_feedback_jefes`: Genera el dataset del grupo 1, realiza merge con el archivo `manager_survey_data.csv`, agrega la columna `average_manager_feedback` y retorna el DataFrame resultante.

### Ejemplos que pueden utilizar otros grupos para utilizar nuestros métodos

#### Ejemplo de como hacer el merge entre 2 DataFrame
```python
#Importar librerias
import os
os.chdir("..")
from src.preprocessing import read_feedback_files as rff
from src.preprocessing.config import EMPLOYEE_COLUMN_JOIN
#Hacer el merge entre df_encuesta_empleados y df_manager_survey_data
df_resultado = rff.merge_dataframe(df_encuesta_empleados,df_manager_survey_data,EMPLOYEE_COLUMN_JOIN)
df_merge_employee_manager.head(2)
```

#### Ejemplo de como llamar al método final procesar_feedback_jefes
```python
#Importar librerias
import os
os.chdir("..")
from src.features.feedback_jefes import procesar_feedback_jefes
#Llamar al metodo procesar_encuesta_empleados y asignarlo a una variable
df_feedback_jefes = procesar_feedback_jefes()
df_feedback_jefes.head(2)
```
#### Resultado de la ejecución (head de los primeros 2 registros)
EmployeeID  ... JobSatisfaction WorkLifeBalance average_manager_feedback
1           ... 3               3               3.0
2           ... 2               4               3.0

## ------------------------------------------------------------------------------------------------
## ------------------------------------------------------------------------------------------------
## ------------------------------------------------------------------------------------------------
## Grupo 3 - Limpieza de Datos y Manejo de Valores Faltantes

#### CONTINUARA!!!

## Grupo 5 - Transformación de variables categóricas con encoding

## Objetivo

Transformar las variables categóricas del dataset para que sean interpretables por algoritmos de Machine Learning, mediante las técnicas de codificación OneHotEncoder y LabelEncoder. Esto permite que el modelo entienda correctamente la información representada por texto.

---

## Identificación de Variables Categóricas

Se utilizó el siguiente comando para identificar las columnas categóricas en el DataFrame:

```python
df.select_dtypes(include=["object"]).columns.tolist()
```

---

Las variables categóricas detectadas en el dataset fueron:
- Attrition
- BusinessTravel
- Department
- EducationField
- Gender
- JobRole
- MaritalStatus
- Over18

---

## Análisis de Variables Categóricas

A continuación, se presenta el análisis de las variables categóricas presentes en el dataset, así como la decisión sobre la técnica de codificación más adecuada para cada una.

| Variable         | Tipo       | Técnica sugerida         | Justificación |
|------------------|------------|---------------------------|---------------|
| `Attrition`       | Binaria    | LabelEncoder              | Solo tiene 2 valores: `"Yes"` / `"No"`. Al ser binaria, puede codificarse como 0 y 1 sin pérdida de información. |
| `BusinessTravel`  | Nominal    | OneHotEncoder             | Tiene múltiples categorías sin un orden lógico, por lo que es mejor representarlas como variables dummy. |
| `Department`      | Nominal    | OneHotEncoder             | Las categorías como `"Sales"`, `"Research & Development"` no tienen jerarquía, por lo tanto OneHot es más apropiado. |
| `EducationField`  | Nominal    | OneHotEncoder             | Al igual que `Department`, no hay un orden implícito entre las categorías. |
| `Gender`          | Binaria    | LabelEncoder              | Tiene dos clases (`"Male"`, `"Female"`), por lo que puede codificarse fácilmente como 0 y 1. |
| `JobRole`         | Nominal    | OneHotEncoder             | Contiene múltiples roles con significados distintos pero sin orden jerárquico, ideal para codificación one-hot. |
| `MaritalStatus`   | Nominal    | OneHotEncoder             | Las categorías como `"Single"`, `"Married"` y `"Divorced"` no representan una escala ordenada. |
| `Over18`          | Binaria    | LabelEncoder               | Contiene 2 valores. |

---

## Implementación

Se implementaron dos funciones de codificación en el archivo `src/preprocessing/encoding.py`:

### 1. `apply_label_encoding(df, columns)`

Aplica codificación binaria a columnas con dos valores únicos.

```python
from sklearn.preprocessing import LabelEncoder

def apply_label_encoding(df, columns):
    df_encoded = df.copy()
    encoders = {}
    for col in columns:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df_encoded[col])
        encoders[col] = le
    return df_encoded, encoders
```

### 2. `apply_one_hot_encoding(df, columns)`

Aplica codificación one-hot a columnas nominales con múltiples categorías.

```python
def apply_one_hot_encoding(df, columns):
    df_encoded = pd.get_dummies(df, columns=columns, drop_first=False)
    return df_encoded
```

---

### Script final

Se implementó una función que contiene toda la codificación de variables en el archivo `src/features/encoding.py`:

#### 1. `encoding_variables()`

```python
  def encoding_variables():

    df_feedback_jefes = procesar_feedback_jefes()

    binary_cols = ['Attrition', 'Gender', 'Over18']
    df_encoded, label_encoders = apply_label_encoding(df_feedback_jefes, binary_cols)

    one_hot_cols = ['BusinessTravel', 'Department', 'EducationField', 'JobRole', 'MaritalStatus']
    df_encoded = apply_one_hot_encoding(df_encoded, one_hot_cols)

    df_encoded.to_csv(RUTA_ENCODED_DATA, index=False)
```

## Pruebas Unitarias

Se desarrollaron pruebas para validar el comportamiento de las funciones en el archivo `tests/preprocessing/test_encoding.py` usando `pytest`.

### Ejemplo de prueba para `apply_label_encoding`:

```python
def test_apply_label_encoding():
    df = pd.DataFrame({
        'Attrition': ['Yes', 'No'],
        'Gender': ['Male', 'Female']
    })
    df_encoded, _ = apply_label_encoding(df, ['Attrition', 'Gender'])
    assert set(df_encoded['Attrition']) <= {0, 1}
    assert set(df_encoded['Gender']) <= {0, 1}
```

### Ejemplo de prueba para `apply_label_encoding`:

```python
def test_apply_one_hot_encoding():
    df = pd.DataFrame({
        'Department': ['Sales', 'HR'],
        'MaritalStatus': ['Single', 'Married']
    })
    df_encoded = apply_one_hot_encoding(df, ['Department', 'MaritalStatus'])
    assert 'Department_Sales' in df_encoded.columns
    assert 'MaritalStatus_Single' in df_encoded.columns
```

## Resultado

- El dataset final codificado se guardó en: data/clean/hr_data_encoded.csv
- Todas las variables categóricas fueron transformadas con éxito
- Las pruebas pasaron correctamente