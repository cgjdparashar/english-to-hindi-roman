import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utility.generic_file_splitter import split_any_file

# Use absolute path to ensure it works from any directory
story_file = project_root / "story" / "input" / "story_31_10.txt"
result = split_any_file(str(story_file))

# Display results
if result["success"]:
    print(f"\n✓ SUCCESS!")
    print(f"Output folder: {result['output_folder']}")
    print(f"Total characters: {result['total_chars']:,}")
    print(f"Files created: {result['files_created']}")
    print(f"\nGenerated files:")
    for i in range(1, min(result['files_created'] + 1, 11)):
        print(f"  - {i}.txt")
    if result['files_created'] > 10:
        print(f"  ... and {result['files_created'] - 10} more files")
else:
    print(f"\n✗ ERROR: {result['error']}")