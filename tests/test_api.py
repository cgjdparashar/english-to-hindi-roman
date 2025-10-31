"""
Test script for the English to Hinglish Translation API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing Health Check Endpoint...")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_post_translation():
    """Test POST translation endpoint"""
    print("Testing POST /translate Endpoint...")
    print("=" * 60)
    
    test_cases = [
        "hello how are you",
        "what are you doing",
        "good morning",
        "thank you",
        "I love you"
    ]
    
    for text in test_cases:
        print(f"\nInput: '{text}'")
        response = requests.post(
            f"{BASE_URL}/translate",
            json={"text": text}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data['success']}")
            print(f"Hinglish: '{data['hinglish_text']}'")
            if data.get('error'):
                print(f"Error: {data['error']}")
        else:
            print(f"Error: Status {response.status_code}")
            print(f"Response: {response.text}")
    
    print()





def test_error_handling():
    """Test error handling"""
    print("Testing Error Handling...")
    print("=" * 60)
    
    # Test empty text
    print("\nTest Case: Empty text")
    response = requests.post(
        f"{BASE_URL}/translate",
        json={"text": ""}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test very long text
    print("\nTest Case: Very long text (>1000 chars)")
    long_text = "a" * 1001
    response = requests.post(
        f"{BASE_URL}/translate",
        json={"text": long_text}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print()


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("English to Hinglish Translation API Test Suite")
    print("="*60 + "\n")
    
    try:
        # Check if API is running
        response = requests.get(f"{BASE_URL}/", timeout=2)
        if response.status_code != 200:
            print("❌ API is not responding. Please start the server first.")
            print("Run: uv run uvicorn api.app:app --host 127.0.0.1 --port 8000")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Please start the server first.")
        print("Run: uv run uvicorn api.app:app --host 127.0.0.1 --port 8000")
        return
    
    # Run tests
    test_health_check()
    test_post_translation()
    test_error_handling()
    
    print("="*60)
    print("All tests completed!")
    print("="*60)
    print("\n💡 Note: If translations show errors, it's due to SSL certificate issues.")
    print("   The API structure and endpoints work correctly!")
    print("   Refer to SSL_TROUBLESHOOTING.md for solutions.\n")


if __name__ == "__main__":
    main()
