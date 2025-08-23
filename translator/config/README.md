````markdown
# Google Gemini API Configuration

## Setup Instructions

1. **Copy the example file:**
   ```bash
   cp gemini_api_key.txt.example gemini_api_key.txt
   ```

2. **Add your API key:**
   Edit `gemini_api_key.txt` and replace `YOUR_GEMINI_API_KEY_HERE` with your actual API key.

## Option 1: Environment Variable (Recommended)
Set your API key as an environment variable:
```bash
export GEMINI_API_KEY="your_api_key_here"
# or
export GOOGLE_API_KEY="your_api_key_here"
```

## Option 2: Config File
Create a file named `gemini_api_key.txt` in this directory with your API key:
```
your_api_key_here
```

## Getting an API Key
1. Go to Google AI Studio: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

## Security Note
- ✅ The `gemini_api_key.txt` file is now in `.gitignore` and won't be committed
- ✅ Use the `gemini_api_key.txt.example` template to set up your API key
- Never commit your actual API key to version control
- Keep your API key secure and private

````
