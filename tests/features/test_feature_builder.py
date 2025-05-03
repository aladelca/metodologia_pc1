"""Tests para el módulo feature_builder."""

import numpy as np
import pandas as pd
import pytest

from src.features.feature_builder import (
    calcular_ratio_salario_edad,
    crear_categorias_edad,
    crear_flags_riesgo,
    crear_indice_satisfaccion,
    crear_variables_dummy,
    get_sample_data,
    seleccionar_mejores_caracteristicas,
)


class TestFeatureBuilder:
    """Pruebas para las funciones del módulo feature_builder."""

    @pytest.fixture
    def df_sample(self):
        """Fixture que proporciona un DataFrame de ejemplo."""
        return get_sample_data()

    def test_crear_categorias_edad(self, df_sample):
        """Prueba la función crear_categorias_edad."""
        # Crear categorías de edad
        result = crear_categorias_edad(df_sample)

        # Verificar que se creó la nueva columna
        assert "grupo_edad" in result.columns

        # Verificar que se asignaron las categorías correctamente
        categories_in_data = result["grupo_edad"].unique()

        if "Menor" in categories_in_data:
            assert "Menor" in result["grupo_edad"].values

        assert "Joven" in result["grupo_edad"].values
        assert "Adulto" in result["grupo_edad"].values
        assert "Senior" in result["grupo_edad"].values

        if "Jubilado" in categories_in_data:
            assert "Jubilado" in result["grupo_edad"].values

        # Verificar que todos los valores tienen una categoría asignada
        assert result["grupo_edad"].notna().all()

        # Verificar la categorización con datos específicos
        # Para Joven (18-30)
        joven_mask = (result["edad"] >= 18) & (result["edad"] < 30)
        if joven_mask.any():
            joven_index = result[joven_mask].index[0]
            assert result.loc[joven_index, "grupo_edad"] == "Joven"

        # Para Adulto (30-50)
        adulto_mask = (result["edad"] >= 30) & (result["edad"] < 50)
        if adulto_mask.any():
            adulto_index = result[adulto_mask].index[0]
            assert result.loc[adulto_index, "grupo_edad"] == "Adulto"

        # Para Senior (50-65)
        senior_mask = (result["edad"] >= 50) & (result["edad"] < 65)
        if senior_mask.any():
            senior_index = result[senior_mask].index[0]
            assert result.loc[senior_index, "grupo_edad"] == "Senior"

    def test_calcular_ratio_salario_edad(self, df_sample):
        """Prueba la función calcular_ratio_salario_edad."""
        # Calcular ratio
        result = calcular_ratio_salario_edad(df_sample)

        # Verificar que se creó la nueva columna
        assert "ratio_salario_edad" in result.columns

        # Verificar que el cálculo es correcto para un registro
        idx = 0
        expected_ratio = (
            df_sample.iloc[idx]["salario"] / df_sample.iloc[idx]["edad"]
        ).round(2)
        assert result.iloc[idx]["ratio_salario_edad"] == expected_ratio

        # Verificar que el tipo de datos es numérico
        assert np.issubdtype(result["ratio_salario_edad"].dtype, np.number)

    def test_crear_indice_satisfaccion(self, df_sample):
        """Prueba la función crear_indice_satisfaccion."""
        # Columnas y pesos para el test
        columnas = [
            "satisfaccion_trabajo",
            "satisfaccion_ambiente",
            "satisfaccion_salario",
        ]
        pesos = [0.5, 0.3, 0.2]

        # Crear índice
        result = crear_indice_satisfaccion(
            df_sample, columnas_satisfaccion=columnas, pesos=pesos
        )

        # Verificar que se creó la nueva columna
        assert "indice_satisfaccion" in result.columns

        # Verificar que el cálculo es correcto para un registro
        idx = 0
        # Calcular valor esperado
        valor_trabajo = df_sample.iloc[idx]["satisfaccion_trabajo"] * 0.5
        valor_ambiente = df_sample.iloc[idx]["satisfaccion_ambiente"] * 0.3
        valor_salario = df_sample.iloc[idx]["satisfaccion_salario"] * 0.2
        expected_index = (valor_trabajo + valor_ambiente + valor_salario).round(2)

        assert result.iloc[idx]["indice_satisfaccion"] == expected_index

        # Verificar que los valores están en el rango esperado (1-5)
        assert result["indice_satisfaccion"].max() <= 5
        assert result["indice_satisfaccion"].min() >= 1

    def test_crear_variables_dummy(self, df_sample):
        """Prueba la función crear_variables_dummy."""
        # Columnas a convertir
        columnas = ["departamento", "ciudad"]

        # Crear dummies
        result = crear_variables_dummy(df_sample, columnas=columnas)

        # Verificar que se crearon las columnas dummy
        for col in columnas:
            # Obtener valores únicos de la columna original
            unique_values = df_sample[col].unique()
            # Para drop_first=True, debe haber n-1 columnas dummy
            expected_columns = len(unique_values) - 1
            # Contar cuántas columnas dummy se crearon para esta columna
            dummy_cols = [c for c in result.columns if c.startswith(f"{col}_")]
            assert len(dummy_cols) == expected_columns

        # Verificar que los valores de las variables dummy son 0 o 1
        for col in result.columns:
            if col.startswith("departamento_") or col.startswith("ciudad_"):
                assert set(result[col].unique()).issubset({0, 1})

    def test_crear_flags_riesgo(self, df_sample):
        """Prueba la función crear_flags_riesgo."""
        # Crear flags
        result = crear_flags_riesgo(df_sample)

        # Verificar que se crearon las nuevas columnas
        assert "flag_baja_satisfaccion" in result.columns
        assert "flag_salario_bajo" in result.columns
        assert "flag_empleado_nuevo" in result.columns
        assert "score_riesgo" in result.columns

        # Verificar que los flags son binarios (0 o 1)
        assert set(result["flag_baja_satisfaccion"].unique()).issubset({0, 1})
        assert set(result["flag_salario_bajo"].unique()).issubset({0, 1})
        assert set(result["flag_empleado_nuevo"].unique()).issubset({0, 1})

        # Verificar que el score de riesgo está entre 0 y 3 (suma de 3 flags)
        assert result["score_riesgo"].max() <= 3
        assert result["score_riesgo"].min() >= 0

        # Verificar que el score de riesgo es la suma de los flags
        for idx in range(len(result)):
            flag1 = result.iloc[idx]["flag_baja_satisfaccion"]
            flag2 = result.iloc[idx]["flag_salario_bajo"]
            flag3 = result.iloc[idx]["flag_empleado_nuevo"]
            expected_score = flag1 + flag2 + flag3
            assert result.iloc[idx]["score_riesgo"] == expected_score

    def test_seleccionar_mejores_caracteristicas(self, df_sample):
        """Prueba la función seleccionar_mejores_caracteristicas."""
        # Seleccionar las 3 mejores características
        k = 3
        result = seleccionar_mejores_caracteristicas(
            df_sample, columna_objetivo="abandono", k=k
        )

        # Verificar que el número de columnas es k + 1 (incluyendo objetivo)
        expected_columns = k + 1
        assert len(result.columns) == expected_columns

        # Verificar que la columna objetivo está incluida
        assert "abandono" in result.columns

        # Verificar que todas las columnas existen en el DataFrame original
        for col in result.columns:
            assert col in df_sample.columns

    def test_get_sample_data(self):
        """Prueba la función get_sample_data."""
        # Obtener datos de ejemplo
        df = get_sample_data()

        # Verificar que se obtiene un DataFrame
        assert isinstance(df, pd.DataFrame)

        # Verificar que tiene el número esperado de filas
        assert len(df) == 100

        # Verificar que contiene todas las columnas esperadas
        expected_columns = [
            "id",
            "edad",
            "salario",
            "antiguedad",
            "departamento",
            "ciudad",
            "satisfaccion_trabajo",
            "satisfaccion_ambiente",
            "satisfaccion_salario",
            "abandono",
        ]
        for col in expected_columns:
            assert col in df.columns

        # Verificar que la variable objetivo tiene valores binarios
        assert set(df["abandono"].unique()).issubset({0, 1})
