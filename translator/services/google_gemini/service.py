#!/usr/bin/env python3
"""
Google Gemini API Translation Service.
Uses Google's Gemini API for translation.
"""

import sys
import json
import requests
import time
import random
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
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

        # Minimal rate limiting - only one request per page now
        self.max_requests_per_minute = 4000  # User's reported quota
        self.max_requests_per_second = 50    # Very conservative
        self.request_history = []
        self.last_request_time = 0
        self.min_request_interval = 1.0      # 1 second between requests
        
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

    def _wait_for_rate_limit(self):
        """Wait if necessary to respect rate limits."""
        current_time = time.time()

        # Clean old request history (older than 1 minute)
        self.request_history = [t for t in self.request_history if current_time - t < 60]

        wait_time = 0

        # Check per-second rate limit
        recent_requests = [t for t in self.request_history if current_time - t < 1]
        if len(recent_requests) >= self.max_requests_per_second:
            # Calculate wait time to stay under per-second limit
            oldest_recent = min(recent_requests)
            second_wait = 1.0 - (current_time - oldest_recent)
            if second_wait > 0:
                print(f"[Gemini API] Rate limit: Per-second limit hit ({len(recent_requests)} requests in last second)")
                print(f"[Gemini API] Waiting {second_wait:.2f} seconds for per-second limit")
                wait_time = max(wait_time, second_wait)

        # Check per-minute rate limit
        if len(self.request_history) >= self.max_requests_per_minute:
            # Calculate wait time to stay under per-minute limit
            oldest_request = min(self.request_history)
            minute_wait = 60.0 - (current_time - oldest_request)
            if minute_wait > 0:
                print(f"[Gemini API] Rate limit: Per-minute limit hit ({len(self.request_history)} requests in last minute)")
                print(f"[Gemini API] Waiting {minute_wait:.2f} seconds for per-minute limit")
                wait_time = max(wait_time, minute_wait)

        # Also enforce minimum interval between requests
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            interval_wait = self.min_request_interval - time_since_last_request
            print(f"[Gemini API] Enforcing minimum interval: Waiting {interval_wait:.3f} seconds")
            wait_time = max(wait_time, interval_wait)

        if wait_time > 0:
            print(f"[Gemini API] Total wait time: {wait_time:.2f} seconds")
            time.sleep(wait_time)

        self.last_request_time = time.time()
        self.request_history.append(time.time())

        print(f"[Gemini API] Request allowed - {len(self.request_history)} total requests in last minute")

    def translate(self, text, target_language):
        """Translate text using Google Gemini API with rate limiting."""
        if not self.is_available():
            return "Translation failed: Gemini API not available - check API key"

        if not text or text.strip() == "":
            return ""

                # Wait for rate limiting before making request
        self._wait_for_rate_limit()

        # Check if this is a batch translation (contains block markers)
        if "__BLOCK_" in text and "__" in text:
            prompt = f"""Translate the following text to {target_language}.

IMPORTANT: This text contains special markers like "__BLOCK_1__", "__BLOCK_2__", etc.
- Keep ALL markers exactly as they are (do not translate them)
- Only translate the content between the markers
- Preserve the structure and formatting
- Do not add explanations or additional text

Text to translate:
{text}"""
        else:
            prompt = f"Translate the following text to {target_language}. Only return the translated text, no explanations:\n\n{text}"

        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 8192,
            }
        }

        print(f"[Gemini API] Making translation request - {len(text)} characters to {target_language}")

        try:
            url = f"{self.api_url}?key={self.api_key}"
            start_time = time.time()
            response = requests.post(url, headers=headers, json=data, timeout=30)
            request_time = time.time() - start_time

            print(f"[Gemini API] Request completed in {request_time:.2f}s - Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        parts = candidate['content']['parts']
                        if len(parts) > 0 and 'text' in parts[0]:
                            translated_text = parts[0]['text'].strip()
                            print(f"[Gemini API] Translation successful - {len(text)} → {len(translated_text)} characters")
                            return translated_text

                print(f"[Gemini API] Unexpected API response format")
                return "Translation failed: Unexpected API response format"
            elif response.status_code == 429:
                return f"Translation failed: Rate limit exceeded (429). Your API quota may be exceeded. Please wait and try again."
            elif response.status_code == 403:
                return f"Translation failed: API key invalid or quota exceeded (403). Please check your API key and billing."
            elif response.status_code == 500:
                return f"Translation failed: Server error (500). Please try again later."
            else:
                return f"Translation failed: API request failed with status {response.status_code}"

        except requests.exceptions.Timeout:
            return "Translation failed: Request timeout. The translation service is taking too long to respond."
        except requests.exceptions.ConnectionError:
            return "Translation failed: Connection error. Please check your internet connection."
        except Exception as e:
            return f"Translation failed: {str(e)}"
