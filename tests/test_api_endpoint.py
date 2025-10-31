"""
Test the API endpoint using requests library
"""
import requests
import json

url = "http://127.0.0.1:8000/translate"
payload = {
    "text": "hello how are you",
    "preserve_punctuation": True
}

print("Testing API endpoint after restructuring...")
print(f"URL: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print("=" * 60)

try:
    response = requests.post(url, json=payload)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("\n✓ API is working correctly!")
    else:
        print(f"\n✗ API returned error: {response.status_code}")
        
except Exception as e:
    print(f"\n✗ Error testing API: {str(e)}")
