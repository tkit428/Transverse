#!/usr/bin/env python3
"""
Local Transformer Translation Service.
Uses Hugging Face transformers for local translation.
"""

import os
import sys
import time
import torch
import shutil
from pathlib import Path

# Add the parent directory to path to import the base class
sys.path.append(str(Path(__file__).parent.parent))
from services import BaseTranslationService

class LocalTransformerService(BaseTranslationService):
    def __init__(self):
        super().__init__()
        self.service_name = "Local Transformer"
        self.model = None
        self.tokenizer = None
        self.model_name = "JungZoona/T3Q-qwen2.5-14b-v1.0-e3"
        self.local_model_path = Path(__file__).parent.parent.parent / "models" / self.model_name.replace("/", "_")
        
    def get_cache_paths(self):
        """Get potential cache paths for the model."""
        cache_paths = []
        
        # Common Hugging Face cache locations
        hf_cache_home = os.environ.get('HF_HOME', os.path.expanduser('~/.cache/huggingface'))
        transformers_cache = os.environ.get('TRANSFORMERS_CACHE', os.path.join(hf_cache_home, 'hub'))
        
        # Look for model in cache with different naming patterns
        model_cache_patterns = [
            f"models--{self.model_name.replace('/', '--')}",
            f"models--{self.model_name.replace('/', '--').lower()}",
        ]
        
        for pattern in model_cache_patterns:
            cache_path = Path(transformers_cache) / pattern
            if cache_path.exists():
                # Look for snapshots folder
                snapshots_path = cache_path / "snapshots"
                if snapshots_path.exists():
                    # Get the latest snapshot (usually the first one)
                    snapshot_dirs = [d for d in snapshots_path.iterdir() if d.is_dir()]
                    if snapshot_dirs:
                        latest_snapshot = max(snapshot_dirs, key=lambda x: x.stat().st_mtime)
                        cache_paths.append(latest_snapshot)
        
        return cache_paths
    
    def copy_model_from_cache(self):
        """Copy model from cache to local model folder if available."""
        cache_paths = self.get_cache_paths()
        
        if not cache_paths:
            print("No cached model found.")
            return False
            
        for cache_path in cache_paths:
            try:
                print(f"Found cached model at: {cache_path}")
                
                # Create local model directory
                self.local_model_path.mkdir(parents=True, exist_ok=True)
                
                # Check if local model already exists and is complete
                if self.is_model_complete(self.local_model_path):
                    print(f"Model already exists locally at: {self.local_model_path}")
                    return True
                
                # Copy model files from cache
                print(f"Copying model from cache to: {self.local_model_path}")
                
                # Copy all files from cache to local path
                for item in cache_path.iterdir():
                    if item.is_file():
                        shutil.copy2(item, self.local_model_path / item.name)
                        print(f"Copied: {item.name}")
                    elif item.is_dir():
                        shutil.copytree(item, self.local_model_path / item.name, dirs_exist_ok=True)
                        print(f"Copied directory: {item.name}")
                
                # Verify the copy was successful
                print(f"Verifying copied model at: {self.local_model_path}")
                if self.is_model_complete(self.local_model_path):
                    print("✓ Model successfully copied from cache!")
                    return True
                else:
                    print("⚠ Copied model appears incomplete")
                    # List what files we actually have
                    actual_files = [f.name for f in self.local_model_path.iterdir() if f.is_file()]
                    print(f"Actual files in local model dir: {actual_files}")
                    return False
                    
            except Exception as e:
                print(f"Error copying from cache {cache_path}: {str(e)}")
                continue
                
        return False
    
    def is_model_complete(self, model_path):
        """Check if model files are complete in the given path."""
        required_files = ['config.json', 'tokenizer_config.json']
        
        # Check for required config files
        for req_file in required_files:
            if not (model_path / req_file).exists():
                print(f"Missing required file: {req_file}")
                return False
        
        # Check for model files - support both safetensors and pytorch formats
        model_file_patterns = [
            'model.safetensors',           # Single safetensors file
            'pytorch_model.bin',           # Single pytorch file
            'model.safetensors.index.json', # Multi-part safetensors
            'pytorch_model-00001-of-*.bin'  # Multi-part pytorch
        ]
        
        has_model_file = False
        
        # Check for single model files
        if (model_path / 'model.safetensors').exists():
            print("Found single safetensors model file")
            has_model_file = True
        elif (model_path / 'pytorch_model.bin').exists():
            print("Found single pytorch model file")
            has_model_file = True
        
        # Check for multi-part safetensors
        elif (model_path / 'model.safetensors.index.json').exists():
            # Verify that safetensors parts exist
            try:
                import json
                with open(model_path / 'model.safetensors.index.json', 'r') as f:
                    index_data = json.load(f)
                
                if 'weight_map' in index_data:
                    # Get unique safetensors files
                    safetensor_files = set(index_data['weight_map'].values())
                    missing_files = []
                    
                    for safetensor_file in safetensor_files:
                        if not (model_path / safetensor_file).exists():
                            missing_files.append(safetensor_file)
                    
                    if missing_files:
                        print(f"Missing safetensors files: {missing_files}")
                        has_model_file = False
                    else:
                        print(f"Found complete multi-part safetensors model ({len(safetensor_files)} files)")
                        has_model_file = True
                else:
                    print("Invalid safetensors index file")
                    has_model_file = False
            except Exception as e:
                print(f"Error reading safetensors index: {e}")
                has_model_file = False
        
        # Check for multi-part pytorch files
        elif list(model_path.glob('pytorch_model-00001-of-*.bin')):
            pytorch_files = list(model_path.glob('pytorch_model-*.bin'))
            print(f"Found multi-part pytorch model ({len(pytorch_files)} files)")
            has_model_file = True
        
        if not has_model_file:
            print("No valid model files found")
            available_files = [f.name for f in model_path.iterdir() if f.is_file()]
            print(f"Available files: {available_files}")
        
        return has_model_file
        
    def load_service(self):
        """Load the translation model with priority: local models folder -> cache -> download."""
        if self.is_loaded:
            return
            
        try:
            print("Loading Local Transformer translation model...")
            from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
            
            # Priority 1: Check local models folder first
            model_path_to_use = self.model_name
            
            if self.is_model_complete(self.local_model_path):
                print(f"✓ Found complete model in local folder: {self.local_model_path}")
                model_path_to_use = str(self.local_model_path)
            else:
                print(f"✗ No complete model found in local folder: {self.local_model_path}")
                
                # Priority 2: Check cache and copy if available
                if self.copy_model_from_cache():
                    print(f"✓ Successfully copied model from cache to: {self.local_model_path}")
                    model_path_to_use = str(self.local_model_path)
                else:
                    print("✗ No cached model found")
                    # Priority 3: Download from HuggingFace (will cache automatically)
                    print(f"→ Downloading model from HuggingFace: {self.model_name}")
                    model_path_to_use = self.model_name
            
            # Configure 4-bit quantization for minimal VRAM usage
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
            )
            
            # Load tokenizer
            print(f"Loading tokenizer from: {model_path_to_use}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_path_to_use, trust_remote_code=True)
            
            # Load model with aggressive optimizations
            print(f"Loading model from: {model_path_to_use}")
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path_to_use,
                quantization_config=bnb_config,
                device_map="auto",
                torch_dtype=torch.float16,
                trust_remote_code=True,
                low_cpu_mem_usage=True,
            )
            
            # If we downloaded the model, copy it to local folder for future use
            if model_path_to_use == self.model_name:
                print("Attempting to copy newly downloaded model to local folder...")
                if self.copy_model_from_cache():
                    print(f"✓ Model cached locally for faster future loading: {self.local_model_path}")
                else:
                    print("⚠ Could not cache model locally (this is not an error)")
            
            self.is_loaded = True
            print("✓ Local Transformer translation model loaded successfully!")
            
        except Exception as e:
            print(f"✗ Error loading Local Transformer model: {str(e)}")
            raise e
    
    def translate(self, text, target_language):
        """
        Translate text to target language using local transformer.
        
        Args:
            text (str): Text to translate
            target_language (str): Target language (e.g., "French", "Spanish", "German")
            
        Returns:
            str: Translated text
        """
        if not self.is_loaded:
            self.load_service()
        
        try:
            # Map language names to more specific prompts for better accuracy
            language_map = {
                "zh-Hant": "Traditional Chinese (繁體中文)",
                "zh-Hans": "Simplified Chinese (简体中文)",
                "Traditional Chinese": "Traditional Chinese (繁體中文)",
                "Chinese": "Simplified Chinese (简体中文)",
                "Japanese": "Japanese (日本語)",
                "Korean": "Korean (한국어)",
                "French": "French (Français)",
                "Spanish": "Spanish (Español)",
                "German": "German (Deutsch)",
                "Italian": "Italian (Italiano)",
                "Portuguese": "Portuguese (Português)",
                "Russian": "Russian (Русский)",
                "Arabic": "Arabic (العربية)",
                "Hindi": "Hindi (हिन्दी)"
            }
            
            # Use specific language mapping if available, otherwise use the original
            specific_language = language_map.get(target_language, target_language)
            
            # Create prompt with the specific format and clear language distinction
            if target_language in ["Traditional Chinese", "zh-Hant"]:
                # Extra explicit prompt for Traditional Chinese to avoid Simplified output
                prompt = f'Translate "{text}" to Traditional Chinese (繁體中文). Use Traditional Chinese characters only, not Simplified Chinese. Only output the translated text.'
            else:
                prompt = f'Only output the translated words. Translate "{text}" to {specific_language}'
            
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
                    max_new_tokens=8192,  # Max token length for longer translations
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
            print(f"Local Transformer translation error: {str(e)}")
            return f"Translation failed: {str(e)}"
    
    def is_available(self):
        """Check if the local transformer service is available."""
        try:
            import torch
            import transformers
            return True
        except ImportError:
            return False

# Create global instance
local_transformer_service = LocalTransformerService()
