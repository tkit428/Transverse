#!/usr/bin/env python3
"""
Translation service that integrates the optimized translator model.
"""

import os
import sys
import time
import torch
from pathlib import Path

# Add the translator directory to Python path
TRANSLATOR_DIR = Path(__file__).parent.parent / "translator"
sys.path.append(str(TRANSLATOR_DIR))

class TranslationService:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        
    def load_model(self):
        """Load the translation model if not already loaded."""
        if self.model_loaded:
            return
            
        try:
            print("Loading translation model...")
            from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
            
            model_name = "JungZoona/T3Q-qwen2.5-14b-v1.0-e3"
            
            # Configure 4-bit quantization for minimal VRAM usage
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
            )
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            
            # Load model with aggressive optimizations
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                quantization_config=bnb_config,
                device_map="auto",
                torch_dtype=torch.float16,
                trust_remote_code=True,
                low_cpu_mem_usage=True,
            )
            
            self.model_loaded = True
            print("Translation model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise e
    
    def translate(self, text, target_language):
        """
        Translate text to target language.
        
        Args:
            text (str): Text to translate
            target_language (str): Target language (e.g., "French", "Spanish", "German")
            
        Returns:
            str: Translated text
        """
        if not self.model_loaded:
            self.load_model()
        
        try:
            # Create prompt with the specific format you requested
            prompt = f'Only output the translated words. Translate "{text}" to {target_language}'
            
            messages = [{"role": "user", "content": prompt}]
            
            # Apply chat template
            inputs = self.tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=True,
                return_dict=True,
                return_tensors="pt",
            ).to(self.model.device)
            
            # Generate with optimized settings
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=50,  # Slightly more tokens for longer sentences
                    do_sample=False,
                    temperature=0.1,
                    pad_token_id=self.tokenizer.eos_token_id,
                    use_cache=True,
                )
            
            # Decode only the new tokens
            generated_text = self.tokenizer.decode(
                outputs[0][inputs["input_ids"].shape[-1]:], 
                skip_special_tokens=True
            )
            
            # Clean up the output - only return the translated text
            translated_text = generated_text.strip()
            
            # Remove any extra explanations or formatting
            if translated_text.startswith('"') and translated_text.endswith('"'):
                translated_text = translated_text[1:-1]
            
            return translated_text
            
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return f"Translation failed: {str(e)}"

# Global instance
translation_service = TranslationService()
