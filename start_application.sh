#!/bin/bash
# Start Transverse Application
echo "Starting Transverse Application..."

# Function to start Django server
start_django() {
    echo "Starting Django backend server..."
    cd transverse_backend
    python manage.py runserver 127.0.0.1:8000
}

# Function to start frontend server (if needed)
start_frontend() {
    echo "Frontend server (if needed) can be started separately"
    echo "Open index.html in browser or use a simple HTTP server"
}

# Check if Django is installed
if ! python3 -c "import django" &> /dev/null; then
    echo "Installing Django and dependencies..."
    pip install django djangorestframework django-cors-headers
fi

# Start Django server in background
start_django &
DJANGO_PID=$!

echo "Django server started with PID: $DJANGO_PID"
echo ""
echo "Application URLs:"
echo "  - Frontend: Open index.html in browser"
echo "  - Backend API: http://127.0.0.1:8000"
echo "  - File Upload: http://127.0.0.1:8000/api/upload/"
echo "  - Translation: http://127.0.0.1:8000/api/translate/"
echo ""
echo "To stop the server, press Ctrl+C or run: kill $DJANGO_PID"

# Wait for Django server
wait $DJANGO_PID
