#!/usr/bin/env bash

# Installer les dépendances
pip install -r requirements.txt

# migrations
python manage.py migrate

# collect static files
python manage.py collectstatic --noinput
