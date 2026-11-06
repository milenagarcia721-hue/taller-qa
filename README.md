# Taller práctico: Pruebas de Software y Garantía de Calidad

Mini-pipeline ETL: CSV → normalización de correos → SQLite.

## Estructura
- `etl/`: transformaciones, pipeline y reportes.
- `tests/`: pruebas unitarias, integración y seguridad.
- `sonar/antes/`: versión intencionalmente vulnerable para el primer análisis.
- `scripts/`: alternar código vulnerable/corregido.
- `evidencias/`: reportes y capturas reales.
- `INFORME.md`: informe breve.
- `sonar-project.properties`: configuración SonarQube.

## 1. Instalar y probar (Windows PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v
```

## 2. Cobertura
```powershell
pytest --cov=etl --cov-report=term-missing --cov-report=xml
```
Genera `coverage.xml`. La validación de preparación dio 27 pruebas aprobadas y 100% de cobertura. Ejecuta localmente y conserva tu propia salida.

## 3. SonarQube
Desde la raíz:
```powershell
docker compose up -d
```
Abre http://localhost:9000, completa el inicio, crea un proyecto con clave `taller-calidad` y genera un token.

Scanner con Docker Desktop en Windows:
```powershell
docker run --rm -e SONAR_HOST_URL="http://host.docker.internal:9000" -e SONAR_TOKEN="TU_TOKEN" -v "${PWD}:/usr/src" sonarsource/sonar-scanner-cli
```
No publiques el token.

### Análisis inicial
Haz commit del proyecto corregido. Ejecuta `scripts/analizar_antes.ps1`, luego el scanner. Guarda capturas reales de Overview, Issues y Security Hotspots en `evidencias/`.

### Análisis corregido
Ejecuta `scripts/analizar_despues.ps1`, luego el scanner otra vez. Guarda capturas de Overview, Issues y Quality Gate.

**No se simulan capturas de SonarQube:** deben salir de tu instancia real y reflejar el Quality Gate verdadero.

## Relación con la rúbrica
| Criterio | Evidencia |
|---|---|
| Unitarias (25%) | `tests/test_transform.py`, salida pytest |
| Integración (25%) | `etl/pipeline.py`, `tests/test_integracion.py` |
| Cobertura (15%) | `coverage.xml`, salida pytest-cov |
| SonarQube (25%) | análisis antes/después y capturas en `evidencias/` |
| Informe (10%) | `INFORME.md` |

No subir `.venv/`, cachés, tokens ni contraseñas.
