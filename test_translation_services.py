#!/usr/bin/env python3
"""
Test script for the new modular translation services.
"""

import sys
import os
from pathlib import Path

# Add the translator path to Python path
translator_path = Path(__file__).parent / "translator"
if str(translator_path) not in sys.path:
    sys.path.insert(0, str(translator_path))

def test_services():
    """Test the translation services."""
    
    print("Testing Translation Services")
    print("=" * 40)
    
    try:
        from services.manager import translation_manager
        
        # Get service info
        print("1. Available Services:")
        available = translation_manager.get_available_services()
        all_info = translation_manager.get_all_services_info()
        
        for service_name, info in all_info.items():
            status = "✓ Available" if service_name in available else "✗ Not Available"
            print(f"   {service_name}: {status}")
            print(f"      - Name: {info.get('name', 'Unknown')}")
            print(f"      - Description: {info.get('description', 'No description')}")
            if not info.get('available', False):
                if 'requires_api_key' in info and info['requires_api_key']:
                    print(f"      - Requires API Key: {info.get('api_key_env_vars', [])}")
        
        print()
        
        if not available:
            print("✗ No translation services are available!")
            print("  Make sure dependencies are installed:")
            print("  - For local transformer: pip install torch transformers accelerate bitsandbytes")
            print("  - For Google Gemini: pip install google-generativeai")
            return False
        
        # Test translation with first available service
        test_service = available[0]
        print(f"2. Testing Translation with '{test_service}':")
        
        # Set the service
        translation_manager.set_service(test_service)
        
        # Test text
        test_text = "Hello, how are you?"
        target_language = "Spanish"
        
        print(f"   Input: {test_text}")
        print(f"   Target: {target_language}")
        print("   Translating... (this may take a moment for first load)")
        
        # Perform translation
        translated = translation_manager.translate(test_text, target_language)
        
        print(f"   Output: {translated}")
        
        if "Translation failed" not in translated:
            print("   ✓ Translation successful!")
        else:
            print("   ✗ Translation failed!")
            return False
        
        print()
        
        # Test service switching if multiple services available
        if len(available) > 1:
            print("3. Testing Service Switching:")
            for service in available:
                print(f"   Setting service to: {service}")
                success = translation_manager.set_service(service)
                if success:
                    current = translation_manager.get_current_service()
                    print(f"   ✓ Current service: {current.service_name}")
                else:
                    print(f"   ✗ Failed to set service: {service}")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import Error: {e}")
        print("  Make sure you're running from the project root directory")
        return False
    except Exception as e:
        print(f"✗ Test Error: {e}")
        return False

def test_backend_integration():
    """Test backend integration."""
    
    print("4. Testing Backend Integration:")
    
    try:
        # Add backend path
        backend_path = Path(__file__).parent / "transverse_backend"
        if str(backend_path) not in sys.path:
            sys.path.insert(0, str(backend_path))
        
        from translation_service import translation_service
        
        # Test if the wrapper works
        print("   Testing translation service wrapper...")
        
        if hasattr(translation_service, 'manager'):
            print("   ✓ New modular service manager loaded")
            available = translation_service.get_available_services()
            print(f"   Available services: {available}")
        else:
            print("   ✓ Legacy translation service loaded")
        
        # Test translation
        test_text = "Good morning"
        result = translation_service.translate(test_text, "French")
        print(f"   Translation test: '{test_text}' -> '{result}'")
        
        if "Translation failed" not in result:
            print("   ✓ Backend integration successful!")
            return True
        else:
            print("   ✗ Backend translation failed")
            return False
        
    except Exception as e:
        print(f"   ✗ Backend integration error: {e}")
        return False

if __name__ == "__main__":
    print("Transverse Translation Services Test")
    print("====================================")
    print()
    
    success = test_services()
    
    if success:
        success = test_backend_integration()
    
    print()
    if success:
        print("✓ All tests passed! Translation services are working correctly.")
    else:
        print("✗ Some tests failed. Check the output above for details.")
        sys.exit(1)
