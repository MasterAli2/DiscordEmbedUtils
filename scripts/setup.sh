set -e

echo "Creating venv..."
python3 -m venv venv > /dev/null
source venv/bin/activate > /dev/null

echo "Installing dependencies..."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt > /dev/null


echo "Generating static stuff..."
python3 static.py > /dev/null

echo "Setup complete! You can now run the site with ./scripts/run_debug.sh or a WSGI server."
