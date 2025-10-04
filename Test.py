import requests
import json

# Vervang dit door de Moxfield deckcode (alleen letters/cijfers, geen /view)
mox_id = "JE_DECKCODE_HIER"

# Moxfield endpoint (gebruik api2.moxfield.com of api.moxfield.com)
url = f"https://api2.moxfield.com/v3/decks/all/{mox_id}"
headers = {"User-Agent": "Mozilla/5.0"}

try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f"HTTP status code: {r.status_code}")

    # Bekijk eerst de raw text
    print("Raw response:")
    print(r.text[:500])  # print de eerste 500 tekens

    # Probeer JSON te parsen
    try:
        data = r.json()
        print("JSON response:")
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"JSON parsing failed: {e}")

except Exception as e:
    print(f"Request failed: {e}")
