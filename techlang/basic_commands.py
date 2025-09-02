import time
from typing import List, Optional, Set
from .core import InterpreterState


class BasicCommandHandler:
    # Core single-word commands for quick value tweaks and prints
    
    KNOWN_COMMANDS: Set[str] = {
        "boot", "ping", "crash", "reboot", "print", "upload",
        "download", "debug", "hack", "lag", "fork", "set", "add",
        "mul", "sub", "div", "loop", "end", "if", "def", "call", "input", "alias", "import",
        "db_create", "db_insert", "db_select", "db_update", "db_delete", "db_execute", "db_close"
    }
    
    @staticmethod
    def handle_boot(state: InterpreterState) -> None:
        state.value = 0
    
    @staticmethod
    def handle_ping(state: InterpreterState) -> None:
        state.value += 1
    
    @staticmethod
    def handle_crash(state: InterpreterState) -> None:
        state.value -= 1
    
    @staticmethod
    def handle_reboot(state: InterpreterState) -> None:
        state.value = 0
    
    @staticmethod
    def handle_print(state: InterpreterState, tokens: List[str], index: int) -> int:
        # Print numbers, variables, or quoted text following the command
        lookahead: Optional[str] = tokens[index + 1] if index + 1 < len(tokens) else None
        
        if lookahead:
            if lookahead.startswith('"') and lookahead.endswith('"'):
                message = lookahead[1:-1]
                state.add_output(message)
                return 1  # Consume the quoted string
            elif lookahead.isalpha() and lookahead not in BasicCommandHandler.KNOWN_COMMANDS:
                if state.has_variable(lookahead):
                    state.add_output(str(state.get_variable(lookahead)))
                else:
                    state.add_error(f"Variable '{lookahead}' is not defined. Use 'set {lookahead} <value>' to create it.")
                return 1  # Consume variable name
        
        # Default behavior prints the current running value
        state.add_output(str(state.value))
        return 0
    
    @staticmethod
    def handle_hack(state: InterpreterState) -> None:
        state.value *= 2
    
    @staticmethod
    def handle_lag(state: InterpreterState) -> None:
        # Small sleep to simulate a pause in execution
        time.sleep(1)
