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
    "else", "finally", "with",  # Extended try/catch and context managers
        "db_create", "db_insert", "db_select", "db_update", "db_delete", "db_execute", "db_close",
        # Advanced DB
        "db_begin", "db_commit", "db_rollback", "db_tables", "db_schema", "db_indexes", "db_connect", "db_disconnect",
    # Array commands - for working with lists
    "array_create", "array_set", "array_get", "array_push", "array_pop",
    "array_map", "array_filter", "array_sort", "array_reverse", "array_find", "array_unique", "array_join",
    "array_slice", "array_comprehend", "range", "enumerate", "array_zip", "array_apply",
    "any", "all", "array_min", "array_max", "array_sorted",
    # Lambda/anonymous functions
    "lambda", "lambda_call",
        # String commands - for working with text
    "str_create", "str_concat", "str_length", "str_substring", "string_interpolate", "string_match",
    "str_split", "str_replace", "str_trim", "str_upper", "str_lower", "str_contains", "str_reverse",
    "str_format", "str_startswith", "str_endswith", "str_count", "str_find", "str_rfind",
    "str_isdigit", "str_isalpha", "str_isalnum",
        # Dictionary commands - for working with key-value pairs
        "dict_create", "dict_set", "dict_get", "dict_keys",
        "dict_values", "dict_items", "dict_update", "dict_pop", "dict_get_default",
        "dict_has_key", "dict_clear", "dict_len",
        # Set commands - for working with unique collections
        "set_create", "set_add", "set_remove", "set_contains", "set_len", "set_clear",
        "set_union", "set_intersection", "set_difference", "set_symmetric_difference",
        "set_issubset", "set_issuperset", "set_to_array", "array_to_set",
        # Advanced comprehensions (Feature 7)
        "dict_comprehend", "set_comprehend", "generator_expr", "comprehend_if",
        # Slice assignment & advanced slicing (Feature 8)
        "array_slice_step", "array_set_slice", "str_slice", "str_slice_step",
        # Unpacking & destructuring (Feature 9)
        "unpack", "unpack_rest", "dict_unpack", "swap",
        # F-strings / format specifiers (Feature 10)
        "fstring", "format_num", "format_align", "str_pad_left", "str_pad_right",
        # Type checking commands - for runtime introspection
        "type_of", "is_number", "is_string", "is_array", "is_dict", "is_struct", "is_set", "is_generator",
        # Generator commands - for lazy iteration
        "generator_create", "generator_next", "generator_reset", "generator_to_array",
        "generator_from_range", "generator_take",
        # Regex commands - for pattern matching
        "regex_match", "regex_find", "regex_replace", "regex_split",
        # Crypto/encoding commands
        "base64_encode", "base64_decode", "md5", "sha256", "sha512", "uuid", "hex_encode", "hex_decode",
        # Assert command - for testing/validation
        "assert",
        # Bitwise operations
        "bit_and", "bit_or", "bit_xor", "bit_not", "bit_shift_left", "bit_shift_right",
        # JSON commands - for parsing and stringifying JSON data
        "json_parse", "json_stringify", "json_read", "json_write",
        # File I/O commands
            "file_read", "file_write", "file_append", "file_exists", "file_delete", "file_list",
            "path_join", "path_basename", "path_dirname", "path_extname",
        # Network commands
        "http_get", "http_post", "http_status", "server_start", "server_route", "server_stop",
        # Graphics commands
        "graphics_init", "graphics_draw_line", "graphics_draw_circle", "graphics_draw_text", "graphics_show"
        ,
        # Memory commands
        "mem_alloc", "mem_free", "mem_read", "mem_write", "mem_dump",
    # Math & time commands
    "math_sin", "math_cos", "math_tan", "math_asin", "math_acos", "math_atan",
    "math_sqrt", "math_pow", "math_mod", "math_random", "math_round", "math_floor", "math_ceil",
            "math_deg2rad", "math_rad2deg", "math_pi", "math_e", "math_seed", "now", "format_date",
        # Help
        "help",
        # Function control
        "return",
        # Module/Library API
        "export",
        # Debugger commands
        "breakpoint", "step", "continue", "inspect", "watch", "unwatch", "clear_breakpoints",
        # Threading & Async
    "thread_create", "thread_join", "thread_sleep", "thread_status", "thread_result", "thread_list", "thread_wait_all", "async_start", "async_wait",
    "mutex_create", "mutex_lock", "mutex_unlock", "queue_push", "queue_pop",
        # System & Processes
        "sys_exec", "sys_env", "sys_time", "sys_date", "sys_sleep", "sys_cwd", "sys_exit",
        "proc_spawn", "proc_kill", "proc_wait", "proc_status",
        # OOP - Classes and Objects
        "class", "new", "extends", "method", "static", "init", "field",
        "get_field", "set_field", "instanceof", "super",
        # First-class functions and closures
        "fn", "fn_ref", "fn_call", "partial", "compose",
        "map_fn", "filter_fn", "reduce_fn",
        # Exception handling
        "throw", "raise",
        # Decorators
        "decorator", "decorate",
        # Context managers
        "context", "with",
        # Async/Await
        "async", "await", "spawn", "gather", "task_status", "task_cancel",
        # Feature 11: Itertools/Functools
        "chain", "cycle", "repeat", "takewhile", "dropwhile", "groupby",
        "accumulate", "pairwise", "product", "permutations", "combinations",
        "reduce", "partial_array", "apply_partial",
        # Feature 12: Date/Time Full Support
        "datetime_now", "datetime_utc", "datetime_parse", "datetime_format",
        "datetime_add", "datetime_diff", "datetime_weekday", "datetime_timestamp",
        "datetime_from_timestamp",
        # Feature 13: Logging System
        "log_init", "log_debug", "log_info", "log_warning", "log_error", "log_critical",
        "log_level", "log_file", "log_clear", "log_count", "log_get",
        # Pythonic Features: Dataclasses & in/not_in operators
        "dataclass", "dataclass_new", "dataclass_get", "dataclass_set",
        "dataclass_eq", "dataclass_str", "dataclass_to_dict",
        "in", "not_in", "contains",
        # Pythonic Features: Property decorators
        "property", "get_property", "set_property"

        ,
        # GUI (tkinter/customtkinter)
        "gui_backend", "gui_window", "gui_label", "gui_button", "gui_entry",
        "gui_entry_get", "gui_entry_set", "gui_destroy", "gui_mainloop",
        # GUI CTk (CustomTkinter) settings
        "gui_ctk_appearance", "gui_ctk_theme", "gui_ctk_scaling",
        # GUI CTk (CustomTkinter) widgets
        "gui_ctk_switch", "gui_ctk_slider", "gui_ctk_progressbar", "gui_ctk_progress_set",
        "gui_ctk_optionmenu", "gui_ctk_combobox", "gui_ctk_tabview", "gui_ctk_tab",
        # GUI Phase 1 primitives
        "gui_set", "gui_get", "gui_pack", "gui_grid", "gui_bind",
        # GUI Phase 2 widgets + vars
        "gui_frame", "gui_checkbutton", "gui_radiobutton", "gui_text", "gui_listbox", "gui_canvas", "gui_scrollbar",
        "gui_canvas_create_line", "gui_canvas_move", "gui_canvas_delete", "gui_canvas_coords",
        "gui_text_insert", "gui_text_get", "gui_text_delete", "gui_text_tag_add", "gui_text_tag_config",
        "gui_var_new", "gui_var_set", "gui_var_get",
        # GUI Phase 3 menus + dialogs
        "gui_menubar", "gui_menu", "gui_menu_item", "gui_messagebox", "gui_filedialog_open", "gui_filedialog_save",
        # GUI Phase 4 ttk
        "gui_ttk_style_set", "gui_ttk_theme_use",
        "gui_ttk_button", "gui_ttk_label", "gui_ttk_entry", "gui_ttk_combobox", "gui_ttk_treeview",
        "gui_ttk_notebook", "gui_ttk_notebook_tab", "gui_ttk_progressbar", "gui_ttk_separator"
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
            elif lookahead not in BasicCommandHandler.KNOWN_COMMANDS and (lookahead.isalnum() or '_' in lookahead):
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
    
    @staticmethod
    def handle_return(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Return values from a function.
        Syntax: return [value1] [value2] ...
        Examples:
          return 42
          return x
          return x "success"
          return  # return nothing
        """
        # Clear previous return values
        state.return_values.clear()
        
        # Collect all values after 'return' until we hit a block keyword or run out
        i = index + 1
        while i < len(tokens):
            token = tokens[i]
            # Stop at block keywords
            if token in {"end", "case", "default", "catch", "else"}:
                break
            
            # Resolve the value (could be variable, string, or literal number)
            value = BasicCommandHandler._resolve_return_value(state, token)
            if value is not None:
                state.return_values.append(value)
            i += 1
        
        # Set flag to stop execution (early return from function)
        state.should_return = True
        
        # Return count of consumed tokens (everything after 'return')
        return i - index - 1
    
    @staticmethod
    def _resolve_return_value(state: InterpreterState, token: str) -> Optional[Union[int, str]]:
        """Resolve a token to its actual value for returning."""
        # Check if it's a quoted string
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]  # Remove quotes
        
        # Check if it's a string variable
        if token in state.strings:
            return state.strings[token]
        
        # Check if it's a numeric variable
        if token in state.variables:
            val = state.variables[token]
            # Convert to string if it's a string value in variables
            return val if isinstance(val, (int, str)) else str(val)
        
        # Try to parse as integer
        try:
            return int(token)
        except ValueError:
            pass
        
        # Try to parse as float and convert to int
        try:
            return int(float(token))
        except ValueError:
            pass
        
        # If we can't resolve it, return the token as-is (as string)
        return token

    @staticmethod
    def handle_export(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Mark a function as exported (public API).
        Syntax: export func_name
        
        Exported functions can be called from outside the module.
        Non-exported functions are private and only callable within the module.
        Note: export can be called before or after the function is defined.
        """
        if index + 1 >= len(tokens):
            state.add_error("export requires a function name")
            return 0
        
        func_name = tokens[index + 1]
        
        # Mark as exported (don't check if function exists yet - it may be defined later)
        state.exported_functions.add(func_name)
        return 1

    @staticmethod
    def handle_throw(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Throw/raise an exception.
        Syntax: throw <message> [type]
        OR: raise <message> [type]
        
        The exception can be caught by a try/catch block.
        If no catch block handles it, the error is added to output.
        """
        if index + 1 >= len(tokens):
            state.add_error("throw requires a message")
            return 0
        
        message_token = tokens[index + 1]
        
        # Resolve message
        if message_token.startswith('"') and message_token.endswith('"'):
            message = message_token[1:-1]
        elif message_token in state.strings:
            message = state.strings[message_token]
        else:
            message = message_token
        
        # Optional exception type
        exc_type = "Error"
        if index + 2 < len(tokens):
            type_token = tokens[index + 2]
            if type_token not in BasicCommandHandler.KNOWN_COMMANDS:
                exc_type = type_token
                state.current_exception = message
                state.exception_type = exc_type
                state.add_error(f"{exc_type}: {message}")
                return 2
        
        # Set exception state
        state.current_exception = message
        state.exception_type = exc_type
        state.add_error(f"{exc_type}: {message}")
        
        return 1
