# Generic File Splitter Utility

A powerful, reusable Python script that can split any large text file into smaller chunks. Accepts complete absolute paths or relative paths and automatically handles output directory organization.

## 🚀 Features

- ✅ **Universal Path Support**: Handles both absolute and relative file paths
- ✅ **Auto-Detection**: Automatically determines output directory and folder names
- ✅ **Flexible Configuration**: Customizable chunk size, output directory, and folder names
- ✅ **Smart Path Resolution**: Converts relative paths to absolute paths automatically
- ✅ **Command-Line Interface**: Full CLI with help, options, and examples
- ✅ **Programmatic API**: Use as a Python module in other scripts
- ✅ **Error Handling**: Comprehensive error handling and validation
- ✅ **Cross-Platform**: Works on Windows, macOS, and Linux

## 📦 Installation

No additional dependencies required - uses only Python standard library.

## 🔧 Usage

### Command Line Usage

#### Basic Syntax
```bash
python utility/generic_file_splitter.py <file_path> [options]
```

#### Examples

```bash
# Basic usage with absolute path
python utility/generic_file_splitter.py "C:/Users/user/Documents/story.txt"

# Basic usage with relative path
python utility/generic_file_splitter.py "story/input/story_31_10.txt"

# Custom chunk size
python utility/generic_file_splitter.py "story/input/story.txt" --chunk-size 1500

# Custom output directory and folder name
python utility/generic_file_splitter.py "story/input/story.txt" --output-dir "story/output" --folder-name "my_story"

# Quiet mode (suppress verbose output)
python utility/generic_file_splitter.py "story/input/story.txt" --quiet

# Show help
python utility/generic_file_splitter.py --help
```

#### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--folder-name` | `-f` | Name for output folder | Auto-generated from filename |
| `--output-dir` | `-o` | Base directory for output | Auto-determined from input path |
| `--chunk-size` | `-c` | Max characters per file | 2000 |
| `--quiet` | `-q` | Suppress verbose output | False (verbose) |
| `--help` | `-h` | Show help message | - |
| `--version` | | Show version | - |

### Programmatic Usage

#### Method 1: Using `split_file_generic()`

```python
from utility.generic_file_splitter import split_file_generic

# Basic usage
result = split_file_generic("C:/path/to/your/file.txt")

# With custom options
result = split_file_generic(
    file_path="/home/user/documents/book.txt",
    output_folder_name="my_book_chapters",
    output_base_dir="output/books",
    max_chars_per_file=1500,
    verbose=True
)

# Check results
if result["success"]:
    print(f"Created {result['files_created']} files")
    print(f"Output folder: {result['output_folder']}")
else:
    print(f"Error: {result['error']}")
```

#### Method 2: Using `split_any_file()` (Convenience Function)

```python
from utility.generic_file_splitter import split_any_file

# Simpler syntax for quick usage
result = split_any_file(
    "story/input/story.txt",
    output_folder_name="quick_split",
    max_chars_per_file=2500
)
```

## 🧠 Smart Auto-Detection

### Auto-Generated Folder Names
If you don't specify a folder name, it's automatically generated from the input filename:
- `story.txt` → folder name: `story`
- `my_book.txt` → folder name: `my_book`
- `/path/to/document.txt` → folder name: `document`

### Auto-Determined Output Directories
The output directory is intelligently determined based on input file location:

| Input File Location | Auto Output Directory | Example |
|-------------------|---------------------|---------|
| `story/input/file.txt` | `story/output/` | Recognizes story structure |
| `/any/other/path/file.txt` | `/any/other/path/output/` | Creates output in same directory |
| `relative/path/file.txt` | `relative/path/output/` | Maintains relative structure |

## 📁 Output Structure

```
<output_base_dir>/
  └── <folder_name>/
      ├── 1.txt
      ├── 2.txt
      ├── 3.txt
      └── ...
```

### Examples

#### Story Structure (Auto-Detected)
```
story/
  ├── input/
  │   └── story_31_10.txt
  └── output/
      └── story_31_10/
          ├── 1.txt
          ├── 2.txt
          └── ...
```

#### Custom Structure
```
custom_output/
  └── my_project/
      ├── 1.txt
      ├── 2.txt
      └── ...
```

## 🔍 Path Resolution Examples

| Input Path Type | Example Input | Resolved Absolute Path |
|----------------|---------------|----------------------|
| **Absolute Windows** | `C:\Users\user\file.txt` | `C:\Users\user\file.txt` |
| **Absolute Unix** | `/home/user/file.txt` | `/home/user/file.txt` |
| **Relative** | `story/input/file.txt` | `C:\project\story\input\file.txt` |
| **Current Directory** | `file.txt` | `C:\project\file.txt` |

## 📊 Function Reference

### `split_file_generic(file_path, **options)`

Main function for splitting files.

**Parameters:**
- `file_path` (str): Absolute or relative path to input file
- `output_folder_name` (str, optional): Output folder name
- `output_base_dir` (str, optional): Base output directory
- `max_chars_per_file` (int, optional): Max characters per file (default: 2000)
- `verbose` (bool, optional): Enable verbose output (default: True)

