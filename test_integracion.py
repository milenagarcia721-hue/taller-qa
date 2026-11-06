import sqlite3
import pytest
from etl.pipeline import ejecutar_pipeline


@pytest.fixture
def conexion():
    con = sqlite3.connect(":memory:")
    yield con
    con.close()


def test_pipeline_carga_clientes(conexion, tmp_path):
    archivo = tmp_path / "clientes.csv"
    archivo.write_text("id,email\n1, Ana@Mail.com\n2,luis@mail.com\n", encoding="utf-8")

    cantidad = ejecutar_pipeline(archivo, conexion)
    filas = conexion.execute(
        "SELECT email FROM clientes ORDER BY id"
    ).fetchall()

    assert cantidad == 2
    assert filas == [("ana@mail.com",), ("luis@mail.com",)]


def test_pipeline_es_idempotente(conexion, tmp_path):
    archivo = tmp_path / "clientes.csv"
    archivo.write_text("id,email\n1,ana@mail.com\n2,luis@mail.com\n", encoding="utf-8")

    ejecutar_pipeline(archivo, conexion)
    ejecutar_pipeline(archivo, conexion)

    cantidad = conexion.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
    assert cantidad == 2


def test_pipeline_rechaza_email_invalido_sin_cargar_filas(conexion, tmp_path):
    archivo = tmp_path / "clientes.csv"
    archivo.write_text("id,email\n1,ana@mail.com\n2,correo-invalido\n", encoding="utf-8")

    with pytest.raises(ValueError, match="registro inválido"):
        ejecutar_pipeline(archivo, conexion)

    cantidad = conexion.execute(
        "SELECT COUNT(*) FROM clientes"
    ).fetchone()[0]
    assert cantidad == 0


def test_pipeline_requiere_columnas(conexion, tmp_path):
    archivo = tmp_path / "clientes.csv"
    archivo.write_text("codigo,nombre\n1,Ana\n", encoding="utf-8")

    with pytest.raises(ValueError, match="columnas"):
        ejecutar_pipeline(archivo, conexion)
