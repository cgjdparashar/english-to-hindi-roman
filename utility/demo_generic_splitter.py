"""
Demo script for the Generic File Splitter utility.
Shows different ways to use the generic file splitter with various file paths and options.
"""

import sys
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utility.generic_file_splitter import split_file_generic, split_any_file
import os


def demo_generic_splitter():
    """
    Demonstrate various usage patterns of the generic file splitter.
    """
    print("\n" + "="*80)
    print("GENERIC FILE SPLITTER - DEMONSTRATION")
    print("="*80)
    
    # Demo 1: Using absolute path
    print("\n📄 Demo 1: Using absolute path")
    print("-" * 50)
    
    current_dir = Path.cwd()
    abs_path = current_dir / "story" / "input" / "story_31_10.txt"
    
    if abs_path.exists():
        result1 = split_file_generic(
            file_path=str(abs_path),
            output_folder_name="demo_absolute_path",
            max_chars_per_file=1500,
            verbose=False  # Suppress verbose output for demo
        )
        
        if result1["success"]:
            print(f"✓ Success: Created {result1['files_created']} files")
            print(f"  Output: {result1['output_folder']}")
        else:
            print(f"✗ Failed: {result1['error']}")
    else:
        print("ℹ Story file not found - skipping absolute path demo")
    
    
    # Demo 2: Using relative path
    print("\n📄 Demo 2: Using relative path")
    print("-" * 50)
    
    if Path("story/input/story_31_10.txt").exists():
        result2 = split_file_generic(
            file_path="story/input/story_31_10.txt",
            output_folder_name="demo_relative_path",
            max_chars_per_file=2500,
            verbose=False
        )
        
        if result2["success"]:
            print(f"✓ Success: Created {result2['files_created']} files")
            print(f"  Output: {result2['output_folder']}")
        else:
            print(f"✗ Failed: {result2['error']}")
    else:
        print("ℹ Story file not found - skipping relative path demo")
    
    
    # Demo 3: Auto-generated names
    print("\n📄 Demo 3: Auto-generated folder name and output directory")
    print("-" * 50)
    
    if Path("story/input/story_31_10.txt").exists():
        result3 = split_file_generic(
            file_path="story/input/story_31_10.txt",
            # Let it auto-generate folder name and output directory
            max_chars_per_file=3000,
            verbose=False
        )
        
        if result3["success"]:
            print(f"✓ Success: Created {result3['files_created']} files")
            print(f"  Output: {result3['output_folder']}")
            print(f"  Auto-generated from file path!")
        else:
            print(f"✗ Failed: {result3['error']}")
    else:
        print("ℹ Story file not found - skipping auto-generation demo")
    
    
    # Demo 4: Using convenience function
    print("\n📄 Demo 4: Using convenience function split_any_file()")
    print("-" * 50)
    
    if Path("story/input/story_31_10.txt").exists():
        result4 = split_any_file(
            "story/input/story_31_10.txt",
            output_folder_name="demo_convenience_function",
            max_chars_per_file=1800,
            verbose=False
        )
        
        if result4["success"]:
            print(f"✓ Success: Created {result4['files_created']} files")
            print(f"  Output: {result4['output_folder']}")
        else:
            print(f"✗ Failed: {result4['error']}")
    else:
        print("ℹ Story file not found - skipping convenience function demo")
    
    
    # Demo 5: Error handling
    print("\n📄 Demo 5: Error handling for non-existent file")
    print("-" * 50)
    
    result5 = split_file_generic(
        file_path="nonexistent/file.txt",
        verbose=False
    )
    
    if not result5["success"]:
        print(f"✓ Correctly handled error: {result5['error']}")
    else:
        print("✗ Should have failed for non-existent file")
    
    
    print("\n" + "="*80)
    print("DEMO COMPLETED")
    print("="*80)
    print("\nThe generic file splitter can handle:")
    print("✓ Absolute file paths")
    print("✓ Relative file paths") 
    print("✓ Auto-generated folder names")
    print("✓ Auto-determined output directories")
    print("✓ Custom chunk sizes")
    print("✓ Error handling")
    print("✓ Both verbose and quiet modes")
    print("\n💡 Check the story/output/ folder for all the demo output!")
    print("\n")


if __name__ == "__main__":
    demo_generic_splitter()