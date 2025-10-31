"""
Quick test to check API response for Postman
"""
import requests
import json
import sys

def test_translate_hello():
    """Test the translate endpoint with 'hello how are you'"""
    
    url = "http://127.0.0.1:8001/translate"
    payload = {
        "text": "hello how are you"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    print("="*70)
    print("Testing: Translate - Hello")
    print("="*70)
    print(f"\nURL: {url}")
    print(f"Method: POST")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print(f"\nSending request...")
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"\n✓ Response received!")
        print(f"\nStatus Code: {response.status_code}")
        print(f"\nResponse Headers:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        print(f"\nResponse Body:")
        print(json.dumps(response.json(), indent=2))
        
        # Check if successful
        data = response.json()
        print(f"\n{'='*70}")
        print("RESULT ANALYSIS:")
        print(f"{'='*70}")
        print(f"✓ Original Text: '{data.get('original_text')}'")
        print(f"✓ Hinglish Text: '{data.get('hinglish_text')}'")
        print(f"✓ Success: {data.get('success')}")
        if data.get('error'):
            print(f"⚠ Error: {data.get('error')}")
        
        if response.status_code == 200 and data.get('success'):
            print(f"\n✅ API IS WORKING CORRECTLY!")
        elif response.status_code == 200 and not data.get('success'):
            print(f"\n⚠️ API RESPONDED BUT TRANSLATION FAILED (likely SSL issue)")
        else:
            print(f"\n❌ API ERROR")
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Could not connect to API at {url}")
        print("Make sure the server is running: uv run uvicorn api.app:app --host 127.0.0.1 --port 8001")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
    
    print(f"{'='*70}\n")

if __name__ == "__main__":
    test_translate_hello()
