#!/usr/bin/env python3
"""
Alternative translator test script with maximum optimizations.
Uses direct model loading for even better control over memory usage.
"""

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
import time

def test_translation_optimized():
    """Test translation with maximum optimizations."""
    
    print("Loading model with maximum optimizations...")
    start_time = time.time()
    
    model_name = "JungZoona/T3Q-qwen2.5-14b-v1.0-e3"
    
    # Configure 4-bit quantization for minimal VRAM usage
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    
    # Load model with aggressive optimizations
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True,
        low_cpu_mem_usage=True,
    )
    
    load_time = time.time() - start_time
    print(f"Model loaded in {load_time:.2f} seconds")
    
    # Test text
    test_text = "Air Canada plans to resume flights Monday evening as union remains on strike, defying federal order"
    
    # Languages to test
    target_languages = [
        "French",
        "Traditional Chinese", 
        "Spanish",
        "German"
    ]
    
    print(f"\nOriginal text: {test_text}\n")
    print("=" * 80)
    
    for language in target_languages:
        print(f"\nTranslating to {language}...")
        
        # Create prompt
        prompt = f"Translate the following English text to {language}: '{test_text}'"
        
        messages = [{"role": "user", "content": prompt}]
        
        try:
            start_time = time.time()
            
            # Apply chat template
            inputs = tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=True,
                return_dict=True,
                return_tensors="pt",
            ).to(model.device)
            
            # Generate with optimized settings
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=30,
                    do_sample=False,
                    temperature=0.1,
                    pad_token_id=tokenizer.eos_token_id,
                    use_cache=True,
                )
            
            # Decode only the new tokens
            generated_text = tokenizer.decode(
                outputs[0][inputs["input_ids"].shape[-1]:], 
                skip_special_tokens=True
            )
            
            translation_time = time.time() - start_time
            
            print(f"{language}: {generated_text.strip()}")
            print(f"Translation time: {translation_time:.2f} seconds")
            print("-" * 60)
            
        except Exception as e:
            print(f"Error translating to {language}: {str(e)}")
            print("-" * 60)

def print_memory_usage():
    """Print current GPU memory usage."""
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            memory_allocated = torch.cuda.memory_allocated(i) / 1024**3
            memory_reserved = torch.cuda.memory_reserved(i) / 1024**3
            print(f"GPU {i}: {memory_allocated:.2f}GB allocated, {memory_reserved:.2f}GB reserved")

if __name__ == "__main__":
    try:
        print_memory_usage()
        test_translation_optimized()
        print("\nFinal memory usage:")
        print_memory_usage()
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Make sure you have run the install script first!")
        print("Run: bash install.sh")
