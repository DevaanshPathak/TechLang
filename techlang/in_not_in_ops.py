"""
in / not in Operators for TechLang.

Provides membership testing with:
- in <value> <container> <result> - Check if value in container
- not_in <value> <container> <result> - Check if value NOT in container
- contains <container> <value> <result> - Alternative (container first)
"""

from typing import Dict, List, Optional, Any
from .core import InterpreterState


class InNotInHandler:
    """Handles in/not in operations in TechLang."""
    
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
    def handle_in(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if a value exists in a container (array, dict, string, set).
        Syntax: in <value> <container> <result>
        
        Examples:
            in 5 myarray found      # found=1 if 5 is in myarray
            in "key" mydict found   # found=1 if "key" is a key in mydict
            in "sub" mystring found # found=1 if "sub" is substring of mystring
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'in' command. Use: in <value> <container> <result>")
            return 0
        
        value_token = tokens[index + 1]
        container_name = tokens[index + 2]
        target = tokens[index + 3]
        
        # Resolve the value to search for
        search_value = InNotInHandler._resolve_value(state, value_token)
        
        result = 0
        
        # Check arrays
        if container_name in state.arrays:
            arr = state.arrays[container_name]
            result = 1 if search_value in arr else 0
        
        # Check dictionaries (check keys)
        elif container_name in state.dictionaries:
            d = state.dictionaries[container_name]
            search_key = str(search_value) if not isinstance(search_value, str) else search_value
            result = 1 if search_key in d else 0
        
        # Check strings (substring search)
        elif container_name in state.strings:
            s = state.strings[container_name]
            search_str = str(search_value) if not isinstance(search_value, str) else search_value
            result = 1 if search_str in s else 0
        
        # Check sets
        elif container_name in state.sets:
            st = state.sets[container_name]
            result = 1 if search_value in st else 0
        
        else:
            state.add_error(f"Container '{container_name}' not found (not an array, dict, string, or set).")
            return 3
        
        state.set_variable(target, result)
        return 3
    
    @staticmethod
    def handle_not_in(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if a value does NOT exist in a container.
        Syntax: not_in <value> <container> <result>
        
        Examples:
            not_in 5 myarray found      # found=1 if 5 is NOT in myarray
            not_in "key" mydict found   # found=1 if "key" is NOT a key in mydict
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'not_in' command. Use: not_in <value> <container> <result>")
            return 0
        
        value_token = tokens[index + 1]
        container_name = tokens[index + 2]
        target = tokens[index + 3]
        
        # Resolve the value to search for
        search_value = InNotInHandler._resolve_value(state, value_token)
        
        result = 1  # Default to "not found"
        
        # Check arrays
        if container_name in state.arrays:
            arr = state.arrays[container_name]
            result = 0 if search_value in arr else 1
        
        # Check dictionaries (check keys)
        elif container_name in state.dictionaries:
            d = state.dictionaries[container_name]
            search_key = str(search_value) if not isinstance(search_value, str) else search_value
            result = 0 if search_key in d else 1
        
        # Check strings (substring search)
        elif container_name in state.strings:
            s = state.strings[container_name]
            search_str = str(search_value) if not isinstance(search_value, str) else search_value
            result = 0 if search_str in s else 1
        
        # Check sets
        elif container_name in state.sets:
            st = state.sets[container_name]
            result = 0 if search_value in st else 1
        
        else:
            state.add_error(f"Container '{container_name}' not found (not an array, dict, string, or set).")
            return 3
        
        state.set_variable(target, result)
        return 3
    
    @staticmethod
    def handle_contains(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Alternative syntax: contains <container> <value> <result>
        (container first, like Python's `value in container` but reads left-to-right)
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'contains' command. Use: contains <container> <value> <result>")
            return 0
        
        container_name = tokens[index + 1]
        value_token = tokens[index + 2]
        target = tokens[index + 3]
        
        # Resolve the value to search for
        search_value = InNotInHandler._resolve_value(state, value_token)
        
        result = 0
        
        # Check arrays
        if container_name in state.arrays:
            arr = state.arrays[container_name]
            result = 1 if search_value in arr else 0
        
        # Check dictionaries (check keys)
        elif container_name in state.dictionaries:
            d = state.dictionaries[container_name]
            search_key = str(search_value) if not isinstance(search_value, str) else search_value
            result = 1 if search_key in d else 0
        
        # Check strings (substring search)
        elif container_name in state.strings:
            s = state.strings[container_name]
            search_str = str(search_value) if not isinstance(search_value, str) else search_value
            result = 1 if search_str in s else 0
        
        # Check sets
        elif container_name in state.sets:
            st = state.sets[container_name]
            result = 1 if search_value in st else 0
        
        else:
            state.add_error(f"Container '{container_name}' not found (not an array, dict, string, or set).")
            return 3
        
        state.set_variable(target, result)
        return 3
