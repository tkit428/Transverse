#!/bin/bash

echo "🚀 Setting up Transverse File Processing Environment..."

# Install Python packages
echo "📦 Installing Python packages..."
pip install -r requirements.txt

# Install Tesseract OCR for image text extraction
echo "🔍 Installing Tesseract OCR..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if command -v brew &> /dev/null; then
        brew install tesseract
        echo "✅ Tesseract installed via Homebrew"
    else
        echo "❌ Homebrew not found. Please install Tesseract manually:"
        echo "   Visit: https://github.com/tesseract-ocr/tesseract"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install tesseract-ocr
        echo "✅ Tesseract installed via apt-get"
    elif command -v yum &> /dev/null; then
        sudo yum install tesseract
        echo "✅ Tesseract installed via yum"
    else
        echo "❌ Package manager not found. Please install Tesseract manually"
    fi
else
    echo "❌ Unsupported OS. Please install Tesseract manually:"
    echo "   Visit: https://github.com/tesseract-ocr/tesseract"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Supported file types:"
echo "   📄 Documents: PDF, DOCX, XLSX, PPTX, TXT"
echo "   📚 E-books: EPUB, MOBI, FB2"
echo "   🎨 Comics: CBZ"
echo "   🖼️  Images: JPG, PNG, GIF, BMP, TIFF, WebP"
echo "   📊 Other: SVG, XPS, HWP"
echo ""
echo "🎯 To test file upload:"
echo "   1. Start Django server: python manage.py runserver"
echo "   2. Visit: http://127.0.0.1:8000/test_upload.html"
echo ""
echo "🔧 Note: Some file types may require additional setup:"
echo "   • XPS: Limited support (requires conversion tools)"
echo "   • MOBI: Requires additional libraries"
echo "   • HWP: Very limited Python support"
echo "   • FB2: Basic XML parsing support"
