"""Configuración global para las pruebas con pytest."""

import os
import sys

import numpy as np
import pandas as pd
import pytest

# Añadir el directorio raíz del proyecto al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def sample_data():
    """Genera un dataset de prueba con datos típicos de RRHH."""
    np.random.seed(42)

    # Crear un DataFrame con datos de ejemplo
    data = {
        "id": list(range(1, 11)) + [3, 5],  # Incluye duplicados
        "edad": [25, 30, np.nan, 28, 40, 35, 42, np.nan, 38, 29, 38, 40],
        "salario": [
            50000,
            55000,
            60000,
            np.nan,
            70000,
            52000,
            90000,
            54000,
            120000,
            51000,
            54000,
            70000,
        ],
        "departamento": [
            "Ventas",
            "Marketing",
            "Ventas",
            np.nan,
            "IT",
            "Marketing",
            "IT",
            "Ventas",
            "Marketing",
            "Ventas",
            "Ventas",
            "IT",
        ],
        "genero": ["M", "F", "m", "F", "M", "f", "M", "F", "M", "F", "F", "M"],
    }

    return pd.DataFrame(data)
