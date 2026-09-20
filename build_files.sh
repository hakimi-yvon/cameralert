#!/bin/bash
set -e

echo "=== CamerAlert: Installation des dependances ==="
python3 -m pip install -r requirements.txt --break-system-packages 2>/dev/null || python3 -m pip install -r requirements.txt || true

echo "=== CamerAlert: Collecte des fichiers statiques ==="
python3 manage.py collectstatic --noinput --clear

# Si DATABASE_URL est definie, appliquer automatiquement les migrations sur PostgreSQL
if [ -n "$DATABASE_URL" ]; then
    echo "=== CamerAlert: Execution automatique des migrations de base de donnees ==="
    python3 manage.py migrate --noinput
fi

echo "=== Build Vercel termine avec succes ==="
