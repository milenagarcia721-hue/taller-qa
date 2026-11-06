import re

PATRON = re.compile(r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$")


def normalizar_email(email):
    """Valida y normaliza un correo electrónico."""
    if not isinstance(email, str) or not email.strip():
        raise ValueError("email vacío o inválido")

    limpio = email.strip().lower()
    if not PATRON.fullmatch(limpio):
        raise ValueError(f"email inválido: {email}")

    return limpio


def calcular_total(precio, cantidad, descuento=0.0):
    """Calcula el total aplicando un descuento entre 0 y 1."""
    if not isinstance(precio, (int, float)) or not isinstance(cantidad, (int, float)):
        raise ValueError("precio y cantidad deben ser numéricos")
    if precio < 0 or cantidad < 0 or not isinstance(descuento, (int, float)):
        raise ValueError("parámetros fuera de rango")
    if not 0 <= descuento <= 1:
        raise ValueError("parámetros fuera de rango")

    return round(precio * cantidad * (1 - descuento), 2)
