#!/usr/bin/env python3
"""
Generic File Splitter Utility
A reusable script that takes any file path as input and splits it into smaller chunks.
Supports both command-line usage and programmatic usage.

Usage:
    python utility/generic_file_splitter.py <file_path> [options]
    
Examples:
    python utility/generic_file_splitter.py "C:/path/to/story.txt"
    python utility/generic_file_splitter.py "/home/user/book.txt" --output-dir "story/output" --folder-name "my_book" --chunk-size 1500
"""

import os
import sys
import argparse
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utility.file_splitter import split_file


def get_absolute_path(file_path: str) -> str:
    """
    Convert relative or absolute path to absolute path.
    
    Args:
        file_path: Input file path (can be relative or absolute)
    
    Returns:
        Absolute path as string
    """
    path = Path(file_path)
    if path.is_absolute():
        return str(path)
    else:
        # If relative, make it relative to current working directory
        return str(Path.cwd() / path)


def auto_generate_folder_name(file_path: str) -> str:
    """
    Generate a folder name based on the input file path.
    
    Args:
        file_path: Input file path
    
    Returns:
        Generated folder name
    """
    file_path = Path(file_path)
    # Use filename without extension as folder name
    return file_path.stem


def auto_determine_output_dir(file_path: str, custom_output_dir: str = None) -> str:
    """
    Determine the best output directory based on input file location.
    
    Args:
        file_path: Input file path
        custom_output_dir: Custom output directory if specified
    
    Returns:
        Output directory path
    """
    if custom_output_dir:
        return custom_output_dir
    
    file_path = Path(file_path)
    
    # If input is in story/input/, output to story/output/
    if "story" in file_path.parts and "input" in file_path.parts:
        return "story/output"
    
    # If input is anywhere else, create output folder in same directory
    return str(file_path.parent / "output")


def split_file_generic(file_path: str, 
                      output_folder_name: str = None,
                      output_base_dir: str = None,
                      max_chars_per_file: int = 2000,
                      verbose: bool = True) -> dict:
    """
    Generic file splitting function that handles any file path.
    
    Args:
        file_path: Absolute or relative path to input file
        output_folder_name: Name for output folder (auto-generated if None)
        output_base_dir: Base directory for output (auto-determined if None)
        max_chars_per_file: Maximum characters per output file
        verbose: Whether to print progress information
    
    Returns:
        Dictionary with operation results
    """
    try:
        # Convert to absolute path
        abs_file_path = get_absolute_path(file_path)
        
        if verbose:
            print(f"\n{'='*80}")
            print("GENERIC FILE SPLITTER")
            print(f"{'='*80}")
            print(f"Input file: {abs_file_path}")
        
        # Validate input file exists
        if not Path(abs_file_path).exists():
            error_msg = f"File not found: {abs_file_path}"
            if verbose:
                print(f"✗ ERROR: {error_msg}")
            return {"success": False, "error": error_msg}
        
        # Auto-generate folder name if not provided
        if output_folder_name is None:
            output_folder_name = auto_generate_folder_name(abs_file_path)
            if verbose:
                print(f"Auto-generated folder name: {output_folder_name}")
        
        # Auto-determine output directory if not provided
        if output_base_dir is None:
            output_base_dir = auto_determine_output_dir(abs_file_path)
            if verbose:
                print(f"Auto-determined output directory: {output_base_dir}")
        
        if verbose:
            print(f"Maximum characters per file: {max_chars_per_file}")
            print(f"{'='*80}")
            print("Processing...")
        
        # Perform the file splitting
        result = split_file(
            input_file_path=abs_file_path,
            output_folder_name=output_folder_name,
            max_chars_per_file=max_chars_per_file,
            output_base_dir=output_base_dir
        )
        
        # Display results
        if result["success"]:
            if verbose:
                print(f"\n✓ SUCCESS!")
                print(f"Output folder: {result['output_folder']}")
                print(f"Total characters: {result['total_chars']:,}")
                print(f"Files created: {result['files_created']}")
                print(f"\nGenerated files:")
                
                # Show first 10 files
                for i in range(1, min(result['files_created'] + 1, 11)):
                    print(f"  - {i}.txt")
                
                if result['files_created'] > 10:
                    print(f"  ... and {result['files_created'] - 10} more files")
                
                print(f"\n{'='*80}")
                print("✓ FILE SPLITTING COMPLETED SUCCESSFULLY!")
                print(f"{'='*80}\n")
        else:
            if verbose:
                print(f"\n✗ FAILED: {result['error']}")
        
        return result
    
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        if verbose:
            print(f"\n✗ ERROR: {error_msg}")
        return {"success": False, "error": error_msg}


def main():
    """
    Main function for command-line usage.
    """
    parser = argparse.ArgumentParser(
        description="Generic File Splitter - Split large text files into smaller chunks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "C:/Users/user/Documents/story.txt"
  %(prog)s "/home/user/book.txt" --chunk-size 1500
  %(prog)s "story/input/story.txt" --output-dir "story/output" --folder-name "my_story"
  %(prog)s "relative/path/file.txt" --chunk-size 1000 --verbose
        """
    )
    
    parser.add_argument("file_path", 
                       help="Path to the input text file (absolute or relative)")
    
    parser.add_argument("--folder-name", "-f",
                       help="Name for the output folder (default: auto-generated from filename)")
    
    parser.add_argument("--output-dir", "-o",
                       help="Base directory for output (default: auto-determined)")
    
    parser.add_argument("--chunk-size", "-c", type=int, default=2000,
                       help="Maximum characters per output file (default: 2000)")
    
    parser.add_argument("--quiet", "-q", action="store_true",
                       help="Suppress verbose output")
    
    parser.add_argument("--version", action="version", version="Generic File Splitter 1.0")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate chunk size
    if args.chunk_size <= 0:
        print("Error: Chunk size must be greater than 0")
        sys.exit(1)
    
    if args.chunk_size > 10000:
        print("Warning: Large chunk size may result in fewer files")
    
    # Execute file splitting
    result = split_file_generic(
        file_path=args.file_path,
        output_folder_name=args.folder_name,
        output_base_dir=args.output_dir,
        max_chars_per_file=args.chunk_size,
        verbose=not args.quiet
    )
    
    # Exit with appropriate code
    if result["success"]:
        sys.exit(0)
    else:
        if not args.quiet:
            print(f"\nOperation failed: {result['error']}")
        sys.exit(1)


# Function for programmatic usage
def split_any_file(file_path: str, **kwargs) -> dict:
    """
    Convenience function for programmatic usage.
    
    Args:
        file_path: Path to input file
        **kwargs: Additional arguments for split_file_generic
    
    Returns:
        Result dictionary
    """
    return split_file_generic(file_path, **kwargs)


if __name__ == "__main__":
    main()