#!/bin/bash
set -e
echo "=== CamerAlert: Preparation de l'environnement de build ==="
python3 -m pip install -r requirements.txt --break-system-packages 2>/dev/null || python3 -m pip install -r requirements.txt || pip3 install -r requirements.txt

echo "=== CamerAlert: Collecte des fichiers statiques ==="
python3 manage.py collectstatic --noinput --clear

echo "=== Build Vercel termine avec succes ==="
