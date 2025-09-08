from typing import List, Dict, Union, Set
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
    functions: Dict[str, List[str]] = None
    
    # Shortcuts for commands (like alias inc ping)
    aliases: Dict[str, str] = None
    
    # Input waiting to be read (for testing and web interface)
    input_queue: List[str] = None
    
    # Files that have been imported to avoid loading them twice
    loaded_files: Set[str] = None
    
    # Arrays that can store lists of numbers or text
    arrays: Dict[str, List[Union[int, str]]] = None
    
    # Text strings that can be manipulated
    strings: Dict[str, str] = None
    
    # Dictionaries that store key-value pairs (like a phone book)
    dictionaries: Dict[str, Dict[str, Union[int, str]]] = None
    
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
        if self.aliases is None:
            self.aliases = {}
        if self.input_queue is None:
            self.input_queue = []
        if self.loaded_files is None:
            self.loaded_files = set()
        if self.arrays is None:
            self.arrays = {}
        if self.strings is None:
            self.strings = {}
        if self.dictionaries is None:
            self.dictionaries = {}
    
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
        self.aliases.clear()
        self.input_queue.clear()
        self.arrays.clear()
        self.strings.clear()
        self.dictionaries.clear()
    
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
