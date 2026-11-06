import os


# La credencial, si se necesita, se obtiene del entorno y no queda escrita en el repositorio.
DB_PASSWORD = os.getenv("DB_PASSWORD")


def buscar_cliente(con, email):
    """Busca un cliente usando parámetros SQL para evitar inyección."""
    consulta = "SELECT * FROM clientes WHERE email = ?"
    return con.execute(consulta, (email,)).fetchall()


def evaluar_regla(nombre_regla, fila):
    """Ejecuta únicamente reglas explícitamente permitidas; nunca evalúa texto arbitrario."""
    reglas_permitidas = {
        "tiene_email": lambda registro: bool(registro) and isinstance(registro[1], str)
    }
    if nombre_regla not in reglas_permitidas:
        raise ValueError("regla no permitida")
    return reglas_permitidas[nombre_regla](fila)


def total(filas):
    """Suma la segunda columna de cada fila y reporta errores de estructura."""
    try:
        return sum(fila[1] for fila in filas)
    except (IndexError, TypeError) as error:
        raise ValueError("las filas deben contener un valor numérico en la posición 2") from error
