"""
WSGI entry point for production deployment.

Supported WSGI servers:
  gunicorn wsgi:app
  uwsgi --module wsgi:app
"""

import sys
import os

# Make the src package importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app import app  # noqa: F401  (imported for the WSGI server)

if __name__ == '__main__':
    app.run()
