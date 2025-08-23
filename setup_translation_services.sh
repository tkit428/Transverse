#!/bin/bash
"""
Setup script for the new modular translation services.
"""

echo "Setting up modular translation services..."

# Check if we're in the right directory
if [ ! -d "translator/services" ]; then
    echo "Error: This script should be run from the project root directory"
    exit 1
fi

echo "✓ Translation services directory structure found"

# Check Python dependencies for local transformer
echo "Checking local transformer dependencies..."
python3 -c "import torch; import transformers; print('✓ Local transformer dependencies available')" 2>/dev/null || echo "⚠ Local transformer dependencies missing - install with: pip install torch transformers accelerate bitsandbytes"

# Check if Google Gemini dependencies are available
echo "Checking Google Gemini API dependencies..."
python3 -c "import google.generativeai; print('✓ Google Gemini API dependencies available')" 2>/dev/null || echo "⚠ Google Gemini API dependencies missing - install with: pip install google-generativeai"

# Test the service manager
echo "Testing service manager..."
cd translator
python3 -c "
try:
    from services.manager import translation_manager
    services = translation_manager.get_available_services()
    print(f'✓ Service manager loaded. Available services: {services}')
    
    if 'local_transformer' in services:
        print('  - Local Transformer: Available')
    else:
        print('  - Local Transformer: Not available')
        
    if 'gemini' in services:
        print('  - Google Gemini API: Available')
    else:
        print('  - Google Gemini API: Not available (check API key)')
        
except Exception as e:
    print(f'✗ Error testing service manager: {e}')
"
cd ..

echo ""
echo "Setup complete!"
echo ""
echo "Available services:"
echo "  1. Local Transformer - Uses local HuggingFace models"
echo "  2. Google Gemini API - Uses Google's Gemini API (requires API key)"
echo ""
echo "To use Google Gemini API:"
echo "  1. Get an API key from: https://makersuite.google.com/app/apikey"
echo "  2. Set environment variable: export GEMINI_API_KEY='your_api_key'"
echo "  3. Or create file: translator/config/gemini_api_key.txt"
echo ""
echo "The system will default to local transformer if available."
