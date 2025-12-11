import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print(f"API Key present: {bool(api_key)}")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemma-3-27b-it')
        response = model.generate_content("Hello, can you hear me?")
        print("Success! Gemini API is working.")
        print("Response:", response.text)
    except Exception as e:
        print(f"Error connecting to Gemini API: {e}")
else:
    print("Error: GEMINI_API_KEY is missing from environment variables.")
