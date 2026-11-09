
import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

if not key:
    print("API key missing")
    raise SystemExit

url = "https://generativelanguage.googleapis.com/v1beta/interactions"

payload = {
    "model": "gemini-3.8-flash",
    "input": "Reply with only the word HELLO."
}

try:
    print("Sending direct REST request...")

    response = requests.post(
        url,
        headers={
            "x-goog-api-key": key,
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=(10, 60)
    )

    print("HTTP Status:", response.status_code)

    if response.ok:
        data = response.json()
        print("API status:", data.get("status"))

        for step in data.get("steps", []):
            if step.get("type") == "model_output":
                for item in step.get("content", []):
                    if item.get("type") == "text":
                        print("Gemini says:", item.get("text"))
    else:
        print("API error:", response.text[:500])

except requests.exceptions.Timeout:
    print("REST generation request timed out.")

except requests.exceptions.RequestException as error:
    print("Connection error:", str(error))
