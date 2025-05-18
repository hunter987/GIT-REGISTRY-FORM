# Proyecto de Validación y Pruebas Automatizadas

## Descripción
Este proyecto automatiza la validación de formularios de registro utilizando validadores personalizados en Python, pruebas unitarias con PyTest y pruebas funcionales con Selenium. También está integrado con SonarQube para control de calidad del código y GitHub Actions para CI/CD.

## Estructura
- `validators.py`: Validaciones personalizadas.
- `test_validators.py`: Pruebas unitarias con PyTest.
- `selenium_test_runner.py`: Automatización de pruebas funcionales con Selenium.
- `usuarios.xlsx`: Archivo de entrada para pruebas.
- `server.py`: Servidor web que simula un formulario de registro.
- `.github/workflows/python-app.yml`: Pipeline de CI con GitHub Actions.
- `sonar-project.properties`: Configuración para análisis con SonarQube.

## Cómo ejecutar
```bash
pip install -r requirements.txt
python server.py  # Inicia el servidor local
python selenium_test_runner.py  # Ejecuta las pruebas funcionales
pytest --cov=validators > coverage.xml  # Genera reporte de cobertura
