#!/usr/bin/env python
"""
Script para verificar que todos los módulos Python en src/ tienen tests.

Este script verifica que:
1. Cada archivo .py en src/ tiene al menos un archivo de test.
2. Los archivos de test siguen la convención test_*.py.
3. Imprime una lista de archivos sin tests.

Uso:
    python scripts/check_test_coverage.py
"""

import os
import sys

# Directorios a ignorar (relativos a src/)
IGNORED_DIRS = [
    "__pycache__",
]

# Archivos a ignorar (solo nombres base, sin ruta)
IGNORED_FILES = [
    "__init__.py",
    "__main__.py",
]


def find_all_modules(src_dir="src"):
    """Encuentra todos los módulos Python en el directorio src."""
    modules = []
    for root, dirs, files in os.walk(src_dir):
        # Ignorar directorios especificados
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:
            if file.endswith(".py") and file not in IGNORED_FILES:
                # Obtener la ruta completa del archivo
                full_path = os.path.join(root, file)
                # Convertir la ruta a un formato de módulo relativo a src/
                module_path = os.path.relpath(full_path, src_dir)
                modules.append(module_path)

    return modules


def find_test_file(module_path, test_dir="tests"):
    """
    Verifica si existe un archivo de test para el módulo dado.

    Busca en varios patrones comunes para los archivos de test.
    """
    # Extraer directorio y nombre del archivo
    module_dir, module_file = os.path.split(module_path)
    module_name = os.path.splitext(module_file)[0]

    # Patrones de búsqueda para archivos de test
    patterns = [
        # test_module.py en el mismo subdirectorio
        os.path.join(test_dir, module_dir, f"test_{module_name}.py"),
        # test_module.py en un subdirectorio llamado tests/
        os.path.join(test_dir, module_dir, "tests", f"test_{module_name}.py"),
        # module_test.py en el mismo subdirectorio
        os.path.join(test_dir, module_dir, f"{module_name}_test.py"),
    ]

    # Verificar cada patrón
    for pattern in patterns:
        if os.path.exists(pattern):
            return pattern

    # Búsqueda alternativa: buscar archivos de test con el nombre del módulo
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            # Verificar si el nombre del archivo sigue el patrón
            if (
                file.startswith("test_")
                and file.endswith(".py")
                and module_name in file
            ):
                return os.path.join(root, file)

    return None


def main():
    """Función principal del script."""
    print("Verificando cobertura de tests para módulos en src/...")

    # Verificar que los directorios existen
    if not os.path.isdir("src"):
        print("Error: No se encontró el directorio 'src/'")
        sys.exit(1)

    if not os.path.isdir("tests"):
        print("Error: No se encontró el directorio 'tests/'")
        sys.exit(1)

    # Encontrar todos los módulos
    modules = find_all_modules()

    # Verificar tests para cada módulo
    missing_tests = []

    for module_path in modules:
        test_file = find_test_file(module_path)
        if test_file:
            print("✓ {} -> {}".format(module_path, test_file))
        else:
            print("✗ {} -> No se encontró archivo de test".format(module_path))
            missing_tests.append(module_path)

    # Mostrar resumen
    total_modules = len(modules)
    covered_modules = total_modules - len(missing_tests)

    print("\nResumen:")
    print("Total de módulos: {}".format(total_modules))
    print("Módulos con tests: {}".format(covered_modules))
    print("Módulos sin tests: {}".format(len(missing_tests)))

    if missing_tests:
        print("\nLos siguientes módulos no tienen tests:")
        for module in missing_tests:
            print("  - {}".format(module))
        sys.exit(1)
    else:
        print("\n¡Todos los módulos tienen tests correspondientes!")
        sys.exit(0)


if __name__ == "__main__":
    main()
