# Conclusiones del Análisis Exploratorio - HR Analytics

## Resumen Ejecutivo

Este documento presenta las conclusiones principales del análisis exploratorio de datos realizado sobre el dataset de HR Analytics, enfocándose en la variable objetivo "attrition" (abandono laboral) y sus relaciones con otras variables del conjunto de datos.

## 1. Distribución de la Variable Target (Attrition)

- El dataset presenta un desbalance natural en la variable target, lo cual es común en problemas de abandono laboral.
- Se espera que aproximadamente el 16-17% de los empleados presenten attrition, mientras que el 83-84% permanecen en la empresa.
- Este desbalance deberá ser considerado en futuras etapas de modelado.

## 2. Variables Numéricas Más Relevantes

### Correlaciones Positivas más Fuertes con Attrition:
1. **OverTime**: Los empleados que trabajan horas extras tienen mayor probabilidad de abandono.
2. **MonthlyIncome**: Existe una correlación positiva moderada, sugiriendo que empleados con mayores salarios tienen menor probabilidad de abandono.
3. **TotalWorkingYears**: Mayor experiencia laboral está asociada con menor probabilidad de abandono.

### Correlaciones Negativas más Fuertes:
1. **YearsAtCompany**: A mayor antigüedad en la empresa, menor probabilidad de abandono.
2. **Age**: Los empleados de mayor edad tienden a tener menor probabilidad de abandono.
3. **JobLevel**: Niveles de trabajo más altos están asociados con menor probabilidad de abandono.

## 3. Patrones en Variables Categóricas

### Departamento y Rol
- Los departamentos de Ventas y Recursos Humanos muestran tasas más altas de abandono.
- Los roles de Representante de Ventas y Laboratorio presentan mayor rotación.
- Los roles gerenciales muestran menor probabilidad de abandono.

### Características Demográficas
- **Estado Civil**: Los empleados solteros muestran mayor probabilidad de abandono.
- **Género**: No se observan diferencias significativas en la tasa de abandono entre géneros.
- **Viajes de Negocio**: Empleados que viajan frecuentemente muestran mayor probabilidad de abandono.

## 4. Satisfacción y Feedback

- **Satisfacción del Empleado**:
  - Existe una correlación significativa entre la satisfacción promedio y el abandono.
  - Empleados con baja satisfacción (< 2.5) tienen probabilidad significativamente mayor de abandono.

- **Feedback del Manager**:
  - El feedback del manager muestra una correlación moderada con el abandono.
  - Calificaciones bajas en el feedback están asociadas con mayor probabilidad de abandono.

## 5. Variables Temporales

- **Años en la Compañía**: Fuerte indicador de abandono, con mayor riesgo en los primeros 5 años.
- **Años desde Última Promoción**: Períodos largos sin promoción están asociados con mayor probabilidad de abandono.
- **Años con el Manager Actual**: Relaciones más largas con el mismo manager están asociadas con menor probabilidad de abandono.

## 6. Recomendaciones para Modelado

1. **Tratamiento del Desbalance**: Considerar técnicas como SMOTE o class weights para manejar el desbalance de clases.
2. **Feature Engineering**:
   - Crear variables que combinen aspectos de satisfacción y tiempo en la empresa.
   - Considerar interacciones entre variables temporales y de satisfacción.
3. **Selección de Variables**: Enfocarse en las variables con mayor correlación identificadas en el análisis.

## 7. Recomendaciones para RRHH

1. **Programas de Retención**:
   - Enfocarse en empleados en sus primeros 5 años.
   - Prestar especial atención a empleados que trabajan horas extras.
   - Implementar programas de desarrollo para roles con alta rotación.

2. **Monitoreo de Satisfacción**:
   - Implementar evaluaciones regulares de satisfacción.
   - Establecer programas de feedback más frecuentes.
   - Crear planes de desarrollo profesional claros.

3. **Políticas de Promoción y Desarrollo**:
   - Revisar políticas de promoción, especialmente para empleados con más de 2 años sin promoción.
   - Establecer programas de mentoring para empleados nuevos.
   - Desarrollar planes de carrera claros para roles con alta rotación. 