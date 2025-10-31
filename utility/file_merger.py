"""
File Merger Utility
Merges split text files (1.txt, 2.txt, etc.) back into a single text file.
Reads files in numerical order and combines them with appropriate spacing.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple


def get_numbered_files(folder_path: str) -> List[Tuple[int, str]]:
    """
    Get all numbered text files from a folder and sort them numerically.
    
    Args:
        folder_path: Path to folder containing numbered files
    
    Returns:
        List of (file_number, file_path) tuples sorted by number
    """
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        return []
    
    numbered_files = []
    
    # Find all .txt files that match the pattern number.txt
    for file_path in folder.glob("*.txt"):
        # Extract number from filename using regex
        match = re.match(r'^(\d+)\.txt$', file_path.name)
        if match:
            file_number = int(match.group(1))
            numbered_files.append((file_number, str(file_path)))
    
    # Sort by file number
    numbered_files.sort(key=lambda x: x[0])
    return numbered_files


def merge_files(input_folder: str, output_file: str = None, 
                separator: str = "\n\n") -> dict:
    """
    Merge numbered text files from a folder into a single file.
    
    Args:
        input_folder: Path to folder containing numbered text files (1.txt, 2.txt, etc.)
        output_file: Path for merged output file (default: merged.txt in input folder)
        separator: Text to insert between merged files (default: double newline)
    
    Returns:
        Dictionary with merge results including:
        - success: bool
        - output_file: path to created merged file
        - files_merged: number of files merged
        - total_chars: total characters in merged file
        - error: error message if failed
    """
    try:
        # Validate input folder
        input_path = Path(input_folder)
        if not input_path.exists():
            return {
                "success": False,
                "error": f"Input folder not found: {input_folder}"
            }
        
        if not input_path.is_dir():
            return {
                "success": False,
                "error": f"Path is not a directory: {input_folder}"
            }
        
        # Get numbered files
        numbered_files = get_numbered_files(input_folder)
        
        if not numbered_files:
            return {
                "success": False,
                "error": f"No numbered text files found in: {input_folder}"
            }
        
        # Set default output file if not provided
        if output_file is None:
            output_file = str(input_path / "merged.txt")
        
        # Read and merge files
        merged_content = []
        files_processed = 0
        
        for file_number, file_path in numbered_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:  # Only add non-empty content
                        merged_content.append(content)
                        files_processed += 1
            except Exception as e:
                print(f"Warning: Could not read file {file_path}: {e}")
                continue
        
        if not merged_content:
            return {
                "success": False,
                "error": "No content found in any of the numbered files"
            }
        
        # Join content with separator
        final_content = separator.join(merged_content)
        total_chars = len(final_content)
        
        # Write merged file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        return {
            "success": True,
            "output_file": str(output_path.absolute()),
            "files_merged": files_processed,
            "total_chars": total_chars,
            "files_found": len(numbered_files)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Merge failed: {str(e)}"
        }


def merge_translated_files(story_name: str, base_dir: str = "story", 
                          output_dir: str = None) -> dict:
    """
    Convenience function to merge translated files for a specific story.
    
    Args:
        story_name: Name of the story (folder name)
        base_dir: Base directory containing translate folder (default: "story")
        output_dir: Directory for output file (default: story/merged/)
    
    Returns:
        Dictionary with merge results
    """
    # Construct paths
    input_folder = Path(base_dir) / "translate" / story_name
    
    if output_dir is None:
        output_dir = Path(base_dir) / "merged"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{story_name}_merged.txt"
    
    return merge_files(str(input_folder), str(output_file))


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Merge numbered text files into a single file')
    parser.add_argument('input_folder', help='Path to folder containing numbered text files')
    parser.add_argument('-o', '--output', help='Output file path (default: merged.txt in input folder)')
    parser.add_argument('-s', '--separator', default='\n\n', 
                       help='Separator between merged files (default: double newline)')
    parser.add_argument('--story-mode', action='store_true',
                       help='Use story mode: treat input as story name in story/translate/')
    
    args = parser.parse_args()
    
    if args.story_mode:
        # Story mode: merge from story/translate/story_name
        result = merge_translated_files(args.input_folder, output_dir=args.output)
    else:
        # Direct folder mode
        result = merge_files(args.input_folder, args.output, args.separator)
    
    if result["success"]:
        print(f"✅ Merge successful!")
        print(f"📁 Output file: {result['output_file']}")
        print(f"📄 Files merged: {result['files_merged']}")
        print(f"📊 Total characters: {result['total_chars']:,}")
        if 'files_found' in result:
            print(f"🔍 Files found: {result['files_found']}")
    else:
        print(f"❌ Merge failed: {result['error']}")