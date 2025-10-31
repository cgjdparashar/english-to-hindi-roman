# File Translator Module

A utility module for batch translating text files from English to Hinglish (Hindi in Roman script).

## Features

- Read text files from `utility/inputfile/` directory
- Translate content using the core `english_to_hinglish` translator
- Save translated files to `utility/outputfile/` directory
- Support for custom output filenames
- Comprehensive error handling and reporting
- Batch translation for multiple files

## Directory Structure

```
utility/
├── file_translator.py          # Main module
├── demo_file_translator.py     # Demo script
├── inputfile/                  # Place input files here
│   └── story.txt              # Sample input file
└── outputfile/                 # Translated files saved here
    ├── story_hinglish.txt
    └── [other translated files]
```

## Usage

### Basic Translation

```python
from utility.file_translator import translate_file

# Translate a file (output will be filename_hinglish.txt)
result = translate_file("story.txt")

if result['success']:
    print(f"Translation saved to: {result['output_path']}")
    print(f"Original: {result['original_text']}")
    print(f"Translated: {result['translated_text']}")
```

### Custom Output Filename

```python
from utility.file_translator import translate_file

# Specify custom output filename
result = translate_file(
    input_filename="story.txt",
    output_filename="my_custom_translation.txt"
)
```

### Batch Translation

```python
from utility.file_translator import translate_multiple_files

# Translate multiple files at once
files = ["story1.txt", "story2.txt", "story3.txt"]
results = translate_multiple_files(files)

# Check results
for result in results:
    if result['success']:
        print(f"✓ {result['input_file']} → {result['output_file']}")
    else:
        print(f"✗ {result['input_file']}: {result['error']}")
```

### Read and Save Utilities

```python
from utility.file_translator import read_file, save_file

# Read a file from inputfile directory
content = read_file("story.txt")

# Save content to outputfile directory
output_path = save_file("output.txt", content)
```

## Running Tests

```bash
# Run comprehensive test suite
python tests/test_file_translator.py
```

Test suite includes:
- ✓ Reading files from inputfile directory
- ✓ Translating single files
- ✓ Custom output filenames
- ✓ Directory structure verification
- ✓ Reading and comparing translated files

## Running Demo

```bash
# Run demo to see the module in action
python utility/demo_file_translator.py
```

The demo will:
1. Translate story.txt with default filename
2. Translate with custom filename
3. List all input and output files

## API Reference

### `translate_file(input_filename, output_filename=None, input_dir=None, output_dir=None)`

Translate a single text file from English to Hinglish.

**Parameters:**
- `input_filename` (str): Name of the input file
- `output_filename` (str, optional): Custom output filename
- `input_dir` (Path, optional): Custom input directory
- `output_dir` (Path, optional): Custom output directory

**Returns:**
Dictionary with keys: `input_file`, `output_file`, `input_path`, `output_path`, `original_text`, `translated_text`, `success`, `error`

### `translate_multiple_files(filenames, input_dir=None, output_dir=None)`

Translate multiple files in batch.

**Parameters:**
- `filenames` (list): List of input filenames
- `input_dir` (Path, optional): Custom input directory
- `output_dir` (Path, optional): Custom output directory

**Returns:**
List of result dictionaries for each file

### `read_file(filename, input_dir=None)`

Read content from a file in the input directory.

**Parameters:**
- `filename` (str): Name of the file to read
- `input_dir` (Path, optional): Custom input directory

**Returns:**
File content as string

### `save_file(filename, content, output_dir=None)`

Save content to a file in the output directory.

**Parameters:**
- `filename` (str): Name of the output file
- `content` (str): Content to write
- `output_dir` (Path, optional): Custom output directory

**Returns:**
Path object of the saved file

## Example Output

**Input (story.txt):**
```
Lila, a curious young girl from a quiet village, found an old key buried beneath a tree in her backyard...
```

**Output (story_hinglish.txt):**
```
eka shAMta gA.Nva kI eka jij~nAsu yuvA la.DakI, lIlA ko apane piChavA.De meM eka pe.Da ke nIche dabI huI eka purAnI chAbI milI...
```

## Notes

- The module uses the existing `english_to_hinglish` translator from `utility/translator.py`
- Translation uses ITRANS transliteration scheme (capital letters indicate aspirated sounds)
- All files are read/written with UTF-8 encoding
- Output directory is created automatically if it doesn't exist
- Files are processed sequentially (not in parallel)

## Error Handling

The module handles common errors gracefully:
- **FileNotFoundError**: When input file doesn't exist
- **IOError**: When file read/write operations fail
- **Translation errors**: Captured and reported in the result dictionary

Example error handling:
```python
result = translate_file("nonexistent.txt")
if not result['success']:
    print(f"Error: {result['error']}")
```
