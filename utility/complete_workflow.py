#!/usr/bin/env python3
"""
Complete Workflow Example: Split, Translate, and Merge
Demonstrates the full pipeline of file processing with the new utilities.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utility.generic_file_splitter import split_any_file
from utility.generic_file_merger import merge_any_folder
from utility.translator import english_to_hinglish


def complete_translation_workflow(input_file: str, final_output: str = None):
    """
    Complete workflow: Split → Translate → Merge
    
    Args:
        input_file: Path to the original large file
        final_output: Path for final merged translated file
    """
    print("🚀 COMPLETE TRANSLATION WORKFLOW")
    print("=" * 50)
    
    # Step 1: Split the large file
    print("📁 Step 1: Splitting large file...")
    print(f"   Input: {input_file}")
    
    split_result = split_any_file(input_file, max_chars_per_file=2000)
    
    if not split_result["success"]:
        print(f"❌ Split failed: {split_result['error']}")
        return False
    
    print(f"✅ Split successful!")
    print(f"   Output folder: {split_result['output_folder']}")
    print(f"   Files created: {split_result['files_created']}")
    print()
    
    # Step 2: Translate each chunk
    print("🔄 Step 2: Translating chunks...")
    output_folder = Path(split_result['output_folder'])
    translate_folder = output_folder.parent / f"{output_folder.name}_translated"
    translate_folder.mkdir(exist_ok=True)
    
    translated_files = 0
    total_chars_translated = 0
    
    for i in range(1, split_result['files_created'] + 1):
        chunk_file = output_folder / f"{i}.txt"
        translated_file = translate_folder / f"{i}.txt"
        
        try:
            # Read original chunk
            with open(chunk_file, 'r', encoding='utf-8') as f:
                original_text = f.read().strip()
            
            if original_text:
                # Translate chunk
                print(f"   Translating chunk {i}/{split_result['files_created']}...")
                translated_text = english_to_hinglish(original_text)
                
                if translated_text and not translated_text.startswith("Translation error"):
                    # Save translated chunk
                    with open(translated_file, 'w', encoding='utf-8') as f:
                        f.write(translated_text)
                    
                    translated_files += 1
                    total_chars_translated += len(translated_text)
                else:
                    print(f"   ⚠️ Translation failed for chunk {i}: {translated_text}")
            
        except Exception as e:
            print(f"   ⚠️ Error processing chunk {i}: {e}")
            continue
    
    print(f"✅ Translation complete!")
    print(f"   Files translated: {translated_files}")
    print(f"   Total characters: {total_chars_translated:,}")
    print()
    
    # Step 3: Merge translated chunks
    print("🔗 Step 3: Merging translated chunks...")
    
    if final_output is None:
        input_name = Path(input_file).stem
        final_output = f"{input_name}_complete_hinglish.txt"
    
    merge_result = merge_any_folder(str(translate_folder), final_output)
    
    if not merge_result["success"]:
        print(f"❌ Merge failed: {merge_result['error']}")
        return False
    
    print(f"✅ Merge successful!")
    print(f"   Final output: {merge_result['output_file']}")
    print(f"   Files merged: {merge_result['files_merged']}")
    print(f"   Total characters: {merge_result['total_chars']:,}")
    print()
    
    # Summary
    print("🎉 WORKFLOW COMPLETE!")
    print("=" * 50)
    print(f"📄 Original file: {input_file}")
    print(f"📁 Split into: {split_result['files_created']} chunks")
    print(f"🔄 Translated: {translated_files} chunks")
    print(f"📄 Final result: {merge_result['output_file']}")
    print(f"📊 Final size: {merge_result['total_chars']:,} characters")
    
    return True


def demo_workflow_with_existing_files():
    """Demo the workflow using existing files."""
    print("🧪 DEMO: Workflow with existing files")
    print("=" * 50)
    
    # Use existing split files for demo
    existing_folder = "story/output/story_31_10"
    
    if not Path(existing_folder).exists():
        print(f"❌ Demo folder not found: {existing_folder}")
        return
    
    print(f"📁 Using existing split files from: {existing_folder}")
    
    # Just demonstrate the merge step (since we already have split files)
    print("🔗 Demonstrating merge step...")
    
    demo_output = "story/demo_workflow_merged.txt"
    result = merge_any_folder(existing_folder, demo_output)
    
    if result["success"]:
        print(f"✅ Demo merge successful!")
        print(f"📄 Output: {result['output_file']}")
        print(f"🔢 Files merged: {result['files_merged']}")
        print(f"📊 Characters: {result['total_chars']:,}")
        
        # Show a sample of the merged content
        with open(result['output_file'], 'r', encoding='utf-8') as f:
            sample = f.read()[:500]
        
        print("\n📖 Sample of merged content:")
        print("-" * 30)
        print(sample)
        if len(sample) >= 500:
            print("... (truncated)")
        print("-" * 30)
    else:
        print(f"❌ Demo merge failed: {result['error']}")


def main():
    """Main function - run demos and examples."""
    print("🚀 COMPLETE WORKFLOW DEMONSTRATION")
    print("This shows how to combine all utilities for full text processing.")
    print()
    
    # Demo with existing files first
    demo_workflow_with_existing_files()
    print()
    
    # Example of complete workflow (commented out to avoid actual translation)
    print("💡 COMPLETE WORKFLOW EXAMPLE")
    print("=" * 50)
    print("To run a complete workflow, use:")
    print()
    print("Python code:")
    print("  from utility.complete_workflow import complete_translation_workflow")
    print('  success = complete_translation_workflow("path/to/large_file.txt")')
    print()
    print("Command line equivalent:")
    print("  # 1. Split")
    print('  python utility/generic_file_splitter.py "large_file.txt"')
    print("  # 2. Translate (your custom code)")
    print("  # 3. Merge")
    print('  python utility/generic_file_merger.py "output_folder_translated"')
    print()
    
    print("🔄 WORKFLOW STEPS:")
    print("1. 📁 Split large file into manageable chunks")
    print("2. 🔄 Translate each chunk to Hinglish")
    print("3. 🔗 Merge translated chunks into final file")
    print("4. 🎉 Complete translated document ready!")


if __name__ == "__main__":
    main()