#!/bin/bash

# Transverse - Quick Start Script
# This script helps you quickly start the Transverse application

echo "🚀 Transverse - Quick Start"
echo "==========================="

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this from the Transverse project root directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first:"
    echo "   ./setup.sh"
    exit 1
fi

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Check if Django can start
echo "🔧 Starting Django server..."
echo ""
echo "📡 Server will be available at:"
echo "   🌐 Main app: http://127.0.0.1:8000"
echo "   📤 File upload test: http://127.0.0.1:8000/test_upload.html"
echo ""
echo "⚠️  Press Ctrl+C to stop the server"
echo ""

# Start the server
python manage.py runserver 127.0.0.1:8000
