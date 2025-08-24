"""Google Gemini API Translation Service"""

# Import with error handling
try:
    from .service import GeminiTranslationService
    # Create global instance
    gemini_service = GeminiTranslationService()
except ImportError as e:
    print(f"Failed to import GeminiTranslationService: {e}")
    # Create a mock service for fallback
    class MockGeminiService:
        def __init__(self):
            self.service_name = "Mock Gemini Service"
        def is_available(self):
            return False
        def translate(self, text, target_language):
            return f"Mock translation: {text} -> {target_language}"
    gemini_service = MockGeminiService()
