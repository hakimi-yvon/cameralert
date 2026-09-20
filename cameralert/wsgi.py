"""
WSGI config for cameralert project.

It exposes the WSGI callable as a module-level variable named ``application`` and ``app``
for standard WSGI servers (Gunicorn) and Serverless platforms (Vercel).
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cameralert.settings')

application = get_wsgi_application()
app = application
