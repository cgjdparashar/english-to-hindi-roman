"""
Playwright Web-based Hinglish Translation Processor
===================================================

This module provides automated web-based translation of text files using
the anythingtranslate.com Hinglish translator. It's designed to work with
the file splitter utility to process large documents.

Workflow:
1. User splits large file using generic_file_splitter.py
2. User runs this processor to translate split files one by one
3. Translated files are saved in translated/ directory

Usage:
    from utility.playwright_translator import translate_single_file, translate_all_files
    
    # Translate one file
    translate_single_file("story/output/story_31_10/1.txt")
    
    # Translate all files in a directory
    translate_all_files("story/output/story_31_10")
"""

import re
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, expect

def check_translator_available():
    """Check if the translator website is accessible"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto("https://anythingtranslate.com/translators/hinglish-translator/", timeout=30000)
            page.wait_for_timeout(3000)
            
            # Check if main elements are visible
            input_textarea = page.get_by_placeholder("Enter text to translate...")
            translate_button = page.get_by_role("button", name="Translate", exact=True)
            
            if input_textarea.is_visible() and translate_button.is_visible():
                browser.close()
                return True, "Translator website is accessible"
            else:
                browser.close()
                return False, "Translator interface elements not found"
                
        except Exception as e:
            browser.close()
            return False, f"Error accessing translator: {str(e)}"

def translate_single_file(file_path, max_chars=None):
    """
    Translate a single text file using the web-based Hinglish translator
    
    Args:
        file_path (str or Path): Path to the text file to translate
        max_chars (int, optional): Maximum characters to translate (None for full file)
    
    Returns:
        dict: Result with success status, output file path, and translation info
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return {
            "success": False,
            "error": f"File not found: {file_path}",
            "output_file": None
        }
    
    # Setup output directory
    parent_dir = file_path.parent
    translated_dir = parent_dir / "translated"
    translated_dir.mkdir(exist_ok=True)
    
    # Read file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if max_chars:
                content = content[:max_chars]
    except Exception as e:
        return {
            "success": False,
            "error": f"Error reading file: {str(e)}",
            "output_file": None
        }
    
    if not content.strip():
        return {
            "success": False,
            "error": "File is empty or contains only whitespace",
            "output_file": None
        }
    
    # Perform translation
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            print(f"🌐 Opening translator for {file_path.name}...")
            page.goto("https://anythingtranslate.com/translators/hinglish-translator/", timeout=30000)
            page.wait_for_timeout(3000)
            
            print(f"📝 Entering text ({len(content)} characters)...")
            # Clear and fill input textarea
            input_textarea = page.get_by_placeholder("Enter text to translate...")
            input_textarea.clear()
            input_textarea.fill(content)
            
            print("🔄 Translating...")
            # Click translate button
            page.get_by_role("button", name="Translate", exact=True).click()
            
            # Wait for translation to complete
            page.wait_for_timeout(8000)
            
            # Get translated text from output textarea
            output_textarea = page.locator('textarea').nth(1)
            translated_text = output_textarea.input_value()
            
            if not translated_text or not translated_text.strip():
                browser.close()
                return {
                    "success": False,
                    "error": "No translation received from website",
                    "output_file": None
                }
            
            # Save translated result
            output_file = translated_dir / f"{file_path.stem}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(translated_text)
            
            browser.close()
            
            print(f"✅ Translation complete!")
            print(f"   Original: {len(content)} chars")
            print(f"   Translated: {len(translated_text)} chars")
            print(f"   Saved to: {output_file}")
            
            return {
                "success": True,
                "output_file": str(output_file),
                "original_chars": len(content),
                "translated_chars": len(translated_text),
                "file_name": file_path.name
            }
            
        except Exception as e:
            browser.close()
            return {
                "success": False,
                "error": f"Translation error: {str(e)}",
                "output_file": None
            }

