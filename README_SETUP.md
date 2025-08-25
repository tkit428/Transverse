# Transverse - Setup Guide

## 🚀 Quick Setup

### One-Command Setup
```bash
# Make sure you're in the project root directory
cd /path/to/Transverse

# Run the complete setup script
./setup.sh
```

That's it! The script will handle everything automatically.

## 📋 What the Setup Script Does

### 🐍 Python Environment
- ✅ Creates a virtual environment (`venv`)
- ✅ Installs all required Python packages
- ✅ Upgrades pip to latest version

### 📦 Dependencies Installed
- **Core Framework**: Django, DRF, CORS headers
- **File Processing**:
  - PyMuPDF (PDF handling)
  - python-docx (Word documents)
  - openpyxl (Excel files)
  - python-pptx (PowerPoint)
  - Pillow (Images)
  - pytesseract (OCR)
  - EbookLib (E-books)
  - BeautifulSoup4 (HTML/XML)
- **AI/ML**: Google Gemini API client
- **System**: Tesseract OCR (when possible)

### 🔧 Configuration
- ✅ Creates `.env` template with all settings
- ✅ Creates helper activation script
- ✅ Sets up necessary directories
- ✅ Tests all installations

### 🧪 Verification
- ✅ Tests each installed library
- ✅ Verifies Tesseract OCR installation
- ✅ Confirms Django is working

## 🚀 After Setup

### 1. Activate Virtual Environment
```bash
# Option 1: Direct activation
source venv/bin/activate

# Option 2: Use helper script
./activate_venv.sh
```

### 2. Configure Environment
Edit the `.env` file with your settings:
```bash
nano .env  # or your preferred editor
```

### 3. Add Google Gemini API Key (Optional)
Get an API key from: https://makersuite.google.com/app/apikey

Set it in `.env`:
```bash
GEMINI_API_KEY=your_actual_api_key_here
```

### 4. Start the Server
```bash
python manage.py runserver 127.0.0.1:8000
```

### 5. Test the Application
- Main app: http://127.0.0.1:8000
- File upload test: http://127.0.0.1:8000/test_upload.html

## 📄 Supported File Types

After setup, you can process these file types:

| Category | Formats | Requirements |
|----------|---------|--------------|
| **Documents** | PDF, DOCX, XLSX, PPTX, TXT | All included |
| **Images** | JPG, PNG, GIF, BMP, TIFF, WebP | Pillow + Tesseract |
| **E-books** | EPUB, MOBI, FB2 | EbookLib |
| **Other** | CBZ, SVG, XPS | Various libraries |

## 🔧 Manual Installation (Alternative)

If you prefer manual setup:

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
pip install "google-generativeai>=0.3.0"

# 3. Install system dependencies
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr

# macOS:
brew install tesseract

# 4. Create directories
mkdir -p transverse_backend/uploads/temp logs

# 5. Copy and edit .env file
cp .env.example .env
nano .env
```

## 🆘 Troubleshooting

### Common Issues

**1. Permission denied when running setup.sh**
```bash
chmod +x setup.sh
./setup.sh
```

**2. Tesseract installation failed**
```bash
# Manual installation
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr

# macOS:
brew install tesseract

# Windows: Download from GitHub
```

**3. Virtual environment issues**
```bash
# Remove and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**4. Google Gemini API not working**
```bash
# Make sure you have the API key
export GEMINI_API_KEY="your-api-key"

# Or add it to .env file
echo "GEMINI_API_KEY=your-api-key" >> .env
```

### Testing Installations

```bash
# Test Django
python3 -c "import django; print('Django OK')"

# Test file processing
python3 -c "import fitz; print('PDF OK')"
python3 -c "import docx; print('Word OK')"

# Test AI
python3 -c "import google.generativeai; print('Gemini OK')"
```

## 📞 Support

If you encounter issues:

1. Check the error messages during setup
2. Verify all system requirements are met
3. Test individual components as shown above
4. Check the logs in the `logs/` directory

## 🎯 Next Steps

After successful setup:

1. **Upload files** via the web interface
2. **Select pages** to translate
3. **Choose target language**
4. **Click translate** and wait for processing
5. **Download** the translated file

Happy translating! 🎉
