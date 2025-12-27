"""
Default & Keyword Arguments for TechLang.

Provides default/keyword argument support with:
- defn <name> <param1> [param2=default] ... do ... end - Define function with defaults
- calln <name> [args...] [param=value ...] [-> returns] - Call with keyword args
"""

from typing import Dict, List, Optional, Any, Tuple, Callable
from .core import InterpreterState
from .blocks import BlockCollector


class FunctionWithDefaults:
    """Represents a function definition with default parameter values."""
    
    def __init__(self, name: str, params: List[Tuple[str, Optional[Any]]], body: List[str]):
        """
        params: List of (param_name, default_value) tuples
        default_value is None if no default provided
        """
        self.name = name
        self.params = params  # [(name, default), ...]
        self.body = body
    
    def __repr__(self):
        param_strs = []
        for name, default in self.params:
            if default is not None:
                param_strs.append(f"{name}={default}")
            else:
                param_strs.append(name)
        return f"Function({self.name}({', '.join(param_strs)}))"


class DefaultArgsHandler:
    """Handles default and keyword argument operations in TechLang."""
    
    @staticmethod
    def _resolve_value(state: InterpreterState, token: str) -> Any:
        """Resolve a token to its actual value."""
        # Check if it's a quoted string
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        
        # Check variables
        if token in state.variables:
            return state.variables[token]
        
        # Check strings
        if token in state.strings:
            return state.strings[token]
        
        # Try numeric parsing
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return token
    
    @staticmethod
    def _parse_default(value_str: str, state: InterpreterState = None) -> Any:
        """Parse a default value string."""
        if value_str.startswith('"') and value_str.endswith('"'):
            return value_str[1:-1]
        
        # Check if it's a variable reference
        if state is not None:
            if value_str in state.variables:
                return state.variables[value_str]
            if value_str in state.strings:
                return state.strings[value_str]
        
        # Try numeric parsing
        try:
            return int(value_str)
        except ValueError:
            try:
                return float(value_str)
            except ValueError:
                return value_str
    
    @staticmethod
    def handle_defn(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Define a function with default/keyword arguments:
        defn <name> <param1> [param2=default] ... do ... end
        
        Example:
        defn greet name greeting="Hello" do
            print greeting
            print name
        end
        """
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'defn'. Use: defn <name> [params...] do ... end")
            return 0
        
        func_name = tokens[index + 1]
        cursor = index + 2
        
        # Collect parameters until we hit 'do'
        params: List[Tuple[str, Optional[Any]]] = []
        
        while cursor < len(tokens) and tokens[cursor] != "do":
            token = tokens[cursor]
            
            if "=" in token:
                # Parameter with default value: param=value
                parts = token.split("=", 1)
                param_name = parts[0]
                default_str = parts[1]
                default_value = DefaultArgsHandler._parse_default(default_str, state)
                params.append((param_name, default_value))
            else:
                # Regular parameter (no default)
                params.append((token, None))
            
            cursor += 1
        
        if cursor >= len(tokens) or tokens[cursor] != "do":
            state.add_error("defn requires 'do' keyword. Use: defn <name> [params] do ... end")
            return cursor - index
        
        # Skip 'do'
        cursor += 1
        
        # Collect function body until 'end'
        body_start = cursor
        body, end_index = BlockCollector.collect_block(body_start, tokens)
        
        # Store function with defaults
        func = FunctionWithDefaults(func_name, params, body)
        
        if state.functions_with_defaults is None:
            state.functions_with_defaults = {}
        state.functions_with_defaults[func_name] = func
        
        # Also register in regular functions for compatibility
        state.functions[func_name] = {
            'params': [p[0] for p in params],
            'body': body,
            'defaults': {p[0]: p[1] for p in params if p[1] is not None}
        }
        
        return end_index - index
    
    @staticmethod
    def handle_calln(state: InterpreterState, tokens: List[str], index: int, 
                     execute_block: Callable) -> int:
        """
        Call a function with keyword arguments:
        calln <name> [arg1] [arg2] [param=value ...] [-> ret1 ret2 ...]
        
        Example:
        calln greet "Alice" greeting="Hi"
        """
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'calln'. Use: calln <name> [args...] [param=value ...]")
            return 0
        
        func_name = tokens[index + 1]
        
        # Find function definition
        func_def = None
        if state.functions_with_defaults and func_name in state.functions_with_defaults:
            func_def = state.functions_with_defaults[func_name]
        elif func_name in state.functions:
            # Regular function - wrap it
            old_def = state.functions[func_name]
            if isinstance(old_def, dict):
                params = [(p, old_def.get('defaults', {}).get(p)) for p in old_def.get('params', [])]
                func_def = FunctionWithDefaults(func_name, params, old_def['body'])
            else:
                func_def = FunctionWithDefaults(func_name, [], old_def)
        
        if func_def is None:
            state.add_error(f"Function '{func_name}' is not defined.")
            return 1
        
        # Collect arguments
        cursor = index + 2
        positional_args = []
        keyword_args = {}
        return_vars = []
        collecting_returns = False
        
        from .basic_commands import BasicCommandHandler
        
        while cursor < len(tokens):
            token = tokens[cursor]
            
            if token == "->":
                collecting_returns = True
                cursor += 1
                continue
            
            if collecting_returns:
                if token in BasicCommandHandler.KNOWN_COMMANDS:
                    break
                return_vars.append(token)
                cursor += 1
                continue
            
            if token in BasicCommandHandler.KNOWN_COMMANDS:
                break
            
            if "=" in token and not token.startswith('"'):
                # Keyword argument
                parts = token.split("=", 1)
                keyword_args[parts[0]] = DefaultArgsHandler._parse_default(parts[1], state)
            else:
                # Positional argument
                positional_args.append(token)
            
            cursor += 1
        
        consumed = cursor - index
        
        # Bind arguments to parameters
        param_values = {}
        
        # First, apply defaults
        for param_name, default in func_def.params:
            if default is not None:
                param_values[param_name] = default
        
        # Then apply positional arguments
        for i, (param_name, _) in enumerate(func_def.params):
            if i < len(positional_args):
                param_values[param_name] = DefaultArgsHandler._resolve_value(state, positional_args[i])
        
        # Then apply keyword arguments
        for key, value in keyword_args.items():
            param_values[key] = value
        
        # Check required parameters
        for param_name, default in func_def.params:
            if default is None and param_name not in param_values:
                state.add_error(f"Missing required argument '{param_name}' for function '{func_name}'.")
                return consumed
        
        # Save current state
        saved_vars = {}
        saved_strings = {}
        for param_name in param_values:
            if param_name in state.variables:
                saved_vars[param_name] = state.variables[param_name]
            if param_name in state.strings:
                saved_strings[param_name] = state.strings[param_name]
        
        # Set parameter values
        for param_name, value in param_values.items():
            if isinstance(value, str):
                state.strings[param_name] = value
            else:
                state.variables[param_name] = value
        
        # Clear return values
        state.return_values.clear()
        state.should_return = False
        
        # Execute function body
        execute_block(func_def.body)
        
        state.should_return = False
        
        # Restore state
        for param_name in param_values:
            if param_name in saved_vars:
                state.variables[param_name] = saved_vars[param_name]
            else:
                state.variables.pop(param_name, None)
            if param_name in saved_strings:
                state.strings[param_name] = saved_strings[param_name]
            else:
                state.strings.pop(param_name, None)
        
        # Assign return values
        for i, var_name in enumerate(return_vars):
            if i < len(state.return_values):
                value = state.return_values[i]
                if isinstance(value, str):
                    state.strings[var_name] = value
                else:
                    state.variables[var_name] = value
        
        return consumed