def translate_all_files(directory_path, max_files=None, max_chars_per_file=None):
    """
    Translate all text files in a directory using the web-based Hinglish translator
    
    Args:
        directory_path (str or Path): Directory containing .txt files to translate
        max_files (int, optional): Maximum number of files to process (None for all)
        max_chars_per_file (int, optional): Maximum characters per file (None for full files)
    
    Returns:
        dict: Summary of translation results
    """
    directory_path = Path(directory_path)
    
    if not directory_path.exists():
        return {
            "success": False,
            "error": f"Directory not found: {directory_path}",
            "files_processed": 0,
            "results": []
        }
    
    # Get all .txt files, sorted numerically
    txt_files = sorted([f for f in directory_path.glob("*.txt")], key=lambda x: int(x.stem) if x.stem.isdigit() else 999)
    
    if max_files:
        txt_files = txt_files[:max_files]
    
    if not txt_files:
        return {
            "success": False,
            "error": f"No .txt files found in {directory_path}",
            "files_processed": 0,
            "results": []
        }
    
    print(f"🚀 Starting batch translation of {len(txt_files)} files...")
    print(f"📁 Source directory: {directory_path}")
    print(f"📁 Output directory: {directory_path}/translated/")
    print("-" * 60)
    
    results = []
    successful = 0
    failed = 0
    
    for i, txt_file in enumerate(txt_files, 1):
        print(f"\n[{i}/{len(txt_files)}] Processing {txt_file.name}...")
        
        result = translate_single_file(txt_file, max_chars_per_file)
        results.append(result)
        
        if result["success"]:
            successful += 1
            print(f"   ✅ Success: {result['original_chars']} → {result['translated_chars']} chars")
        else:
            failed += 1
            print(f"   ❌ Failed: {result['error']}")
        
        # Small delay between files to avoid overwhelming the website
        if i < len(txt_files):  # Don't wait after the last file
            print("   ⏳ Waiting 3 seconds before next file...")
            import time
            time.sleep(3)
    
    print("\n" + "=" * 60)
    print(f"📊 BATCH TRANSLATION SUMMARY")
    print(f"   Total files: {len(txt_files)}")
    print(f"   Successful: {successful}")
    print(f"   Failed: {failed}")
    print(f"   Success rate: {(successful/len(txt_files)*100):.1f}%")
    
    if successful > 0:
        total_original = sum(r.get('original_chars', 0) for r in results if r['success'])
        total_translated = sum(r.get('translated_chars', 0) for r in results if r['success'])
        print(f"   Total characters: {total_original} → {total_translated}")
        print(f"   Output location: {directory_path}/translated/")
    
    return {
        "success": failed == 0,  # Success if no failures
        "files_processed": len(txt_files),
        "successful": successful,
        "failed": failed,
        "results": results,
        "output_directory": str(directory_path / "translated")
    }

def translate_specific_files(directory_path, file_numbers):
    """
    Translate specific numbered files from a directory
    
    Args:
        directory_path (str or Path): Directory containing .txt files
        file_numbers (list): List of file numbers to translate (e.g., [1, 3, 5])
    
    Returns:
        dict: Summary of translation results
    """
    directory_path = Path(directory_path)
    results = []
    
    print(f"🎯 Translating specific files: {file_numbers}")
    print(f"📁 Source directory: {directory_path}")
    
    for i, file_num in enumerate(file_numbers, 1):
        file_path = directory_path / f"{file_num}.txt"
        
        if not file_path.exists():
            print(f"[{i}/{len(file_numbers)}] ⚠️  File not found: {file_num}.txt")
            results.append({
                "success": False,
                "error": f"File {file_num}.txt not found",
                "file_name": f"{file_num}.txt"
            })
            continue
        
        print(f"[{i}/{len(file_numbers)}] Processing {file_num}.txt...")
        result = translate_single_file(file_path)
        results.append(result)
        
        # Small delay between files
        if i < len(file_numbers):
            import time
            time.sleep(2)
    
    successful = sum(1 for r in results if r.get('success', False))
    print(f"\n📊 Completed: {successful}/{len(file_numbers)} files translated successfully")
    
    return {
        "success": successful == len(file_numbers),
        "files_requested": len(file_numbers),
        "successful": successful,
        "results": results
    }


# Demo and utility functions
def demo_translation():
    """Demo function to show how to use the translator"""
    print("🎭 PLAYWRIGHT HINGLISH TRANSLATOR DEMO")
    print("=" * 50)
    
    # Check if translator is available
    print("🔍 Checking translator availability...")
    available, message = check_translator_available()
    print(f"   {message}")
    
    if not available:
        print("❌ Cannot proceed - translator not available")
        return False
    
    # Demo with sample text
    sample_text = "Hello, how are you today? I hope you are doing well and staying healthy."
    
    # Create temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(sample_text)
        temp_file = f.name
    
    print(f"\n📝 Demo text: {sample_text}")
    print("🔄 Translating...")
    
    result = translate_single_file(temp_file)
    
    # Cleanup
    os.unlink(temp_file)
    if result['success'] and result['output_file']:
        os.unlink(result['output_file'])
    
    if result['success']:
        print("✅ Demo translation successful!")
        return True
    else:
        print(f"❌ Demo failed: {result['error']}")
        return False


if __name__ == "__main__":
    # Run demo when executed directly
    demo_translation()