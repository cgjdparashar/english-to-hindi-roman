"""
File translator utility module

This module reads text files from inputfile directory, translates them
using the english_to_hinglish translator, and saves the output to outputfile directory.
"""

import os
from pathlib import Path
from typing import Optional
from .translator import english_to_hinglish


# Get the base directory for utility module
UTILITY_DIR = Path(__file__).parent
INPUT_DIR = UTILITY_DIR / "inputfile"
OUTPUT_DIR = UTILITY_DIR / "outputfile"


def ensure_output_directory() -> Path:
    """
    Ensure the output directory exists, create it if it doesn't.
    
    Returns:
        Path object for the output directory
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


def read_file(filename: str, input_dir: Optional[Path] = None) -> str:
    """
    Read content from a file in the input directory.
    
    Args:
        filename: Name of the file to read
        input_dir: Optional custom input directory path. Uses default INPUT_DIR if not provided.
        
    Returns:
        Content of the file as string
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    if input_dir is None:
        input_dir = INPUT_DIR
    
    file_path = input_dir / filename
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        raise IOError(f"Error reading file {file_path}: {str(e)}")


def save_file(filename: str, content: str, output_dir: Optional[Path] = None) -> Path:
    """
    Save translated content to a file in the output directory.
    
    Args:
        filename: Name of the file to save
        content: Content to write to the file
        output_dir: Optional custom output directory path. Uses default OUTPUT_DIR if not provided.
        
    Returns:
        Path object of the saved file
        
    Raises:
        IOError: If there's an error writing the file
    """
    if output_dir is None:
        output_dir = ensure_output_directory()
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = output_dir / filename
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    except Exception as e:
        raise IOError(f"Error writing file {file_path}: {str(e)}")


def translate_file(
    input_filename: str,
    output_filename: Optional[str] = None,
    input_dir: Optional[Path] = None,
    output_dir: Optional[Path] = None
) -> dict:
    """
    Translate a text file from English to Hinglish.
    
    Reads a file from the input directory, translates its content using
    english_to_hinglish, and saves the result to the output directory.
    
    Args:
        input_filename: Name of the input file to translate
        output_filename: Name for the output file. If not provided, uses input filename
                        with '_hinglish' suffix before extension.
        input_dir: Optional custom input directory path
        output_dir: Optional custom output directory path
        
    Returns:
        Dictionary with translation details:
        {
            'input_file': str,
            'output_file': str,
            'input_path': Path,
            'output_path': Path,
            'original_text': str,
            'translated_text': str,
            'success': bool,
            'error': Optional[str]
        }
    """
    result = {
        'input_file': input_filename,
        'output_file': None,
        'input_path': None,
        'output_path': None,
        'original_text': '',
        'translated_text': '',
        'success': False,
        'error': None
    }
    
    try:
        # Generate output filename if not provided
        if output_filename is None:
            name_parts = input_filename.rsplit('.', 1)
            if len(name_parts) == 2:
                output_filename = f"{name_parts[0]}_hinglish.{name_parts[1]}"
            else:
                output_filename = f"{input_filename}_hinglish"
        
        result['output_file'] = output_filename
        
        # Read the input file
        print(f"Reading file: {input_filename}...")
        original_text = read_file(input_filename, input_dir)
        result['original_text'] = original_text
        result['input_path'] = (input_dir or INPUT_DIR) / input_filename
        
        # Translate the content
        print(f"Translating text ({len(original_text)} characters)...")
        translated_text = english_to_hinglish(original_text)
        result['translated_text'] = translated_text
        
        # Save the translated content
        print(f"Saving translation to: {output_filename}...")
        output_path = save_file(output_filename, translated_text, output_dir)
        result['output_path'] = output_path
        
        result['success'] = True
        print(f"✓ Translation complete! Saved to: {output_path}")
        
    except FileNotFoundError as e:
        result['error'] = str(e)
        print(f"✗ Error: {e}")
    except Exception as e:
        result['error'] = f"Translation failed: {str(e)}"
        print(f"✗ Error: {e}")
    
    return result


def translate_multiple_files(
    filenames: list[str],
    input_dir: Optional[Path] = None,
    output_dir: Optional[Path] = None
) -> list[dict]:
    """
    Translate multiple files from English to Hinglish.
    
    Args:
        filenames: List of input filenames to translate
        input_dir: Optional custom input directory path
        output_dir: Optional custom output directory path
        
    Returns:
        List of result dictionaries for each file translation
    """
    results = []
    
    print(f"\nTranslating {len(filenames)} file(s)...")
    print("=" * 60)
    
    for i, filename in enumerate(filenames, 1):
        print(f"\n[{i}/{len(filenames)}] Processing: {filename}")
        print("-" * 60)
        result = translate_file(filename, input_dir=input_dir, output_dir=output_dir)
        results.append(result)
    
    # Summary
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    print("\n" + "=" * 60)
    print(f"Translation Summary: {successful} succeeded, {failed} failed")
    print("=" * 60)
    
    return results


def main():
    """
    Example usage of the file translator.
    """
    print("File Translator Utility")
    print("=" * 60)
    
    # Example: Translate story.txt
    result = translate_file("story.txt")
    
    if result['success']:
        print(f"\nOriginal text preview:")
        print(f"{result['original_text'][:100]}...")
        print(f"\nTranslated text preview:")
        print(f"{result['translated_text'][:100]}...")
    else:
        print(f"\nTranslation failed: {result['error']}")


if __name__ == "__main__":
    main()
