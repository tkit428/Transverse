#!/usr/bin/env python3
"""
Google Gemini API Translation Service.
Uses Google's Gemini API for translation.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to path to import the base class
sys.path.append(str(Path(__file__).parent.parent))
from services import BaseTranslationService

class GeminiTranslationService(BaseTranslationService):
    def __init__(self):
        super().__init__()
        self.service_name = "Google Gemini API"
        self.client = None
        self.api_key = None
        
    def load_service(self):
        """Load the Google Gemini API client."""
        if self.is_loaded:
            return
            
        try:
            # Check for API key in environment variables
            self.api_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
            
            if not self.api_key:
                # Check for API key in a config file
                config_file = Path(__file__).parent.parent.parent / "config" / "gemini_api_key.txt"
                if config_file.exists():
                    with open(config_file, 'r') as f:
                        self.api_key = f.read().strip()
            
            if not self.api_key:
                raise ValueError(
                    "Google Gemini API key not found. Please set GEMINI_API_KEY environment variable "
                    "or create a config/gemini_api_key.txt file with your API key."
                )
            
            # Import and configure Google Gemini
            from google import genai
            
            # Initialize the client
            self.client = genai.Client(api_key=self.api_key)
            
            self.is_loaded = True
            print("✓ Google Gemini API translation service loaded successfully!")
            
        except ImportError:
            raise ImportError(
                "Google Generative AI library not installed. "
                "Install with: pip install google-genai"
            )
        except Exception as e:
            print(f"✗ Error loading Google Gemini API: {str(e)}")
            raise e
    
    def translate(self, text, target_language):
        """
        Translate text to target language using Google Gemini API.
        
        Args:
            text (str): Text to translate
            target_language (str): Target language (e.g., "French", "Spanish", "German")
            
        Returns:
            str: Translated text
        """
        if not self.is_loaded:
            self.load_service()
        
        try:
            # Create prompt for translation
            prompt = f"""Translate the following text to {target_language}. 
Only output the translated text, no explanations or additional formatting:

{text}"""
            
            # Generate translation using Gemini 2.5 Flash
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )
            
            if response.text:
                translated_text = response.text.strip()
                
                # Clean up any potential formatting
                if translated_text.startswith('"') and translated_text.endswith('"'):
                    translated_text = translated_text[1:-1]
                
                return translated_text
            else:
                return f"Translation failed: No response from Gemini API"
                
        except Exception as e:
            print(f"Google Gemini API translation error: {str(e)}")
            return f"Translation failed: {str(e)}"
    
    def is_available(self):
        """Check if the Google Gemini API service is available."""
        try:
            from google import genai
            # Check if API key is available
            api_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
            if api_key:
                return True
            
            # Check for API key file
            config_file = Path(__file__).parent.parent.parent / "config" / "gemini_api_key.txt"
            return config_file.exists()
        except ImportError:
            return False
    
    def get_service_info(self):
        """Get information about this service."""
        info = super().get_service_info()
        info.update({
            "requires_api_key": True,
            "api_key_env_vars": ["GEMINI_API_KEY", "GOOGLE_API_KEY"],
            "api_key_file": "config/gemini_api_key.txt",
            "dependencies": ["google-genai"],
            "model": "gemini-2.5-flash",
            "cost": "Pay-per-use",
            "speed": "Very Fast (API call)",
            "languages_supported": "100+",
        })
        return info

# Create global instance
gemini_service = GeminiTranslationService()
