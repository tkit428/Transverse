#!/usr/bin/env python3
"""
Translator test script using Qwen2.5 model for translation tasks.
Optimized for lower VRAM usage and faster inference.
"""

from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import time

def test_translation():
    """Test the translation model with various languages."""
    
    print("Loading the translation model with optimizations...")
    start_time = time.time()
    
    # Check if CUDA is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Load with optimizations for lower VRAM usage
    model_name = "JungZoona/T3Q-qwen2.5-14b-v1.0-e3"
    
    # Option 1: Use pipeline with optimizations
    pipe = pipeline(
        "text-generation", 
        model=model_name,
        torch_dtype=torch.float16,  # Use half precision
        device_map="auto",          # Automatically distribute across available GPUs
        trust_remote_code=True,
        model_kwargs={
            "load_in_8bit": True,   # 8-bit quantization to reduce VRAM
            "device_map": "auto",
        }
    )
    
    load_time = time.time() - start_time
    print(f"Model loaded in {load_time:.2f} seconds")
    
    # Test text to translate
    test_text = "Air Canada plans to resume flights Monday evening as union remains on strike, defying federal order"
    
    # Languages to translate to
    target_languages = [
        "French",
        "Spanish", 
        "German",
        "Traditional Chinese",
        "Japanese",
        "Korean"
    ]
    
    print(f"\nOriginal text: {test_text}\n")
    print("=" * 80)
    
    for language in target_languages:
        print(f"\nTranslating to {language}...")
        
        messages = [
            {
                "role": "user", 
                "content": f"Translate the following English text to {language}: '{test_text}'"
            }
        ]
        
        try:
            start_time = time.time()
            result = pipe(
                messages, 
                max_new_tokens=50,      # Reduced for faster generation
                do_sample=False,        # Use greedy decoding for speed
                temperature=0.1,        # Lower temperature for more focused output
                pad_token_id=pipe.tokenizer.eos_token_id,
                return_full_text=False  # Only return the generated part
            )
            translation_time = time.time() - start_time
            
            # Extract the generated text
            generated_text = result[0]['generated_text'][-1]['content'] if isinstance(result[0]['generated_text'], list) else result[0]['generated_text']
            
            print(f"{language}: {generated_text}")
            print(f"Translation time: {translation_time:.2f} seconds")
            print("-" * 60)
            
        except Exception as e:
            print(f"Error translating to {language}: {str(e)}")
            print("-" * 60)

if __name__ == "__main__":
    try:
        test_translation()
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Make sure you have run the install script first!")
        print("Run: bash install.sh")