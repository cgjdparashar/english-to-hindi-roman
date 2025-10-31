"""
Demo script for file_splitter utility.
Demonstrates how to use the file splitter to break large text files into smaller chunks.
"""

from utility.file_splitter import split_file


def demo_file_splitter():
    """
    Demonstrate the file splitter with the existing story.txt file.
    """
    print("\n" + "="*70)
    print("FILE SPLITTER DEMO")
    print("="*70)
    
    # Example 1: Split the existing story.txt file
    print("\n📄 Example 1: Splitting utility/inputfile/story.txt")
    print("-" * 70)
    
    result = split_file(
        input_file_path="utility/inputfile/story.txt",
        output_folder_name="story1",  # Will create story/story1/
        max_chars_per_file=2000
    )
    
    if result["success"]:
        print("✓ SUCCESS!")
        print(f"\n  Output folder: {result['output_folder']}")
        print(f"  Total characters: {result['total_chars']:,}")
        print(f"  Files created: {result['files_created']}")
        print(f"\n  Generated files:")
        for i in range(1, result['files_created'] + 1):
            chunk_size = len(result['chunks'][i-1])
            print(f"    - {i}.txt ({chunk_size} characters)")
    else:
        print(f"✗ FAILED: {result['error']}")
    
    # Example 2: Using custom chunk size
    print("\n\n📄 Example 2: Using smaller chunk size (1000 characters)")
    print("-" * 70)
    
    result2 = split_file(
        input_file_path="utility/inputfile/story.txt",
        output_folder_name="story1_small_chunks",
        max_chars_per_file=1000
    )
    
    if result2["success"]:
        print("✓ SUCCESS!")
        print(f"\n  Output folder: {result2['output_folder']}")
        print(f"  Total characters: {result2['total_chars']:,}")
        print(f"  Files created: {result2['files_created']}")
        print(f"\n  Generated files:")
        for i in range(1, min(result2['files_created'] + 1, 6)):  # Show first 5
            chunk_size = len(result2['chunks'][i-1])
            print(f"    - {i}.txt ({chunk_size} characters)")
        if result2['files_created'] > 5:
            print(f"    ... and {result2['files_created'] - 5} more files")
    else:
        print(f"✗ FAILED: {result2['error']}")
    
    print("\n" + "="*70)
    print("Demo complete! Check the story/ folder for output files.")
    print("="*70 + "\n")


if __name__ == "__main__":
    demo_file_splitter()
