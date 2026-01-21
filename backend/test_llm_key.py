import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load env vars
load_dotenv()

def test_key():
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"Loaded Key: {api_key[:5]}... (Length: {len(api_key) if api_key else 0})")
    
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment.")
        return

    print(f"Loaded Key: {api_key[:5]}... (Length: {len(api_key)})")
    genai.configure(api_key=api_key)

    candidates = [
        "gemini-2.5-flash",
        "gemini-2.0-flash-exp",
        "gemini-1.5-flash", 
        "gemini-1.5-flash-latest", 
        "gemini-1.5-flash-001",
        "gemini-1.0-pro",
        "gemini-pro"
    ]
    
    print("--- Model Scan ---")
    for model_name in candidates:
        print(f"Testing {model_name}...", end=" ")
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hi")
            print(f"SUCCESS! \u2705")
            print(f"Response: {response.text}")
            return # Found one!
        except Exception as e:
            print(f"Failed ({type(e).__name__})")
            # print(e) # Optional: print detailed error if needed
            
    print("--- Scan Complete: No working models found. ---")

if __name__ == "__main__":
    test_key()
