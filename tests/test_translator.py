import sys
import os

# Add parent directory to path to import utility module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utility.translator import english_to_hinglish


def test_english_to_hinglish_basic():
    """Test basic English to Hinglish translation."""
    # Test case 1: Simple greeting
    result = english_to_hinglish("hello how are you")
    print(f"Test 1 - Input: 'hello how are you'")
    print(f"Test 1 - Output: '{result}'")
    assert len(result) > 0, "Translation should not be empty"
    
    # Test case 2: Question
    result = english_to_hinglish("what are you doing")
    print(f"\nTest 2 - Input: 'what are you doing'")
    print(f"Test 2 - Output: '{result}'")
    assert len(result) > 0, "Translation should not be empty"


def test_english_to_hinglish_various_inputs():
    """Test various English inputs."""
    test_cases = [
        "good morning",
        "thank you",
        "I am fine",
        "where are you going",
        "what is your name",
        "I love you",
        "how old are you",
    ]
    
    print("\n" + "="*50)
    print("Testing various English inputs:")
    print("="*50)
    
    for test_input in test_cases:
        result = english_to_hinglish(test_input)
        print(f"\nInput:  '{test_input}'")
        print(f"Output: '{result}'")
        assert len(result) > 0, f"Translation for '{test_input}' should not be empty"


def test_special_cases():
    """Test special cases and edge inputs."""
    test_cases = [
        ("hello", "Expected: greeting in Hinglish"),
        ("yes", "Expected: haan or similar"),
        ("no", "Expected: nahi or similar"),
    ]
    
    print("\n" + "="*50)
    print("Testing special cases:")
    print("="*50)
    
    for english_input, description in test_cases:
        result = english_to_hinglish(english_input)
        print(f"\nInput:    '{english_input}'")
        print(f"Output:   '{result}'")
        print(f"Note:     {description}")
        assert len(result) > 0, "Translation should not be empty"


def test_empty_input():
    """Test with empty input."""
    result = english_to_hinglish("")
    print(f"\nTest empty input - Output: '{result}'")
    assert isinstance(result, str), "Should return a string"


def run_all_tests():
    """Run all tests."""
    print("Starting English to Hinglish Translation Tests")
    print("="*60)
    
    try:
        test_english_to_hinglish_basic()
        print("\n✓ Basic translation tests passed")
    except AssertionError as e:
        print(f"\n✗ Basic translation tests failed: {e}")
    except Exception as e:
        print(f"\n✗ Basic translation tests error: {e}")
    
    try:
        test_english_to_hinglish_various_inputs()
        print("\n✓ Various inputs tests passed")
    except AssertionError as e:
        print(f"\n✗ Various inputs tests failed: {e}")
    except Exception as e:
        print(f"\n✗ Various inputs tests error: {e}")
    
    try:
        test_special_cases()
        print("\n✓ Special cases tests passed")
    except AssertionError as e:
        print(f"\n✗ Special cases tests failed: {e}")
    except Exception as e:
        print(f"\n✗ Special cases tests error: {e}")
    
    try:
        test_empty_input()
        print("\n✓ Empty input test passed")
    except AssertionError as e:
        print(f"\n✗ Empty input test failed: {e}")
    except Exception as e:
        print(f"\n✗ Empty input test error: {e}")
    
    print("\n" + "="*60)
    print("All tests completed!")


if __name__ == "__main__":
    run_all_tests()
