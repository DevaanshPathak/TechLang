from typing import List, Callable
from .core import InterpreterState
from .basic_commands import BasicCommandHandler
from .variables import VariableHandler
from .stack import StackHandler
from .control_flow import ControlFlowHandler
from .imports import ImportHandler
from .database import DatabaseHandler
from .data_types import DataTypesHandler
from .file_ops import FileOpsHandler


class CommandExecutor:
    """
    The main command dispatcher for TechLang.
    This class reads through the program line by line and figures out what to do.
    Think of it as the conductor of an orchestra - it tells each part what to play.
    """
    
    def __init__(self, state: InterpreterState, base_dir: str):
        """
        Set up the command executor.
        state: The interpreter's memory and state
        base_dir: The directory to look for imported files
        """
        self.state = state
        self.base_dir = base_dir
    
    def execute_block(self, tokens: List[str]) -> None:
        """
        Execute a block of TechLang code.
        This is the main function that runs through each command and executes it.
        """
        i = 0
        while i < len(tokens):
            token = tokens[i]
            consumed = 0  # How many tokens this command used up
            
            # Basic math and display commands
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
            
            # Variable operations - storing and manipulating data
            elif token == "set":
                consumed = VariableHandler.handle_set(self.state, tokens, i)
            elif token in {"add", "mul", "sub", "div"}:
                consumed = VariableHandler.handle_math_operation(self.state, tokens, i, token)
            elif token == "input":
                consumed = VariableHandler.handle_input(self.state, tokens, i)
            
            # Stack operations - temporary storage for numbers
            elif token == "upload":
                StackHandler.handle_upload(self.state)
            elif token == "download":
                StackHandler.handle_download(self.state)
            elif token == "fork":
                StackHandler.handle_fork(self.state)
            elif token == "debug":
                StackHandler.handle_debug(self.state)
            
            # Control flow - loops, conditions, and functions
            elif token == "loop":
                consumed = ControlFlowHandler.handle_loop(self.state, tokens, i, self.execute_block)
            elif token == "while":
                consumed = ControlFlowHandler.handle_while(self.state, tokens, i, self.execute_block)
            elif token == "if":
                consumed = ControlFlowHandler.handle_if(self.state, tokens, i, self.execute_block)
            elif token == "switch":
                consumed = ControlFlowHandler.handle_switch(self.state, tokens, i, self.execute_block)
            elif token == "def":
                consumed = ControlFlowHandler.handle_def(self.state, tokens, i)
            elif token == "call":
                consumed = ControlFlowHandler.handle_call(self.state, tokens, i, self.execute_block)
            
            # File operations - loading other TechLang files
            elif token == "import":
                consumed = ImportHandler.handle_import(self.state, tokens, i, self.base_dir)
            
            # Database operations - working with SQLite databases
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
            
            # Array operations - working with lists of data
            elif token == "array_create":
                consumed = DataTypesHandler.handle_array_create(self.state, tokens, i)
            elif token == "array_set":
                consumed = DataTypesHandler.handle_array_set(self.state, tokens, i)
            elif token == "array_get":
                consumed = DataTypesHandler.handle_array_get(self.state, tokens, i)
            elif token == "array_push":
                consumed = DataTypesHandler.handle_array_push(self.state, tokens, i)
            elif token == "array_pop":
                consumed = DataTypesHandler.handle_array_pop(self.state, tokens, i)
            
            # String operations - working with text
            elif token == "str_create":
                consumed = DataTypesHandler.handle_str_create(self.state, tokens, i)
            elif token == "str_concat":
                consumed = DataTypesHandler.handle_str_concat(self.state, tokens, i)
            elif token == "str_length":
                consumed = DataTypesHandler.handle_str_length(self.state, tokens, i)
            elif token == "str_substring":
                consumed = DataTypesHandler.handle_str_substring(self.state, tokens, i)
            
            # Dictionary operations - working with key-value pairs
            elif token == "dict_create":
                consumed = DataTypesHandler.handle_dict_create(self.state, tokens, i)
            elif token == "dict_set":
                consumed = DataTypesHandler.handle_dict_set(self.state, tokens, i)
            elif token == "dict_get":
                consumed = DataTypesHandler.handle_dict_get(self.state, tokens, i)
            elif token == "dict_keys":
                consumed = DataTypesHandler.handle_dict_keys(self.state, tokens, i)
            
            # File I/O
            elif token == "file_read":
                consumed = FileOpsHandler.handle_file_read(self.state, tokens, i, self.base_dir)
            elif token == "file_write":
                consumed = FileOpsHandler.handle_file_write(self.state, tokens, i, self.base_dir)
            elif token == "file_append":
                consumed = FileOpsHandler.handle_file_append(self.state, tokens, i, self.base_dir)
            elif token == "file_exists":
                consumed = FileOpsHandler.handle_file_exists(self.state, tokens, i, self.base_dir)
            elif token == "file_delete":
                consumed = FileOpsHandler.handle_file_delete(self.state, tokens, i, self.base_dir)
            elif token == "file_list":
                consumed = FileOpsHandler.handle_file_list(self.state, tokens, i, self.base_dir)

            # Try/Catch
            elif token == "try":
                consumed = ControlFlowHandler.handle_try(self.state, tokens, i, self.execute_block)

            # End of block - marks the end of loops, functions, etc.
            elif token == "end":
                pass
            
            # Unknown command - something we don't recognize
            else:
                self.state.add_error(f"Unknown command '{token}'. Check your syntax and make sure all commands are spelled correctly.")
            
            # Move to the next command, skipping any tokens this command used
            i += 1 + consumed
