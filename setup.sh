#!/bin/bash

# Transverse - Complete Setup Script
# This script sets up the entire Transverse application environment

set -e  # Exit on any error

echo "🚀 Transverse - Complete Setup Script"
echo "======================================"

# Function to print colored output
print_green() {
    echo -e "\033[0;32m$1\033[0m"
}

print_yellow() {
    echo -e "\033[1;33m$1\033[0m"
}

print_red() {
    echo -e "\033[0;31m$1\033[0m"
}

print_blue() {
    echo -e "\033[0;34m$1\033[0m"
}

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    print_red "❌ Error: This script should be run from the Transverse project root directory"
    print_red "   Please navigate to the directory containing requirements.txt"
    exit 1
fi

print_green "✅ Found project files - starting setup..."

# Create Python virtual environment
print_blue "🐍 Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_green "✅ Created virtual environment"
else
    print_yellow "⚠️  Virtual environment already exists, skipping creation"
fi

# Activate virtual environment
print_blue "🔄 Activating virtual environment..."
source venv/bin/activate
print_green "✅ Virtual environment activated"

# Upgrade pip
print_blue "📦 Upgrading pip..."
pip install --upgrade pip
print_green "✅ Pip upgraded"

# Install core Python dependencies
print_blue "📦 Installing core Python dependencies..."
pip install -r requirements.txt
print_green "✅ Core dependencies installed"

# Install Google Gemini API
print_blue "🌐 Installing Google Gemini API dependencies..."
pip install "google-generativeai>=0.3.0"
print_green "✅ Google Gemini API installed"

# Optional: Install local transformer dependencies (commented out by default)
print_yellow "🤖 Local Transformer dependencies (optional):"
echo "   To install local AI model support, run:"
echo "   pip install torch==2.1.0 transformers==4.35.0 accelerate==0.24.0 bitsandbytes==0.41.2"
echo ""

# Install Tesseract OCR
print_blue "🔍 Installing Tesseract OCR for image text extraction..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if command -v brew &> /dev/null; then
        brew install tesseract
        print_green "✅ Tesseract installed via Homebrew"
    else
        print_red "❌ Homebrew not found. Please install Tesseract manually:"
        echo "   Visit: https://github.com/tesseract-ocr/tesseract"
        echo "   Or install Homebrew first: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v apt-get &> /dev/null; then
        print_blue "🔄 Updating package list..."
        sudo apt-get update
        print_blue "📦 Installing Tesseract..."
        sudo apt-get install -y tesseract-ocr
        print_green "✅ Tesseract installed via apt-get"
    elif command -v yum &> /dev/null; then
        sudo yum install -y tesseract
        print_green "✅ Tesseract installed via yum"
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y tesseract
        print_green "✅ Tesseract installed via dnf"
    else
        print_red "❌ Package manager not found. Please install Tesseract manually:"
        echo "   For Ubuntu/Debian: sudo apt-get install tesseract-ocr"
        echo "   For CentOS/RHEL: sudo yum install tesseract"
        echo "   For Fedora: sudo dnf install tesseract"
    fi
else
    print_red "❌ Unsupported OS for automatic Tesseract installation."
    echo "   Please install Tesseract manually:"
    echo "   Visit: https://github.com/tesseract-ocr/tesseract"
    echo "   Or use your system's package manager"
fi

# Test installations
print_blue "🧪 Testing installations..."

# Test Django
python3 -c "import django; print(f'✅ Django {django.get_version()}')" 2>/dev/null || print_red "❌ Django not working"

# Test PyMuPDF
python3 -c "import fitz; print('✅ PyMuPDF (fitz)')" 2>/dev/null || print_red "❌ PyMuPDF not working"

# Test other libraries
python3 -c "import docx; print('✅ python-docx')" 2>/dev/null || print_yellow "⚠️  python-docx not working"
python3 -c "import openpyxl; print('✅ openpyxl')" 2>/dev/null || print_yellow "⚠️  openpyxl not working"
python3 -c "import pptx; print('✅ python-pptx')" 2>/dev/null || print_yellow "⚠️  python-pptx not working"
python3 -c "import PIL; print('✅ Pillow')" 2>/dev/null || print_yellow "⚠️  Pillow not working"
python3 -c "import pytesseract; print('✅ pytesseract')" 2>/dev/null || print_yellow "⚠️  pytesseract not working"
python3 -c "import ebooklib; print('✅ EbookLib')" 2>/dev/null || print_yellow "⚠️  EbookLib not working"
python3 -c "import bs4; print('✅ BeautifulSoup4')" 2>/dev/null || print_yellow "⚠️  BeautifulSoup4 not working"

