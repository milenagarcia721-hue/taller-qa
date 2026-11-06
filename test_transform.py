import pytest
from etl.transform import normalizar_email, calcular_total


@pytest.mark.parametrize("entrada, esperado", [
    (" Ana@Mail.COM ", "ana@mail.com"),
    ("luis.p+datos@uni.edu.co", "luis.p+datos@uni.edu.co"),
    ("USUARIO@EJEMPLO.COM", "usuario@ejemplo.com"),
])
def test_normalizar_email_valido(entrada, esperado):
    assert normalizar_email(entrada) == esperado


@pytest.mark.parametrize("entrada", ["", "   ", "sin-arroba", None, "ana@dominio"])
def test_normalizar_email_invalido(entrada):
    with pytest.raises(ValueError):
        normalizar_email(entrada)


@pytest.mark.parametrize("precio, cantidad, descuento, esperado", [
    (100, 2, 0, 200.00),
    (100, 2, 1, 0.00),
    (19.999, 3, 0, 60.00),
    (100, 3, 0.10, 270.00),
])
def test_calcular_total_valido(precio, cantidad, descuento, esperado):
    assert calcular_total(precio, cantidad, descuento) == esperado


@pytest.mark.parametrize("precio, cantidad, descuento", [
    (-1, 2, 0),
    (10, -2, 0),
    (10, 2, 1.1),
    (10, 2, -0.1),
])
def test_calcular_total_invalido(precio, cantidad, descuento):
    with pytest.raises(ValueError):
        calcular_total(precio, cantidad, descuento)


def test_calcular_total_rechaza_precio_no_numerico():
    with pytest.raises(ValueError):
        calcular_total("100", 2, 0)
