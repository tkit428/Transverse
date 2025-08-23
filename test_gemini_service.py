#!/usr/bin/env python3
"""
Simple test for Gemini service availability.
"""

import sys
from pathlib import Path

# Add the translator path to Python path
translator_path = Path(__file__).parent / "translator"
if str(translator_path) not in sys.path:
    sys.path.insert(0, str(translator_path))

def test_gemini_service():
    """Test if Gemini service is available."""
    
    print("Testing Gemini Service Availability")
    print("=" * 40)
    
    try:
        from services.google_gemini.service import gemini_service
        
        print("✓ Gemini service imported successfully")
        
        # Check if it's available
        available = gemini_service.is_available()
        print(f"Service available: {available}")
        
        if available:
            print("✓ Gemini service is available")
            
            # Try to load the service
            print("Loading Gemini service...")
            gemini_service.load_service()
            print(f"Service loaded: {gemini_service.is_loaded}")
            
            if gemini_service.is_loaded:
                print("✓ Gemini service loaded successfully")
                
                # Test translation
                test_text = "Hello world"
                print(f"Testing translation: '{test_text}' -> Spanish")
                result = gemini_service.translate(test_text, "Spanish")
                print(f"Result: {result}")
                
                if "Translation failed" not in result:
                    print("✓ Gemini translation test successful!")
                    return True
                else:
                    print("✗ Gemini translation test failed")
                    return False
            else:
                print("✗ Failed to load Gemini service")
                return False
        else:
            print("✗ Gemini service not available")
            print("Possible reasons:")
            print("  - google-genai package not installed")
            print("  - API key not found or invalid")
            print("  - Network connectivity issues")
            return False
            
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Make sure you have installed: pip install google-genai")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_gemini_service()
    if not success:
        print("\nTo fix Gemini service issues:")
        print("1. Install dependencies: pip install google-genai")
        print("2. Check API key in translator/config/gemini_api_key.txt")
        print("3. Verify internet connectivity")
        sys.exit(1)
    else:
        print("\n✓ Gemini service is working correctly!")
