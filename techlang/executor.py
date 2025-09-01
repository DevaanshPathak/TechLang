# techlang/executor.py

from typing import List, Callable
from .core import InterpreterState
from .basic_commands import BasicCommandHandler
from .variables import VariableHandler
from .stack import StackHandler
from .control_flow import ControlFlowHandler
from .imports import ImportHandler
from .database import DatabaseHandler


class CommandExecutor:
    """Main executor that coordinates all command handlers."""
    
    def __init__(self, state: InterpreterState, base_dir: str):
        """
        Initialize the command executor.
        
        Args:
            state: The interpreter state
            base_dir: Base directory for imports
        """
        self.state = state
        self.base_dir = base_dir
    
    def execute_block(self, tokens: List[str]) -> None:
        """
        Execute a block of tokens.
        
        Args:
            tokens: List of tokens to execute
        """
        i = 0
        while i < len(tokens):
            token = tokens[i]
            consumed = 0
            
            # Basic commands
            if token == "boot":
                BasicCommandHandler.handle_boot(self.state)
            elif token == "ping":
                BasicCommandHandler.handle_ping(self.state)
            elif token == "crash":
                BasicCommandHandler.handle_crash(self.state)
            elif token == "reboot":
                BasicCommandHandler.handle_reboot(self.state)
            elif token == "print":
                consumed = BasicCommandHandler.handle_print(self.state, tokens, i)
            elif token == "hack":
                BasicCommandHandler.handle_hack(self.state)
            elif token == "lag":
                BasicCommandHandler.handle_lag(self.state)
            
            # Variable operations
            elif token == "set":
                consumed = VariableHandler.handle_set(self.state, tokens, i)
            elif token in {"add", "mul", "sub", "div"}:
                consumed = VariableHandler.handle_math_operation(self.state, tokens, i, token)
            elif token == "input":
                consumed = VariableHandler.handle_input(self.state, tokens, i)
            
            # Stack operations
            elif token == "upload":
                StackHandler.handle_upload(self.state)
            elif token == "download":
                StackHandler.handle_download(self.state)
            elif token == "fork":
                StackHandler.handle_fork(self.state)
            elif token == "debug":
                StackHandler.handle_debug(self.state)
            
            # Control flow
            elif token == "loop":
                consumed = ControlFlowHandler.handle_loop(self.state, tokens, i, self.execute_block)
            elif token == "if":
                consumed = ControlFlowHandler.handle_if(self.state, tokens, i, self.execute_block)
            elif token == "def":
                consumed = ControlFlowHandler.handle_def(self.state, tokens, i)
            elif token == "call":
                consumed = ControlFlowHandler.handle_call(self.state, tokens, i, self.execute_block)
            
            # Import
            elif token == "import":
                consumed = ImportHandler.handle_import(self.state, tokens, i, self.base_dir)
            
            # Database operations
            elif token == "db_create":
                consumed = DatabaseHandler.handle_db_create(self.state, tokens, i)
            elif token == "db_insert":
                consumed = DatabaseHandler.handle_db_insert(self.state, tokens, i)
            elif token == "db_select":
                consumed = DatabaseHandler.handle_db_select(self.state, tokens, i)
            elif token == "db_update":
                consumed = DatabaseHandler.handle_db_update(self.state, tokens, i)
            elif token == "db_delete":
                consumed = DatabaseHandler.handle_db_delete(self.state, tokens, i)
            elif token == "db_execute":
                consumed = DatabaseHandler.handle_db_execute(self.state, tokens, i)
            elif token == "db_close":
                DatabaseHandler.handle_db_close(self.state)
            
            # End of block
            elif token == "end":
                pass  # Just consume the token
            
            # Unknown command
            else:
                self.state.add_error(f"Unknown command '{token}'. Check your syntax and make sure all commands are spelled correctly.")
            
            i += 1 + consumed
