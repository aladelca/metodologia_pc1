import pytest
import pandas as pd
import tempfile
import os

from src.preprocessing.read_employee_files import read_file, merge_files, mean_columns

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

def test_read_file_success(sample_files):
    """Verifica que read_file lee correctamente un archivo CSV existente."""
    df = read_file(sample_files[0])
    assert not df.empty
    assert list(df.columns) == ["EmployeeID", "Name"]

def test_read_file_not_found():
    """Verifica que read_file lanza un FileNotFoundError si el archivo no existe."""
    with pytest.raises(FileNotFoundError):
        read_file("no_existe.csv")

def test_merge_files_success(sample_files):
    """Verifica que merge_files una correctamente los archivos si la columna existe."""
    df = merge_files(sample_files[0], sample_files[1], "EmployeeID")
    assert df.shape == (2, 4)
    assert "Score1" in df.columns

def test_merge_files_missing_column(sample_files):
    """Verifica que merge_files lanza un error si falta la columna de unión."""
    with pytest.raises(KeyError):
        merge_files(sample_files[0], sample_files[1], "ID")

def test_mean_columns_success():
    """Verifica que mean_columns agrega correctamente la nueva columna promedio."""
    df = pd.DataFrame({
        "EmployeeID": [1, 2],
        "A": [3, 4],
        "B": [5, 6]
    })
    result = mean_columns(df, "avg", ["A", "B"])
    assert "avg" in result.columns
    assert result["avg"].tolist() == [4.0, 5.0]

def test_mean_columns_missing_column():
    """Verifica que mean_columns lanza un error si alguna columna falta."""
    df = pd.DataFrame({
        "A": [1, 2],
        "B": [3, 4]
    })
    with pytest.raises(KeyError):
        mean_columns(df, "prom", ["A", "B", "C"])

def test_mean_columns_empty_list():
    """Verifica que mean_columns lanza un error si la lista de columnas está vacía."""
    df = pd.DataFrame({
        "A": [1, 2]
    })
    with pytest.raises(ValueError):
        mean_columns(df, "prom", [])