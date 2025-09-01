# techlang/basic_commands.py

import time
from typing import List, Optional, Set
from .core import InterpreterState


class BasicCommandHandler:
    """Handles basic commands in TechLang."""
    
    # Known commands for print lookahead
    KNOWN_COMMANDS: Set[str] = {
        "boot", "ping", "crash", "reboot", "print", "upload",
        "download", "debug", "hack", "lag", "fork", "set", "add",
        "mul", "sub", "div", "loop", "end", "if", "def", "call", "input", "alias", "import",
        "db_create", "db_insert", "db_select", "db_update", "db_delete", "db_execute", "db_close"
    }
    
    @staticmethod
    def handle_boot(state: InterpreterState) -> None:
        """Handle the 'boot' command to set value to 0."""
        state.value = 0
    
    @staticmethod
    def handle_ping(state: InterpreterState) -> None:
        """Handle the 'ping' command to increment value."""
        state.value += 1
    
    @staticmethod
    def handle_crash(state: InterpreterState) -> None:
        """Handle the 'crash' command to decrement value."""
        state.value -= 1
    
    @staticmethod
    def handle_reboot(state: InterpreterState) -> None:
        """Handle the 'reboot' command to set value to 0."""
        state.value = 0
    
    @staticmethod
    def handle_print(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Handle the 'print' command to output value or variable.
        
        Args:
            state: The interpreter state
            tokens: List of tokens
            index: Current token index
            
        Returns:
            Number of tokens consumed
        """
        # Check for variable name or quoted string after print
        lookahead: Optional[str] = tokens[index + 1] if index + 1 < len(tokens) else None
        
        if lookahead:
            # Handle quoted string
            if lookahead.startswith('"') and lookahead.endswith('"'):
                # Remove quotes and print the string
                message = lookahead[1:-1]
                state.add_output(message)
                return 1  # Consume the quoted string
            # Handle variable name
            elif lookahead.isalpha() and lookahead not in BasicCommandHandler.KNOWN_COMMANDS:
                if state.has_variable(lookahead):
                    state.add_output(str(state.get_variable(lookahead)))
                else:
                    state.add_error(f"Variable '{lookahead}' is not defined. Use 'set {lookahead} <value>' to create it.")
                return 1  # Consume variable name
        
        # Default: print current value
        state.add_output(str(state.value))
        return 0
    
    @staticmethod
    def handle_hack(state: InterpreterState) -> None:
        """Handle the 'hack' command to double the value."""
        state.value *= 2
    
    @staticmethod
    def handle_lag(state: InterpreterState) -> None:
        """Handle the 'lag' command to pause execution."""
        time.sleep(1)
