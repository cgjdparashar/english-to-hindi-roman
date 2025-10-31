import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "http://127.0.0.1:8001/translate"
payload = {
    "text": "hello how are you"
}

print("Testing API endpoint...")
print(f"URL: {url}")
print(f"Payload: {payload}")
print("-" * 50)

try:
    response = requests.post(url, json=payload, verify=False, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    result = response.json()
    if result.get("success"):
        print("\n✅ SUCCESS!")
        print(f"Original: {result['original_text']}")
        print(f"Hinglish: {result['hinglish_text']}")
    else:
        print(f"\n❌ FAILED: {result.get('error')}")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
