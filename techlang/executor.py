from typing import List, Callable
from .core import InterpreterState
from .basic_commands import BasicCommandHandler
from .variables import VariableHandler
from .stack import StackHandler
from .control_flow import ControlFlowHandler
from .imports import ImportHandler, ModuleHandler
from .database import DatabaseHandler
from .data_types import DataTypesHandler
from .struct_ops import StructHandler
from .file_ops import FileOpsHandler
from .net_ops import NetOpsHandler, NetServerHandler
from .graphics_ops import GraphicsOpsHandler
from .memory_ops import MemoryOpsHandler
from .help_ops import HelpOpsHandler
from .thread_ops import ThreadOpsHandler
from .system_ops import SystemOpsHandler, ProcessOpsHandler
from .math_ops import MathOpsHandler
from .debugger import DebuggerHandler
from .gui_ops import GuiOpsHandler
from .class_ops import ClassOpsHandler
from .function_ops import FunctionOpsHandler
from .decorator_ops import DecoratorOpsHandler
from .context_ops import ContextOpsHandler
from .async_ops import AsyncOpsHandler
from .pythonic_ops import PythonicOpsHandler


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
            # Check if we should pause for debugging
            if DebuggerHandler.check_breakpoint(self.state):
                # In a real interactive debugger, we'd wait for user input here
                # For now, just continue (users can implement interactive loop externally)
                pass
            
            token = tokens[i]
            consumed = 0  # How many tokens this command used up
            
            # Increment command counter for debugging
            self.state.command_count += 1
            
            # Debugger commands
            if token == "breakpoint":
                consumed = DebuggerHandler.handle_breakpoint(self.state, tokens, i)
            elif token == "step":
                consumed = DebuggerHandler.handle_step(self.state, tokens, i)
            elif token == "continue":
                consumed = DebuggerHandler.handle_continue(self.state, tokens, i)
            elif token == "inspect":
                consumed = DebuggerHandler.handle_inspect(self.state, tokens, i)
            elif token == "watch":
                consumed = DebuggerHandler.handle_watch(self.state, tokens, i)
            elif token == "unwatch":
                consumed = DebuggerHandler.handle_unwatch(self.state, tokens, i)
            elif token == "clear_breakpoints":
                consumed = DebuggerHandler.handle_clear_breakpoints(self.state, tokens, i)
            
            # Basic math and display commands
            elif token == "boot":
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
            elif token == "sleep":
                consumed = BasicCommandHandler.handle_sleep(self.state, tokens, i)
            elif token == "yield":
                BasicCommandHandler.handle_yield(self.state)

            # Advanced math, date, and time helpers
            elif token == "math_sin":
                consumed = MathOpsHandler.handle_math_sin(self.state, tokens, i)
            elif token == "math_cos":
                consumed = MathOpsHandler.handle_math_cos(self.state, tokens, i)
            elif token == "math_tan":
                consumed = MathOpsHandler.handle_math_tan(self.state, tokens, i)
            elif token == "math_asin":
                consumed = MathOpsHandler.handle_math_asin(self.state, tokens, i)
            elif token == "math_acos":
                consumed = MathOpsHandler.handle_math_acos(self.state, tokens, i)
            elif token == "math_atan":
                consumed = MathOpsHandler.handle_math_atan(self.state, tokens, i)
            elif token == "math_sqrt":
                consumed = MathOpsHandler.handle_math_sqrt(self.state, tokens, i)
            elif token == "math_pow":
                consumed = MathOpsHandler.handle_math_pow(self.state, tokens, i)
            elif token == "math_mod":
                consumed = MathOpsHandler.handle_math_mod(self.state, tokens, i)
            elif token == "math_random":
                consumed = MathOpsHandler.handle_math_random(self.state, tokens, i)
            elif token == "math_seed":
                consumed = MathOpsHandler.handle_math_seed(self.state, tokens, i)
            elif token == "math_round":
                consumed = MathOpsHandler.handle_math_round(self.state, tokens, i)
            elif token == "math_floor":
                consumed = MathOpsHandler.handle_math_floor(self.state, tokens, i)
            elif token == "math_ceil":
                consumed = MathOpsHandler.handle_math_ceil(self.state, tokens, i)
            elif token == "math_deg2rad":
                consumed = MathOpsHandler.handle_math_deg2rad(self.state, tokens, i)
            elif token == "math_rad2deg":
                consumed = MathOpsHandler.handle_math_rad2deg(self.state, tokens, i)
            elif token == "math_pi":
                MathOpsHandler.handle_math_pi(self.state)
            elif token == "math_e":
                MathOpsHandler.handle_math_e(self.state)
            elif token == "now":
                consumed = MathOpsHandler.handle_now(self.state, tokens, i)
            elif token == "format_date":
                consumed = MathOpsHandler.handle_format_date(self.state, tokens, i)
            
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
            elif token == "return":
                consumed = BasicCommandHandler.handle_return(self.state, tokens, i)
            elif token == "export":
                consumed = BasicCommandHandler.handle_export(self.state, tokens, i)
            
            # Control flow - loops, conditions, and functions
            elif token == "loop":
                consumed = ControlFlowHandler.handle_loop(self.state, tokens, i, self.execute_block)
            elif token == "while":
                consumed = ControlFlowHandler.handle_while(self.state, tokens, i, self.execute_block)
            elif token == "if":
                consumed = ControlFlowHandler.handle_if(self.state, tokens, i, self.execute_block)
            elif token == "switch":
                consumed = ControlFlowHandler.handle_switch(self.state, tokens, i, self.execute_block)
            elif token == "match":
                consumed = ControlFlowHandler.handle_match(self.state, tokens, i, self.execute_block)
            elif token == "def":
                consumed = ControlFlowHandler.handle_def(self.state, tokens, i)
            elif token == "call":
                consumed = ControlFlowHandler.handle_call(self.state, tokens, i, self.execute_block)
            
            # File operations - loading other TechLang files
            elif token == "import":
                consumed = ImportHandler.handle_import(self.state, tokens, i, self.base_dir)
            elif token == "package":
                consumed = ModuleHandler.handle_package(self.state, tokens, i, self.base_dir)
            
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
            elif token == "db_connect":
                consumed = DatabaseHandler.handle_db_connect(self.state, tokens, i)
            elif token == "db_disconnect":
                DatabaseHandler.handle_db_disconnect(self.state)
            elif token == "db_begin":
                DatabaseHandler.handle_db_begin(self.state)
            elif token == "db_commit":
                DatabaseHandler.handle_db_commit(self.state)
            elif token == "db_rollback":
                DatabaseHandler.handle_db_rollback(self.state)
            elif token == "db_tables":
                DatabaseHandler.handle_db_tables(self.state)
            elif token == "db_schema":
                consumed = DatabaseHandler.handle_db_schema(self.state, tokens, i)
            elif token == "db_indexes":
                consumed = DatabaseHandler.handle_db_indexes(self.state, tokens, i)
            
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
            elif token == "array_map":
                consumed = DataTypesHandler.handle_array_map(self.state, tokens, i)
            elif token == "array_filter":
                consumed = DataTypesHandler.handle_array_filter(self.state, tokens, i)
            elif token == "array_sort":
                consumed = DataTypesHandler.handle_array_sort(self.state, tokens, i)
            elif token == "array_reverse":
                consumed = DataTypesHandler.handle_array_reverse(self.state, tokens, i)
            elif token == "array_find":
                consumed = DataTypesHandler.handle_array_find(self.state, tokens, i)
            elif token == "array_unique":
                consumed = DataTypesHandler.handle_array_unique(self.state, tokens, i)
            elif token == "array_join":
                consumed = DataTypesHandler.handle_array_join(self.state, tokens, i)
            
            # String operations - working with text
            elif token == "str_create":
                consumed = DataTypesHandler.handle_str_create(self.state, tokens, i)
            elif token == "str_concat":
                consumed = DataTypesHandler.handle_str_concat(self.state, tokens, i)
            elif token == "str_length":
                consumed = DataTypesHandler.handle_str_length(self.state, tokens, i)
            elif token == "str_substring":
                consumed = DataTypesHandler.handle_str_substring(self.state, tokens, i)
            elif token == "str_split":
                consumed = DataTypesHandler.handle_str_split(self.state, tokens, i)
            elif token == "str_replace":
                consumed = DataTypesHandler.handle_str_replace(self.state, tokens, i)
            elif token == "str_trim":
                consumed = DataTypesHandler.handle_str_trim(self.state, tokens, i)
            elif token == "str_upper":
                consumed = DataTypesHandler.handle_str_upper(self.state, tokens, i)
            elif token == "str_lower":
                consumed = DataTypesHandler.handle_str_lower(self.state, tokens, i)
            elif token == "str_contains":
                consumed = DataTypesHandler.handle_str_contains(self.state, tokens, i)
            elif token == "str_reverse":
                consumed = DataTypesHandler.handle_str_reverse(self.state, tokens, i)
            elif token == "string_interpolate":
                consumed = VariableHandler.handle_string_interpolate(self.state, tokens, i)
            elif token == "string_match":
                consumed = VariableHandler.handle_string_match(self.state, tokens, i)
            
            # Dictionary operations - working with key-value pairs
            elif token == "dict_create":
                consumed = DataTypesHandler.handle_dict_create(self.state, tokens, i)
            elif token == "dict_set":
                consumed = DataTypesHandler.handle_dict_set(self.state, tokens, i)
            elif token == "dict_get":
                consumed = DataTypesHandler.handle_dict_get(self.state, tokens, i)
            elif token == "dict_keys":
                consumed = DataTypesHandler.handle_dict_keys(self.state, tokens, i)
            
            # Type checking operations - runtime introspection
            elif token == "type_of":
                consumed = DataTypesHandler.handle_type_of(self.state, tokens, i)
            elif token == "is_number":
                consumed = DataTypesHandler.handle_is_number(self.state, tokens, i)
            elif token == "is_string":
                consumed = DataTypesHandler.handle_is_string(self.state, tokens, i)
            elif token == "is_array":
                consumed = DataTypesHandler.handle_is_array(self.state, tokens, i)
            elif token == "is_dict":
                consumed = DataTypesHandler.handle_is_dict(self.state, tokens, i)
            elif token == "is_struct":
                consumed = DataTypesHandler.handle_is_struct(self.state, tokens, i)
            elif token == "is_set":
                consumed = DataTypesHandler.handle_is_set(self.state, tokens, i)
            elif token == "is_generator":
                consumed = DataTypesHandler.handle_is_generator(self.state, tokens, i)
            
            # Generator operations - lazy iteration
            elif token == "generator_create":
                consumed = DataTypesHandler.handle_generator_create(self.state, tokens, i)
            elif token == "generator_next":
                consumed = DataTypesHandler.handle_generator_next(self.state, tokens, i)
            elif token == "generator_reset":
                consumed = DataTypesHandler.handle_generator_reset(self.state, tokens, i)
            elif token == "generator_to_array":
                consumed = DataTypesHandler.handle_generator_to_array(self.state, tokens, i)
            elif token == "generator_from_range":
                consumed = DataTypesHandler.handle_generator_from_range(self.state, tokens, i)
            elif token == "generator_take":
                consumed = DataTypesHandler.handle_generator_take(self.state, tokens, i)
            
            # Regex operations - pattern matching
            elif token == "regex_match":
                consumed = DataTypesHandler.handle_regex_match(self.state, tokens, i)
            elif token == "regex_find":
                consumed = DataTypesHandler.handle_regex_find(self.state, tokens, i)
            elif token == "regex_replace":
                consumed = DataTypesHandler.handle_regex_replace(self.state, tokens, i)
            elif token == "regex_split":
                consumed = DataTypesHandler.handle_regex_split(self.state, tokens, i)
            
            # Crypto/encoding operations
            elif token == "base64_encode":
                consumed = DataTypesHandler.handle_base64_encode(self.state, tokens, i)
            elif token == "base64_decode":
                consumed = DataTypesHandler.handle_base64_decode(self.state, tokens, i)
            elif token == "md5":
                consumed = DataTypesHandler.handle_md5(self.state, tokens, i)
            elif token == "sha256":
                consumed = DataTypesHandler.handle_sha256(self.state, tokens, i)
            elif token == "sha512":
                consumed = DataTypesHandler.handle_sha512(self.state, tokens, i)
            elif token == "uuid":
                consumed = DataTypesHandler.handle_uuid(self.state, tokens, i)
            elif token == "hex_encode":
                consumed = DataTypesHandler.handle_hex_encode(self.state, tokens, i)
            elif token == "hex_decode":
                consumed = DataTypesHandler.handle_hex_decode(self.state, tokens, i)
            
            # Assert command
            elif token == "assert":
                consumed = DataTypesHandler.handle_assert(self.state, tokens, i)
            
            # Python-like array operations
            elif token == "array_slice":
                consumed = DataTypesHandler.handle_array_slice(self.state, tokens, i)
            elif token == "range":
                consumed = DataTypesHandler.handle_range(self.state, tokens, i)
            elif token == "array_comprehend":
                consumed = DataTypesHandler.handle_array_comprehend(self.state, tokens, i)
            elif token == "enumerate":
                consumed = DataTypesHandler.handle_enumerate(self.state, tokens, i)
            elif token == "array_zip":
                consumed = DataTypesHandler.handle_array_zip(self.state, tokens, i)
            
            # Lambda/anonymous functions
            elif token == "lambda":
                consumed = DataTypesHandler.handle_lambda(self.state, tokens, i)
            elif token == "array_apply":
                consumed = DataTypesHandler.handle_array_apply(self.state, tokens, i)
            elif token == "lambda_call":
                consumed = DataTypesHandler.handle_lambda_call(self.state, tokens, i)
            
            # Any/All and Min/Max
            elif token == "any":
                consumed = DataTypesHandler.handle_any(self.state, tokens, i)
            elif token == "all":
                consumed = DataTypesHandler.handle_all(self.state, tokens, i)
            elif token == "array_min":
                consumed = DataTypesHandler.handle_array_min(self.state, tokens, i)
            elif token == "array_max":
                consumed = DataTypesHandler.handle_array_max(self.state, tokens, i)
            elif token == "array_sorted":
                consumed = DataTypesHandler.handle_array_sorted(self.state, tokens, i)
            
            # String formatting and methods
            elif token == "str_format":
                consumed = DataTypesHandler.handle_str_format(self.state, tokens, i)
            elif token == "str_startswith":
                consumed = DataTypesHandler.handle_str_startswith(self.state, tokens, i)
            elif token == "str_endswith":
                consumed = DataTypesHandler.handle_str_endswith(self.state, tokens, i)
            elif token == "str_count":
                consumed = DataTypesHandler.handle_str_count(self.state, tokens, i)
            elif token == "str_find":
                consumed = DataTypesHandler.handle_str_find(self.state, tokens, i)
            elif token == "str_rfind":
                consumed = DataTypesHandler.handle_str_rfind(self.state, tokens, i)
            elif token == "str_isdigit":
                consumed = DataTypesHandler.handle_str_isdigit(self.state, tokens, i)
            elif token == "str_isalpha":
                consumed = DataTypesHandler.handle_str_isalpha(self.state, tokens, i)
            elif token == "str_isalnum":
                consumed = DataTypesHandler.handle_str_isalnum(self.state, tokens, i)
            
            # Dict methods
            elif token == "dict_values":
                consumed = DataTypesHandler.handle_dict_values(self.state, tokens, i)
            elif token == "dict_items":
                consumed = DataTypesHandler.handle_dict_items(self.state, tokens, i)
            elif token == "dict_update":
                consumed = DataTypesHandler.handle_dict_update(self.state, tokens, i)
            elif token == "dict_pop":
                consumed = DataTypesHandler.handle_dict_pop(self.state, tokens, i)
            elif token == "dict_get_default":
                consumed = DataTypesHandler.handle_dict_get_default(self.state, tokens, i)
            elif token == "dict_has_key":
                consumed = DataTypesHandler.handle_dict_has_key(self.state, tokens, i)
            elif token == "dict_clear":
                consumed = DataTypesHandler.handle_dict_clear(self.state, tokens, i)
            elif token == "dict_len":
                consumed = DataTypesHandler.handle_dict_len(self.state, tokens, i)
            
            # Set operations
            elif token == "set_create":
                consumed = DataTypesHandler.handle_set_create(self.state, tokens, i)
            elif token == "set_add":
                consumed = DataTypesHandler.handle_set_add(self.state, tokens, i)
            elif token == "set_remove":
                consumed = DataTypesHandler.handle_set_remove(self.state, tokens, i)
            elif token == "set_contains":
                consumed = DataTypesHandler.handle_set_contains(self.state, tokens, i)
            elif token == "set_len":
                consumed = DataTypesHandler.handle_set_len(self.state, tokens, i)
            elif token == "set_clear":
                consumed = DataTypesHandler.handle_set_clear(self.state, tokens, i)
            elif token == "set_union":
                consumed = DataTypesHandler.handle_set_union(self.state, tokens, i)
            elif token == "set_intersection":
                consumed = DataTypesHandler.handle_set_intersection(self.state, tokens, i)
            elif token == "set_difference":
                consumed = DataTypesHandler.handle_set_difference(self.state, tokens, i)
            elif token == "set_symmetric_difference":
                consumed = DataTypesHandler.handle_set_symmetric_difference(self.state, tokens, i)
            elif token == "set_issubset":
                consumed = DataTypesHandler.handle_set_issubset(self.state, tokens, i)
            elif token == "set_issuperset":
                consumed = DataTypesHandler.handle_set_issuperset(self.state, tokens, i)
            elif token == "set_to_array":
                consumed = DataTypesHandler.handle_set_to_array(self.state, tokens, i)
            elif token == "array_to_set":
                consumed = DataTypesHandler.handle_array_to_set(self.state, tokens, i)
            
            # Feature 7: Advanced Comprehensions
            elif token == "dict_comprehend":
                consumed = DataTypesHandler.handle_dict_comprehend(self.state, tokens, i)
            elif token == "set_comprehend":
                consumed = DataTypesHandler.handle_set_comprehend(self.state, tokens, i)
            elif token == "generator_expr":
                consumed = DataTypesHandler.handle_generator_expr(self.state, tokens, i)
            elif token == "comprehend_if":
                consumed = DataTypesHandler.handle_comprehend_if(self.state, tokens, i)
            
            # Feature 8: Slice Assignment & Advanced Slicing
            elif token == "array_slice_step":
                consumed = DataTypesHandler.handle_array_slice_step(self.state, tokens, i)
            elif token == "array_set_slice":
                consumed = DataTypesHandler.handle_array_set_slice(self.state, tokens, i)
            elif token == "str_slice":
                consumed = DataTypesHandler.handle_str_slice(self.state, tokens, i)
            elif token == "str_slice_step":
                consumed = DataTypesHandler.handle_str_slice_step(self.state, tokens, i)
            
            # Feature 9: Unpacking & Destructuring
            elif token == "unpack":
                consumed = DataTypesHandler.handle_unpack(self.state, tokens, i)
            elif token == "unpack_rest":
                consumed = DataTypesHandler.handle_unpack_rest(self.state, tokens, i)
            elif token == "dict_unpack":
                consumed = DataTypesHandler.handle_dict_unpack(self.state, tokens, i)
            elif token == "swap":
                consumed = DataTypesHandler.handle_swap(self.state, tokens, i)
            
            # Feature 10: F-Strings / Format Specifiers
            elif token == "fstring":
                consumed = DataTypesHandler.handle_fstring(self.state, tokens, i)
            elif token == "format_num":
                consumed = DataTypesHandler.handle_format_num(self.state, tokens, i)
            elif token == "format_align":
                consumed = DataTypesHandler.handle_format_align(self.state, tokens, i)
            elif token == "str_pad_left":
                consumed = DataTypesHandler.handle_str_pad_left(self.state, tokens, i)
            elif token == "str_pad_right":
                consumed = DataTypesHandler.handle_str_pad_right(self.state, tokens, i)
            
            # Bitwise operations
            elif token == "bit_and":
                consumed = DataTypesHandler.handle_bit_and(self.state, tokens, i)
            elif token == "bit_or":
                consumed = DataTypesHandler.handle_bit_or(self.state, tokens, i)
            elif token == "bit_xor":
                consumed = DataTypesHandler.handle_bit_xor(self.state, tokens, i)
            elif token == "bit_not":
                consumed = DataTypesHandler.handle_bit_not(self.state, tokens, i)
            elif token == "bit_shift_left":
                consumed = DataTypesHandler.handle_bit_shift_left(self.state, tokens, i)
            elif token == "bit_shift_right":
                consumed = DataTypesHandler.handle_bit_shift_right(self.state, tokens, i)
            
            # JSON operations - parsing and stringifying JSON
            elif token == "json_parse":
                consumed = DataTypesHandler.handle_json_parse(self.state, tokens, i)
            elif token == "json_stringify":
                consumed = DataTypesHandler.handle_json_stringify(self.state, tokens, i)
            elif token == "json_read":
                consumed = DataTypesHandler.handle_json_read(self.state, tokens, i, self.base_dir)
            elif token == "json_write":
                consumed = DataTypesHandler.handle_json_write(self.state, tokens, i, self.base_dir)

            # Feature 11: Itertools/Functools Equivalents
            elif token == "chain":
                consumed = DataTypesHandler.handle_chain(self.state, tokens, i)
            elif token == "cycle":
                consumed = DataTypesHandler.handle_cycle(self.state, tokens, i)
            elif token == "repeat":
                consumed = DataTypesHandler.handle_repeat(self.state, tokens, i)
            elif token == "takewhile":
                consumed = DataTypesHandler.handle_takewhile(self.state, tokens, i)
            elif token == "dropwhile":
                consumed = DataTypesHandler.handle_dropwhile(self.state, tokens, i)
            elif token == "groupby":
                consumed = DataTypesHandler.handle_groupby(self.state, tokens, i)
            elif token == "accumulate":
                consumed = DataTypesHandler.handle_accumulate(self.state, tokens, i)
            elif token == "pairwise":
                consumed = DataTypesHandler.handle_pairwise(self.state, tokens, i)
            elif token == "product":
                consumed = DataTypesHandler.handle_product(self.state, tokens, i)
            elif token == "permutations":
                consumed = DataTypesHandler.handle_permutations(self.state, tokens, i)
            elif token == "combinations":
                consumed = DataTypesHandler.handle_combinations(self.state, tokens, i)
            elif token == "reduce":
                consumed = DataTypesHandler.handle_reduce(self.state, tokens, i)
            elif token == "partial_array":
                consumed = DataTypesHandler.handle_partial_array(self.state, tokens, i)
            elif token == "apply_partial":
                consumed = DataTypesHandler.handle_apply_partial(self.state, tokens, i)

            # Feature 12: Date/Time Full Support
            elif token == "datetime_now":
                consumed = DataTypesHandler.handle_datetime_now(self.state, tokens, i)
            elif token == "datetime_utc":
                consumed = DataTypesHandler.handle_datetime_utc(self.state, tokens, i)
            elif token == "datetime_parse":
                consumed = DataTypesHandler.handle_datetime_parse(self.state, tokens, i)
            elif token == "datetime_format":
                consumed = DataTypesHandler.handle_datetime_format(self.state, tokens, i)
            elif token == "datetime_add":
                consumed = DataTypesHandler.handle_datetime_add(self.state, tokens, i)
            elif token == "datetime_diff":
                consumed = DataTypesHandler.handle_datetime_diff(self.state, tokens, i)
            elif token == "datetime_weekday":
                consumed = DataTypesHandler.handle_datetime_weekday(self.state, tokens, i)
            elif token == "datetime_timestamp":
                consumed = DataTypesHandler.handle_datetime_timestamp(self.state, tokens, i)
            elif token == "datetime_from_timestamp":
                consumed = DataTypesHandler.handle_datetime_from_timestamp(self.state, tokens, i)

            # Feature 13: Logging System
            elif token == "log_init":
                consumed = DataTypesHandler.handle_log_init(self.state, tokens, i)
            elif token == "log_debug":
                consumed = DataTypesHandler.handle_log_debug(self.state, tokens, i)
            elif token == "log_info":
                consumed = DataTypesHandler.handle_log_info(self.state, tokens, i)
            elif token == "log_warning":
                consumed = DataTypesHandler.handle_log_warning(self.state, tokens, i)
            elif token == "log_error":
                consumed = DataTypesHandler.handle_log_error(self.state, tokens, i)
            elif token == "log_critical":
                consumed = DataTypesHandler.handle_log_critical(self.state, tokens, i)
            elif token == "log_level":
                consumed = DataTypesHandler.handle_log_level(self.state, tokens, i)
            elif token == "log_file":
                consumed = DataTypesHandler.handle_log_file(self.state, tokens, i)
            elif token == "log_clear":
                consumed = DataTypesHandler.handle_log_clear(self.state, tokens, i)
            elif token == "log_count":
                consumed = DataTypesHandler.handle_log_count(self.state, tokens, i)
            elif token == "log_get":
                consumed = DataTypesHandler.handle_log_get(self.state, tokens, i)

            # Struct definitions and instances
            elif token == "struct":
                consumed = StructHandler.handle_struct(self.state, tokens, i)
            
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

            # Path helpers (store into target)
            elif token == "path_join":
                consumed = FileOpsHandler.handle_path_join(self.state, tokens, i)
            elif token == "path_basename":
                consumed = FileOpsHandler.handle_path_basename(self.state, tokens, i)
            elif token == "path_dirname":
                consumed = FileOpsHandler.handle_path_dirname(self.state, tokens, i)
            elif token == "path_extname":
                consumed = FileOpsHandler.handle_path_extname(self.state, tokens, i)

            # HTTP client
            elif token == "http_get":
                consumed = NetOpsHandler.handle_http_get(self.state, tokens, i)
            elif token == "http_post":
                consumed = NetOpsHandler.handle_http_post(self.state, tokens, i)
            elif token == "http_status":
                consumed = NetOpsHandler.handle_http_status(self.state, tokens, i)

            # Server stubs
            elif token == "server_start":
                consumed = NetServerHandler.handle_server_start(self.state, tokens, i)
            elif token == "server_route":
                consumed = NetServerHandler.handle_server_route(self.state, tokens, i)
            elif token == "server_stop":
                NetServerHandler.handle_server_stop(self.state)

            # Graphics
            elif token == "graphics_init":
                consumed = GraphicsOpsHandler.handle_graphics_init(self.state, tokens, i)
            elif token == "graphics_draw_line":
                consumed = GraphicsOpsHandler.handle_graphics_draw_line(self.state, tokens, i)
            elif token == "graphics_draw_circle":
                consumed = GraphicsOpsHandler.handle_graphics_draw_circle(self.state, tokens, i)
            elif token == "graphics_draw_text":
                consumed = GraphicsOpsHandler.handle_graphics_draw_text(self.state, tokens, i)
            elif token == "graphics_show":
                GraphicsOpsHandler.handle_graphics_show(self.state)

            # GUI (tkinter/customtkinter)
            elif token == "gui_backend":
                consumed = GuiOpsHandler.handle_gui_backend(self.state, tokens, i)
            elif token == "gui_ctk_appearance":
                consumed = GuiOpsHandler.handle_gui_ctk_appearance(self.state, tokens, i)
            elif token == "gui_ctk_theme":
                consumed = GuiOpsHandler.handle_gui_ctk_theme(self.state, tokens, i)
            elif token == "gui_ctk_scaling":
                consumed = GuiOpsHandler.handle_gui_ctk_scaling(self.state, tokens, i)
            elif token == "gui_ctk_switch":
                consumed = GuiOpsHandler.handle_gui_ctk_switch(self.state, tokens, i)
            elif token == "gui_ctk_slider":
                consumed = GuiOpsHandler.handle_gui_ctk_slider(self.state, tokens, i)
            elif token == "gui_ctk_progressbar":
                consumed = GuiOpsHandler.handle_gui_ctk_progressbar(self.state, tokens, i)
            elif token == "gui_ctk_progress_set":
                consumed = GuiOpsHandler.handle_gui_ctk_progress_set(self.state, tokens, i)
            elif token == "gui_ctk_optionmenu":
                consumed = GuiOpsHandler.handle_gui_ctk_optionmenu(self.state, tokens, i)
            elif token == "gui_ctk_combobox":
                consumed = GuiOpsHandler.handle_gui_ctk_combobox(self.state, tokens, i)
            elif token == "gui_ctk_tabview":
                consumed = GuiOpsHandler.handle_gui_ctk_tabview(self.state, tokens, i)
            elif token == "gui_ctk_tab":
                consumed = GuiOpsHandler.handle_gui_ctk_tab(self.state, tokens, i)
            elif token == "gui_window":
                consumed = GuiOpsHandler.handle_gui_window(self.state, tokens, i)
            elif token == "gui_set":
                consumed = GuiOpsHandler.handle_gui_set(self.state, tokens, i)
            elif token == "gui_get":
                consumed = GuiOpsHandler.handle_gui_get(self.state, tokens, i)
            elif token == "gui_pack":
                consumed = GuiOpsHandler.handle_gui_pack(self.state, tokens, i)
            elif token == "gui_grid":
                consumed = GuiOpsHandler.handle_gui_grid(self.state, tokens, i)
            elif token == "gui_bind":
                consumed = GuiOpsHandler.handle_gui_bind(self.state, tokens, i)
            elif token == "gui_label":
                consumed = GuiOpsHandler.handle_gui_label(self.state, tokens, i)
            elif token == "gui_button":
                consumed = GuiOpsHandler.handle_gui_button(self.state, tokens, i)
            elif token == "gui_entry":
                consumed = GuiOpsHandler.handle_gui_entry(self.state, tokens, i)
            elif token == "gui_frame":
                consumed = GuiOpsHandler.handle_gui_frame(self.state, tokens, i)
            elif token == "gui_checkbutton":
                consumed = GuiOpsHandler.handle_gui_checkbutton(self.state, tokens, i)
            elif token == "gui_radiobutton":
                consumed = GuiOpsHandler.handle_gui_radiobutton(self.state, tokens, i)
            elif token == "gui_text":
                consumed = GuiOpsHandler.handle_gui_text(self.state, tokens, i)
            elif token == "gui_listbox":
                consumed = GuiOpsHandler.handle_gui_listbox(self.state, tokens, i)
            elif token == "gui_canvas":
                consumed = GuiOpsHandler.handle_gui_canvas(self.state, tokens, i)
            elif token == "gui_scrollbar":
                consumed = GuiOpsHandler.handle_gui_scrollbar(self.state, tokens, i)
            elif token == "gui_canvas_create_line":
                consumed = GuiOpsHandler.handle_gui_canvas_create_line(self.state, tokens, i)
            elif token == "gui_canvas_move":
                consumed = GuiOpsHandler.handle_gui_canvas_move(self.state, tokens, i)
            elif token == "gui_canvas_delete":
                consumed = GuiOpsHandler.handle_gui_canvas_delete(self.state, tokens, i)
            elif token == "gui_canvas_coords":
                consumed = GuiOpsHandler.handle_gui_canvas_coords(self.state, tokens, i)
            elif token == "gui_text_insert":
                consumed = GuiOpsHandler.handle_gui_text_insert(self.state, tokens, i)
            elif token == "gui_text_get":
                consumed = GuiOpsHandler.handle_gui_text_get(self.state, tokens, i)
            elif token == "gui_text_delete":
                consumed = GuiOpsHandler.handle_gui_text_delete(self.state, tokens, i)
            elif token == "gui_text_tag_add":
                consumed = GuiOpsHandler.handle_gui_text_tag_add(self.state, tokens, i)
            elif token == "gui_text_tag_config":
                consumed = GuiOpsHandler.handle_gui_text_tag_config(self.state, tokens, i)
            elif token == "gui_var_new":
                consumed = GuiOpsHandler.handle_gui_var_new(self.state, tokens, i)
            elif token == "gui_var_set":
                consumed = GuiOpsHandler.handle_gui_var_set(self.state, tokens, i)
            elif token == "gui_var_get":
                consumed = GuiOpsHandler.handle_gui_var_get(self.state, tokens, i)
            elif token == "gui_menubar":
                consumed = GuiOpsHandler.handle_gui_menubar(self.state, tokens, i)
            elif token == "gui_menu":
                consumed = GuiOpsHandler.handle_gui_menu(self.state, tokens, i)
            elif token == "gui_menu_item":
                consumed = GuiOpsHandler.handle_gui_menu_item(self.state, tokens, i)
            elif token == "gui_messagebox":
                consumed = GuiOpsHandler.handle_gui_messagebox(self.state, tokens, i)
            elif token == "gui_filedialog_open":
                consumed = GuiOpsHandler.handle_gui_filedialog_open(self.state, tokens, i)
            elif token == "gui_filedialog_save":
                consumed = GuiOpsHandler.handle_gui_filedialog_save(self.state, tokens, i)
            elif token == "gui_ttk_style_set":
                consumed = GuiOpsHandler.handle_gui_ttk_style_set(self.state, tokens, i)
            elif token == "gui_ttk_theme_use":
                consumed = GuiOpsHandler.handle_gui_ttk_theme_use(self.state, tokens, i)
            elif token == "gui_ttk_button":
                consumed = GuiOpsHandler.handle_gui_ttk_button(self.state, tokens, i)
            elif token == "gui_ttk_label":
                consumed = GuiOpsHandler.handle_gui_ttk_label(self.state, tokens, i)
            elif token == "gui_ttk_entry":
                consumed = GuiOpsHandler.handle_gui_ttk_entry(self.state, tokens, i)
            elif token == "gui_ttk_combobox":
                consumed = GuiOpsHandler.handle_gui_ttk_combobox(self.state, tokens, i)
            elif token == "gui_ttk_treeview":
                consumed = GuiOpsHandler.handle_gui_ttk_treeview(self.state, tokens, i)
            elif token == "gui_ttk_notebook":
                consumed = GuiOpsHandler.handle_gui_ttk_notebook(self.state, tokens, i)
            elif token == "gui_ttk_notebook_tab":
                consumed = GuiOpsHandler.handle_gui_ttk_notebook_tab(self.state, tokens, i)
            elif token == "gui_ttk_progressbar":
                consumed = GuiOpsHandler.handle_gui_ttk_progressbar(self.state, tokens, i)
            elif token == "gui_ttk_separator":
                consumed = GuiOpsHandler.handle_gui_ttk_separator(self.state, tokens, i)
            elif token == "gui_entry_get":
                consumed = GuiOpsHandler.handle_gui_entry_get(self.state, tokens, i)
            elif token == "gui_entry_set":
                consumed = GuiOpsHandler.handle_gui_entry_set(self.state, tokens, i)
            elif token == "gui_destroy":
                consumed = GuiOpsHandler.handle_gui_destroy(self.state, tokens, i)
            elif token == "gui_mainloop":
                consumed = GuiOpsHandler.handle_gui_mainloop(self.state, tokens, i, self.base_dir)

            # Memory
            elif token == "mem_alloc":
                consumed = MemoryOpsHandler.handle_mem_alloc(self.state, tokens, i)
            elif token == "mem_free":
                consumed = MemoryOpsHandler.handle_mem_free(self.state, tokens, i)
            elif token == "mem_read":
                consumed = MemoryOpsHandler.handle_mem_read(self.state, tokens, i)
            elif token == "mem_write":
                consumed = MemoryOpsHandler.handle_mem_write(self.state, tokens, i)
            elif token == "mem_dump":
                MemoryOpsHandler.handle_mem_dump(self.state)

            # Help
            elif token == "help":
                consumed = HelpOpsHandler.handle_help(self.state, tokens, i, sorted(BasicCommandHandler.KNOWN_COMMANDS))

            # Threading & Async
            elif token == "thread_create":
                consumed = ThreadOpsHandler.handle_thread_create(self.state, tokens, i, self.base_dir)
            elif token == "thread_join":
                consumed = ThreadOpsHandler.handle_thread_join(self.state, tokens, i)
            elif token == "thread_sleep":
                consumed = ThreadOpsHandler.handle_thread_sleep(self.state, tokens, i)
            elif token == "thread_status":
                consumed = ThreadOpsHandler.handle_thread_status(self.state, tokens, i)
            elif token == "thread_result":
                consumed = ThreadOpsHandler.handle_thread_result(self.state, tokens, i)
            elif token == "thread_list":
                consumed = ThreadOpsHandler.handle_thread_list(self.state)
            elif token == "thread_wait_all":
                consumed = ThreadOpsHandler.handle_thread_wait_all(self.state)
            elif token == "mutex_create":
                consumed = ThreadOpsHandler.handle_mutex_create(self.state, tokens, i)
            elif token == "mutex_lock":
                consumed = ThreadOpsHandler.handle_mutex_lock(self.state, tokens, i)
            elif token == "mutex_unlock":
                consumed = ThreadOpsHandler.handle_mutex_unlock(self.state, tokens, i)
            elif token == "queue_push":
                consumed = ThreadOpsHandler.handle_queue_push(self.state, tokens, i)
            elif token == "queue_pop":
                consumed = ThreadOpsHandler.handle_queue_pop(self.state, tokens, i)
            elif token == "async_start":
                consumed = ThreadOpsHandler.handle_async_start(self.state, tokens, i, self.base_dir)
            elif token == "async_wait":
                consumed = ThreadOpsHandler.handle_async_wait(self.state, tokens, i)

            # System
            elif token == "sys_exec":
                consumed = SystemOpsHandler.handle_sys_exec(self.state, tokens, i)
            elif token == "sys_env":
                consumed = SystemOpsHandler.handle_sys_env(self.state, tokens, i)
            elif token == "sys_time":
                consumed = SystemOpsHandler.handle_sys_time(self.state, tokens, i)
            elif token == "sys_date":
                SystemOpsHandler.handle_sys_date(self.state)
            elif token == "sys_sleep":
                consumed = SystemOpsHandler.handle_sys_sleep(self.state, tokens, i)
            elif token == "sys_cwd":
                consumed = SystemOpsHandler.handle_sys_cwd(self.state)
            elif token == "sys_exit":
                consumed = SystemOpsHandler.handle_sys_exit(self.state, tokens, i)

            # Processes
            elif token == "proc_spawn":
                consumed = ProcessOpsHandler.handle_proc_spawn(self.state, tokens, i)
            elif token == "proc_wait":
                consumed = ProcessOpsHandler.handle_proc_wait(self.state, tokens, i)
            elif token == "proc_kill":
                consumed = ProcessOpsHandler.handle_proc_kill(self.state, tokens, i)
            elif token == "proc_status":
                consumed = ProcessOpsHandler.handle_proc_status(self.state, tokens, i)

            # Try/Catch/Else/Finally
            elif token == "try":
                consumed = ControlFlowHandler.handle_try(self.state, tokens, i, self.execute_block)

            # Context managers (with statement)
            elif token == "with":
                consumed = ControlFlowHandler.handle_with(self.state, tokens, i, self.execute_block)

            # OOP - Classes and Objects
            elif token == "class":
                consumed = ClassOpsHandler.handle_class(self.state, tokens, i)
            elif token == "new":
                consumed = ClassOpsHandler.handle_new(self.state, tokens, i, self.execute_block)
            elif token == "get_field":
                consumed = ClassOpsHandler.handle_get_field(self.state, tokens, i)
            elif token == "set_field":
                consumed = ClassOpsHandler.handle_set_field(self.state, tokens, i)
            elif token == "instanceof":
                consumed = ClassOpsHandler.handle_instanceof(self.state, tokens, i)

            # First-class functions and closures
            elif token == "fn":
                consumed = FunctionOpsHandler.handle_fn(self.state, tokens, i)
            elif token == "fn_ref":
                consumed = FunctionOpsHandler.handle_fn_ref(self.state, tokens, i)
            elif token == "fn_call":
                consumed = FunctionOpsHandler.handle_fn_call(self.state, tokens, i, self.execute_block)
            elif token == "partial":
                consumed = FunctionOpsHandler.handle_partial(self.state, tokens, i)
            elif token == "compose":
                consumed = FunctionOpsHandler.handle_compose(self.state, tokens, i)
            elif token == "map_fn":
                consumed = FunctionOpsHandler.handle_map_fn(self.state, tokens, i, self.execute_block)
            elif token == "filter_fn":
                consumed = FunctionOpsHandler.handle_filter_fn(self.state, tokens, i, self.execute_block)
            elif token == "reduce_fn":
                consumed = FunctionOpsHandler.handle_reduce_fn(self.state, tokens, i, self.execute_block)

            # Exception handling - throw/raise
            elif token in ("throw", "raise"):
                consumed = BasicCommandHandler.handle_throw(self.state, tokens, i)

            # Decorators
            elif token == "decorator":
                consumed = DecoratorOpsHandler.handle_decorator_def(self.state, tokens, i)
            elif token == "decorate":
                consumed = DecoratorOpsHandler.handle_decorate(self.state, tokens, i, self.execute_block)

            # Context managers
            elif token == "context":
                consumed = ContextOpsHandler.handle_context_def(self.state, tokens, i)

            # Async/Await
            elif token == "async":
                consumed = AsyncOpsHandler.handle_async_def(self.state, tokens, i)
            elif token == "await":
                consumed = AsyncOpsHandler.handle_await(self.state, tokens, i, self.execute_block)
            elif token == "spawn":
                consumed = AsyncOpsHandler.handle_spawn_task(self.state, tokens, i, self.execute_block, self.base_dir)
            elif token == "gather":
                consumed = AsyncOpsHandler.handle_gather(self.state, tokens, i, self.execute_block)
            elif token == "task_status":
                consumed = AsyncOpsHandler.handle_task_status(self.state, tokens, i)
            elif token == "task_cancel":
                consumed = AsyncOpsHandler.handle_task_cancel(self.state, tokens, i)

            # Pythonic Features: Dataclasses
            elif token == "dataclass":
                consumed = PythonicOpsHandler.handle_dataclass(self.state, tokens, i)
            elif token == "dataclass_new":
                consumed = PythonicOpsHandler.handle_dataclass_new(self.state, tokens, i)
            elif token == "dataclass_get":
                consumed = PythonicOpsHandler.handle_dataclass_get(self.state, tokens, i)
            elif token == "dataclass_set":
                consumed = PythonicOpsHandler.handle_dataclass_set(self.state, tokens, i)
            elif token == "dataclass_eq":
                consumed = PythonicOpsHandler.handle_dataclass_eq(self.state, tokens, i)
            elif token == "dataclass_str":
                consumed = PythonicOpsHandler.handle_dataclass_str(self.state, tokens, i)
            elif token == "dataclass_to_dict":
                consumed = PythonicOpsHandler.handle_dataclass_to_dict(self.state, tokens, i)

            # Pythonic Features: in/not_in operators
            elif token == "in":
                consumed = PythonicOpsHandler.handle_in(self.state, tokens, i)
            elif token == "not_in":
                consumed = PythonicOpsHandler.handle_not_in(self.state, tokens, i)
            elif token == "contains":
                consumed = PythonicOpsHandler.handle_contains(self.state, tokens, i)

            # Pythonic Features: Property decorators
            elif token == "get_property":
                consumed = PythonicOpsHandler.handle_get_property(self.state, tokens, i, self.execute_block)
            elif token == "set_property":
                consumed = PythonicOpsHandler.handle_set_property(self.state, tokens, i, self.execute_block)

            # End of block - marks the end of loops, functions, etc.
            elif token == "end":
                pass
            
            # Unknown command - something we don't recognize
            else:
                self.state.add_error(f"Unknown command '{token}'. Check your syntax and make sure all commands are spelled correctly.")
            
            # Check if we should stop execution (early return from function)
            if self.state.should_return:
                break
            
            # Move to the next command, skipping any tokens this command used
            i += 1 + consumed
