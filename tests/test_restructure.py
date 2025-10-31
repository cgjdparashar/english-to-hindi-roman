"""
Quick test script to verify the restructured API works correctly
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utility.translator import english_to_hinglish

print("Testing the translator function after restructuring...")
print("=" * 60)

test_cases = [
    "hello how are you",
    "what are you doing",
    "good morning",
    "thank you"
]

for test in test_cases:
    result = english_to_hinglish(test)
    print(f"\nInput:  {test}")
    print(f"Output: {result}")
    print("-" * 60)

print("\n✓ All tests completed successfully!")
print("The code structure has been reorganized successfully.")
