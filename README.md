# Secure File Shredder
![Security](https://img.shields.io/badge/security-data%20destruction-blue)
![Python](https://img.shields.io/badge/python-3.6%2B-green)

A tool that securely deletes files by overwriting them multiple times before deletion, making recovery extremely difficult.

## Features

- Multiple overwrite passes with different patterns (DoD 5220.22-M compliant)
- Supports both files and directories
- Recursive directory shredding option
- Verbose mode for progress tracking
- File renaming before deletion to obscure original names

## Why Use This?

When you delete a file normally, the data remains on disk until overwritten. This tool ensures sensitive data is completely unrecoverable by:

1. Overwriting files with multiple patterns (including random data)
2. Renaming files before deletion
3. Performing secure deletion according to industry standards

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/secure-file-shredder.git
   cd secure-file-shredder
   ```
## Usage
   ```bash
   usage: secure_shredder.py [-h] [-p PASSES] [-r] [-v] paths [paths ...]
   
   Secure File Shredder - Permanently delete files to prevent recovery
   
   positional arguments:
     paths                 Files or directories to shred
   
   optional arguments:
     -h, --help            show this help message and exit
     -p PASSES, --passes PASSES
                           Number of overwrite passes (default: 3)
     -r, --recursive       Recursively shred directories
     -v, --verbose         Show detailed progress
   ```

## Examples

1.   Shred a single file with default settings (3 passes):
   ```bash
      python secure_shredder.py sensitive.docx
   ```
2.   Shred multiple files with 7 passes and verbose output:
   ```bash
     python secure_shredder.py -p 7 -v file1.txt file2.csv
   ```
3.   Shred a directory recursively:
   ```bash
      python secure_shredder.py -r /path/to/directory
   ```

## Security Notes
   The default 3-pass overwrite is sufficient for most users
   For maximum security, use 7+ passes (especially for highly sensitive data)
   This tool cannot securely delete files on SSD drives with wear-leveling
   Always test on non-critical files first

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT

## Key Features

1. **Multiple Overwrite Patterns**: Uses both predefined patterns (DoD 5220.22-M compliant) and random data
2. **Flexible Usage**: Handles both files and directories, with recursive options
3. **Security Focused**: Renames files before deletion and ensures proper flushing to disk
4. **Configurable**: Users can specify number of passes and verbosity
5. **Detailed Documentation**: Clear README with usage examples and security notes

This implementation provides a robust solution for secure file deletion while being easy to use and understand. 
