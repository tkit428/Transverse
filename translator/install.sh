#!/bin/bash

echo "Installing translator dependencies..."

# Install required Python packages with optimizations
pip install transformers torch accelerate bitsandbytes optimum

echo "Cloning the model repository..."
# Clone the model repository
git clone https://huggingface.co/JungZoona/T3Q-qwen2.5-14b-v1.0-e3

echo "Installation complete!"
echo "You can now run the test script with: python test.py"