**Returns:**
```python
{
    "success": bool,           # True if operation succeeded
    "output_folder": str,      # Path to created output folder
    "files_created": int,      # Number of files created
    "total_chars": int,        # Total characters processed
    "chunks": list,            # List of text chunks (if success)
    "error": str               # Error message (if success=False)
}
```

### `split_any_file(file_path, **kwargs)`

Convenience function with same functionality as `split_file_generic()`.

## ⚡ Performance & Limits

- **Maximum file size**: 300,000 characters (~300KB for ASCII text)
- **Chunk size range**: 1 - 10,000 characters (10,000+ shows warning)
- **Smart splitting**: Breaks at sentence boundaries when possible
- **Memory efficient**: Processes files in memory but optimized for large text files

## 🛠️ Advanced Examples

### Example 1: Batch Processing Multiple Files

```python
from utility.generic_file_splitter import split_any_file
from pathlib import Path

# Process all txt files in a directory
input_dir = Path("documents")
for txt_file in input_dir.glob("*.txt"):
    result = split_any_file(
        str(txt_file),
        output_base_dir="processed_documents",
        max_chars_per_file=1800,
        verbose=False
    )
    print(f"{txt_file.name}: {result['files_created']} files created")
```

### Example 2: Processing Files from Different Locations

```python
files_to_process = [
    "C:/Users/user/Documents/book1.txt",
    "/home/user/stories/story.txt",
    "relative/path/document.txt"
]

for file_path in files_to_process:
    result = split_any_file(
        file_path,
        max_chars_per_file=2000,
        verbose=False
    )
    if result["success"]:
        print(f"✓ {file_path}: {result['files_created']} files")
    else:
        print(f"✗ {file_path}: {result['error']}")
```

### Example 3: Integration with Translation Pipeline

```python
from utility.generic_file_splitter import split_any_file
from utility.translator import english_to_hinglish

# Step 1: Split large file
split_result = split_any_file(
    "large_story.txt",
    output_folder_name="story_chunks",
    max_chars_per_file=2000
)

# Step 2: Translate each chunk
if split_result["success"]:
    output_folder = Path(split_result["output_folder"])
    for i in range(1, split_result["files_created"] + 1):
        chunk_file = output_folder / f"{i}.txt"
        with open(chunk_file, 'r') as f:
            text = f.read()
        
        translated = english_to_hinglish(text)
        
        # Save translated version
        translated_file = output_folder / f"{i}_hinglish.txt"
        with open(translated_file, 'w') as f:
            f.write(translated)
```

## 🚨 Error Handling

The utility provides comprehensive error handling:

| Error Type | Description | Return Value |
|-----------|-------------|--------------|
| **File Not Found** | Input file doesn't exist | `{"success": False, "error": "File not found: ..."}` |
| **Empty File** | Input file has no content | `{"success": False, "error": "Input file is empty"}` |
| **File Too Large** | File exceeds 300,000 characters | `{"success": False, "error": "File too large: ..."}` |
| **Permission Error** | Cannot read input or write output | `{"success": False, "error": "Permission denied: ..."}` |
| **Invalid Path** | Path is malformed | `{"success": False, "error": "Invalid path: ..."}` |

## 🔧 Troubleshooting

### Common Issues

1. **Module Import Error**
   ```
   ModuleNotFoundError: No module named 'utility'
   ```
   **Solution**: Run from project root or use absolute imports

2. **Permission Denied**
   ```
   PermissionError: [Errno 13] Permission denied
   ```
   **Solution**: Check file permissions and ensure write access to output directory

3. **File Not Found with Relative Path**
   **Solution**: Ensure you're running from the correct directory or use absolute paths

### Debug Mode

For debugging, use verbose mode:
```bash
python utility/generic_file_splitter.py "file.txt" --verbose
```

## 🔗 Integration

### With Existing Project Components

This utility integrates seamlessly with other project components:

- **Translation Pipeline**: Split large files before translation
- **API Processing**: Prepare text chunks for API consumption
- **Batch Processing**: Process multiple files in parallel

### Use in Other Projects

The utility is self-contained and can be copied to other projects:

1. Copy `utility/generic_file_splitter.py`
2. Copy `utility/file_splitter.py` (dependency)
3. Adjust import paths if needed

## 📝 Examples Gallery

### Real-World Usage Examples

```bash
# Split a large ebook for processing
python utility/generic_file_splitter.py "C:/Books/war_and_peace.txt" --chunk-size 3000 --folder-name "war_and_peace_chapters"

# Process user-uploaded documents
python utility/generic_file_splitter.py "./uploads/user_document.txt" --output-dir "./processed" --quiet

# Prepare files for translation API
python utility/generic_file_splitter.py "story/input/novel.txt" --chunk-size 1500 --folder-name "novel_for_translation"
```

## 🤝 Contributing

To extend this utility:

1. Add new features to `split_file_generic()` function
2. Update command-line argument parser for new options
3. Add comprehensive error handling
4. Update documentation and examples

## 📄 License

Part of the English to Hinglish Translator project. See main project README for license information.

---

**💡 Pro Tip**: Use the `--quiet` flag when integrating with other scripts to suppress verbose output and only capture the result dictionary.