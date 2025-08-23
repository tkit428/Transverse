#!/usr/bin/env python3
"""
Simple script to start Django server for Transverse application.
"""

import os
import sys
import subprocess
from pathlib import Path

def start_django_server():
    """Start the Django development server."""
    # Add the project directory to Python path
    project_dir = Path(__file__).parent / "transverse_backend"
    os.chdir(project_dir)

    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transverse_backend.settings')

    # Check if Django is available
    try:
        import django
        django.setup()
    except ImportError:
        print("Django not installed. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'django', 'djangorestframework', 'django-cors-headers'])

    # Start the server
    print("Starting Django server on http://127.0.0.1:8000")
    print("API endpoints available:")
    print("  - POST /api/upload/ - File upload")
    print("  - POST /api/translate/ - Text translation")
    print("Press Ctrl+C to stop the server")

    # Run the Django development server
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])

if __name__ == "__main__":
    start_django_server()
