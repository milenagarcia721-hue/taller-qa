import csv
from etl.transform import normalizar_email


def ejecutar_pipeline(ruta_csv, con):
    """Carga clientes desde CSV a SQLite; rechaza el archivo si hay datos inválidos."""
    con.execute(
        "CREATE TABLE IF NOT EXISTS clientes "
        "(id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE)"
    )

    filas = []
    with open(ruta_csv, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        if lector.fieldnames is None or not {"id", "email"}.issubset(lector.fieldnames):
            raise ValueError("el CSV debe contener las columnas id y email")

        for numero_fila, registro in enumerate(lector, start=2):
            try:
                identificador = int(registro["id"])
                correo = normalizar_email(registro["email"])
            except (TypeError, ValueError) as error:
                raise ValueError(f"registro inválido en la fila {numero_fila}: {error}") from error
            filas.append((identificador, correo))

    con.executemany(
        "INSERT OR REPLACE INTO clientes (id, email) VALUES (?, ?)",
        filas
    )
    con.commit()
    return len(filas)
