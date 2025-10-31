"""
Script to split story_31_10.txt into smaller chunks.
"""

from utility.file_splitter import split_file

# Split the story file
result = split_file(
    input_file_path='story/input/story_31_10.txt',
    output_folder_name='story_31_10',
    max_chars_per_file=2000,
    output_base_dir='story/output'
)

# Display results
if result["success"]:
    print("\n" + "="*70)
    print("✓ FILE SPLITTING SUCCESSFUL!")
    print("="*70)
    print(f"\nInput file: story/input/story_31_10.txt")
    print(f"Output folder: {result['output_folder']}")
    print(f"Total characters: {result['total_chars']:,}")
    print(f"Files created: {result['files_created']}")
    print(f"\nGenerated files:")
    for i in range(1, min(result['files_created'] + 1, 11)):
        print(f"  - {i}.txt")
    if result['files_created'] > 10:
        print(f"  ... and {result['files_created'] - 10} more files")
    print("\n" + "="*70)
else:
    print(f"\n✗ ERROR: {result['error']}")
