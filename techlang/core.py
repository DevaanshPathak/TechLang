from typing import List, Dict, Union, Set, Optional
from dataclasses import dataclass


@dataclass
class InterpreterState:
    """
    The heart of TechLang - stores everything the interpreter needs to run.
    Think of this as the computer's memory where all your programs live.
    """
    # The current number we're working with (like a calculator display)
    value: int = 0
    
    # A stack for storing numbers (like a stack of plates)
    stack: List[int] = None
    
    # All the text that gets printed to the user
    output: List[str] = None
    
    # Variables that store numbers or text (like x = 5)
    variables: Dict[str, Union[int, str]] = None
    
    # Functions that can be called (like def my_function)
    # Now stores dict with 'params' (list of param names) and 'body' (list of tokens)
    functions: Dict[str, dict] = None
    
    # Function return values (set by 'return' command, read by caller)
    return_values: List[Union[int, str]] = None

    # Compile-time macros expanded before execution
    macros: Dict[str, dict] = None
    
    # Shortcuts for commands (like alias inc ping)
    aliases: Dict[str, str] = None
    
    # Input waiting to be read (for testing and web interface)
    input_queue: List[str] = None
    
    # Files that have been imported to avoid loading them twice
    loaded_files: Set[str] = None

    # Modules loaded via `package use`; maps module name -> module info dict
    modules: Dict[str, object] = None

    # Track raw module identifiers to skip duplicate loads
    loaded_modules: Set[str] = None

    # Optional parent scope (used by modules for fallback lookups)
    parent_state: Optional["InterpreterState"] = None
    
    # Arrays that can store lists of numbers or text
    arrays: Dict[str, List[Union[int, str]]] = None

    # Arrays created without a fixed size (allow growth via array_set and safe out-of-bounds reads)
    dynamic_arrays: Set[str] = None
    
    # Text strings that can be manipulated
    strings: Dict[str, str] = None
    
    # Dictionaries that store key-value pairs (like a phone book)
    dictionaries: Dict[str, Dict[str, Union[int, str]]] = None

    # Struct type definitions (field name -> type) and instances (instance -> {type, fields})
    struct_defs: Dict[str, Dict[str, str]] = None
    structs: Dict[str, Dict[str, object]] = None

    # Simple memory model
    memory: Dict[int, int] = None
    next_address: int = 1

    # Threading/Async bookkeeping
    threads: Dict[int, object] = None
    thread_results: Dict[int, str] = None
    next_thread_id: int = 1
    mutexes: Dict[str, object] = None
    queues: Dict[str, object] = None

    # Subprocess management
    processes: Dict[int, object] = None
    next_process_id: int = 1

    # Subprocess timing (used for more deterministic status polling)
    process_start_times: Dict[int, float] = None
    
    # Debugger state
    breakpoints: Set[int] = None  # Line numbers where execution should pause
    
    # Return statement control
    should_return: bool = False  # Flag to stop execution when return is called
    debug_mode: bool = False  # Whether debugger is active
    stepping: bool = False  # Whether to pause after each command
    watched_vars: Set[str] = None  # Variables to monitor
    command_count: int = 0  # Current command/instruction number
    paused: bool = False  # Whether execution is currently paused
    
    # Export/visibility control for library APIs
    exported_functions: Set[str] = None  # Functions marked as public (callable from outside modules)

    # GUI (tkinter/customtkinter) specification storage
    # Note: GUI widgets are stored as *specs* during execution; real windows are created by gui_mainloop.
    gui_backend: str = "tk"  # "tk" | "ctk"
    gui_specs: Dict[str, Dict[str, object]] = None  # name -> spec dict
    gui_order: List[str] = None  # creation order (used to realize widgets deterministically)

    # GUI runtime storage (populated only while gui_mainloop is running)
    gui_runtime_widgets: Dict[str, object] = None  # name -> tk/ctk widget object
    gui_runtime_vars: Dict[str, object] = None  # name -> tk variable object (StringVar/IntVar/...)
    gui_runtime_base_dir: str = "."

    # GUI variable specs (Tk variables)
    gui_vars: Dict[str, Dict[str, object]] = None  # name -> {type, value}

    # GUI ttk style specs
    gui_ttk_styles: Dict[str, Dict[str, object]] = None  # style name -> options
    gui_ttk_theme: str = ""  # optional theme name
    
    def __post_init__(self):
        """
        Set up empty containers when the interpreter starts.
        This runs automatically when we create a new InterpreterState.
        """
        if self.stack is None:
            self.stack = []
        if self.output is None:
            self.output = []
        if self.variables is None:
            self.variables = {}
        if self.functions is None:
            self.functions = {}
        if self.return_values is None:
            self.return_values = []
        if self.macros is None:
            self.macros = {}
        if self.aliases is None:
            self.aliases = {}
        if self.input_queue is None:
            self.input_queue = []
        if self.loaded_files is None:
            self.loaded_files = set()
        if self.modules is None:
            self.modules = {}
        if self.loaded_modules is None:
            self.loaded_modules = set()
        if self.arrays is None:
            self.arrays = {}
        if self.dynamic_arrays is None:
            self.dynamic_arrays = set()
        if self.strings is None:
            self.strings = {}
        if self.dictionaries is None:
            self.dictionaries = {}
        if self.struct_defs is None:
            self.struct_defs = {}
        if self.structs is None:
            self.structs = {}
        if self.memory is None:
            self.memory = {}
        if self.threads is None:
            self.threads = {}
        if self.thread_results is None:
            self.thread_results = {}
        if self.mutexes is None:
            self.mutexes = {}
        if self.queues is None:
            self.queues = {}
        if self.processes is None:
            self.processes = {}
        if self.process_start_times is None:
            self.process_start_times = {}
        if self.breakpoints is None:
            self.breakpoints = set()
        if self.watched_vars is None:
            self.watched_vars = set()
        if self.exported_functions is None:
            self.exported_functions = set()

        if self.gui_specs is None:
            self.gui_specs = {}
        if self.gui_order is None:
            self.gui_order = []

        if self.gui_runtime_widgets is None:
            self.gui_runtime_widgets = {}
        if self.gui_runtime_vars is None:
            self.gui_runtime_vars = {}
        if not hasattr(self, "gui_runtime_base_dir") or self.gui_runtime_base_dir is None:
            self.gui_runtime_base_dir = "."
        if self.gui_vars is None:
            self.gui_vars = {}

        if self.gui_ttk_styles is None:
            self.gui_ttk_styles = {}
        if not hasattr(self, "gui_ttk_theme") or self.gui_ttk_theme is None:
            self.gui_ttk_theme = ""
    
    def reset(self) -> None:
        """
        Clear everything and start fresh.
        Like restarting your computer - all programs stop and memory is cleared.
        We keep loaded_files so we don't have to reload the same files again.
        """
        self.value = 0
        self.stack.clear()
        self.output.clear()
        self.variables.clear()
        self.functions.clear()
        self.macros.clear()
        self.aliases.clear()
        self.input_queue.clear()
        self.arrays.clear()
        self.dynamic_arrays.clear()
        self.strings.clear()
        self.dictionaries.clear()
        self.struct_defs.clear()
        self.structs.clear()
        self.memory.clear()
        self.next_address = 1
        self.threads.clear()
        self.thread_results.clear()
        self.next_thread_id = 1
        self.mutexes.clear()
        self.queues.clear()
        self.processes.clear()
        self.next_process_id = 1
        self.process_start_times.clear()
        self.modules.clear()
        self.loaded_modules.clear()
    
    def get_output(self) -> str:
        """
        Join all output lines into one big string.
        This is what gets shown to the user at the end.
        """
        return "\n".join(self.output)
    
    def add_output(self, message: str) -> None:
        """
        Add a line to the output that will be shown to the user.
        Like printing something to the screen.
        """
        self.output.append(message)
    
    def add_error(self, message: str) -> None:
        """
        Add an error message to the output.
        Errors are wrapped in [Error: ...] so they're easy to spot.
        """
        self.add_output(f"[Error: {message}]")
    
    def get_variable(self, name: str, default: Union[int, str] = 0) -> Union[int, str]:
        """
        Get the value of a variable, or return a default if it doesn't exist.
        Like looking up someone's phone number in a phone book.
        """
        return self.variables.get(name, default)
    
    def set_variable(self, name: str, value: Union[int, str]) -> None:
        """
        Store a value in a variable.
        Like writing someone's phone number in your phone book.
        """
        self.variables[name] = value
    
    def has_variable(self, name: str) -> bool:
        """
        Check if a variable exists.
        Like checking if someone's name is in your phone book.
        """
        return name in self.variables
    
    def push_stack(self, value: int) -> None:
        """
        Put a number on top of the stack.
        Like putting a plate on a stack of plates.
        """
        self.stack.append(value)
    
    def pop_stack(self) -> int:
        """
        Take the top number off the stack and return it.
        Like taking the top plate off a stack of plates.
        """
        if not self.stack:
            raise IndexError("Stack is empty")
        return self.stack.pop()
    
    def peek_stack(self) -> int:
        """
        Look at the top number on the stack without removing it.
        Like looking at the top plate without taking it off.
        """
        if not self.stack:
            raise IndexError("Stack is empty")
        return self.stack[-1]
    
    def is_stack_empty(self) -> bool:
        """
        Check if the stack has any numbers in it.
        Like checking if there are any plates on the stack.
        """
        return len(self.stack) == 0
    
    def get_input(self) -> str:
        """
        Get the next piece of input from the queue.
        Used by tests and web interface to provide input to programs.
        """
        if self.input_queue:
            return self.input_queue.pop(0)
        raise IndexError("No input available")
    
    def has_input(self) -> bool:
        """
        Check if there's any input waiting to be read.
        Like checking if there are any messages in your inbox.
        """
        return len(self.input_queue) > 0
