# Práctica Calificada: Metodología para Data Science

## Descripción del Proyecto

Este proyecto consiste en el análisis de un dataset de Recursos Humanos, donde el objetivo es predecir la variable `attrition`. El objetivo principal es practicar el flujo completo de un proyecto de data science, desde la limpieza y manipulación de datos hasta la preparación para modelado, tal como vimos en clase, utilizando Git como herramienta principal de control de versiones.

## Dataset

El dataset utilizado es el [HR Analytics Case Study](https://www.kaggle.com/datasets/vjchoudhary7/hr-analytics-case-study/data), que contiene información sobre empleados y su desempeño en la empresa.

## Estructura del Proyecto
```
├── data/                  # Datos originales y procesados
│   ├── raw/              # Datos originales
│   └── processed/        # Datos procesados
├── notebooks/            # Jupyter notebooks con el análisis
├── src/                  # Código fuente
│   ├── preprocessing/    # Scripts de limpieza y procesamiento
│   ├── features/         # Feature engineering
│   └── test/             # Test
├── reports/              # Reportes y visualizaciones
├── .github/              # Configuración de GitHub
│   └── workflows/        # GitHub Actions workflows
├── .pre-commit-config.yaml # Configuración de pre-commit hooks
├── tests/                # Tests unitarios y de integración
└── README.md             # Este archivo
```

## Tareas a Realizar

### 1. Unir datasets con datos de encuesta de empleados
- Hacer un cruce de los datasets `general_data.csv` y `employee_survey_data.csv`. Pueden utilizar los comandos `merge` de `pandas`.
- Crear las variables `average_employee_satisfaction` que vendría a ser el promedio de las variables del dataset `employee_surve_data.csv`.
- Crear una documentación en formato `.md` indicando los pasos tomados en el cruce


### 2. Unir datasets con datos de feedback de jefes
- Unir el dataset del paso uno con `manager_survey_data.csv`. Pueden utilizar los comandos `merge` de `pandas`.
- Crear las variables `average_manager_feedback` que vendría a ser el promedio de las variables del dataset `manager_surve_data.csv`.
- Actualizar la documentación del paso uno indicando lo adicional.


### 3. Limpieza de Datos y Manejo de Valores Faltantes
- Identificación de valores faltantes
- Implementación de estrategias de manejo
- Crear módulo `src/preprocessing/cleaner.py` con funciones de limpieza
- Implementar tests para las funciones de limpieza en `tests/preprocessing/`

### 4. Detección y Manejo de Outliers
- Identificación de outliers mediante técnicas estadísticas (pueden utilizar el método
`IsolationForest` y/o un simple boxplot)
- Desarrollar estrategias para manejar outliers
- Implementar funciones en `src/preprocessing/outlier_detector.py`
- Crear tests para validar funcionalidad en `tests/preprocessing/`

### 5. Transformación de Variables Categóricas
- Identificación de variables categóricas
- Investigar y aplicar técnicas de encoding (pueden revisar `OneHotEncoder` y/o `LabelEncoder` de la librería `sklearn`)
- Documentación del proceso tomando en cuenta el caso de uso
- El dataset final, después de culminados todos los cambios hasta esta etapa, deberá guardarse en una carpeta llamada `clean`.


### 6. Feature Engineering
- Haciendo uso de los datasets `in_time.csv` y `out_time.csv`, que indica la fecha de entrada y salida de los trabajadores, genera variables asociadas al tiempo efectivo de trabajo (promedio mensual de horas trabajadas, desviación estándar de las horas trabajadas, etc.). Deberán generar al menos 6 nuevas variables.
- Los archivos que sirvan para generar las variables deberán estar en `src/features`.
- El dataset final, después de culminada esta etapa, deberá guardarse en una carpeta llamada `feature`.

### 7. Análisis exploratorio
- Haciendo uso del dataset generado hasta este momento, se deberán analizar las variables indicando si es que hay algunos patrones interesantes en los datos y/o variables que está correlacionadas con la variable target `attrition`. Esto deberá estar en notebook.
- Las conclusiones finales del análisis exploratorio deberán guardarse en un archivo `.md` adicional.


## Entregables

Cada estudiante deberá:
1. Crear ramas descriptivas para cada tarea
2. Realizar commits con mensajes significativos
3. Documentar el proceso en el README.md
4. Crear un pull request final que incluya:
   - Descripción de cambios realizados
   - Justificación de decisiones
   - Resultados obtenidos
   - Visualizaciones relevantes
   - Evidencia de que los tests pasan correctamente

## Criterios de Evaluación

1. **Uso de Git y Flujo de Trabajo (30%)**
   - Estructura de ramas
   - Calidad de commits
   - Configuración de pre-commit hooks
   - Implementación de flujo PR
   - Documentación en pull request

2. **Limpieza y Manipulación de Datos (30%)**
   - Calidad de limpieza
   - Justificación de decisiones
   - Eficiencia de código
   - Modularidad y reusabilidad

3. **Tests y Calidad de Código (20%)**
   - Cobertura de tests
   - Calidad de tests
   - Uso correcto de fixtures y mocks
   - Implementación de CI/CD

4. **Documentación (20%)**
   - Claridad de documentación
   - Docstrings completos
   - Visualizaciones
   - Explicación de decisiones

## Recursos Adicionales

- [Documentación de Git](https://git-scm.com/doc)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/documentation.html)
- [Pytest Documentation](https://docs.pytest.org/)
- [Pre-commit Documentation](https://pre-commit.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
