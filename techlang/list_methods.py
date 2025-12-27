"""
List Methods as Commands for TechLang.

Provides list/array operations:
- array_insert <arr> <idx> <val> - Insert at index
- array_extend <target> <source> - Extend with another array
- array_clear <arr> - Clear all elements
- array_copy <src> <dest> - Shallow copy
- array_count <arr> <val> <result> - Count occurrences
- array_remove <arr> <val> - Remove first occurrence
- array_len <arr> <result> - Get length
- array_index <arr> <val> <result> - Find index (-1 if not found)
"""

from typing import Dict, List, Optional, Any
from .core import InterpreterState


class ListMethodsHandler:
    """Handles list/array method operations in TechLang."""
    
    @staticmethod
    def _resolve_value(state: InterpreterState, token: str) -> Any:
        """Resolve a token to its actual value."""
        # Quoted string
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        
        # Check variables first
        if state.has_variable(token):
            return state.get_variable(token)
        
        # Check strings
        if token in state.strings:
            return state.strings[token]
        
        # Try as integer
        try:
            return int(token)
        except ValueError:
            pass
        
        # Try as float
        try:
            return float(token)
        except ValueError:
            pass
        
        # Return 0 as default
        return 0
    
    @staticmethod
    def _resolve_target_name(state: InterpreterState, token: str) -> str:
        """Resolve target variable name, handling -> prefix."""
        if token.startswith("->"):
            return token[2:]
        return token
    
    @staticmethod
    def handle_array_insert(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Insert element at specific index, like Python's list.insert().
        Syntax: array_insert <array> <index> <value>
        """
        if index + 3 >= len(tokens):
            state.add_error("array_insert requires array, index, and value. Use: array_insert <arr> <idx> <val>")
            return 0
        
        arr_name = tokens[index + 1]
        idx_token = tokens[index + 2]
        val_token = tokens[index + 3]
        
        if arr_name not in state.arrays:
            state.add_error(f"Array '{arr_name}' does not exist")
            return 0
        
        # Resolve index
        try:
            idx = int(idx_token)
        except ValueError:
            idx = state.get_variable(idx_token, None)
            if not isinstance(idx, int):
                state.add_error(f"array_insert index must be integer, got '{idx_token}'")
                return 0
        
        # Resolve value
        value = ListMethodsHandler._resolve_value(state, val_token)
        
        # Insert
        state.arrays[arr_name].insert(idx, value)
        return 3
    
    @staticmethod
    def handle_array_extend(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Extend array with another array, like Python's list.extend().
        Syntax: array_extend <target_array> <source_array>
        """
        if index + 2 >= len(tokens):
            state.add_error("array_extend requires target and source. Use: array_extend <target> <source>")
            return 0
        
        target_name = tokens[index + 1]
        source_name = tokens[index + 2]
        
        if target_name not in state.arrays:
            state.add_error(f"Target array '{target_name}' does not exist")
            return 0
        
        if source_name not in state.arrays:
            state.add_error(f"Source array '{source_name}' does not exist")
            return 0
        
        state.arrays[target_name].extend(state.arrays[source_name])
        return 2
    
    @staticmethod
    def handle_array_clear(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Clear all elements from array, like Python's list.clear().
        Syntax: array_clear <array>
        """
        if index + 1 >= len(tokens):
            state.add_error("array_clear requires array name. Use: array_clear <arr>")
            return 0
        
        arr_name = tokens[index + 1]
        
        if arr_name not in state.arrays:
            state.add_error(f"Array '{arr_name}' does not exist")
            return 0
        
        state.arrays[arr_name].clear()
        return 1
    
    @staticmethod
    def handle_array_copy(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create a shallow copy of array, like Python's list.copy().
        Syntax: array_copy <source> <target>
        """
        if index + 2 >= len(tokens):
            state.add_error("array_copy requires source and target. Use: array_copy <src> <dest>")
            return 0
        
        source_name = tokens[index + 1]
        target_name = ListMethodsHandler._resolve_target_name(state, tokens[index + 2])
        
        if source_name not in state.arrays:
            state.add_error(f"Source array '{source_name}' does not exist")
            return 0
        
        state.arrays[target_name] = list(state.arrays[source_name])
        return 2
    
    @staticmethod
    def handle_array_count(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Count occurrences of value in array, like Python's list.count().
        Syntax: array_count <array> <value> <result>
        """
        if index + 3 >= len(tokens):
            state.add_error("array_count requires array, value, and result. Use: array_count <arr> <val> <result>")
            return 0
        
        arr_name = tokens[index + 1]
        val_token = tokens[index + 2]
        result_name = ListMethodsHandler._resolve_target_name(state, tokens[index + 3])
        
        if arr_name not in state.arrays:
            state.add_error(f"Array '{arr_name}' does not exist")
            return 0
        
        value = ListMethodsHandler._resolve_value(state, val_token)
        count = state.arrays[arr_name].count(value)
        state.set_variable(result_name, count)
        return 3
    
    @staticmethod
    def handle_array_remove(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Remove first occurrence of value from array, like Python's list.remove().
        Syntax: array_remove <array> <value>
        """
        if index + 2 >= len(tokens):
            state.add_error("array_remove requires array and value. Use: array_remove <arr> <val>")
            return 0
        
        arr_name = tokens[index + 1]
        val_token = tokens[index + 2]
        
        if arr_name not in state.arrays:
            state.add_error(f"Array '{arr_name}' does not exist")
            return 0
        
        value = ListMethodsHandler._resolve_value(state, val_token)
        
        try:
            state.arrays[arr_name].remove(value)
        except ValueError:
            state.add_error(f"Value {value} not found in array '{arr_name}'")
        
        return 2
    
    @staticmethod
    def handle_array_len(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get length of array, like Python's len().
        Syntax: array_len <array> <result>
        """
        if index + 2 >= len(tokens):
            state.add_error("array_len requires array and result. Use: array_len <arr> <result>")
            return 0
        
        arr_name = tokens[index + 1]
        result_name = ListMethodsHandler._resolve_target_name(state, tokens[index + 2])
        
        if arr_name not in state.arrays:
            state.add_error(f"Array '{arr_name}' does not exist")
            return 0
        
        length = len(state.arrays[arr_name])
        state.set_variable(result_name, length)
        return 2
    
    @staticmethod
    def handle_array_index(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Find index of value in array, like Python's list.index().
        Syntax: array_index <array> <value> <result>
        Returns -1 if not found.
        """
        if index + 3 >= len(tokens):
            state.add_error("array_index requires array, value, and result. Use: array_index <arr> <val> <result>")
            return 0
        
        arr_name = tokens[index + 1]
        val_token = tokens[index + 2]
        result_name = ListMethodsHandler._resolve_target_name(state, tokens[index + 3])
        
        if arr_name not in state.arrays:
            state.add_error(f"Array '{arr_name}' does not exist")
            return 0
        
        value = ListMethodsHandler._resolve_value(state, val_token)
        
        try:
            idx = state.arrays[arr_name].index(value)
        except ValueError:
            idx = -1
        
        state.set_variable(result_name, idx)
        return 3
