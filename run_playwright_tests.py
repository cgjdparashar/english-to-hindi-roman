#!/usr/bin/env python3
"""
DEPRECATED: This file is no longer needed.

Use the new translation interface instead:
    python translate_files.py

Or use the translation utilities directly:
    from utility.playwright_translator import translate_single_file, translate_all_files
"""

import sys
from pathlib import Path

def main():
    print("⚠️  NOTICE: This script has been replaced!")
    print("=" * 50)
    print("The Playwright tests have been converted to a proper translation processor.")
    print()
    print("🚀 NEW USAGE:")
    print("   python translate_files.py          # Interactive translation interface")
    print()
    print("📚 OR USE DIRECTLY:")
    print("   from utility.playwright_translator import translate_single_file")
    print("   result = translate_single_file('story/output/story_31_10/1.txt')")
    print()
    print("📖 WORKFLOW:")
    print("   1. Split large files: python utility/demo_generic_splitter.py")
    print("   2. Translate files: python translate_files.py")
    print("   3. Files saved to: story/output/[name]/translated/")
    print()
    
    choice = input("Run the new translation interface? (y/N): ").strip().lower()
    if choice == 'y':
        # Import and run the new interface
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root))
        
        from translate_files import main as translate_main
        translate_main()
    else:
        print("👋 Run 'python translate_files.py' when you're ready to translate!")

if __name__ == "__main__":
    main()