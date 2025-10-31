#!/usr/bin/env python3
"""
Interactive Hinglish Translation Interface
=========================================

This script provides an easy-to-use interface for translating split story files
using the web-based Hinglish translator.

Prerequisites:
1. Files must be split using generic_file_splitter.py first
2. Playwright must be installed: uv add playwright
3. Browsers must be installed: python setup_playwright.py

Usage:
    python translate_files.py
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utility.playwright_translator import (
    translate_single_file, 
    translate_all_files, 
    translate_specific_files,
    check_translator_available,
    demo_translation
)

def find_story_directories():
    """Find all available story directories"""
    story_output = project_root / "story" / "output"
    if not story_output.exists():
        return []
    
    return [d for d in story_output.iterdir() if d.is_dir() and list(d.glob("*.txt"))]

def show_file_info(directory):
    """Show information about files in directory"""
    txt_files = sorted([f for f in directory.glob("*.txt")], key=lambda x: int(x.stem) if x.stem.isdigit() else 999)
    translated_dir = directory / "translated"
    
    print(f"\n📁 Directory: {directory.name}")
    print(f"   📄 Text files: {len(txt_files)}")
    
    if txt_files:
        print(f"   📊 File range: {txt_files[0].stem} - {txt_files[-1].stem}")
        
        # Check for existing translations
        if translated_dir.exists():
            translated_files = list(translated_dir.glob("*.txt"))
            print(f"   ✅ Already translated: {len(translated_files)}")
        else:
            print(f"   ⏳ Translated: 0")

def main():
    print("🎭 HINGLISH FILE TRANSLATOR")
    print("=" * 50)
    
    # Check translator availability
    print("🔍 Checking translator website...")
    available, message = check_translator_available()
    print(f"   {message}")
    
    if not available:
        print("\n❌ Cannot proceed. Please check your internet connection and try again.")
        return
    
    # Find story directories
    story_dirs = find_story_directories()
    
    if not story_dirs:
        print("\n❌ No story directories found!")
        print("   Please run the file splitter first:")
        print("   python utility/demo_generic_splitter.py")
        return
    
    # Show available directories
    print(f"\n📁 Found {len(story_dirs)} story directories:")
    for i, story_dir in enumerate(story_dirs, 1):
        print(f"   {i}. {story_dir.name}")
        show_file_info(story_dir)
    
    # Directory selection
    while True:
        try:
            choice = input(f"\nSelect directory (1-{len(story_dirs)}) or 'q' to quit: ").strip().lower()
            
            if choice == 'q':
                print("👋 Goodbye!")
                return
            
            dir_index = int(choice) - 1
            if 0 <= dir_index < len(story_dirs):
                selected_dir = story_dirs[dir_index]
                break
            else:
                print(f"Invalid choice. Enter 1-{len(story_dirs)} or 'q'")
        except ValueError:
            print("Invalid input. Enter a number or 'q'")
    
    # Get file info
    txt_files = sorted([f for f in selected_dir.glob("*.txt")], key=lambda x: int(x.stem) if x.stem.isdigit() else 999)
    
    print(f"\n📂 Selected: {selected_dir.name}")
    print(f"   📄 Available files: {len(txt_files)} ({txt_files[0].stem} - {txt_files[-1].stem})")
    
    # Translation options
    print(f"\n🔄 TRANSLATION OPTIONS:")
    print(f"   1. Translate single file")
    print(f"   2. Translate specific files (by numbers)")
    print(f"   3. Translate first 3 files (test batch)")
    print(f"   4. Translate first 10 files")
    print(f"   5. Translate ALL files ({len(txt_files)} files)")
    print(f"   6. Run demo translation")
    
    while True:
        option = input(f"\nChoose option (1-6) or 'q' to quit: ").strip().lower()
        
        if option == 'q':
            print("👋 Goodbye!")
            return
        
        if option == '1':
            # Single file
            file_num = input(f"Enter file number (1-{len(txt_files)}): ").strip()
            try:
                file_path = selected_dir / f"{file_num}.txt"
                if file_path.exists():
                    print(f"\n🚀 Translating {file_num}.txt...")
                    result = translate_single_file(file_path)
                    if result['success']:
                        print(f"✅ Success! Saved to: translated/{file_num}.txt")
                    else:
                        print(f"❌ Failed: {result['error']}")
                else:
                    print(f"❌ File {file_num}.txt not found!")
            except Exception as e:
                print(f"❌ Error: {e}")
            break
            
        elif option == '2':
            # Specific files
            file_nums = input("Enter file numbers separated by commas (e.g., 1,3,5,10): ").strip()
            try:
                numbers = [int(x.strip()) for x in file_nums.split(',')]
                print(f"\n🚀 Translating files: {numbers}")
                result = translate_specific_files(selected_dir, numbers)
                print(f"✅ Completed: {result['successful']}/{result['files_requested']} files")
            except Exception as e:
                print(f"❌ Error: {e}")
            break
            
        elif option == '3':
            # First 3 files
            print(f"\n🚀 Translating first 3 files...")
            result = translate_all_files(selected_dir, max_files=3)
            print(f"✅ Completed: {result['successful']}/{result['files_processed']} files")
            break
            
        elif option == '4':
            # First 10 files
            print(f"\n🚀 Translating first 10 files...")
            result = translate_all_files(selected_dir, max_files=10)
            print(f"✅ Completed: {result['successful']}/{result['files_processed']} files")
            break
            
        elif option == '5':
            # All files
            confirm = input(f"⚠️  This will translate ALL {len(txt_files)} files. Continue? (y/N): ").strip().lower()
            if confirm == 'y':
                print(f"\n🚀 Translating all {len(txt_files)} files...")
                result = translate_all_files(selected_dir)
                print(f"✅ Completed: {result['successful']}/{result['files_processed']} files")
            else:
                print("Cancelled.")
            break
            
        elif option == '6':
            # Demo
            print(f"\n🎭 Running demo translation...")
            demo_translation()
            break
            
        else:
            print("Invalid option. Choose 1-6 or 'q'")

if __name__ == "__main__":
    main()