"""Este módulo contiene los tests para el método del módulo read_feedback_files.py."""

import os
import tempfile

import pandas as pd
import pytest

from src.preprocessing.read_feedback_files import merge_dataframe


@pytest.fixture
def sample_files():
    """Crea dos archivos temporales con contenido CSV para pruebas de unión."""
    file1 = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".csv")
    file2 = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".csv")

    file1.write("EmployeeID,Name\n1,Ana\n2,Juan\n")
    file2.write("EmployeeID,Score1,Score2\n1,3,4\n2,5,6\n")

    file1.close()
    file2.close()

    yield file1.name, file2.name

    os.unlink(file1.name)
    os.unlink(file2.name)


def test_merge_dataframe_success(sample_files):
    """Verifica que se una correctamente los archivos si la columna existe."""
    df = merge_dataframe(sample_files[0], sample_files[1], "EmployeeID")
    assert df.shape == (2, 4)
    assert "Score1" in df.columns
    assert "Name" in df.columns


def test_merge_dataframe_missing_column(sample_files):
    """Verifica que merge_dataframe lanza un error si falta la columna de unión."""
    with pytest.raises(KeyError):
        merge_dataframe(sample_files[0], sample_files[1], "ID")


def test_merge_dataframe_empty_files():
    """Verifica que merge_dataframe maneje archivos vacíos correctamente."""
    file1 = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".csv")
    file2 = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".csv")

    file1.close()
    file2.close()

    with pytest.raises(pd.errors.EmptyDataError):
        merge_dataframe(file1.name, file2.name, "EmployeeID")

    os.unlink(file1.name)
    os.unlink(file2.name)


def test_merge_dataframe_different_columns():
    """Verifica que merge_dataframe maneje archivos con columnas diferentes."""
    file1 = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".csv")
    file2 = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".csv")

    file1.write("EmployeeID,Name\n1,Ana\n2,Juan\n")
    file2.write("ID,Score1,Score2\n1,3,4\n2,5,6\n")

    file1.close()
    file2.close()

    with pytest.raises(KeyError):
        merge_dataframe(file1.name, file2.name, "EmployeeID")

    os.unlink(file1.name)
    os.unlink(file2.name)


def test_merge_dataframe_no_common_rows(sample_files):
    """Verifica que merge_dataframe maneje correctamente cuando no hay filas comunes."""
    file1 = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".csv")
    file2 = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".csv")

    file1.write("EmployeeID,Name\n3,Ana\n4,Juan\n")
    file2.write("EmployeeID,Score1,Score2\n1,3,4\n2,5,6\n")

    file1.close()
    file2.close()

    df = merge_dataframe(file1.name, file2.name, "EmployeeID")
    assert df.empty

    os.unlink(file1.name)
    os.unlink(file2.name)
