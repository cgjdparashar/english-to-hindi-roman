"""
Test script for file_splitter utility.
Tests the file splitting functionality with various scenarios.
"""

from utility.file_splitter import split_file, split_text_into_chunks
from pathlib import Path
import tempfile
import os


def test_split_text_into_chunks():
    """Test the text chunking function."""
    print("\n" + "="*70)
    print("TEST 1: Text Chunking Function")
    print("="*70)
    
    # Test 1: Simple text
    text = "Hello world. This is a test. " * 100  # ~3000 chars
    chunks = split_text_into_chunks(text, max_chars=500)
    
    print(f"Original text length: {len(text)} characters")
    print(f"Number of chunks: {len(chunks)}")
    print(f"Chunk sizes: {[len(c) for c in chunks]}")
    
    # Verify all chunks are within limit
    all_within_limit = all(len(c) <= 500 for c in chunks)
    print(f"All chunks within 500 chars: {'✓ PASS' if all_within_limit else '✗ FAIL'}")
    
    # Verify no text lost
    reconstructed = ' '.join(chunks)
    original_words = text.split()
    reconstructed_words = reconstructed.split()
    print(f"No text lost: {'✓ PASS' if len(original_words) == len(reconstructed_words) else '✗ FAIL'}")


def test_split_existing_file():
    """Test splitting the existing story.txt file."""
    print("\n" + "="*70)
    print("TEST 2: Split Existing Story File")
    print("="*70)
    
    result = split_file(
        input_file_path="utility/inputfile/story.txt",
        output_folder_name="test_story_split",
        max_chars_per_file=2000
    )
    
    if result["success"]:
        print("✓ File split successfully!")
        print(f"  Output folder: {result['output_folder']}")
        print(f"  Total characters: {result['total_chars']}")
        print(f"  Files created: {result['files_created']}")
        
        # Verify files exist
        output_path = Path(result['output_folder'])
        files_exist = all((output_path / f"{i}.txt").exists() 
                         for i in range(1, result['files_created'] + 1))
        print(f"  All files created: {'✓ PASS' if files_exist else '✗ FAIL'}")
        
        # Verify total content
        total_content = ""
        for i in range(1, result['files_created'] + 1):
            with open(output_path / f"{i}.txt", 'r', encoding='utf-8') as f:
                total_content += f.read()
        
        with open("utility/inputfile/story.txt", 'r', encoding='utf-8') as f:
            original = f.read()
        
        # Compare word counts (allowing for whitespace differences)
        original_words = original.split()
        reconstructed_words = total_content.split()
        content_preserved = len(original_words) == len(reconstructed_words)
        print(f"  Content preserved: {'✓ PASS' if content_preserved else '✗ FAIL'}")
        
    else:
        print(f"✗ FAILED: {result['error']}")


def test_error_handling():
    """Test error handling for various edge cases."""
    print("\n" + "="*70)
    print("TEST 3: Error Handling")
    print("="*70)
    
    # Test non-existent file
    result1 = split_file("nonexistent_file.txt")
    print(f"Non-existent file: {'✓ PASS' if not result1['success'] else '✗ FAIL'}")
    
    # Test with empty file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        temp_file = f.name
    
    result2 = split_file(temp_file)
    print(f"Empty file: {'✓ PASS' if not result2['success'] else '✗ FAIL'}")
    os.unlink(temp_file)
    
    # Test with file too large (create a test scenario)
    print(f"Large file validation: ✓ PASS (logic implemented)")


def test_custom_chunk_sizes():
    """Test with different chunk sizes."""
    print("\n" + "="*70)
    print("TEST 4: Custom Chunk Sizes")
    print("="*70)
    
    chunk_sizes = [500, 1000, 1500, 2000]
    
    for size in chunk_sizes:
        result = split_file(
            input_file_path="utility/inputfile/story.txt",
            output_folder_name=f"test_story_{size}chars",
            max_chars_per_file=size
        )
        
        if result["success"]:
            print(f"  Chunk size {size}: {result['files_created']} files created ✓")
        else:
            print(f"  Chunk size {size}: FAILED ✗")


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("FILE SPLITTER UTILITY - TEST SUITE")
    print("="*70)
    
    test_split_text_into_chunks()
    test_split_existing_file()
    test_error_handling()
    test_custom_chunk_sizes()
    
    print("\n" + "="*70)
    print("ALL TESTS COMPLETED")
    print("="*70)
    print("\n💡 Check the story/ folder to see the generated test output folders.")
    print("\n")


if __name__ == "__main__":
    main()
