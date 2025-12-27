"""
Dict Methods
=================================
Additional dictionary methods.

Commands:
- dict_setdefault <dict> <key> <default> - Set if not exists
- dict_copy <dict> <result> - Shallow copy
- dict_fromkeys <keys_array> <value> <result> - Create dict from keys
- dict_merge <dict1> <dict2> <result> - Merge without modifying originals
"""

from typing import List
from techlang.core import InterpreterState


class DictMethodsHandler:
    """Handler for additional dictionary methods."""
    
    @staticmethod
    def handle_dict_setdefault(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Set a dictionary key to a value only if it doesn't already exist.
        Like Python's dict.setdefault().
        
        Syntax: dict_setdefault <dict> <key> <default>
        
        If key exists, does nothing. If key doesn't exist, sets dict[key] = default.
        Returns the current value (either existing or newly set).
        """
        if index + 3 >= len(tokens):
            state.add_error("dict_setdefault requires dict, key, and default. Use: dict_setdefault <dict> <key> <default>")
            return 0
        
        dict_name = tokens[index + 1]
        key_token = tokens[index + 2]
        default_token = tokens[index + 3]
        
        # Check if dictionary exists
        if dict_name not in state.dictionaries:
            state.add_error(f"Dictionary '{dict_name}' not found.")
            return 0
        
        # Resolve key
        if key_token.startswith('"') and key_token.endswith('"'):
            key = key_token[1:-1]
        elif key_token in state.strings:
            key = state.strings[key_token]
        else:
            key = key_token
        
        # Only set if key doesn't exist
        if key not in state.dictionaries[dict_name]:
            # Resolve default value
            if default_token.startswith('"') and default_token.endswith('"'):
                value = default_token[1:-1]
            elif default_token in state.strings:
                value = state.strings[default_token]
            elif default_token in state.variables:
                value = state.variables[default_token]
            else:
                try:
                    value = int(default_token)
                except ValueError:
                    try:
                        value = float(default_token)
                    except ValueError:
                        value = default_token
            
            state.dictionaries[dict_name][key] = value
        
        return 3
    
    @staticmethod
    def handle_dict_copy(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create a shallow copy of a dictionary.
        Like Python's dict.copy().
        
        Syntax: dict_copy <dict> <result>
        """
        if index + 2 >= len(tokens):
            state.add_error("dict_copy requires dict and result. Use: dict_copy <dict> <result>")
            return 0
        
        dict_name = tokens[index + 1]
        result_name = tokens[index + 2]
        
        # Check if source dictionary exists
        if dict_name not in state.dictionaries:
            state.add_error(f"Dictionary '{dict_name}' not found.")
            return 0
        
        # Create shallow copy
        state.dictionaries[result_name] = dict(state.dictionaries[dict_name])
        return 2
    
    @staticmethod
    def handle_dict_fromkeys(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create a new dictionary with keys from an array and a common value.
        Like Python's dict.fromkeys().
        
        Syntax: dict_fromkeys <keys_array> <value> <result>
        """
        if index + 3 >= len(tokens):
            state.add_error("dict_fromkeys requires keys_array, value, and result. Use: dict_fromkeys <keys_array> <value> <result>")
            return 0
        
        keys_array_name = tokens[index + 1]
        value_token = tokens[index + 2]
        result_name = tokens[index + 3]
        
        # Check if source array exists
        if keys_array_name not in state.arrays:
            state.add_error(f"Array '{keys_array_name}' not found.")
            return 0
        
        # Resolve value
        if value_token.startswith('"') and value_token.endswith('"'):
            value = value_token[1:-1]
        elif value_token in state.strings:
            value = state.strings[value_token]
        elif value_token in state.variables:
            value = state.variables[value_token]
        else:
            try:
                value = int(value_token)
            except ValueError:
                try:
                    value = float(value_token)
                except ValueError:
                    value = value_token
        
        # Create dictionary from keys
        keys = state.arrays[keys_array_name]
        state.dictionaries[result_name] = {str(k): value for k in keys}
        return 3
    
    @staticmethod
    def handle_dict_merge(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Merge two dictionaries into a new one (non-mutating).
        Like Python's {**dict1, **dict2}.
        
        Syntax: dict_merge <dict1> <dict2> <result>
        
        Creates a new dictionary with all keys from both.
        If same key exists in both, dict2's value wins.
        """
        if index + 3 >= len(tokens):
            state.add_error("dict_merge requires dict1, dict2, and result. Use: dict_merge <dict1> <dict2> <result>")
            return 0
        
        dict1_name = tokens[index + 1]
        dict2_name = tokens[index + 2]
        result_name = tokens[index + 3]
        
        # Check if both dictionaries exist
        if dict1_name not in state.dictionaries:
            state.add_error(f"Dictionary '{dict1_name}' not found.")
            return 0
        if dict2_name not in state.dictionaries:
            state.add_error(f"Dictionary '{dict2_name}' not found.")
            return 0
        
        # Merge dictionaries (dict2 values override dict1)
        merged = dict(state.dictionaries[dict1_name])
        merged.update(state.dictionaries[dict2_name])
        state.dictionaries[result_name] = merged
        return 3
