#!/bin/bash

# Transverse - Status Check Script
# This script checks the status of all components

echo "🔍 Transverse - System Status Check"
echo "==================================="

# Function to print colored output
print_green() {
    echo -e "\033[0;32m$1\033[0m"
}

print_red() {
    echo -e "\033[0;31m$1\033[0m"
}

print_yellow() {
    echo -e "\033[1;33m$1\033[0m"
}

print_blue() {
    echo -e "\033[0;34m$1\033[0m"
}

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    print_red "❌ Error: Please run this from the Transverse project root directory"
    exit 1
fi

print_blue "📋 Checking system components..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_green "✅ Python: $PYTHON_VERSION"
else
    print_red "❌ Python 3 not found"
fi

# Check virtual environment
if [ -d "venv" ]; then
    print_green "✅ Virtual environment: Found"
else
    print_red "❌ Virtual environment: Not found"
fi

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == *"/venv" ]]; then
    print_green "✅ Virtual environment: Activated"
else
    print_yellow "⚠️  Virtual environment: Not activated"
fi

# Check Django
if python3 -c "import django; print(f'Django {django.get_version()}')" 2>/dev/null; then
    print_green "✅ Django: Working"
else
    print_red "❌ Django: Not working"
fi

# Check file processing libraries
echo ""
print_blue "📄 File Processing Libraries:"

# PDF processing
if python3 -c "import fitz; print('OK')" 2>/dev/null; then
    print_green "✅ PyMuPDF (PDF): Working"
else
    print_red "❌ PyMuPDF (PDF): Not working"
fi

# Office documents
if python3 -c "import docx; print('OK')" 2>/dev/null; then
    print_green "✅ python-docx (Word): Working"
else
    print_yellow "⚠️  python-docx (Word): Not working"
fi

if python3 -c "import openpyxl; print('OK')" 2>/dev/null; then
    print_green "✅ openpyxl (Excel): Working"
else
    print_yellow "⚠️  openpyxl (Excel): Not working"
fi

if python3 -c "import pptx; print('OK')" 2>/dev/null; then
    print_green "✅ python-pptx (PowerPoint): Working"
else
    print_yellow "⚠️  python-pptx (PowerPoint): Not working"
fi

# Images and OCR
if python3 -c "import PIL; print('OK')" 2>/dev/null; then
    print_green "✅ Pillow (Images): Working"
else
    print_yellow "⚠️  Pillow (Images): Not working"
fi

if python3 -c "import pytesseract; print('OK')" 2>/dev/null; then
    print_green "✅ pytesseract (OCR): Working"
else
    print_yellow "⚠️  pytesseract (OCR): Not working"
fi

# E-books
if python3 -c "import ebooklib; print('OK')" 2>/dev/null; then
    print_green "✅ EbookLib (E-books): Working"
else
    print_yellow "⚠️  EbookLib (E-books): Not working"
fi

if python3 -c "import bs4; print('OK')" 2>/dev/null; then
    print_green "✅ BeautifulSoup4 (HTML/XML): Working"
else
    print_yellow "⚠️  BeautifulSoup4 (HTML/XML): Not working"
fi

# AI/ML
echo ""
print_blue "🤖 AI/ML Libraries:"

if python3 -c "import google.generativeai; print('OK')" 2>/dev/null; then
    print_green "✅ Google Gemini API: Working"
else
    print_yellow "⚠️  Google Gemini API: Not working (API key needed)"
fi

# System dependencies
echo ""
print_blue "🔧 System Dependencies:"

if command -v tesseract &> /dev/null; then
    TESSERACT_VERSION=$(tesseract --version | head -1)
    print_green "✅ Tesseract OCR: $TESSERACT_VERSION"
else
    print_yellow "⚠️  Tesseract OCR: Not found (optional for image text extraction)"
fi

# Configuration files
echo ""
print_blue "⚙️  Configuration:"

if [ -f ".env" ]; then
    print_green "✅ .env file: Found"
else
    print_yellow "⚠️  .env file: Not found (create with: cp .env.example .env)"
fi

if [ -d "transverse_backend/uploads/temp" ]; then
    print_green "✅ Upload directories: Created"
else
    print_yellow "⚠️  Upload directories: Not found"
fi

# Django server check
echo ""
print_blue "🌐 Django Server:"

if lsof -i :8000 &> /dev/null; then
    print_green "✅ Django server: Running on port 8000"
else
    print_yellow "⚠️  Django server: Not running"
fi

# Summary
echo ""
print_green "📊 Status Summary:"
echo "=================="

# Count working components
WORKING=0
TOTAL=0

((TOTAL++))
if python3 -c "import django" 2>/dev/null; then ((WORKING++)); fi

((TOTAL++))
if python3 -c "import fitz" 2>/dev/null; then ((WORKING++)); fi

((TOTAL++))
if python3 -c "import docx" 2>/dev/null; then ((WORKING++)); fi

((TOTAL++))
if python3 -c "import openpyxl" 2>/dev/null; then ((WORKING++)); fi

((TOTAL++))
if python3 -c "import pptx" 2>/dev/null; then ((WORKING++)); fi

((TOTAL++))
if python3 -c "import PIL" 2>/dev/null; then ((WORKING++)); fi

((TOTAL++))
if python3 -c "import pytesseract" 2>/dev/null; then ((WORKING++)); fi

((TOTAL++))
if python3 -c "import ebooklib" 2>/dev/null; then ((WORKING++)); fi

((TOTAL++))
if python3 -c "import bs4" 2>/dev/null; then ((WORKING++)); fi

((TOTAL++))
if python3 -c "import google.generativeai" 2>/dev/null; then ((WORKING++)); fi

((TOTAL++))
if command -v tesseract &> /dev/null; then ((WORKING++)); fi

print_green "✅ Working: $WORKING/$TOTAL components"

if [ $WORKING -eq $TOTAL ]; then
    print_green "🎉 All components are working! Ready to translate!"
elif [ $WORKING -ge 5 ]; then
    print_yellow "⚠️  Most components working. Some optional features may be limited."
else
    print_red "❌ Many components not working. Run setup.sh to fix."
fi

echo ""
print_blue "🚀 Quick Actions:"
echo "   Start server: ./start.sh"
echo "   Run setup: ./setup.sh"
echo "   Activate venv: source venv/bin/activate"
