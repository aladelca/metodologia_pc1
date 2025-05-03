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

## Ejecutando Tests y Validaciones

### Preparación del Entorno

Antes de ejecutar cualquier test o validación, asegúrate de tener el entorno correctamente configurado:

```bash
# Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar pre-commit
pip install pre-commit
pre-commit install
```

### Ejecutando Tests

Puedes ejecutar los tests de varias maneras:

```bash
# Ejecutar todos los tests
python -m pytest

# Ejecutar tests con información detallada
python -m pytest -v

# Ejecutar tests específicos
python -m pytest tests/preprocessing/test_cleaner.py
python -m pytest tests/features/test_feature_builder.py

# Ejecutar un test específico
python -m pytest tests/preprocessing/test_cleaner.py::test_fill_missing_values_with_mean

# Ejecutar tests con cobertura
python -m pytest --cov=src
```

### Validaciones de Calidad de Código

#### Usando pre-commit

Pre-commit ejecutará automáticamente las verificaciones al hacer un commit, pero también puedes ejecutarlas manualmente:

```bash
# Ejecutar todas las verificaciones en archivos preparados para commit
pre-commit run

# Ejecutar todas las verificaciones en todos los archivos
pre-commit run --all-files

# Ejecutar una verificación específica
pre-commit run flake8 --all-files
pre-commit run black --all-files
pre-commit run mypy --all-files
```

#### Verificaciones manuales

También puedes ejecutar las herramientas directamente:

```bash
# Formatear código
black src tests

# Ordenar imports
isort src tests

# Verificar estilo
flake8 src tests

# Verificar tipos
mypy src tests
```

### Solución de Problemas Comunes

1. **Error en pre-commit con `double-quote-string-fixer`**:
   - Si hay modificaciones constantes, ejecuta `black .` y luego intenta hacer commit nuevamente.
   - Si persiste, considera comentar el hook en `.pre-commit-config.yaml`.

2. **Error en tests**:
   - Lee cuidadosamente el mensaje de error para identificar el problema
   - Verifica si hay cambios en la API o dependencias que requieran actualización

3. **Errores de mypy**:
   - Asegúrate de que todas las anotaciones de tipo sean correctas
   - Puedes añadir `# type: ignore` para casos específicos donde sea necesario

4. **Conflictos al fusionar ramas**:
   - Mantén tu rama actualizada regularmente:
     ```bash
     git fetch origin
     git merge origin/main
     ```
   - Resuelve conflictos manualmente y asegúrate de que los tests sigan pasando después
