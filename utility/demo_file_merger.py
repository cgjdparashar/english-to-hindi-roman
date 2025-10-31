#!/usr/bin/env python3
"""
Demo: File Merger Utility
Demonstrates how to use the file merger utilities to combine split text files.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utility.file_merger import merge_files, merge_translated_files
from utility.generic_file_merger import merge_any_folder


def demo_basic_merge():
    """Demo basic file merging functionality."""
    print("="*60)
    print("📁 DEMO: Basic File Merging")
    print("="*60)
    
    # Example folder with split files
    test_folder = "story/output/story_31_10"
    
    print(f"🔧 Merging files from: {test_folder}")
    
    # Merge with default settings
    result = merge_files(test_folder)
    
    if result["success"]:
        print(f"✅ Merge successful!")
        print(f"📄 Output: {result['output_file']}")
        print(f"🔢 Files merged: {result['files_merged']}")
        print(f"📊 Characters: {result['total_chars']:,}")
    else:
        print(f"❌ Merge failed: {result['error']}")
    
    print()


def demo_custom_output():
    """Demo merging with custom output file and separator."""
    print("="*60)
    print("📝 DEMO: Custom Output & Separator")
    print("="*60)
    
    test_folder = "story/output/story_31_10"
    custom_output = "story/custom_merged_story.txt"
    custom_separator = "\n\n--- CHAPTER BREAK ---\n\n"
    
    print(f"🔧 Merging files from: {test_folder}")
    print(f"📄 Output file: {custom_output}")
    print(f"🔗 Custom separator: {repr(custom_separator)}")
    
    result = merge_files(test_folder, custom_output, custom_separator)
    
    if result["success"]:
        print(f"✅ Custom merge successful!")
        print(f"📄 Output: {result['output_file']}")
        print(f"🔢 Files merged: {result['files_merged']}")
        print(f"📊 Characters: {result['total_chars']:,}")
    else:
        print(f"❌ Custom merge failed: {result['error']}")
    
    print()


def demo_generic_merger():
    """Demo the generic file merger (works with any folder path)."""
    print("="*60)
    print("🌐 DEMO: Generic File Merger")
    print("="*60)
    
    test_folder = "story/output/story_31_10"
    
    print(f"🔧 Using generic merger on: {test_folder}")
    
    result = merge_any_folder(test_folder)
    
    if result["success"]:
        print(f"✅ Generic merge successful!")
        print(f"📁 Input: {result['input_folder_original']}")
        print(f"📄 Output: {result['output_file']}")
        print(f"🔢 Files merged: {result['files_merged']}")
        print(f"📊 Characters: {result['total_chars']:,}")
    else:
        print(f"❌ Generic merge failed: {result['error']}")
    
    print()


def demo_story_mode():
    """Demo merging translated files using story mode."""
    print("="*60)
    print("📚 DEMO: Story Mode (for translated files)")
    print("="*60)
    
    story_name = "story_31_10"
    
    print(f"🔧 Merging translated files for story: {story_name}")
    print(f"📁 Looking in: story/translate/{story_name}/")
    
    # Note: This will fail if there are no translated files yet
    result = merge_translated_files(story_name)
    
    if result["success"]:
        print(f"✅ Story mode merge successful!")
        print(f"📄 Output: {result['output_file']}")
        print(f"🔢 Files merged: {result['files_merged']}")
        print(f"📊 Characters: {result['total_chars']:,}")
    else:
        print(f"ℹ️ Story mode info: {result['error']}")
        print(f"💡 This is expected if you haven't created translated files yet.")
    
    print()


def demo_error_handling():
    """Demo error handling with invalid inputs."""
    print("="*60)
    print("⚠️  DEMO: Error Handling")
    print("="*60)
    
    # Test with non-existent folder
    print("🔧 Testing with non-existent folder...")
    result = merge_files("nonexistent/folder")
    print(f"Expected error: {result['error']}")
    
    # Test with empty folder
    print("\n🔧 Testing with empty folder...")
    empty_folder = "story/translate/story_31_10"  # This should be empty
    result = merge_files(empty_folder)
    print(f"Expected error: {result['error']}")
    
    print()


def main():
    """Run all demos."""
    print("🚀 FILE MERGER UTILITY DEMOS")
    print("This demo shows different ways to merge split text files.")
    print()
    
    # Run demos
    demo_basic_merge()
    demo_custom_output()
    demo_generic_merger()
    demo_story_mode()
    demo_error_handling()
    
    print("="*60)
    print("🎯 USAGE EXAMPLES")
    print("="*60)
    print("Command line usage:")
    print('  python utility/generic_file_merger.py "story/output/story_31_10"')
    print('  python utility/generic_file_merger.py "C:/temp/chunks" --output "final.txt"')
    print()
    print("Programmatic usage:")
    print("  from utility.generic_file_merger import merge_any_folder")
    print('  result = merge_any_folder("story/output/story_31_10")')
    print()
    print("For translated files:")
    print("  from utility.file_merger import merge_translated_files")
    print('  result = merge_translated_files("story_31_10")')
    print()


if __name__ == "__main__":
    main()