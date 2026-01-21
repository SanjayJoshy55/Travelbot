import time
import os
import sys

# Try to import openai, install if missing
try:
    from openai import OpenAI
except ImportError:
    print("OpenAI library not found. Installing...")
    os.system(f"{sys.executable} -m pip install openai")
    from openai import OpenAI

# The key provided by the user. 
# Prefix 'gsk_' indicates this is a Groq API key (https://groq.com), 
# which is different from xAI's Grok. Groq is known for high speed inference chips (LPUs).
api_key = os.getenv("GROQ_API_KEY")

# Configure for Groq
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

def test_speed():
    output_lines = []
    output_lines.append("Testing API Key (detected as Groq API due to 'gsk_' prefix)...")
    
    # Using a fast model available on Groq
    model = "llama-3.1-8b-instant" 
    output_lines.append(f"Target Model: {model}")
    
    start_time = time.time()
    try:
        # We use a slightly longer prompt to get a measurable generation time/speed
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Explain the physics of light speed in two paragraphs.",
                }
            ],
            model=model,
        )
        end_time = time.time()
        
        duration = end_time - start_time
        content = completion.choices[0].message.content
        
        output_lines.append("\n--- API Response ---")
        output_lines.append(content)
        output_lines.append("--------------------")
        
        # usage details
        usage = completion.usage
        if usage:
            output_lines.append(f"\nPerformance Stats:")
            output_lines.append(f"Request Duration: {duration:.4f} seconds")
            output_lines.append(f"Input Tokens: {usage.prompt_tokens}")
            output_lines.append(f"Output Tokens: {usage.completion_tokens}")
            output_lines.append(f"Total Tokens: {usage.total_tokens}")
            
            if usage.completion_tokens > 0:
                output_lines.append(f"Approximate Throughput: {usage.completion_tokens / duration:.2f} tokens/sec")
                
    except Exception as e:
        output_lines.append(f"Error occurred: {e}")
        # If the model is not found or other error, hint at what might be wrong
        if "401" in str(e):
            output_lines.append("Note: 401 Unauthorized usually means the API key is invalid.")
        if "404" in str(e):
            output_lines.append("Note: 404 Not Found might mean the model name is incorrect or the endpoint is wrong.")

    # Write to file
    with open("test_grok_results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    print("Test finished. Results written to test_grok_results.txt")

if __name__ == "__main__":
    test_speed()
