"""
WSGI config for HealthSphere project.

This file helps deploy the project to a production environment using WSGI-compliant servers like Gunicorn or uWSGI.
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the Django settings module environment variable to point to the correct settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create and expose the WSGI application callable to be used by the server
application = get_wsgi_application()