# Test Google Gemini API
python3 -c "import google.generativeai; print('✅ Google Gemini API')" 2>/dev/null || print_yellow "⚠️  Google Gemini API not working (API key needed for full functionality)"

# Test Tesseract
if command -v tesseract &> /dev/null; then
    print_green "✅ Tesseract OCR found"
else
    print_yellow "⚠️  Tesseract OCR not found in PATH"
fi

# Create necessary directories
print_blue "📁 Creating necessary directories..."
mkdir -p transverse_backend/uploads/temp
mkdir -p logs
print_green "✅ Directories created"

# Create .env template
print_blue "⚙️  Creating environment configuration template..."
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# Transverse Environment Configuration

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Google Gemini API (optional - only needed if using Gemini)
GEMINI_API_KEY=your-gemini-api-key-here

# File Upload Settings
MAX_FILE_SIZE=10485760  # 10MB in bytes
ALLOWED_FILE_TYPES=pdf,docx,xlsx,pptx,txt,jpg,jpeg,png,gif,bmp,tiff,webp,epub,mobi,fb2,cbz,svg,xps

# Translation Settings
DEFAULT_TARGET_LANGUAGE=en
MAX_PAGES_PER_TRANSLATION=50
EOF
    print_green "✅ Created .env template"
else
    print_yellow "⚠️  .env file already exists, skipping creation"
fi

# Create activation script
print_blue "🔧 Creating virtual environment activation helper..."
cat > activate_venv.sh << 'EOF'
#!/bin/bash
# Quick activation script for the Transverse virtual environment

echo "🐍 Activating Transverse virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated!"
echo ""
echo "🚀 To start the Django server:"
echo "   python manage.py runserver 127.0.0.1:8000"
echo ""
echo "📖 To test file upload:"
echo "   Visit: http://127.0.0.1:8000/test_upload.html"
echo ""
echo "🔧 To deactivate:"
echo "   deactivate"
EOF

chmod +x activate_venv.sh
print_green "✅ Created activation helper script"

# Final summary
echo ""
print_green "🎉 Setup Complete!"
echo "=================="

echo ""
print_blue "📋 What was installed:"
echo "   ✅ Python virtual environment"
echo "   ✅ Django web framework"
echo "   ✅ File processing libraries (PDF, DOCX, XLSX, etc.)"
echo "   ✅ Google Gemini API client"
echo "   ✅ Tesseract OCR (if supported)"
echo "   ✅ All necessary directories"

echo ""
print_blue "🚀 Next steps:"
echo "   1. Activate the virtual environment:"
echo "      source venv/bin/activate"
echo "      # OR use the helper script:"
echo "      ./activate_venv.sh"

echo ""
echo "   2. Configure your environment:"
echo "      Edit the .env file with your settings"
echo "      For Google Gemini API, get a key from:"
echo "      https://makersuite.google.com/app/apikey"

echo ""
echo "   3. Start the Django server:"
echo "      python manage.py runserver 127.0.0.1:8000"

echo ""
echo "   4. Test the application:"
echo "      Visit: http://127.0.0.1:8000"
echo "      Test file upload: http://127.0.0.1:8000/test_upload.html"

echo ""
print_blue "📄 Supported file types:"
echo "   📄 Documents: PDF, DOCX, XLSX, PPTX, TXT"
echo "   🎨 Images: JPG, PNG, GIF, BMP, TIFF, WebP"
echo "   📚 E-books: EPUB, MOBI, FB2"
echo "   🎯 Other: CBZ, SVG, XPS"

echo ""
print_yellow "⚠️  Notes:"
echo "   • Some file types may require additional system libraries"
echo "   • Google Gemini API needs a valid API key for translation"
echo "   • Tesseract OCR is required for image text extraction"
echo "   • The application will gracefully handle missing optional dependencies"

echo ""
print_green "🎯 Happy translating!"

# Deactivate virtual environment
deactivate
