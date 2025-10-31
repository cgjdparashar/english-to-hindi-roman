# File Merger Utility

The File Merger utility provides tools to combine split text files (numbered files like 1.txt, 2.txt, etc.) back into a single merged file. This is especially useful after processing files with translators or other text processing tools.

## Features

- **Automatic File Detection**: Finds and sorts numbered text files (1.txt, 2.txt, etc.) automatically
- **Flexible Path Handling**: Works with both relative and absolute paths
- **Custom Output**: Specify custom output file paths and separators
- **Error Handling**: Comprehensive error handling for missing files or empty folders
- **Multiple Interfaces**: Command-line tool and programmatic API

## Files Overview

### Core Utilities

- **`utility/file_merger.py`**: Core merging functionality
- **`utility/generic_file_merger.py`**: Generic merger that works with any folder path
- **`utility/demo_file_merger.py`**: Demonstration script showing various merge scenarios

### Test Files

- **`tests/test_file_merger.py`**: Comprehensive test suite for all merger functionality

## Quick Start

### Command Line Usage

```bash
# Basic merge - merges files in folder to merged.txt
python utility/generic_file_merger.py "story/output/story_31_10"

# Custom output file
python utility/generic_file_merger.py "story/output/story_31_10" --output "final_story.txt"

# Custom separator between merged files
python utility/generic_file_merger.py "story/output/story_31_10" --separator "\n---\n"
```

### Programmatic Usage

```python
from utility.generic_file_merger import merge_any_folder
from utility.file_merger import merge_files, merge_translated_files

# Basic merge
result = merge_any_folder("story/output/story_31_10")

# Custom output and separator
result = merge_files("story/output/story_31_10", 
                    "custom_output.txt", 
                    "\n\n--- CHAPTER ---\n\n")

# Merge translated files (story mode)
result = merge_translated_files("story_31_10")
```

## Detailed Usage

### Command Line Interface

```bash
python utility/generic_file_merger.py <folder_path> [options]
```

**Arguments:**
- `folder_path`: Path to folder containing numbered text files (1.txt, 2.txt, etc.)

**Options:**
- `-o, --output`: Output file path (default: auto-generated based on folder name)
- `-s, --separator`: Text separator between merged files (default: double newline)

**Examples:**
```bash
# Merge files from Windows path
python utility/generic_file_merger.py "C:\temp\split_files"

# Merge with custom output
python utility/generic_file_merger.py "story/output/story_31_10" -o "merged_story.txt"

# Merge with chapter breaks
python utility/generic_file_merger.py "story/translate/story_31_10" --separator "\n\n=== CHAPTER ===\n\n"
```

### Programmatic API

#### `merge_files(input_folder, output_file=None, separator="\n\n")`

Core merge function that combines numbered files from a folder.

**Parameters:**
- `input_folder` (str): Path to folder containing numbered files
- `output_file` (str, optional): Output file path (default: merged.txt in input folder)
- `separator` (str): Text to insert between merged files (default: double newline)

**Returns:**
```python
{
    "success": bool,           # Whether merge succeeded
    "output_file": str,        # Path to created merged file
    "files_merged": int,       # Number of files successfully merged
    "total_chars": int,        # Total characters in merged file
    "files_found": int,        # Total numbered files found
    "error": str               # Error message if failed
}
```

#### `merge_any_folder(folder_path, output_file=None, separator="\n\n")`

Generic merger that handles path resolution and auto-generates output file names.

**Parameters:**
- `folder_path` (str): Input folder path (relative or absolute)
- `output_file` (str, optional): Output file path (auto-generated if not provided)
- `separator` (str): Text separator between merged files

**Returns:** Same format as `merge_files()` plus:
```python
{
    "input_folder_original": str,  # Original input path provided
    "input_folder_absolute": str   # Resolved absolute path
}
```

#### `merge_translated_files(story_name, base_dir="story", output_dir=None)`

Convenience function for merging translated files following the project's story structure.

**Parameters:**
- `story_name` (str): Name of the story (folder name)
- `base_dir` (str): Base directory containing translate folder (default: "story")
- `output_dir` (str, optional): Directory for output file (default: story/merged/)

## File Detection Logic

The merger automatically detects numbered text files using this pattern:

1. **File Pattern**: Looks for files matching `{number}.txt` (e.g., 1.txt, 2.txt, 10.txt)
2. **Sorting**: Files are sorted numerically (not alphabetically), so 10.txt comes after 9.txt
3. **Content Handling**: Empty files are skipped, only non-empty content is merged
4. **Error Tolerance**: If individual files can't be read, they're skipped with a warning

## Output Examples

### Default Separator (Double Newline)
```
Content from 1.txt here

Content from 2.txt here

Content from 3.txt here
```

### Custom Separator
```
Content from 1.txt here

--- CHAPTER BREAK ---

Content from 2.txt here

--- CHAPTER BREAK ---

Content from 3.txt here
```

## Integration with Translation Workflow

The merger integrates perfectly with the translation pipeline:

```python
# 1. Split a large file
from utility.generic_file_splitter import split_any_file
split_result = split_any_file("large_story.txt")

# 2. Translate each chunk (your translation code here)
# ... translation processing ...

# 3. Merge translated chunks back
from utility.generic_file_merger import merge_any_folder
merge_result = merge_any_folder(split_result["output_folder"])
```

## Error Handling

The merger provides comprehensive error handling:

- **Missing Folder**: Clear error if input folder doesn't exist
- **Empty Folder**: Detects when no numbered files are found
- **File Read Errors**: Individual file read errors don't stop the entire process
- **Path Issues**: Handles both relative and absolute path resolution

## Testing

Run the test suite to verify functionality:

```bash
python tests/test_file_merger.py
```

The test suite covers:
- Numbered file detection
- Basic merge functionality
- Custom separators
- Error handling
- Content verification

## Demo Script

Run the demo to see all features in action:

```bash
python utility/demo_file_merger.py
```

The demo shows:
- Basic merging
- Custom output and separators
- Generic merger usage
- Story mode for translated files
- Error handling examples

## Best Practices

1. **File Organization**: Keep numbered files in dedicated folders for easy merging
2. **Custom Separators**: Use meaningful separators for different content types:
   - `"\n\n"`: For continuous prose
   - `"\n---\n"`: For clear section breaks
   - `"\n\n=== CHAPTER ===\n\n"`: For chapter divisions
3. **Output Naming**: Use descriptive output file names to avoid conflicts
4. **Error Checking**: Always check the `success` field in the result dictionary
5. **Path Handling**: Use absolute paths when working across different directories

## Troubleshooting

### Common Issues

**"No numbered text files found"**
- Ensure files are named correctly (1.txt, 2.txt, etc.)
- Check that files have .txt extension
- Verify the folder path is correct

**"Input folder not found"**
- Check the folder path spelling
- Use absolute paths if relative paths aren't working
- Ensure the folder exists

**Empty merged file**
- Check that source files contain content
- Verify files are readable and not corrupted
- Look for warnings about individual file read errors

### File Naming Requirements

Files must follow this pattern:
- ✅ Correct: `1.txt`, `2.txt`, `10.txt`, `100.txt`
- ❌ Wrong: `file1.txt`, `01.txt`, `1.doc`, `1`

## Related Documentation

- [File Splitter Documentation](FILE_SPLITTER.md) - For splitting files before processing
- [Generic File Splitter](GENERIC_FILE_SPLITTER.md) - For splitting any file type
- [Translation Workflow](FILE_TRANSLATOR.md) - For translating split files