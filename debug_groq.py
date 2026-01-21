import os
from groq import Groq

# Use the key from the code
api_key = os.getenv("GROQ_API_KEY")

try:
    print(f"Initializing Groq client with key ending in ...{api_key[-4:]}")
    client = Groq(api_key=api_key)
    
    model = "llama-3.1-8b-instant"
    print(f"Testing model: {model}")
    
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Hello",
            }
        ],
        model=model,
    )
    print("Success!")
    print(completion.choices[0].message.content)
    
except Exception as e:
    print(f"Error: {e}")
