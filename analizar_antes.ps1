Copy-Item "sonar/antes/reportes.py" "etl/reportes.py" -Force
pytest --cov=etl --cov-report=xml
