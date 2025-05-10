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
