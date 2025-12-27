"""
Multiple Return Values (Tuple Unpacking) for TechLang.

Provides tuple unpacking support with:
- unpack <array> <var1> [var2] ... - Unpack array into variables
- pack <array> <val1> [val2] ... - Pack values into array
- return_multi <val1> [val2] ... - Return multiple values
"""

from typing import Dict, List, Optional, Any
from .core import InterpreterState


class MultiReturnHandler:
    """Handles multiple return value operations in TechLang."""
    
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
    def handle_unpack(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Unpack an array into multiple variables:
        unpack <array> <var1> [var2] [var3] ...
        
        Example:
        array_create result 3
        array_set result 0 10
        array_set result 1 20
        array_set result 2 30
        unpack result a b c
        # a=10, b=20, c=30
        """
        if index + 2 >= len(tokens):
            state.add_error("Invalid 'unpack'. Use: unpack <array> <var1> [var2] ...")
            return 0
        
        array_name = tokens[index + 1]
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist.")
            return 1
        
        arr = state.arrays[array_name]
        cursor = index + 2
        var_index = 0
        
        from .basic_commands import BasicCommandHandler
        
        while cursor < len(tokens):
            token = tokens[cursor]
            if token in BasicCommandHandler.KNOWN_COMMANDS:
                break
            
            # Assign value from array
            if var_index < len(arr):
                value = arr[var_index]
                if isinstance(value, str):
                    state.strings[token] = value
                else:
                    state.variables[token] = value
            else:
                # Not enough values - set to 0/empty
                state.variables[token] = 0
            
            var_index += 1
            cursor += 1
        
        return cursor - index
    
    @staticmethod
    def handle_pack(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Pack multiple values into an array:
        pack <array> <val1> [val2] [val3] ...
        
        Example:
        set x 10
        set y 20
        set z 30
        pack result x y z
        # result = [10, 20, 30]
        """
        if index + 2 >= len(tokens):
            state.add_error("Invalid 'pack'. Use: pack <array> <val1> [val2] ...")
            return 0
        
        array_name = tokens[index + 1]
        cursor = index + 2
        values = []
        
        from .basic_commands import BasicCommandHandler
        
        while cursor < len(tokens):
            token = tokens[cursor]
            if token in BasicCommandHandler.KNOWN_COMMANDS:
                break
            
            value = MultiReturnHandler._resolve_value(state, token)
            values.append(value)
            cursor += 1
        
        state.arrays[array_name] = values
        # Return tokens consumed AFTER 'pack' (executor adds 1 for the command itself)
        return cursor - index - 1
    
    @staticmethod
    def handle_return_multi(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Return multiple values from a function:
        return_multi <val1> [val2] [val3] ...
        
        Example (inside a function):
        return_multi quotient remainder
        
        Called as:
        call divmod 17 5 -> q r
        """
        cursor = index + 1
        
        from .basic_commands import BasicCommandHandler
        
        while cursor < len(tokens):
            token = tokens[cursor]
            if token in BasicCommandHandler.KNOWN_COMMANDS or token == "end":
                break
            
            value = MultiReturnHandler._resolve_value(state, token)
            state.return_values.append(value)
            cursor += 1
        
        state.should_return = True
        # Return tokens consumed AFTER 'return_multi' (executor adds 1 for the command itself)
        return cursor - index - 1
