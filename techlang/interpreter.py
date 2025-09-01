# techlang/interpreter.py

import os
from typing import List, Optional, Set
from .parser import parse
from .core import InterpreterState
from .aliases import AliasHandler
from .executor import CommandExecutor


def run(code: str, inputs: Optional[List[str]] = None, loaded_files: Optional[Set[str]] = None, base_dir: Optional[str] = None) -> str:
    """
    Execute TechLang code and return the output as a string.
    
    Args:
        code: The TechLang source code to execute
        inputs: Optional list of input values for input commands
        loaded_files: Optional set of already loaded files to prevent circular imports
        base_dir: Optional base directory for resolving relative imports (defaults to current directory)
        
    Returns:
        A string containing the output from executing the code
        
    Raises:
        FileNotFoundError: If an imported file cannot be found
        ValueError: If there are syntax or runtime errors in the code
    """
    # Set base directory for imports
    if base_dir is None:
        base_dir = os.getcwd()
    else:
        base_dir = os.path.abspath(base_dir)

    # Initialize interpreter state
    state = InterpreterState()
    state.input_queue = inputs or []
    state.loaded_files = loaded_files or set()

    # Parse the code
    tokens: List[str] = parse(code)
    
    # Process aliases
    tokens = AliasHandler.process_aliases(tokens, state)
    
    # Create executor and run the code
    executor = CommandExecutor(state, base_dir)
    executor.execute_block(tokens)
    
    return state.get_output()