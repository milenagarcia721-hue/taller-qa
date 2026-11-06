import sqlite3
import pytest
from etl.reportes import buscar_cliente, evaluar_regla, total


@pytest.fixture
def conexion_con_datos():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE clientes (id INTEGER PRIMARY KEY, email TEXT)")
    con.execute("INSERT INTO clientes VALUES (1, 'ana@mail.com')")
    yield con
    con.close()


def test_buscar_cliente_encuentra_correo(conexion_con_datos):
    assert buscar_cliente(conexion_con_datos, "ana@mail.com") == [(1, "ana@mail.com")]


def test_buscar_cliente_resiste_inyeccion_sql(conexion_con_datos):
    intento = "' OR '1'='1"
    assert buscar_cliente(conexion_con_datos, intento) == []


def test_evaluar_regla_permitida():
    assert evaluar_regla("tiene_email", (1, "ana@mail.com")) is True


def test_evaluar_regla_rechaza_texto_arbitrario():
    with pytest.raises(ValueError, match="no permitida"):
        evaluar_regla("__import__('os').system('echo inseguro')", (1, "ana@mail.com"))


def test_total_suma_segunda_columna():
    assert total([(1, 10), (2, 20), (3, 5)]) == 35


def test_total_informa_filas_invalidas():
    with pytest.raises(ValueError):
        total([(1,)])
