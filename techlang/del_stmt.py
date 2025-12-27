"""
del Statement

Provides deletion of variables, array elements, and dict keys like Python's del.

Commands:
- del <name> - Delete a variable, string, array, dict, or set
- del_array <array> <index> - Delete an element from array by index
- del_dict <dict> <key> - Delete a key from dictionary
"""

from typing import List
from .core import InterpreterState


class DelHandler:
    """Handler for del statement and related deletion commands."""
    
    @staticmethod
    def handle_del(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Delete a variable, string, array, dict, set, or other named entity.
        
        Syntax: del <name>
        
        Removes the named item from the interpreter state.
        Can delete: variables, strings, arrays, dictionaries, sets.
        
        Example:
            set x 10
            del x
            # x no longer exists
        """
        if index + 1 >= len(tokens):
            state.add_error("del requires a name. Use: del <name>")
            return 0
        
        name = tokens[index + 1]
        
        # Remove quotes if present
        if name.startswith('"') and name.endswith('"'):
            name = name[1:-1]
        
        deleted = False
        
        # Try to delete from variables
        if name in state.variables:
            del state.variables[name]
            deleted = True
        
        # Try to delete from strings
        if name in state.strings:
            del state.strings[name]
            deleted = True
        
        # Try to delete from arrays
        if name in state.arrays:
            del state.arrays[name]
            if name in state.dynamic_arrays:
                state.dynamic_arrays.discard(name)
            deleted = True
        
        # Try to delete from dictionaries
        if name in state.dictionaries:
            del state.dictionaries[name]
            deleted = True
        
        # Try to delete from sets
        if name in state.sets:
            del state.sets[name]
            deleted = True
        
        # Try to delete from struct instances
        if name in state.structs:
            del state.structs[name]
            deleted = True
        
        # Try to delete from class instances
        if name in state.instances:
            del state.instances[name]
            deleted = True
        
        # Try to delete from functions
        if name in state.functions:
            del state.functions[name]
            deleted = True
        
        if not deleted:
            state.add_error(f"Cannot delete '{name}': not found")
        
        return 1
    
    @staticmethod
    def handle_del_array(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Delete an element from an array by index.
        
        Syntax: del_array <array> <index>
        
        Removes the element at the specified index. Array is reindexed after deletion.
        
        Example:
            array_create nums
            array_push nums 1
            array_push nums 2
            array_push nums 3
            del_array nums 1
            # nums is now [1, 3]
        """
        if index + 2 >= len(tokens):
            state.add_error("del_array requires array name and index. Use: del_array <array> <index>")
            return 0
        
        array_name = tokens[index + 1]
        index_token = tokens[index + 2]
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 2
        
        # Resolve index
        try:
            if index_token in state.variables:
                arr_index = int(state.variables[index_token])
            else:
                arr_index = int(index_token)
        except ValueError:
            state.add_error(f"Invalid index: '{index_token}'")
            return 2
        
        arr = state.arrays[array_name]
        
        if arr_index < 0 or arr_index >= len(arr):
            state.add_error(f"Index {arr_index} out of range for array '{array_name}' (length {len(arr)})")
            return 2
        
        del arr[arr_index]
        return 2
    
    @staticmethod
    def handle_del_dict(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Delete a key from a dictionary.
        
        Syntax: del_dict <dict> <key>
        
        Removes the key and its associated value from the dictionary.
        
        Example:
            dict_create d
            dict_set d "name" "Alice"
            dict_set d "age" 30
            del_dict d "age"
            # d now only has "name"
        """
        if index + 2 >= len(tokens):
            state.add_error("del_dict requires dict name and key. Use: del_dict <dict> <key>")
            return 0
        
        dict_name = tokens[index + 1]
        key = tokens[index + 2]
        
        if dict_name not in state.dictionaries:
            state.add_error(f"Dictionary '{dict_name}' does not exist")
            return 2
        
        # Remove quotes from key if present
        if key.startswith('"') and key.endswith('"'):
            key = key[1:-1]
        
        d = state.dictionaries[dict_name]
        
        # Try both string and int forms of key
        actual_key = key
        if key not in d:
            try:
                int_key = int(key)
                if int_key in d:
                    actual_key = int_key
                else:
                    state.add_error(f"Key '{key}' not found in dictionary '{dict_name}'")
                    return 2
            except ValueError:
                state.add_error(f"Key '{key}' not found in dictionary '{dict_name}'")
                return 2
        
        del d[actual_key]
        return 2
