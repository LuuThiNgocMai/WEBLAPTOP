import google.generativeai as genai
import sys
import os

# Add parent directory to path to find config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import GEMINI_API_KEY
    genai.configure(api_key=GEMINI_API_KEY)

    print("--- Available Models ---")
    models = genai.list_models()
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model ID: {m.name}")
except Exception as e:
    print(f"Error: {str(e)}")
