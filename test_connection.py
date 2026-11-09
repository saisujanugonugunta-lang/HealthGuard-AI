
import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

if not key:
    print("API key missing")
    raise SystemExit

url = "https://generativelanguage.googleapis.com/v1beta/models"

try:
    print("Checking Gemini API...")
    response = requests.get(
        url,
        params={"key": key},
        timeout=15
    )

    print("HTTP Status:", response.status_code)

    if response.ok:
        print("Gemini API connection successful!")
        print("Models endpoint responded.")
    else:
        print("API response:", response.text[:500])

except requests.exceptions.Timeout:
    print("REST request timed out.")

except requests.exceptions.RequestException as e:
    print("Connection error:", str(e))
