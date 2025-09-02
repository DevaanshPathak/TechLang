import os
from typing import List, Optional, Set
from .parser import parse
from .core import InterpreterState
from .aliases import AliasHandler
from .executor import CommandExecutor


def run(code: str, inputs: Optional[List[str]] = None, loaded_files: Optional[Set[str]] = None, base_dir: Optional[str] = None) -> str:
    # Entry point: parse, expand aliases, execute, return output
    if base_dir is None:
        base_dir = os.getcwd()
    else:
        base_dir = os.path.abspath(base_dir)

    state = InterpreterState()
    state.input_queue = inputs or []
    state.loaded_files = loaded_files or set()

    tokens: List[str] = parse(code)
    
    tokens = AliasHandler.process_aliases(tokens, state)
    
    executor = CommandExecutor(state, base_dir)
    executor.execute_block(tokens)
    
    return state.get_output()