#!/usr/bin/env python3
"""
Generic File Merger Utility
A reusable script that takes any folder path containing numbered text files and merges them into a single file.
Supports both command-line usage and programmatic usage.

Usage:
    python utility/generic_file_merger.py <folder_path> [options]
    
Examples:
    python utility/generic_file_merger.py "story/output/story_31_10"
    python utility/generic_file_merger.py "C:/path/to/chunks" --output "merged_story.txt"
    python utility/generic_file_merger.py "story/translate/story_31_10" --separator "\n---\n"
"""

import os
import sys
import argparse
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utility.file_merger import merge_files


def get_absolute_path(folder_path: str) -> str:
    """
    Convert relative or absolute path to absolute path.
    
    Args:
        folder_path: Input folder path (can be relative or absolute)
    
    Returns:
        Absolute path as string
    """
    path = Path(folder_path)
    if path.is_absolute():
        return str(path)
    else:
        # If relative, make it relative to current working directory
        return str(Path.cwd() / path)


def auto_generate_output_file(folder_path: str, suffix: str = "_merged") -> str:
    """
    Generate an output file name based on the input folder path.
    
    Args:
        folder_path: Input folder path
        suffix: Suffix to add to folder name (default: "_merged")
    
    Returns:
        Generated output file path
    """
    folder = Path(folder_path)
    parent_dir = folder.parent
    folder_name = folder.name
    
    return str(parent_dir / f"{folder_name}{suffix}.txt")


def merge_any_folder(folder_path: str, output_file: str = None, 
                    separator: str = "\n\n") -> dict:
    """
    Merge numbered files from any folder path.
    Automatically handles path resolution and output file generation.
    
    Args:
        folder_path: Input folder path (relative or absolute)
        output_file: Output file path (optional, auto-generated if not provided)
        separator: Text separator between merged files
    
    Returns:
        Dictionary with merge results
    """
    try:
        # Convert to absolute path
        abs_folder_path = get_absolute_path(folder_path)
        
        # Auto-generate output file if not provided
        if output_file is None:
            output_file = auto_generate_output_file(abs_folder_path)
        else:
            # Convert output file to absolute path if relative
            output_file = get_absolute_path(output_file)
        
        # Call the core merge function
        result = merge_files(abs_folder_path, output_file, separator)
        
        # Add original paths to result for reference
        result["input_folder_original"] = folder_path
        result["input_folder_absolute"] = abs_folder_path
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to merge folder {folder_path}: {str(e)}"
        }


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description='Merge numbered text files from any folder into a single file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python utility/generic_file_merger.py "story/output/story_31_10"
  python utility/generic_file_merger.py "C:/temp/chunks" --output "final.txt"
  python utility/generic_file_merger.py "translate/story" --separator "\\n---\\n"
        """
    )
    
    parser.add_argument('folder_path', 
                       help='Path to folder containing numbered text files (1.txt, 2.txt, etc.)')
    parser.add_argument('-o', '--output', 
                       help='Output file path (default: auto-generated based on folder name)')
    parser.add_argument('-s', '--separator', default='\n\n',
                       help='Text separator between merged files (default: double newline)')
    parser.add_argument('--chunk-size', type=int, 
                       help='Not used for merging (kept for consistency with splitter)')
    
    args = parser.parse_args()
    
    print(f"🔧 Starting file merge operation...")
    print(f"📁 Input folder: {args.folder_path}")
    
    # Perform merge
    result = merge_any_folder(args.folder_path, args.output, args.separator)
    
    # Display results
    if result["success"]:
        print(f"\n✅ Merge completed successfully!")
        print(f"📁 Input folder: {result['input_folder_absolute']}")
        print(f"📄 Output file: {result['output_file']}")
        print(f"🔢 Files merged: {result['files_merged']}")
        print(f"📊 Total characters: {result['total_chars']:,}")
        if 'files_found' in result:
            print(f"🔍 Files found: {result['files_found']}")
        
        print(f"\n💡 Tip: You can now view the merged file at:")
        print(f"    {result['output_file']}")
        
    else:
        print(f"\n❌ Merge failed!")
        print(f"💥 Error: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()