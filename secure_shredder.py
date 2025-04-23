import os
import random
import argparse
from typing import List

class SecureFileShredder:
    """
    A tool that securely deletes files by overwriting them multiple times before deletion,
    making recovery extremely difficult.
    """
    
    def __init__(self, passes: int = 3, verbose: bool = False):
        """
        Initialize the shredder with the number of overwrite passes.
        
        Args:
            passes (int): Number of overwrite passes (default: 3)
            verbose (bool): Show detailed progress (default: False)
        """
        self.passes = passes
        self.verbose = verbose
        self.overwrite_patterns = [
            b'\x55\x55\x55\x55',  # Pattern 1: 0101...
            b'\xAA\xAA\xAA\xAA',  # Pattern 2: 1010...
            b'\xFF\xFF\xFF\xFF',  # Pattern 3: All 1s
            b'\x00\x00\x00\x00',  # Pattern 4: All 0s
            b'\x92\x49\x24\x92',  # Pattern 5: Random-looking
            b'\x49\x24\x92\x49',  # Pattern 6: Random-looking
            b'\x24\x92\x49\x24',  # Pattern 7: Random-looking
        ]
        
    def log(self, message: str):
        """Print log message if verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    def get_random_pattern(self, size: int) -> bytes:
        """Generate random bytes for overwriting."""
        return bytes([random.randint(0, 255) for _ in range(size)])
    
    def shred_file(self, file_path: str) -> bool:
        """
        Securely shred a file by overwriting it multiple times before deletion.
        
        Args:
            file_path (str): Path to the file to be shredded
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not os.path.exists(file_path):
            self.log(f"Error: File not found - {file_path}")
            return False
        
        try:
            file_size = os.path.getsize(file_path)
            
            with open(file_path, 'rb+') as file:
                # Overwrite the file multiple times with different patterns
                for pass_num in range(1, self.passes + 1):
                    # Use predefined patterns for first few passes, then random
                    if pass_num - 1 < len(self.overwrite_patterns):
                        pattern = self.overwrite_patterns[pass_num - 1]
                        # Repeat the pattern to fill the file
                        data = pattern * (file_size // len(pattern) + 1)
                        data = data[:file_size]
                    else:
                        data = self.get_random_pattern(file_size)
                    
                    file.seek(0)
                    file.write(data)
                    file.flush()
                    os.fsync(file.fileno())
                    
                    self.log(f"Pass {pass_num}/{self.passes} completed for {file_path}")
            
            # Rename the file to obscure the original name
            dir_name, file_name = os.path.split(file_path)
            temp_name = os.path.join(dir_name, f"temp_shred_{random.randint(0, 9999999)}")
            os.rename(file_path, temp_name)
            
            # Finally, delete the file
            os.remove(temp_name)
            
            self.log(f"Successfully shredded: {file_path}")
            return True
            
        except Exception as e:
            self.log(f"Error shredding {file_path}: {str(e)}")
            return False
    
    def shred_directory(self, dir_path: str, recursive: bool = False) -> bool:
        """
        Securely shred all files in a directory.
        
        Args:
            dir_path (str): Path to the directory
            recursive (bool): Whether to shred subdirectories recursively
            
        Returns:
            bool: True if all files were shredded successfully, False otherwise
        """
        if not os.path.isdir(dir_path):
            self.log(f"Error: Directory not found - {dir_path}")
            return False
            
        all_success = True
        
        try:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if not self.shred_file(file_path):
                        all_success = False
                
                if not recursive:
                    break
                    
            return all_success
            
        except Exception as e:
            self.log(f"Error shredding directory {dir_path}: {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description="Secure File Shredder - Permanently delete files to prevent recovery",
        epilog="Warning: This operation is irreversible. Use with caution."
    )
    parser.add_argument('paths', nargs='+', help='Files or directories to shred')
    parser.add_argument('-p', '--passes', type=int, default=3,
                       help='Number of overwrite passes (default: 3)')
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='Recursively shred directories')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show detailed progress')
    
    args = parser.parse_args()
    
    shredder = SecureFileShredder(passes=args.passes, verbose=args.verbose)
    
    all_success = True
    
    for path in args.paths:
        if os.path.isfile(path):
            if not shredder.shred_file(path):
                all_success = False
        elif os.path.isdir(path):
            if not shredder.shred_directory(path, args.recursive):
                all_success = False
        else:
            print(f"Error: Path not found - {path}")
            all_success = False
    
    if all_success:
        print("File shredding completed successfully.")
    else:
        print("File shredding completed with some errors.")
        exit(1)

if __name__ == "__main__":
    main()
