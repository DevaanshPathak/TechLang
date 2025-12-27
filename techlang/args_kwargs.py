"""
*args / **kwargs (Variadic Functions) for TechLang.

Provides variadic function support with:
- defv <name> [params...] [*args] [**kwargs] do ... end - Define variadic function
- callv <name> [args...] [key=value ...] [-> returns] - Call variadic function
"""

from typing import Dict, List, Optional, Any, Callable
from .core import InterpreterState
from .blocks import BlockCollector


class VariadicFunction:
    """Represents a variadic function with *args and/or **kwargs."""
    
    def __init__(self, name: str, regular_params: List[str], 
                 has_args: bool, args_name: str,
                 has_kwargs: bool, kwargs_name: str,
                 body: List[str]):
        self.name = name
        self.regular_params = regular_params
        self.has_args = has_args
        self.args_name = args_name
        self.has_kwargs = has_kwargs
        self.kwargs_name = kwargs_name
        self.body = body


class ArgsKwargsHandler:
    """Handles variadic function operations in TechLang."""
    
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
    def handle_defv(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Define a variadic function:
        defv <name> [params...] [*args] [**kwargs] do ... end
        
        Example:
        defv sum_all *nums do
            set total 0
            foreach nums n do
                add total n
            end
            return total
        end
        """
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'defv'. Use: defv <name> [params...] [*args] [**kwargs] do ... end")
            return 0
        
        func_name = tokens[index + 1]
        cursor = index + 2
        
        regular_params = []
        has_args = False
        args_name = "args"
        has_kwargs = False
        kwargs_name = "kwargs"
        
        # Parse parameters
        while cursor < len(tokens) and tokens[cursor] != "do":
            token = tokens[cursor]
            
            if token.startswith("**"):
                # **kwargs
                has_kwargs = True
                kwargs_name = token[2:] if len(token) > 2 else "kwargs"
            elif token.startswith("*"):
                # *args
                has_args = True
                args_name = token[1:] if len(token) > 1 else "args"
            else:
                # Regular parameter
                regular_params.append(token)
            
            cursor += 1
        
        if cursor >= len(tokens) or tokens[cursor] != "do":
            state.add_error("defv requires 'do' keyword.")
            return cursor - index
        
        cursor += 1  # Skip 'do'
        
        # Collect function body
        body, end_index = BlockCollector.collect_block(cursor, tokens)
        
        # Store variadic function
        vfunc = VariadicFunction(
            func_name, regular_params,
            has_args, args_name,
            has_kwargs, kwargs_name,
            body
        )
        
        if state.variadic_functions is None:
            state.variadic_functions = {}
        state.variadic_functions[func_name] = vfunc
        
        # Also store in regular functions with special marker
        state.functions[func_name] = {
            'params': regular_params,
            'body': body,
            'variadic': True,
            'args_name': args_name if has_args else None,
            'kwargs_name': kwargs_name if has_kwargs else None
        }
        
        return end_index - index
    
    @staticmethod
    def handle_callv(state: InterpreterState, tokens: List[str], index: int,
                     execute_block: Callable) -> int:
        """
        Call a variadic function:
        callv <name> [args...] [key=value ...] [-> returns...]
        
        Example:
        callv sum_all 1 2 3 4 5 -> result
        """
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'callv'. Use: callv <name> [args...] [key=value ...]")
            return 0
        
        func_name = tokens[index + 1]
        
        # Find variadic function
        vfunc = None
        if state.variadic_functions and func_name in state.variadic_functions:
            vfunc = state.variadic_functions[func_name]
        
        if vfunc is None:
            state.add_error(f"Variadic function '{func_name}' is not defined. Use 'defv' to define it.")
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
                parts = token.split("=", 1)
                keyword_args[parts[0]] = ArgsKwargsHandler._parse_default(parts[1], state)
            else:
                positional_args.append(ArgsKwargsHandler._resolve_value(state, token))
            
            cursor += 1
        
        consumed = cursor - index
        
        # Bind regular parameters
        saved_vars = {}
        saved_strings = {}
        saved_arrays = {}
        saved_dicts = {}
        
        for i, param in enumerate(vfunc.regular_params):
            if param in state.variables:
                saved_vars[param] = state.variables[param]
            if param in state.strings:
                saved_strings[param] = state.strings[param]
            
            if i < len(positional_args):
                value = positional_args[i]
                if isinstance(value, str):
                    state.strings[param] = value
                else:
                    state.variables[param] = value
        
        # Remaining positional args go to *args
        extra_positional = positional_args[len(vfunc.regular_params):]
        
        if vfunc.has_args:
            args_name = vfunc.args_name
            if args_name in state.arrays:
                saved_arrays[args_name] = state.arrays[args_name].copy()
            state.arrays[args_name] = extra_positional
        
        # Keyword args go to **kwargs
        if vfunc.has_kwargs:
            kwargs_name = vfunc.kwargs_name
            if kwargs_name in state.dictionaries:
                saved_dicts[kwargs_name] = state.dictionaries[kwargs_name].copy()
            state.dictionaries[kwargs_name] = keyword_args
        
        # Execute
        state.return_values.clear()
        state.should_return = False
        execute_block(vfunc.body)
        state.should_return = False
        
        # Restore state
        for param in vfunc.regular_params:
            if param in saved_vars:
                state.variables[param] = saved_vars[param]
            else:
                state.variables.pop(param, None)
            if param in saved_strings:
                state.strings[param] = saved_strings[param]
            else:
                state.strings.pop(param, None)
        
        if vfunc.has_args:
            args_name = vfunc.args_name
            if args_name in saved_arrays:
                state.arrays[args_name] = saved_arrays[args_name]
            else:
                state.arrays.pop(args_name, None)
        
        if vfunc.has_kwargs:
            kwargs_name = vfunc.kwargs_name
            if kwargs_name in saved_dicts:
                state.dictionaries[kwargs_name] = saved_dicts[kwargs_name]
            else:
                state.dictionaries.pop(kwargs_name, None)
        
        # Assign return values
        for i, var_name in enumerate(return_vars):
            if i < len(state.return_values):
                value = state.return_values[i]
                if isinstance(value, str):
                    state.strings[var_name] = value
                else:
                    state.variables[var_name] = value
        
        return consumed
