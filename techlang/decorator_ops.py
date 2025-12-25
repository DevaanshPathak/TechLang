"""
Decorator support for TechLang.

This module implements Python-like function decorators that wrap functions
with additional behavior.

Decorators can:
- Log function calls
- Time function execution
- Memoize/cache results
- Validate inputs
- Transform outputs
"""

from typing import Dict, List, Optional, Any, Callable
from .core import InterpreterState


class DecoratorDefinition:
    """Represents a decorator definition."""
    
    def __init__(self, name: str, params: List[str], body: List[str]):
        self.name = name
        self.params = params  # The decorated function is passed as first param
        self.body = body
    
    def __repr__(self):
        return f"<decorator @{self.name}>"


class DecoratorOpsHandler:
    """Handles decorator operations in TechLang."""
    
    @staticmethod
    def handle_decorator_def(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Define a decorator:
        decorator <name> func [params...] do ... end
        
        The first parameter is always the function being decorated.
        """
        if index + 1 >= len(tokens):
            state.add_error("Invalid decorator definition. Use: decorator <name> func [params...] do ... end")
            return 0
        
        name = tokens[index + 1]
        cursor = index + 2
        
        # Collect parameters (first is the decorated function, rest are decorator args)
        params = []
        while cursor < len(tokens) and tokens[cursor] != "do":
            params.append(tokens[cursor])
            cursor += 1
        
        if cursor >= len(tokens) or tokens[cursor] != "do":
            state.add_error("Expected 'do' in decorator definition")
            return cursor - index
        
        if len(params) < 1:
            state.add_error("Decorator must have at least one parameter (the function to decorate)")
            return cursor - index
        
        cursor += 1  # Skip 'do'
        
        # Find matching 'end'
        body_start = cursor
        depth = 1
        while cursor < len(tokens):
            t = tokens[cursor]
            if t in {"decorator", "def", "fn", "if", "loop", "while", "switch", "try", "match", "do", "class"}:
                depth += 1
            elif t == "end":
                depth -= 1
                if depth == 0:
                    break
            cursor += 1
        
        if cursor >= len(tokens):
            state.add_error("Decorator definition missing 'end'")
            return cursor - index
        
        body = tokens[body_start:cursor]
        
        # Store decorator definition
        if not hasattr(state, 'decorators') or state.decorators is None:
            state.decorators = {}
        
        decorator = DecoratorDefinition(name, params, body)
        state.decorators[name] = decorator
        
        return cursor - index
    
    @staticmethod
    def handle_decorate(state: InterpreterState, tokens: List[str], index: int,
                       execute_block: Callable) -> int:
        """
        Apply a decorator to a function:
        @<decorator_name> [args...]
        def <func_name> ...
        
        Or inline:
        decorate <func_name> with <decorator_name> [args...] as <new_name>
        """
        if index + 1 >= len(tokens):
            state.add_error("Invalid decorate command")
            return 0
        
        func_name = tokens[index + 1]
        
        # Check for 'with' keyword
        if index + 3 >= len(tokens) or tokens[index + 2] != "with":
            state.add_error("Use: decorate <func> with <decorator> [args...] as <new_name>")
            return 1
        
        decorator_name = tokens[index + 3]
        cursor = index + 4
        
        # Collect decorator arguments until 'as'
        decorator_args = []
        while cursor < len(tokens) and tokens[cursor] != "as":
            decorator_args.append(tokens[cursor])
            cursor += 1
        
        if cursor >= len(tokens) or tokens[cursor] != "as":
            state.add_error("decorate command requires 'as <new_name>'")
            return cursor - index
        
        cursor += 1  # Skip 'as'
        
        if cursor >= len(tokens):
            state.add_error("decorate command requires a new function name after 'as'")
            return cursor - index
        
        new_name = tokens[cursor]
        
        # Get the decorator
        if not hasattr(state, 'decorators') or state.decorators is None:
            state.decorators = {}
        
        decorator = state.decorators.get(decorator_name)
        if decorator is None:
            state.add_error(f"Decorator '{decorator_name}' is not defined")
            return cursor - index
        
        # Get the original function
        if func_name not in state.functions:
            state.add_error(f"Function '{func_name}' is not defined")
            return cursor - index
        
        original_func = state.functions[func_name]
        
        # Create the wrapped function
        # The decorator body should call the original function via a special variable
        wrapped_body = DecoratorOpsHandler._create_wrapped_function(
            state, decorator, original_func, func_name, decorator_args
        )
        
        # Store the new decorated function
        if isinstance(original_func, dict):
            state.functions[new_name] = {
                'params': original_func.get('params', []),
                'body': wrapped_body,
                '_decorated_by': decorator_name,
                '_original': func_name
            }
        else:
            state.functions[new_name] = {
                'params': [],
                'body': wrapped_body,
                '_decorated_by': decorator_name,
                '_original': func_name
            }
        
        return cursor - index
    
    @staticmethod
    def _create_wrapped_function(state: InterpreterState, decorator: DecoratorDefinition,
                                 original_func: Any, func_name: str,
                                 decorator_args: List[str]) -> List[str]:
        """
        Create the body of a decorated function.
        
        This replaces references to the decorator's func parameter with actual calls
        to the original function.
        """
        wrapped_body = []
        func_param = decorator.params[0]  # First param is the decorated function
        
        for token in decorator.body:
            if token == func_param:
                # Replace with call to original function
                wrapped_body.append("call")
                wrapped_body.append(func_name)
            elif token.startswith(f"{func_param}."):
                # Handle func.property access if needed
                wrapped_body.append(token.replace(f"{func_param}.", f"{func_name}."))
            else:
                wrapped_body.append(token)
        
        return wrapped_body
    
    @staticmethod
    def handle_at_decorator(state: InterpreterState, tokens: List[str], index: int) -> tuple:
        """
        Handle @decorator syntax before a function definition.
        Returns (decorator_name, decorator_args, consumed_count)
        
        @<name> [args...]
        """
        if index >= len(tokens):
            return None, [], 0
        
        token = tokens[index]
        if not token.startswith("@"):
            return None, [], 0
        
        decorator_name = token[1:]  # Remove @ prefix
        cursor = index + 1
        
        # Collect arguments until we hit def/fn/class
        decorator_args = []
        while cursor < len(tokens) and tokens[cursor] not in {"def", "fn", "class"}:
            decorator_args.append(tokens[cursor])
            cursor += 1
        
        return decorator_name, decorator_args, cursor - index
    
    @staticmethod
    def apply_decorator_to_function(state: InterpreterState, decorator_name: str,
                                   decorator_args: List[str], func_name: str,
                                   execute_block: Callable) -> bool:
        """
        Apply a decorator to a newly defined function.
        Modifies the function in place.
        """
        if not hasattr(state, 'decorators') or state.decorators is None:
            state.decorators = {}
        
        decorator = state.decorators.get(decorator_name)
        if decorator is None:
            state.add_error(f"Decorator '@{decorator_name}' is not defined")
            return False
        
        if func_name not in state.functions:
            state.add_error(f"Function '{func_name}' is not defined")
            return False
        
        original_func = state.functions[func_name]
        
        # Create wrapped body
        wrapped_body = DecoratorOpsHandler._create_wrapped_function(
            state, decorator, original_func, func_name, decorator_args
        )
        
        # Update function in place
        if isinstance(original_func, dict):
            original_func['body'] = wrapped_body
            original_func['_decorated_by'] = decorator_name
        else:
            state.functions[func_name] = {
                'params': [],
                'body': wrapped_body,
                '_decorated_by': decorator_name
            }
        
        return True


# Built-in decorators

def register_builtin_decorators(state: InterpreterState) -> None:
    """Register built-in decorators like @log, @time, @memoize."""
    if not hasattr(state, 'decorators') or state.decorators is None:
        state.decorators = {}
    
    # @log - logs function calls
    state.decorators['log'] = DecoratorDefinition(
        'log',
        ['func'],
        ['print', '"[LOG] Calling function"', 'func', 'print', '"[LOG] Function complete"']
    )
    
    # @time - times function execution
    state.decorators['time'] = DecoratorDefinition(
        'time',
        ['func'],
        ['sys_time', 'start', 'func', 'sys_time', 'end_time', 
         'set', 'elapsed', 'end_time', 'sub', 'elapsed', 'start',
         'print', '"Elapsed time:"', 'print', 'elapsed']
    )
