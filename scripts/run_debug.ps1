# Activate virtual environment
& "$PWD\venv\Scripts\Activate.ps1"

# Environment variables
$env:FLASK_APP = "deu.py"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"

$env:FLASK_RUN_PORT = "8080"
$env:FLASK_RUN_HOST = "0.0.0.0"

# Run flask
flask run
