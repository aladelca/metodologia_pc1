# Configuración de Protección de Rama Main

Para establecer la protección de la rama principal (`main`) en GitHub, sigue estos pasos:

## Pasos para Configurar la Protección de Rama

1. Ve al repositorio en GitHub
2. Haz clic en "Settings" (Configuración)
3. En el menú lateral, haz clic en "Branches" (Ramas)
4. En "Branch protection rules" (Reglas de protección de ramas), haz clic en "Add rule" (Agregar regla)

## Configuración Recomendada

Aplica la siguiente configuración:

- Branch name pattern: `main`
- Require a pull request before merging: ✓
  - Require approvals: ✓ 
  - Required number of approvals before merging: 1
- Require status checks to pass before merging: ✓
  - Require branches to be up to date before merging: ✓
  - Status checks that are required:
    - test (Python CI)
- Do not allow bypassing the above settings: ✓

## Flujo de Trabajo Recomendado

1. Nunca trabajar directamente en la rama `main`
2. Para cada tarea o feature, crear una nueva rama:
   ```
   git checkout -b feature/nombre-descriptivo
   ```
3. Realizar los cambios necesarios
4. Confirmar que los tests pasan localmente:
   ```
   pytest
   ```
5. Asegurarse que el código cumple con los estándares de estilo:
   ```
   black src tests
   isort src tests
   flake8
   ```
6. Hacer commit de los cambios:
   ```
   git add .
   git commit -m "Descripción clara del cambio"
   ```
7. Subir la rama al repositorio remoto:
   ```
   git push -u origin feature/nombre-descriptivo
   ```
8. Crear un Pull Request en GitHub
9. Solicitar revisión del código
10. Una vez aprobado, hacer merge a `main`

Este flujo de trabajo asegura que todo el código que llega a `main` ha sido revisado y probado adecuadamente. 