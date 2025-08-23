# Transverse Translation Services

This document describes the new modular translation service architecture for the Transverse PDF translation system.

## Architecture Overview

The translation system has been reorganized into a modular architecture that supports multiple translation backends:

```
translator/
├── services/
│   ├── __init__.py                 # Base translation service interface
│   ├── manager.py                  # Service manager and coordination
│   ├── local_transformer/         # Local transformer service
│   │   ├── __init__.py
│   │   └── service.py
│   └── google_gemini/              # Google Gemini API service
│       ├── __init__.py
│       └── service.py
├── config/
│   ├── README.md                   # Configuration instructions
│   └── gemini_api_key.txt          # (create this file with your API key)
├── models/                         # Local model storage
└── requirements-gemini.txt         # Additional dependencies for Gemini
```

## Available Services

### 1. Local Transformer (local_transformer)
- **Description**: Uses local HuggingFace transformer models for translation
- **Model**: JungZoona/T3Q-qwen2.5-14b-v1.0-e3
- **Pros**: 
  - No API costs
  - Works offline
  - Full data privacy
- **Cons**: 
  - Requires significant local resources (GPU recommended)
  - Slower initialization
- **Dependencies**: `torch`, `transformers`, `accelerate`, `bitsandbytes`

### 2. Google Gemini API (gemini)
- **Description**: Uses Google's Gemini API for translation
- **Pros**: 
  - Fast response times
  - High-quality translations
  - No local resource requirements
- **Cons**: 
  - Requires API key
  - Pay-per-use
  - Requires internet connection
- **Dependencies**: `google-generativeai`
- **Setup**: Requires API key (see Configuration section)

## Configuration

### Setting up Google Gemini API

1. **Get an API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the generated key

2. **Configure the API Key** (choose one method):

   **Option A: Environment Variable (Recommended)**
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   # or
   export GOOGLE_API_KEY="your_api_key_here"
   ```

   **Option B: Configuration File**
   ```bash
   echo "your_api_key_here" > translator/config/gemini_api_key.txt
   ```

### Installing Dependencies

**For Local Transformer:**
```bash
pip install torch transformers accelerate bitsandbytes
```

**For Google Gemini API:**
```bash
pip install google-generativeai
# or
pip install -r translator/requirements-gemini.txt
```

## Usage

### Backend API Endpoints

The system provides several new API endpoints for managing translation services:

1. **Get Available Services**
   ```
   GET /api/translation-services/
   ```
   Returns information about available translation services.

2. **Set Active Service**
   ```
   POST /api/translation-services/set/
   Content-Type: application/json
   
   {
     "service_name": "local_transformer" | "gemini"
   }
   ```

3. **Load/Initialize Service**
   ```
   POST /api/translation-services/load/
   Content-Type: application/json
   
   {
     "service_name": "local_transformer"  // optional
   }
   ```

### Python API

```python
from translator.services.manager import translation_manager

# Get available services
available = translation_manager.get_available_services()
print(f"Available: {available}")

# Set active service
translation_manager.set_service('gemini')

# Translate text
result = translation_manager.translate("Hello world", "Spanish")
print(f"Translation: {result}")

# Get service information
info = translation_manager.get_all_services_info()
```

### Backwards Compatibility

The existing backend code continues to work without changes. The `translation_service` in `transverse_backend/translation_service.py` now acts as a wrapper that provides the same interface while using the new modular services underneath.

## Service Priority

The system automatically selects services in this order:

1. **Local Transformer** - if PyTorch and transformers are available
2. **Google Gemini API** - if google-generativeai is installed and API key is configured

You can explicitly set a service using the API endpoints or Python interface.

## Testing

### Quick Test
Run the test script to verify everything is working:
```bash
python3 test_translation_services.py
```

### Setup Script
Run the setup script to check dependencies and configuration:
```bash
./setup_translation_services.sh
```

## Model Loading Priority (Local Transformer)

For the local transformer service, models are loaded in this priority order:

1. **Local Models Folder**: `translator/models/JungZoona_T3Q-qwen2.5-14b-v1.0-e3/`
2. **HuggingFace Cache**: `~/.cache/huggingface/hub/`
3. **Download**: From HuggingFace Hub (automatically cached)

## Error Handling

- If a service fails to load, the system falls back to available services
- Translation errors are gracefully handled and return error messages
- The system provides detailed error information for troubleshooting

## Development

### Adding New Services

To add a new translation service:

1. Create a new directory under `translator/services/`
2. Implement a service class inheriting from `BaseTranslationService`
3. Add the service to the manager in `manager.py`
4. Update dependencies and documentation

### Base Service Interface

All services must implement:
- `load_service()`: Initialize the service
- `translate(text, target_language)`: Perform translation
- `is_available()`: Check if service can be used
- `get_service_info()`: Return service information

## Security Notes

- Never commit API keys to version control
- Add `translator/config/gemini_api_key.txt` to `.gitignore`
- Use environment variables for production deployments
- Keep API keys secure and rotate them regularly

## Troubleshooting

### Common Issues

1. **No services available**:
   - Install required dependencies
   - Check API key configuration for Gemini
   - Verify Python path includes translator directory

2. **Local transformer fails to load**:
   - Check available GPU memory
   - Ensure PyTorch is installed with CUDA support
   - Try downloading model manually to `translator/models/`

3. **Gemini API errors**:
   - Verify API key is correct
   - Check internet connection
   - Ensure API key has proper permissions

### Debug Mode

Set environment variable for detailed logging:
```bash
export TRANSLATION_DEBUG=1
```

## Performance Considerations

- **Local Transformer**: First load is slow, subsequent translations are faster
- **Gemini API**: Consistent fast response times, limited by API rate limits
- **Memory**: Local transformer requires ~8-16GB RAM with quantization
- **GPU**: Local transformer benefits significantly from GPU acceleration
