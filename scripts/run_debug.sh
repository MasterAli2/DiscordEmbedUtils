set -e

source "${PWD}/venv/bin/activate"

export FLASK_APP=main.py
export FLASK_ENV=development
export FLASK_DEBUG=1

export FLASK_RUN_PORT=8080
export FLASK_RUN_HOST=0.0.0.0

flask run
