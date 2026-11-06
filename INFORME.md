# Informe breve – Taller práctico de Pruebas de Software y QA

## 1. Objetivo
Implementar y verificar un mini-pipeline ETL que lee clientes desde un archivo CSV, normaliza los correos electrónicos y los almacena en SQLite. Se aplican pruebas unitarias, pruebas de integración, medición de cobertura y revisión de seguridad y mantenibilidad.

## 2. Implementación
Se separó la solución en tres módulos:
- `transform.py`: normaliza y valida correos electrónicos y calcula totales con descuento.
- `pipeline.py`: lee el CSV, valida los registros y carga los datos en SQLite.
- `reportes.py`: consulta clientes de forma segura, aplica reglas permitidas y calcula totales.

## 3. Pruebas realizadas
Se incluyen pruebas parametrizadas para correos válidos e inválidos, y para el cálculo de totales. También se verifican descuentos de 0 y 1, valores negativos, descuentos fuera del rango permitido y redondeo. Las pruebas de integración comprueban la carga CSV → SQLite, la idempotencia, el rechazo de archivos con correos inválidos y la validación de columnas. Finalmente, se comprueba que la búsqueda de clientes no permita una inyección SQL.

Ejecutar `pytest -v` para obtener el resultado de las pruebas y `pytest --cov=etl --cov-report=term-missing --cov-report=xml` para obtener el porcentaje de cobertura. Adjuntar al informe el resultado real de la terminal después de ejecutar los comandos.

## 4. Hallazgos y correcciones de seguridad
| Hallazgo intencional | Riesgo | Corrección aplicada |
|---|---|---|
| Contraseña fija `admin123` | Exposición de credenciales | Lectura desde variable de entorno `DB_PASSWORD`; no se almacena el secreto en el repositorio |
| Consulta SQL con f-string | Inyección SQL | Consulta parametrizada con `?` |
| Uso de `eval()` | Ejecución de código arbitrario | Eliminación de `eval`; reglas explícitas permitidas |
| `except:` y fallo silencioso | Oculta errores y dificulta diagnóstico | Captura de excepciones específicas y generación de `ValueError` |

La prueba con la entrada `' OR '1'='1` confirma que el valor se trata como dato y no como parte de la consulta SQL.

## 5. Conclusión
Las pruebas unitarias permiten verificar funciones aisladas y detectar errores en sus límites. Las pruebas de integración comprueban el comportamiento conjunto del archivo CSV, las transformaciones y SQLite. La idempotencia evita duplicar registros al repetir una carga. Las consultas parametrizadas, la eliminación de `eval` y el manejo explícito de errores reducen riesgos de seguridad y mejoran la mantenibilidad.

## 6. Evidencia de SonarQube
Completar esta sección después de ejecutar SonarQube localmente:
- Quality Gate: [registrar resultado real].
- Cobertura: [registrar porcentaje real].
- Bugs, vulnerabilidades y code smells: [registrar cantidades reales].
- Capturas antes y después: [insertar evidencias].

No se consignan métricas de SonarQube sin ejecutar el análisis en una instancia real.
