import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "http://127.0.0.1:8001"

test_cases = [
    {
        "name": "Health Check",
        "method": "GET",
        "url": f"{base_url}/health",
        "payload": None
    },
    {
        "name": "Translate - Hello",
        "method": "POST",
        "url": f"{base_url}/translate",
        "payload": {"text": "hello how are you"}
    },
    {
        "name": "Translate - What are you doing",
        "method": "POST",
        "url": f"{base_url}/translate",
        "payload": {"text": "what are you doing"}
    },
    {
        "name": "Translate - Good Morning",
        "method": "POST",
        "url": f"{base_url}/translate",
        "payload": {"text": "good morning"}
    },
    {
        "name": "Translate - Thank You",
        "method": "POST",
        "url": f"{base_url}/translate",
        "payload": {"text": "thank you very much"}
    },
    {
        "name": "Translate - Long Sentence",
        "method": "POST",
        "url": f"{base_url}/translate",
        "payload": {"text": "I am going to the market to buy some vegetables and fruits"}
    },
    {
        "name": "Error - Empty Text",
        "method": "POST",
        "url": f"{base_url}/translate",
        "payload": {"text": ""}
    }
]

print("Testing all Postman requests...")
print("=" * 70)

results = {"passed": 0, "failed": 0}

for test in test_cases:
    print(f"\n{test['name']}")
    print("-" * 70)
    
    try:
        if test['method'] == 'GET':
            response = requests.get(test['url'], verify=False, timeout=10)
        else:
            response = requests.post(test['url'], json=test['payload'], verify=False, timeout=10)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code in [200, 422]:  # Accept 200 and validation errors
            result_data = response.json()
            print(f"Response: {result_data}")
            
            # Check if it's a translation success
            if 'hinglish_text' in result_data and result_data.get('success'):
                print(f"✅ Translation: '{result_data['original_text']}' → '{result_data['hinglish_text']}'")
                results["passed"] += 1
            elif 'status' in result_data:  # Health check
                print(f"✅ Health check passed")
                results["passed"] += 1
            elif response.status_code == 422:  # Validation error expected
                print(f"✅ Validation error (expected)")
                results["passed"] += 1
            else:
                print(f"❌ Unexpected response format")
                results["failed"] += 1
        else:
            print(f"❌ Unexpected status code")
            results["failed"] += 1
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        results["failed"] += 1

print("\n" + "=" * 70)
print(f"RESULTS: {results['passed']} passed, {results['failed']} failed")
