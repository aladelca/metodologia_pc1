# Conclusiones del Análisis Exploratorio - HR Analytics

## Resumen Ejecutivo

Este documento presenta las conclusiones principales del análisis exploratorio de datos realizado sobre el dataset de HR Analytics, enfocándose en la variable objetivo "attrition" (abandono laboral) y sus relaciones con otras variables del conjunto de datos.

## 1. Distribución de la Variable Target (Attrition)

- El dataset presenta un desbalance natural en la variable target.
- La distribución muestra que aproximadamente el 16-17% de los empleados presentan attrition.
- Este desbalance deberá ser considerado en las etapas posteriores de modelado.

## 2. Variables Numéricas Más Relevantes

### Correlaciones más Significativas con Attrition:
1. **MonthlyIncome**: Existe una correlación negativa, indicando que empleados con mayores salarios tienen menor probabilidad de abandono.
2. **Age**: Los empleados de mayor edad tienden a tener menor probabilidad de abandono.
3. **JobLevel**: Niveles de trabajo más altos están asociados con menor probabilidad de abandono.

## 3. Patrones en Variables Categóricas

### Departamento
- Los departamentos están codificados como variables dummy (Department_Human Resources, Department_Research & Development, Department_Sales)
- Se observan diferentes tasas de abandono entre departamentos

### Rol de Trabajo
- Los roles están representados como variables dummy
- Incluye posiciones como Healthcare Representative, Human Resources, Laboratory Technician, Manager, Sales Representative, entre otros
- Cada rol muestra diferentes patrones de abandono

### Estado Civil
- Codificado en tres categorías: Divorced, Married, Single
- Se observan diferencias en las tasas de abandono según el estado civil


## 4. Variables de Satisfacción

- **EnvironmentSatisfaction**: Mide la satisfacción con el ambiente laboral
- **JobSatisfaction**: Indica el nivel de satisfacción con el trabajo
- **WorkLifeBalance**: Refleja el balance entre trabajo y vida personal
- **average_employee_satisfaction**: Medida promedio de satisfacción del empleado
- **average_manager_feedback**: Retroalimentación promedio del manager

## 5. Variables Temporales

Las siguientes variables temporales muestran relación con el attrition:
- **YearsAtCompany**: Tiempo total en la empresa
- **YearsSinceLastPromotion**: Tiempo desde la última promoción
- **YearsWithCurrManager**: Tiempo con el manager actual
- **TotalWorkingYears**: Años totales de experiencia laboral

## 6. Recomendaciones para Modelado

1. **Tratamiento del Desbalance**:
   - Considerar técnicas para manejar el desbalance de clases (16-17% vs 83-84%)
   - Evaluar el impacto del desbalance en el rendimiento del modelo

2. **Feature Engineering**:
   - Utilizar las variables dummy existentes para departamentos y roles
   - Considerar las variables de satisfacción como predictores importantes
   - Aprovechar las variables temporales disponibles

3. **Selección de Variables**:
   - Priorizar variables con correlaciones significativas identificadas
   - Incluir variables categóricas codificadas como dummy
   - Considerar las variables de satisfacción y temporales como features importantes

## 7. Limitaciones del Análisis

- El análisis se basa en datos ya codificados (variables dummy)
- Algunas variables mencionadas en análisis previos (como OverTime) no están disponibles en el conjunto de datos actual
- Las variables categóricas están pre-procesadas como variables dummy, lo que puede afectar la interpretabilidad 