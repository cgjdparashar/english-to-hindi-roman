"""
Demo script for file translation utility

This script demonstrates how to use the file_translator module
to translate text files from English to Hinglish.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utility.file_translator import translate_file, translate_multiple_files, INPUT_DIR, OUTPUT_DIR


def demo_single_file():
    """Demo: Translate a single file"""
    print("\n" + "=" * 70)
    print("DEMO 1: Translating a single file (story.txt)")
    print("=" * 70)
    
    result = translate_file("story.txt")
    
    if result['success']:
        print("\n✓ Translation successful!")
        print(f"\nOriginal text (English):")
        print("-" * 70)
        print(result['original_text'])
        print("\nTranslated text (Hinglish - Roman script):")
        print("-" * 70)
        print(result['translated_text'])
        print(f"\n✓ Saved to: {result['output_path']}")
    else:
        print(f"\n✗ Translation failed: {result['error']}")


def demo_custom_filename():
    """Demo: Translate with custom output filename"""
    print("\n" + "=" * 70)
    print("DEMO 2: Translating with custom output filename")
    print("=" * 70)
    
    custom_name = "my_translated_story.txt"
    result = translate_file("story.txt", output_filename=custom_name)
    
    if result['success']:
        print(f"\n✓ Translation saved with custom filename: {result['output_path'].name}")


def demo_list_files():
    """Demo: List available files in input and output directories"""
    print("\n" + "=" * 70)
    print("DEMO 3: Listing available files")
    print("=" * 70)
    
    print(f"\nInput directory: {INPUT_DIR}")
    input_files = list(INPUT_DIR.glob("*.txt"))
    print(f"Available files ({len(input_files)}):")
    for file in input_files:
        print(f"  - {file.name}")
    
    print(f"\nOutput directory: {OUTPUT_DIR}")
    output_files = list(OUTPUT_DIR.glob("*.txt"))
    print(f"Translated files ({len(output_files)}):")
    for file in output_files:
        print(f"  - {file.name}")


def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("FILE TRANSLATOR UTILITY - DEMO")
    print("=" * 70)
    
    # Demo 1: Single file translation
    demo_single_file()
    
    # Demo 2: Custom filename
    demo_custom_filename()
    
    # Demo 3: List files
    demo_list_files()
    
    print("\n" + "=" * 70)
    print("Demo complete!")
    print("=" * 70)
    print("\nUsage examples:")
    print("  from utility.file_translator import translate_file")
    print("  result = translate_file('story.txt')")
    print("  result = translate_file('story.txt', output_filename='custom.txt')")
    print("=" * 70)


if __name__ == "__main__":
    main()
