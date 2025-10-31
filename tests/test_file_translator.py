"""
Test script for file_translator module

This script tests the file translation functionality by translating story.txt
from inputfile directory to outputfile directory.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import utility module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utility.file_translator import (
    translate_file,
    translate_multiple_files,
    read_file,
    save_file,
    INPUT_DIR,
    OUTPUT_DIR
)


def test_read_file():
    """Test reading a file from inputfile directory."""
    print("\n" + "=" * 60)
    print("TEST 1: Reading story.txt")
    print("=" * 60)
    
    try:
        content = read_file("story.txt")
        print(f"✓ File read successfully")
        print(f"  Content length: {len(content)} characters")
        print(f"  Preview: {content[:100]}...")
        assert len(content) > 0, "File content should not be empty"
        return True
    except Exception as e:
        print(f"✗ Failed to read file: {e}")
        return False


def test_translate_single_file():
    """Test translating story.txt."""
    print("\n" + "=" * 60)
    print("TEST 2: Translating story.txt")
    print("=" * 60)
    
    result = translate_file("story.txt")
    
    if result['success']:
        print(f"\n✓ Translation successful!")
        print(f"  Input file: {result['input_path']}")
        print(f"  Output file: {result['output_path']}")
        print(f"  Original length: {len(result['original_text'])} characters")
        print(f"  Translated length: {len(result['translated_text'])} characters")
        
        print(f"\n  Original text:")
        print(f"  {result['original_text'][:200]}...")
        
        print(f"\n  Translated text (Hinglish):")
        print(f"  {result['translated_text'][:200]}...")
        
        # Verify output file exists
        assert result['output_path'].exists(), "Output file should exist"
        print(f"\n✓ Output file verified at: {result['output_path']}")
        
        return True
    else:
        print(f"\n✗ Translation failed: {result['error']}")
        return False


def test_custom_output_filename():
    """Test translating with a custom output filename."""
    print("\n" + "=" * 60)
    print("TEST 3: Translating with custom output filename")
    print("=" * 60)
    
    custom_output = "story_custom_hinglish.txt"
    result = translate_file("story.txt", output_filename=custom_output)
    
    if result['success']:
        print(f"✓ Translation successful with custom filename!")
        print(f"  Output file: {result['output_path']}")
        assert result['output_path'].name == custom_output, "Output filename should match"
        print(f"✓ Custom filename verified")
        return True
    else:
        print(f"✗ Translation failed: {result['error']}")
        return False


def test_output_directory_structure():
    """Verify the output directory structure."""
    print("\n" + "=" * 60)
    print("TEST 4: Verifying directory structure")
    print("=" * 60)
    
    print(f"  Input directory: {INPUT_DIR}")
    print(f"  Output directory: {OUTPUT_DIR}")
    
    # Check if directories exist
    assert INPUT_DIR.exists(), "Input directory should exist"
    assert OUTPUT_DIR.exists(), "Output directory should exist"
    
    print(f"✓ Both directories exist")
    
    # List files in output directory
    output_files = list(OUTPUT_DIR.glob("*.txt"))
    print(f"\n  Files in output directory ({len(output_files)}):")
    for file in output_files:
        print(f"    - {file.name}")
    
    return True


def test_read_and_compare():
    """Read the translated file and compare with original."""
    print("\n" + "=" * 60)
    print("TEST 5: Reading and comparing translated file")
    print("=" * 60)
    
    try:
        # Read original
        original = read_file("story.txt", INPUT_DIR)
        print(f"  Original text length: {len(original)} characters")
        
        # Read translated
        translated_path = OUTPUT_DIR / "story_hinglish.txt"
        if translated_path.exists():
            with open(translated_path, 'r', encoding='utf-8') as f:
                translated = f.read()
            
            print(f"  Translated text length: {len(translated)} characters")
            print(f"\n  Original (first 150 chars):")
            print(f"  {original[:150]}...")
            print(f"\n  Translated (first 150 chars):")
            print(f"  {translated[:150]}...")
            
            assert len(translated) > 0, "Translated content should not be empty"
            print(f"\n✓ Translation file successfully read and verified")
            return True
        else:
            print(f"✗ Translated file not found at: {translated_path}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def run_all_tests():
    """Run all test cases."""
    print("\n" + "=" * 70)
    print("FILE TRANSLATOR UTILITY - TEST SUITE")
    print("=" * 70)
    
    tests = [
        ("Read File", test_read_file),
        ("Translate Single File", test_translate_single_file),
        ("Custom Output Filename", test_custom_output_filename),
        ("Directory Structure", test_output_directory_structure),
        ("Read and Compare", test_read_and_compare),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' raised an exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "=" * 70)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
