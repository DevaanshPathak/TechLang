from typing import List, Dict, Union, Set
from dataclasses import dataclass


@dataclass
class InterpreterState:
    # Central runtime container: numbers, variables, stack, aliases, and output
    value: int = 0
    stack: List[int] = None
    output: List[str] = None
    variables: Dict[str, Union[int, str]] = None
    functions: Dict[str, List[str]] = None
    aliases: Dict[str, str] = None
    input_queue: List[str] = None
    loaded_files: Set[str] = None
    
    def __post_init__(self):
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
        self.value = 0
        self.stack.clear()
        self.output.clear()
        self.variables.clear()
        self.functions.clear()
        self.aliases.clear()
        self.input_queue.clear()
        # Keep loaded_files to avoid re-importing the same files
    
    def get_output(self) -> str:
        return "\n".join(self.output)
    
    def add_output(self, message: str) -> None:
        self.output.append(message)
    
    def add_error(self, message: str) -> None:
        # Standardized error format for consistent test and UI output
        self.add_output(f"[Error: {message}]")
    
    def get_variable(self, name: str, default: Union[int, str] = 0) -> Union[int, str]:
        return self.variables.get(name, default)
    
    def set_variable(self, name: str, value: Union[int, str]) -> None:
        self.variables[name] = value
    
    def has_variable(self, name: str) -> bool:
        return name in self.variables
    
    def push_stack(self, value: int) -> None:
        self.stack.append(value)
    
    def pop_stack(self) -> int:
        if not self.stack:
            raise IndexError("Stack is empty")
        return self.stack.pop()
    
    def peek_stack(self) -> int:
        if not self.stack:
            raise IndexError("Stack is empty")
        return self.stack[-1]
    
    def is_stack_empty(self) -> bool:
        return len(self.stack) == 0
    
    def get_input(self) -> str:
        # Pull one item from the queued inputs (used by tests and web UI)
        if self.input_queue:
            return self.input_queue.pop(0)
        raise IndexError("No input available")
    
    def has_input(self) -> bool:
        return len(self.input_queue) > 0
