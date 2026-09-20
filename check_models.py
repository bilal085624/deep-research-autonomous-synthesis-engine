import os
import requests
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("API Key not found. Please check your .env file.")
    exit()

print("🔍 Querying Google's API for available models...\n")

# Hit the raw REST API to bypass any SDK versioning issues
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url)

if response.status_code == 200:
    print("✅ Valid models authorized for your API key:\n")
    models = response.json().get("models", [])
    for m in models:
        # We only care about text-generation models, not embedding models
        if "generateContent" in m.get("supportedGenerationMethods", []):
            # Clean up the output string (e.g., 'models/gemini-2.5-flash' -> 'gemini-2.5-flash')
            clean_name = m['name'].replace('models/', '')
            print(f" - {clean_name}")
else:
    print(f"❌ Error connecting to API: {response.text}")