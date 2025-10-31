# File Splitter Utility

A Python utility to split large text files (up to 300,000 characters) into smaller chunks of configurable size (default: 2000 characters per file).

## Features

- ✅ Splits large text files into manageable chunks
- ✅ Smart text splitting at sentence/word boundaries
- ✅ Creates organized output folders in `story/` directory
- ✅ Handles files up to 300,000 characters
- ✅ Configurable chunk size
- ✅ Command-line and programmatic usage

## Installation

No additional dependencies required - uses only Python standard library.

## Usage

### Command Line

```bash
# Basic usage - splits into 2000 char chunks
python utility/file_splitter.py <input_file_path>

# Specify custom output folder name
python utility/file_splitter.py <input_file_path> <output_folder_name>

# Specify custom chunk size
python utility/file_splitter.py <input_file_path> <output_folder_name> <max_chars>
```

#### Examples

```bash
# Split story.txt into default chunks
python utility/file_splitter.py utility/inputfile/story.txt

# Split with custom folder name
python utility/file_splitter.py utility/inputfile/story.txt my_story

# Split with custom chunk size (1500 chars)
python utility/file_splitter.py utility/inputfile/story.txt my_story 1500
```

### Programmatic Usage

```python
from utility.file_splitter import split_file

# Basic usage
result = split_file("path/to/your/file.txt")

# With custom parameters
result = split_file(
    input_file_path="path/to/your/file.txt",
    output_folder_name="my_custom_folder",
    max_chars_per_file=1500
)

# Check results
if result["success"]:
    print(f"Created {result['files_created']} files")
    print(f"Output folder: {result['output_folder']}")
else:
    print(f"Error: {result['error']}")
```

## Output Structure

The utility creates a folder structure like this:

```
story/
  └── <output_folder_name>/
      ├── 1.txt
      ├── 2.txt
      ├── 3.txt
      └── ...
```

- **Folder location**: Always created inside the `story/` directory
- **Folder name**: Uses input filename (without extension) by default, or custom name if provided
- **File naming**: Sequential numbers starting from `1.txt`

## Function Reference

### `split_file(input_file_path, output_folder_name, max_chars_per_file)`

Main function to split a text file.

**Parameters:**
- `input_file_path` (str): Path to the input text file
- `output_folder_name` (str, optional): Name for output folder (default: input filename)
- `max_chars_per_file` (int, optional): Maximum characters per output file (default: 2000)

**Returns:**
```python
{
    "success": bool,           # True if split was successful
    "output_folder": str,      # Path to created folder
    "files_created": int,      # Number of files created
    "total_chars": int,        # Total characters processed
    "chunks": list,            # List of text chunks
    "error": str               # Error message (only if success=False)
}
```

### `split_text_into_chunks(text, max_chars)`

Helper function to split text into chunks.

**Parameters:**
- `text` (str): Text to split
- `max_chars` (int): Maximum characters per chunk

**Returns:**
- List of text chunks (list of strings)

## Smart Text Splitting

The utility intelligently splits text at natural boundaries:

1. **Sentence boundaries**: Tries to break at `.`, `!`, or `?` within the last 200 characters
2. **Word boundaries**: Falls back to breaking at spaces if no sentence boundary found
3. **Hard break**: Only breaks mid-word if absolutely necessary

This ensures readable chunks that don't cut off in the middle of sentences or words.

## Error Handling

The utility handles various error cases:

- ❌ File not found
- ❌ Empty files
- ❌ Files larger than 300,000 characters
- ❌ Invalid file paths
- ❌ Permission errors

All errors are returned in the result dictionary with descriptive messages.

## Testing

Run the test suite:

```bash
# Set Python path and run tests
$env:PYTHONPATH="$PWD"; python tests/test_file_splitter.py
```

Run the demo:

```bash
python -m utility.demo_file_splitter
```

## Examples

### Example 1: Split a large story file

```python
from utility.file_splitter import split_file

result = split_file(
    input_file_path="utility/inputfile/story.txt",
    output_folder_name="my_story",
    max_chars_per_file=2000
)

# Output:
# story/
#   └── my_story/
#       ├── 1.txt (max 2000 chars)
#       ├── 2.txt (max 2000 chars)
#       └── 3.txt (remaining chars)
```

### Example 2: Handle large files

```python
# For a 50,000 character file with 1500 char chunks
result = split_file("large_book.txt", "book_chapters", 1500)

# Creates approximately 34 files (50000 / 1500)
if result["success"]:
    print(f"Split into {result['files_created']} files")
```

### Example 3: Error handling

```python
result = split_file("nonexistent.txt")

if not result["success"]:
    print(f"Failed: {result['error']}")
    # Output: "Failed: Input file not found: nonexistent.txt"
```

## Limitations

- Maximum file size: 300,000 characters (~300KB for ASCII text)
- Encoding: UTF-8 only
- Output location: Always in `story/` directory (relative to project root)

## Use Cases

1. **Preparing text for translation**: Break large documents into chunks for API processing
2. **E-book processing**: Split books into chapters or manageable sections
3. **Text analysis**: Process large texts in smaller batches
4. **Data preprocessing**: Prepare text data for machine learning pipelines
5. **API payload management**: Keep text sizes within API limits

## Related Utilities

- `file_translator.py`: Translates text files to Hinglish (can be combined with file splitter)
- `translator.py`: Core translation logic for individual text strings

## Support

For issues or questions, check:
- Test file: `tests/test_file_splitter.py`
- Demo file: `utility/demo_file_splitter.py`
- Main documentation: `README.md`
