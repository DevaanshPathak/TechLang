# techlang/imports.py

import os
from typing import List
from .core import InterpreterState
from .parser import parse


class ImportHandler:
    """Handles import operations in TechLang."""
    
    @staticmethod
    def handle_import(state: InterpreterState, tokens: List[str], index: int, base_dir: str) -> int:
        """
        Handle the 'import' command to include external files.
        
        Args:
            state: The interpreter state
            tokens: List of tokens
            index: Current token index
            base_dir: Base directory for resolving imports
            
        Returns:
            Number of tokens consumed
        """
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'import' command. Use: import <filename>")
            return 0
        
        filename_token = tokens[index + 1]
        imported_tokens = ImportHandler._import_file(filename_token, state, base_dir)
        
        # If import was successful, insert the imported tokens into the current block
        if imported_tokens and not any(token.startswith("[IMPORT ERROR") for token in imported_tokens):
            # Insert imported tokens after the import statement
            tokens[index+2:index+2] = imported_tokens
            return 1  # Consume filename token
        else:
            # Add error messages to output
            for token in imported_tokens:
                state.add_output(token)
            return 1  # Consume filename token
    
    @staticmethod
    def _import_file(filename_token: str, state: InterpreterState, base_dir: str) -> List[str]:
        """
        Import a file and return its tokens.
        
        Args:
            filename_token: The filename to import
            state: The interpreter state
            base_dir: Base directory for resolving imports
            
        Returns:
            List of tokens from the imported file, or error message if file not found
        """
        # Add .tl extension if not present
        if not filename_token.endswith(".tl"):
            filename_token += ".tl"
        
        # Check if already loaded to prevent circular imports
        if filename_token in state.loaded_files:
            return []
        
        # Resolve the full path relative to base directory
        try:
            full_path = os.path.abspath(os.path.join(base_dir, filename_token))
            
            # Security check: ensure the resolved path is within the base directory
            if not full_path.startswith(base_dir):
                return [f"[IMPORT ERROR: Security violation - file '{filename_token}' is outside the allowed directory.]"]
            
            # Check if file exists before adding to loaded_files
            if not os.path.isfile(full_path):
                return [f"[IMPORT ERROR: File '{filename_token}' not found. Searched in: {base_dir}]"]
            
            state.loaded_files.add(filename_token)
            
            # Read and parse the file
            with open(full_path, "r", encoding="utf-8") as f:
                imported_code: str = f.read()
            return parse(imported_code)
            
        except (OSError, IOError) as e:
            return [f"[IMPORT ERROR: Cannot read file '{filename_token}': {str(e)}]"]
        except Exception as e:
            return [f"[IMPORT ERROR: Unexpected error importing '{filename_token}': {str(e)}]"]
