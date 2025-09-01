# techlang/core.py

from typing import List, Dict, Union, Set
from dataclasses import dataclass


@dataclass
class InterpreterState:
    """
    Core state management for the TechLang interpreter.
    
    This class holds all the runtime state including variables, stack,
    functions, aliases, and output.
    """
    value: int = 0
    stack: List[int] = None
    output: List[str] = None
    variables: Dict[str, Union[int, str]] = None
    functions: Dict[str, List[str]] = None
    aliases: Dict[str, str] = None
    input_queue: List[str] = None
    loaded_files: Set[str] = None
    
    def __post_init__(self):
        """Initialize mutable default values."""
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
    
    def reset(self) -> None:
        """Reset the interpreter state to initial values."""
        self.value = 0
        self.stack.clear()
        self.output.clear()
        self.variables.clear()
        self.functions.clear()
        self.aliases.clear()
        self.input_queue.clear()
        # Note: loaded_files is not cleared to prevent re-importing
    
    def get_output(self) -> str:
        """Get the current output as a string."""
        return "\n".join(self.output)
    
    def add_output(self, message: str) -> None:
        """Add a message to the output."""
        self.output.append(message)
    
    def add_error(self, message: str) -> None:
        """Add an error message to the output."""
        self.add_output(f"[Error: {message}]")
    
    def get_variable(self, name: str, default: Union[int, str] = 0) -> Union[int, str]:
        """Get a variable value with a default."""
        return self.variables.get(name, default)
    
    def set_variable(self, name: str, value: Union[int, str]) -> None:
        """Set a variable value."""
        self.variables[name] = value
    
    def has_variable(self, name: str) -> bool:
        """Check if a variable exists."""
        return name in self.variables
    
    def push_stack(self, value: int) -> None:
        """Push a value onto the stack."""
        self.stack.append(value)
    
    def pop_stack(self) -> int:
        """Pop a value from the stack."""
        if not self.stack:
            raise IndexError("Stack is empty")
        return self.stack.pop()
    
    def peek_stack(self) -> int:
        """Peek at the top value of the stack without removing it."""
        if not self.stack:
            raise IndexError("Stack is empty")
        return self.stack[-1]
    
    def is_stack_empty(self) -> bool:
        """Check if the stack is empty."""
        return len(self.stack) == 0
    
    def get_input(self) -> str:
        """Get the next input value from the queue."""
        if self.input_queue:
            return self.input_queue.pop(0)
        raise IndexError("No input available")
    
    def has_input(self) -> bool:
        """Check if there are input values available."""
        return len(self.input_queue) > 0
