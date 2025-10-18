import time
from typing import List, Optional, Set, Union
from .core import InterpreterState


class BasicCommandHandler:
    """
    Handles the basic commands in TechLang.
    These are the simple commands that work with numbers and basic operations.
    Think of this as the calculator part of TechLang.
    """
    
    # All the commands that TechLang knows about
    # This helps us tell the difference between commands and variable names
    KNOWN_COMMANDS: Set[str] = {
        "boot", "ping", "crash", "reboot", "print", "upload",
    "download", "debug", "hack", "lag", "sleep", "yield", "fork", "set", "add",
    "mul", "sub", "div", "loop", "while", "switch", "match", "try", "catch", "default", "case", "end", "if", "def", "call", "input", "alias", "import", "package", "struct", "macro", "inline", "do",
        "db_create", "db_insert", "db_select", "db_update", "db_delete", "db_execute", "db_close",
        # Advanced DB
        "db_begin", "db_commit", "db_rollback", "db_tables", "db_schema", "db_indexes", "db_connect", "db_disconnect",
    # Array commands - for working with lists
    "array_create", "array_set", "array_get", "array_push", "array_pop",
    "array_map", "array_filter",
        # String commands - for working with text
    "str_create", "str_concat", "str_length", "str_substring", "string_interpolate", "string_match",
        # Dictionary commands - for working with key-value pairs
        "dict_create", "dict_set", "dict_get", "dict_keys",
        # File I/O commands
        "file_read", "file_write", "file_append", "file_exists", "file_delete", "file_list",
        # Network commands
        "http_get", "http_post", "http_status", "server_start", "server_route", "server_stop",
        # Graphics commands
        "graphics_init", "graphics_draw_line", "graphics_draw_circle", "graphics_draw_text", "graphics_show"
        ,
        # Memory commands
        "mem_alloc", "mem_free", "mem_read", "mem_write", "mem_dump",
        # Help
        "help",
        # Threading & Async
    "thread_create", "thread_join", "thread_sleep", "thread_status", "thread_result", "thread_list", "thread_wait_all", "async_start", "async_wait",
    "mutex_create", "mutex_lock", "mutex_unlock", "queue_push", "queue_pop",
        # System & Processes
        "sys_exec", "sys_env", "sys_time", "sys_date", "sys_sleep", "sys_cwd", "sys_exit",
        "proc_spawn", "proc_kill", "proc_wait", "proc_status"
    }
    
    @staticmethod
    def handle_boot(state: InterpreterState) -> None:
        """
        Reset the current value to 0.
        Like pressing the clear button on a calculator.
        """
        state.value = 0
    
    @staticmethod
    def handle_ping(state: InterpreterState) -> None:
        """
        Add 1 to the current value.
        Like pressing the +1 button on a calculator.
        """
        state.value += 1
    
    @staticmethod
    def handle_crash(state: InterpreterState) -> None:
        """
        Subtract 1 from the current value.
        Like pressing the -1 button on a calculator.
        """
        state.value -= 1
    
    @staticmethod
    def handle_reboot(state: InterpreterState) -> None:
        """
        Reset the current value to 0 (same as boot).
        Like restarting your computer.
        """
        state.value = 0
    
    @staticmethod
    def handle_print(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Print something to the screen.
        Can print numbers, variables, strings, or quoted text.
        Like the print statement in other programming languages.
        """
        # Look at the next word to see what we should print
        lookahead: Optional[str] = tokens[index + 1] if index + 1 < len(tokens) else None
        
        if lookahead:
            if lookahead.startswith('"') and lookahead.endswith('"'):
                # It's a quoted string, print it directly
                message = lookahead[1:-1]
                state.add_output(message)
                return 1  # Tell the interpreter we used 1 token
            if lookahead in state.structs:
                from .struct_ops import StructHandler  # local import to avoid circular dependency

                state.add_output(StructHandler.format_instance(state.structs[lookahead]))
                return 1
            elif lookahead.isalpha() and lookahead not in BasicCommandHandler.KNOWN_COMMANDS:
                # It's a variable name, print its value
                if lookahead in state.strings:
                    # It's a string variable
                    state.add_output(state.strings[lookahead])
                elif state.has_variable(lookahead):
                    # It's a regular variable
                    state.add_output(str(state.get_variable(lookahead)))
                else:
                    state.add_error(f"Variable '{lookahead}' is not defined. Use 'set {lookahead} <value>' or 'str_create {lookahead} <value>' to create it.")
                return 1  # Tell the interpreter we used 1 token
        
        # If nothing specific to print, print the current value
        state.add_output(str(state.value))
        return 0
    
    @staticmethod
    def handle_hack(state: InterpreterState) -> None:
        """
        Double the current value.
        Like multiplying by 2.
        """
        state.value *= 2
    
    @staticmethod
    def _sleep_seconds(seconds: float) -> None:
        time.sleep(seconds)

    @staticmethod
    def _resolve_numeric_value(state: InterpreterState, token: str, description: str) -> Optional[float]:
        try:
            return float(token)
        except ValueError:
            if state.has_variable(token):
                value: Union[int, float, str] = state.get_variable(token)
                if isinstance(value, (int, float)):
                    return float(value)
                state.add_error(f"{description} must be numeric; variable '{token}' is not a number")
                return None
            state.add_error(f"{description} must be a number or numeric variable")
            return None

    @staticmethod
    def handle_lag(state: InterpreterState) -> None:
        """
        Pause execution for 1 second.
        Like waiting for something to load.
        Useful for demonstrations or slowing down programs.
        """
        BasicCommandHandler._sleep_seconds(1.0)

    @staticmethod
    def handle_sleep(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("sleep requires milliseconds")
            return 0
        duration_token = tokens[index + 1]
        duration = BasicCommandHandler._resolve_numeric_value(state, duration_token, "sleep duration")
        if duration is None:
            return 0
        if duration < 0:
            state.add_error("sleep duration must be non-negative")
            return 0
        BasicCommandHandler._sleep_seconds(duration / 1000.0)
        return 1

    @staticmethod
    def handle_yield(state: InterpreterState) -> None:
        BasicCommandHandler._sleep_seconds(0.0)
