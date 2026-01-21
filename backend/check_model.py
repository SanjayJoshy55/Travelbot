import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def check(name):
    print(f"Testing {name}...", end=" ")
    try:
        model = genai.GenerativeModel(name)
        model.generate_content("Hi")
        print("WORKS!")
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False

# Prioritize User Request, then probable real Experimental model
if check("gemini-2.5-flash"):
    print("SELECTED: gemini-2.5-flash")
elif check("gemini-2.0-flash-exp"):
    print("SELECTED: gemini-2.0-flash-exp")
elif check("gemini-1.5-flash"):
    print("SELECTED: gemini-1.5-flash")
else:
    print("ALL FAILED")
