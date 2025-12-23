import os
from typing import List, Optional, Set
from .parser import parse
from .core import InterpreterState
from .macros import MacroHandler
from .aliases import AliasHandler
from .executor import CommandExecutor
from .system_ops import ProcessOpsHandler


def initialize_state(
    state: InterpreterState,
    inputs: Optional[List[str]] = None,
    loaded_files: Optional[Set[str]] = None,
) -> None:
    """Initialize an existing InterpreterState for execution.

    The CLI REPL keeps a persistent state object and needs the same baseline
    initialization that `run()` applies to a fresh state.
    """

    ProcessOpsHandler.prime_cached_streams(state)
    state.input_queue = list(inputs or [])
    state.loaded_files = set(loaded_files or set())


def run(code: str, inputs: Optional[List[str]] = None, loaded_files: Optional[Set[str]] = None, base_dir: Optional[str] = None) -> str:
    # Entry point: parse, expand aliases, execute, return output
    if base_dir is None:
        base_dir = os.getcwd()
    else:
        base_dir = os.path.abspath(base_dir)

    state = InterpreterState()
    initialize_state(state, inputs=inputs, loaded_files=loaded_files)

    tokens: List[str] = parse(code)
    
    tokens = MacroHandler.process_macros(tokens, state)
    tokens = AliasHandler.process_aliases(tokens, state)
    
    executor = CommandExecutor(state, base_dir)
    executor.execute_block(tokens)
    
    return state.get_output()