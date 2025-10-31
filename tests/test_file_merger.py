#!/usr/bin/env python3
"""
Test File Merger Functionality
Tests the file merger utilities to ensure they work correctly.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utility.file_merger import merge_files, merge_translated_files, get_numbered_files
from utility.generic_file_merger import merge_any_folder


def test_get_numbered_files():
    """Test the numbered files detection function."""
    print("🧪 Testing numbered files detection...")
    
    test_folder = "story/output/story_31_10"
    numbered_files = get_numbered_files(test_folder)
    
    print(f"📁 Test folder: {test_folder}")
    print(f"🔢 Found {len(numbered_files)} numbered files:")
    
    for file_num, file_path in numbered_files:
        print(f"  {file_num}: {Path(file_path).name}")
    
    assert len(numbered_files) > 0, "Should find numbered files"
    assert numbered_files[0][0] == 1, "First file should be numbered 1"
    print("✅ Numbered files detection works correctly!\n")


def test_basic_merge():
    """Test basic file merging."""
    print("🧪 Testing basic merge functionality...")
    
    test_folder = "story/output/story_31_10"
    result = merge_files(test_folder)
    
    print(f"📁 Test folder: {test_folder}")
    print(f"🎯 Result: {result}")
    
    assert result["success"], f"Merge should succeed: {result.get('error', '')}"
    assert result["files_merged"] > 0, "Should merge some files"
    assert result["total_chars"] > 0, "Should have some content"
    assert os.path.exists(result["output_file"]), "Output file should exist"
    
    print("✅ Basic merge works correctly!\n")


def test_generic_merger():
    """Test generic file merger."""
    print("🧪 Testing generic file merger...")
    
    test_folder = "story/output/story_31_10"
    custom_output = "tests/test_generic_merge.txt"
    
    result = merge_any_folder(test_folder, custom_output)
    
    print(f"📁 Test folder: {test_folder}")
    print(f"📄 Custom output: {custom_output}")
    print(f"🎯 Result: {result}")
    
    assert result["success"], f"Generic merge should succeed: {result.get('error', '')}"
    assert result["files_merged"] > 0, "Should merge some files"
    assert os.path.exists(result["output_file"]), "Output file should exist"
    
    # Clean up test file
    if os.path.exists(result["output_file"]):
        os.remove(result["output_file"])
        print(f"🧹 Cleaned up test file: {result['output_file']}")
    
    print("✅ Generic merger works correctly!\n")


def test_custom_separator():
    """Test merging with custom separator."""
    print("🧪 Testing custom separator...")
    
    test_folder = "story/output/story_31_10"
    custom_output = "tests/test_custom_separator.txt"
    custom_separator = "\n\n=== SECTION BREAK ===\n\n"
    
    result = merge_files(test_folder, custom_output, custom_separator)
    
    print(f"📁 Test folder: {test_folder}")
    print(f"🔗 Custom separator: {repr(custom_separator)}")
    
    assert result["success"], f"Custom separator merge should succeed: {result.get('error', '')}"
    
    # Verify the custom separator is in the file
    if os.path.exists(result["output_file"]):
        with open(result["output_file"], 'r', encoding='utf-8') as f:
            content = f.read()
            assert "=== SECTION BREAK ===" in content, "Custom separator should be in merged file"
        
        # Clean up
        os.remove(result["output_file"])
        print(f"🧹 Cleaned up test file: {result['output_file']}")
    
    print("✅ Custom separator works correctly!\n")


def test_error_handling():
    """Test error handling with invalid inputs."""
    print("🧪 Testing error handling...")
    
    # Test non-existent folder
    result = merge_files("nonexistent/folder")
    assert not result["success"], "Should fail for non-existent folder"
    assert "not found" in result["error"].lower(), "Error should mention folder not found"
    print(f"✅ Non-existent folder error: {result['error']}")
    
    # Test empty folder (if it exists)
    empty_folder = "story/translate/story_31_10"
    if os.path.exists(empty_folder):
        result = merge_files(empty_folder)
        assert not result["success"], "Should fail for empty folder"
        assert "no numbered text files" in result["error"].lower(), "Error should mention no files"
        print(f"✅ Empty folder error: {result['error']}")
    
    print("✅ Error handling works correctly!\n")


def test_file_content_verification():
    """Test that merged content is correct."""
    print("🧪 Testing merged content verification...")
    
    test_folder = "story/output/story_31_10"
    temp_output = "tests/test_content_verification.txt"
    
    # Get the numbered files
    numbered_files = get_numbered_files(test_folder)
    
    # Read original files content
    original_content = []
    for file_num, file_path in numbered_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content.append(f.read().strip())
    
    # Merge files
    result = merge_files(test_folder, temp_output)
    assert result["success"], "Merge should succeed"
    
    # Read merged content
    with open(result["output_file"], 'r', encoding='utf-8') as f:
        merged_content = f.read()
    
    # Verify all original content is in merged file
    for i, content in enumerate(original_content):
        if content:  # Skip empty content
            assert content in merged_content, f"Content from file {i+1} should be in merged file"
    
    # Clean up
    os.remove(result["output_file"])
    print(f"🧹 Cleaned up test file: {result['output_file']}")
    
    print("✅ Content verification passed!\n")


def main():
    """Run all tests."""
    print("🚀 TESTING FILE MERGER UTILITIES")
    print("=" * 50)
    
    try:
        # Create tests directory if it doesn't exist
        Path("tests").mkdir(exist_ok=True)
        
        # Run tests
        test_get_numbered_files()
        test_basic_merge()
        test_generic_merger()
        test_custom_separator()
        test_error_handling()
        test_file_content_verification()
        
        print("🎉 ALL TESTS PASSED!")
        print("=" * 50)
        print("✅ File merger utilities are working correctly!")
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()