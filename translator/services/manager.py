#!/usr/bin/env python3
"""
Translation Service Manager.
Manages multiple translation services and provides a unified interface.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Import the base class and services
from . import BaseTranslationService
from .google_gemini import gemini_service

class TranslationServiceManager:
    def __init__(self):
        self.services: Dict[str, BaseTranslationService] = {
            'gemini': gemini_service,
        }
        self.default_service = 'gemini'  # Only Gemini API available
        self.current_service = 'gemini'  # Force Gemini usage
        
    def get_available_services(self) -> List[str]:
        """Get list of available services."""
        available = []
        for name, service in self.services.items():
            if service.is_available():
                available.append(name)
        return available
    
    def get_service_info(self, service_name: str) -> Optional[Dict]:
        """Get information about a specific service."""
        if service_name in self.services:
            return self.services[service_name].get_service_info()
        return None
    
    def get_all_services_info(self) -> Dict[str, Dict]:
        """Get information about all services."""
        info = {}
        for name, service in self.services.items():
            info[name] = service.get_service_info()
            info[name]['available'] = service.is_available()
        return info
    
    def set_service(self, service_name: str) -> bool:
        """
        Set the active translation service.
        
        Args:
            service_name (str): Name of the service to use
            
        Returns:
            bool: True if service was set successfully
        """
        if service_name not in self.services:
            print(f"Unknown service: {service_name}")
            return False
            
        if not self.services[service_name].is_available():
            print(f"Service not available: {service_name}")
            return False
            
        self.current_service = service_name
        print(f"Translation service set to: {service_name}")
        return True
    
    def get_current_service(self) -> Optional[BaseTranslationService]:
        """Get the currently active service (always Gemini)."""
        if self.current_service and self.current_service in self.services:
            service = self.services[self.current_service]
            if service.is_available():
                return service

        # Force Gemini usage
        if 'gemini' in self.services and self.services['gemini'].is_available():
            self.current_service = 'gemini'
            return self.services['gemini']

        return None
    
    def translate(self, text: str, target_language: str, service_name: Optional[str] = None) -> str:
        """
        Translate text using Gemini API (only available service).

        Args:
            text (str): Text to translate
            target_language (str): Target language
            service_name (str, optional): Ignored - always uses Gemini

        Returns:
            str: Translated text
        """
        # Always use Gemini
        service = self.services.get('gemini')
        if not service or not service.is_available():
            return "Translation failed: Gemini API not available"

        try:
            return service.translate(text, target_language)
        except Exception as e:
            return f"Translation failed: {str(e)}"
    
    def load_service(self, service_name: Optional[str] = None) -> bool:
        """
        Load Gemini service (only available service).

        Args:
            service_name (str, optional): Ignored - always loads Gemini

        Returns:
            bool: True if service loaded successfully
        """
        # Always load Gemini
        service = self.services.get('gemini')
        if not service or not service.is_available():
            print("Gemini API not available - check API key")
            return False

        try:
            service.load_service()
            return True
        except Exception as e:
            print(f"Failed to load Gemini service: {str(e)}")
            return False

# Create global instance
translation_manager = TranslationServiceManager()

# Backwards compatibility - provide the old interface (always uses Gemini)
def load_model():
    """Load the Gemini translation service (backwards compatibility)."""
    return translation_manager.load_service()

def translate_text(text: str, target_language: str) -> str:
    """Translate text using Gemini API (backwards compatibility)."""
    return translation_manager.translate(text, target_language)
