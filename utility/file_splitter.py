"""
File Splitter Utility
Splits large text files (up to 300,000 characters) into smaller chunks of max 2000 characters each.
Creates a folder in story/ directory named after the input file, containing numbered output files.
"""

import os
from pathlib import Path
from typing import List


def split_text_into_chunks(text: str, max_chars: int = 2000) -> List[str]:
    """
    Split text into chunks of maximum size.
    
    Args:
        text: The text to split
        max_chars: Maximum characters per chunk (default: 2000)
    
    Returns:
        List of text chunks
    """
    chunks = []
    current_pos = 0
    text_length = len(text)
    
    while current_pos < text_length:
        # Calculate end position for this chunk
        end_pos = min(current_pos + max_chars, text_length)
        
        # If not at the end of text, try to break at a sentence or word boundary
        if end_pos < text_length:
            # Look for sentence endings (., !, ?) within last 200 chars
            search_start = max(current_pos, end_pos - 200)
            last_sentence = max(
                text.rfind('. ', search_start, end_pos),
                text.rfind('! ', search_start, end_pos),
                text.rfind('? ', search_start, end_pos)
            )
            
            if last_sentence != -1 and last_sentence > current_pos:
                end_pos = last_sentence + 1  # Include the punctuation
            else:
                # If no sentence boundary, try word boundary
                last_space = text.rfind(' ', search_start, end_pos)
                if last_space != -1 and last_space > current_pos:
                    end_pos = last_space
        
        # Extract chunk and add to list
        chunk = text[current_pos:end_pos].strip()
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)
        
        current_pos = end_pos
    
    return chunks


def split_file(input_file_path: str, output_folder_name: str = None, 
               max_chars_per_file: int = 2000, output_base_dir: str = None) -> dict:
    """
    Split a large text file into smaller files.
    
    Args:
        input_file_path: Path to the input text file
        output_folder_name: Name for output folder (default: uses input filename)
        max_chars_per_file: Maximum characters per output file (default: 2000)
        output_base_dir: Base directory for output (default: story/)
    
    Returns:
        Dictionary with split results including:
        - success: bool
        - output_folder: path to created folder
        - files_created: number of files created
        - total_chars: total characters processed
        - error: error message if failed
    """
    try:
        # Validate input file
        input_path = Path(input_file_path)
        if not input_path.exists():
            return {
                "success": False,
                "error": f"Input file not found: {input_file_path}"
            }
        
        if not input_path.is_file():
            return {
                "success": False,
                "error": f"Path is not a file: {input_file_path}"
            }
        
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        total_chars = len(text_content)
        
        # Validate file size
        if total_chars > 300000:
            return {
                "success": False,
                "error": f"File too large: {total_chars} characters (max 300,000)"
            }
        
        if total_chars == 0:
            return {
                "success": False,
                "error": "Input file is empty"
            }
        
        # Determine output folder name
        if output_folder_name is None:
            output_folder_name = input_path.stem  # Filename without extension
        
        # Create output folder path
        project_root = Path(__file__).parent.parent
        if output_base_dir is None:
            # Default: story/ directory
            base_dir = project_root / "story"
        else:
            # Custom base directory (can be absolute or relative to project root)
            base_dir = Path(output_base_dir) if Path(output_base_dir).is_absolute() else project_root / output_base_dir
        
        output_folder = base_dir / output_folder_name
        
        # Create the output folder
        output_folder.mkdir(parents=True, exist_ok=True)
        
        # Split text into chunks
        chunks = split_text_into_chunks(text_content, max_chars_per_file)
        
        # Write chunks to separate files
        files_created = 0
        for i, chunk in enumerate(chunks, start=1):
            output_file = output_folder / f"{i}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(chunk)
            files_created += 1
        
        return {
            "success": True,
            "output_folder": str(output_folder),
            "files_created": files_created,
            "total_chars": total_chars,
            "chunks": chunks  # Include chunks for reference
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Error splitting file: {str(e)}"
        }


def main():
    """
    Main function for command-line usage.
    """
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python file_splitter.py <input_file_path> [output_folder_name] [max_chars_per_file]")
        print("\nExample:")
        print("  python file_splitter.py utility/inputfile/story.txt")
        print("  python file_splitter.py utility/inputfile/story.txt my_story")
        print("  python file_splitter.py utility/inputfile/story.txt my_story 1500")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else None
    max_chars = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
    
    print(f"\n{'='*60}")
    print("FILE SPLITTER UTILITY")
    print(f"{'='*60}")
    print(f"Input file: {input_file}")
    print(f"Max chars per file: {max_chars}")
    print(f"{'='*60}\n")
    
    result = split_file(input_file, output_folder, max_chars)
    
    if result["success"]:
        print("✓ SUCCESS!")
        print(f"\nOutput folder: {result['output_folder']}")
        print(f"Total characters: {result['total_chars']:,}")
        print(f"Files created: {result['files_created']}")
        print(f"\nFiles:")
        for i in range(1, result['files_created'] + 1):
            print(f"  - {i}.txt")
    else:
        print("✗ FAILED!")
        print(f"\nError: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
