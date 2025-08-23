#!/usr/bin/env python3
"""
Translation services package.
Contains different translation service implementations.
"""

from abc import ABC, abstractmethod

class BaseTranslationService(ABC):
    """Abstract base class for translation services."""
    
    def __init__(self):
        self.service_name = "base"
        self.is_loaded = False
    
    @abstractmethod
    def load_service(self):
        """Load/initialize the translation service."""
        pass
    
    @abstractmethod
    def translate(self, text, target_language):
        """
        Translate text to target language.
        
        Args:
            text (str): Text to translate
            target_language (str): Target language (e.g., "French", "Spanish", "German")
            
        Returns:
            str: Translated text
        """
        pass
    
    @abstractmethod
    def is_available(self):
        """Check if the service is available/configured."""
        pass
    
    def get_service_info(self):
        """Get information about this translation service."""
        return {
            'name': self.service_name,
            'loaded': self.is_loaded,
            'available': self.is_available()
        }
