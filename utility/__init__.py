"""
Utility module for English to Hinglish translation
"""

from .translator import english_to_hinglish
from .file_translator import (
    translate_file,
    translate_multiple_files,
    read_file,
    save_file,
    INPUT_DIR,
    OUTPUT_DIR
)

__all__ = [
    'english_to_hinglish',
    'translate_file',
    'translate_multiple_files',
    'read_file',
    'save_file',
    'INPUT_DIR',
    'OUTPUT_DIR'
]
