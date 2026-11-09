
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

print("Loading API key...")
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key missing!")
    raise SystemExit

print("Connecting to Gemini...")

try:
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=120000)
    )

    print("Sending message...")

    response = client.interactions.create(
        model="gemini-3.8-flash",
        input="Reply with only the word HELLO."
    )

    print("Gemini response:")
    print(response.output_text)

except Exception as e:
    print("ERROR:", repr(e))
