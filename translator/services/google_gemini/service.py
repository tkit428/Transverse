#!/usr/bin/env python3
"""
Google Gemini API Translation Service.
Uses Google's Gemini API for translation.
"""

import sys
import json
import requests
from pathlib import Path

# Add the translator directory to Python path
translator_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(translator_dir))

from services import BaseTranslationService

class GeminiTranslationService(BaseTranslationService):
    def __init__(self):
        super().__init__()
        self.service_name = "Google Gemini 2.5 Flash"
        self.api_key = None
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
        
    def load_api_key(self):
        """Load API key from file."""
        try:
            # Try the most common path first
            api_key_file = Path.cwd() / "translator" / "config" / "gemini_api_key.txt"
            if not api_key_file.exists():
                # Fallback to absolute path
                api_key_file = Path("/home/tkit/Transverse/translator/config/gemini_api_key.txt")

            if api_key_file.exists():
                with open(api_key_file, 'r') as f:
                    self.api_key = f.read().strip()
                return True
            return False
        except Exception as e:
            print(f"Error loading API key: {e}")
            return False
    
    def is_available(self):
        """Check if the Gemini API service is available."""
        if not self.api_key:
            self.load_api_key()
        return self.api_key is not None
    
    def load_service(self):
        """Load/initialize the service."""
        if not self.is_available():
            raise Exception("Gemini API key not available")
        self.is_loaded = True
    
    def translate(self, text, target_language):
        """Translate text using Google Gemini API."""
        if not self.is_available():
            return "Translation failed: Gemini API not available - check API key"
        
        if not text or text.strip() == "":
            return ""

        prompt = f"Translate the following text to {target_language}. Only return the translated text, no explanations:\n\n{text}"
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 8192,
            }
        }
        
        try:
            url = f"{self.api_url}?key={self.api_key}"
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        parts = candidate['content']['parts']
                        if len(parts) > 0 and 'text' in parts[0]:
                            translated_text = parts[0]['text'].strip()
                            return translated_text
                
                return "Translation failed: Unexpected API response format"
            else:
                return f"Translation failed: API request failed with status {response.status_code}"
                
        except Exception as e:
            return f"Translation failed: {str(e)}"
