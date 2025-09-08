from typing import List, Dict, Union, Optional
from .core import InterpreterState


class DataTypesHandler:
    """
    Handles advanced data types in TechLang.
    This class manages arrays (lists), strings (text), and dictionaries (key-value pairs).
    Think of it as the toolbox for working with complex data structures.
    """
    
    @staticmethod
    def handle_array_create(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create a new array with a specific size.
        Like creating an empty box with a certain number of slots.
        Example: array_create mylist 5 creates an array with 5 empty slots.
        """
        if index + 2 >= len(tokens):
            state.add_error("array_create requires array name and size. Use: array_create <name> <size>")
            return 0
        
        array_name = tokens[index + 1]
        try:
            size = int(tokens[index + 2])
            if size < 0:
                state.add_error("Array size must be non-negative")
                return 0
            # Create an array filled with zeros
            state.arrays[array_name] = [0] * size
            state.add_output(f"Array '{array_name}' created with size {size}")
            return 2  # Tell the interpreter we used 2 tokens
        except ValueError:
            state.add_error(f"Array size must be a number, got '{tokens[index + 2]}'")
            return 0
    
    @staticmethod
    def handle_array_set(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Put a value at a specific position in an array.
        Like putting an item in a specific slot of a box.
        Example: array_set mylist 0 42 puts 42 in the first slot of mylist.
        """
        if index + 3 >= len(tokens):
            state.add_error("array_set requires array name, index, and value. Use: array_set <name> <index> <value>")
            return 0
        
        array_name = tokens[index + 1]
        
        # Try to get array index - could be a number or variable
        try:
            array_index = int(tokens[index + 2])
        except ValueError:
            # Check if it's a variable
            if state.has_variable(tokens[index + 2]):
                array_index = state.get_variable(tokens[index + 2])
                if not isinstance(array_index, int):
                    state.add_error(f"Variable '{tokens[index + 2]}' is not a number. Array index must be a number.")
                    return 0
            else:
                state.add_error(f"Array index must be a number or variable, but got '{tokens[index + 2]}'")
                return 0
        
        value = tokens[index + 3]
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 0
        
        if array_index < 0 or array_index >= len(state.arrays[array_name]):
            state.add_error(f"Array index {array_index} out of bounds for array '{array_name}'")
            return 0
        
        # Try to convert to number, otherwise keep as text
        try:
            value = int(value)
        except ValueError:
            # Check if it's a variable
            if state.has_variable(value):
                value = state.get_variable(value)
                if not isinstance(value, int) and not isinstance(value, str):
                    state.add_error(f"Variable '{value}' has invalid type for array value")
                    return 0
            elif value.startswith('"') and value.endswith('"'):
                # Remove quotes if it's a quoted string
                value = value[1:-1]
        
        state.arrays[array_name][array_index] = value
        return 3  # Tell the interpreter we used 3 tokens
    
    @staticmethod
    def handle_array_get(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get the value at a specific position in an array.
        Like looking at what's in a specific slot of a box.
        Example: array_get mylist 0 gets the value in the first slot of mylist.
        """
        if index + 2 >= len(tokens):
            state.add_error("array_get requires array name and index. Use: array_get <name> <index>")
            return 0
        
        array_name = tokens[index + 1]
        try:
            array_index = int(tokens[index + 2])
            
            if array_name not in state.arrays:
                state.add_error(f"Array '{array_name}' does not exist")
                return 0
            
            if array_index < 0 or array_index >= len(state.arrays[array_name]):
                state.add_error(f"Array index {array_index} out of bounds for array '{array_name}'")
                return 0
            
            value = state.arrays[array_name][array_index]
            state.add_output(str(value))
            return 2  # Consume array name and index
        except ValueError:
            state.add_error("Array index must be a number")
            return 0
    
    @staticmethod
    def handle_array_push(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Add a value to the end of an array.
        Like adding an item to the end of a line.
        Example: array_push mylist 99 adds 99 to the end of mylist.
        """
        if index + 2 >= len(tokens):
            state.add_error("array_push requires array name and value. Use: array_push <name> <value>")
            return 0
        
        array_name = tokens[index + 1]
        value = tokens[index + 2]
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 0
        
        # Try to convert to int, otherwise keep as string
        try:
            value = int(value)
        except ValueError:
            # Remove quotes if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
        
        state.arrays[array_name].append(value)
        return 2  # Consume array name and value
    
    @staticmethod
    def handle_array_pop(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Remove and return the last value from an array.
        Like taking the last item from the end of a line.
        Example: array_pop mylist removes and returns the last item in mylist.
        """
        if index + 1 >= len(tokens):
            state.add_error("array_pop requires array name. Use: array_pop <name>")
            return 0
        
        array_name = tokens[index + 1]
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 0
        
        if not state.arrays[array_name]:
            state.add_error(f"Array '{array_name}' is empty")
            return 0
        
        value = state.arrays[array_name].pop()
        state.add_output(str(value))
        return 1  # Consume array name
    
    @staticmethod
    def handle_str_create(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create a new string variable.
        Like creating a text box to store words.
        Example: str_create mystring "hello" creates a string containing "hello".
        """
        if index + 2 >= len(tokens):
            state.add_error("str_create requires string name and value. Use: str_create <name> <value>")
            return 0
        
        string_name = tokens[index + 1]
        value = tokens[index + 2]
        
        # Remove quotes if present
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        
        state.strings[string_name] = value
        return 2  # Consume string name and value
    
    @staticmethod
    def handle_str_concat(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Add text to the end of an existing string.
        Like adding words to the end of a sentence.
        Example: str_concat mystring " world" adds " world" to the end of mystring.
        """
        if index + 2 >= len(tokens):
            state.add_error("str_concat requires string name and value to append. Use: str_concat <name> <value>")
            return 0
        
        string_name = tokens[index + 1]
        value = tokens[index + 2]
        
        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0
        
        # Check if value is a string variable or a literal
        if value in state.strings:
            # It's a string variable
            value = state.strings[value]
        elif value.startswith('"') and value.endswith('"'):
            # It's a quoted string literal
            value = value[1:-1]
        # Otherwise treat as literal string
        
        state.strings[string_name] += value
        return 2  # Consume string name and value
    
    @staticmethod
    def handle_str_length(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get the number of characters in a string.
        Like counting the letters in a word.
        Example: str_length mystring returns how many characters are in mystring.
        """
        if index + 1 >= len(tokens):
            state.add_error("str_length requires string name. Use: str_length <name>")
            return 0
        
        string_name = tokens[index + 1]
        
        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0
        
        length = len(state.strings[string_name])
        state.add_output(str(length))
        return 1  # Consume string name
    
    @staticmethod
    def handle_str_substring(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Extract part of a string.
        Like cutting out a piece of text from a sentence.
        Example: str_substring mystring 0 5 gets characters 0 through 4 from mystring.
        """
        if index + 3 >= len(tokens):
            state.add_error("str_substring requires string name, start, and end. Use: str_substring <name> <start> <end>")
            return 0
        
        string_name = tokens[index + 1]
        try:
            start = int(tokens[index + 2])
            end = int(tokens[index + 3])
            
            if string_name not in state.strings:
                state.add_error(f"String '{string_name}' does not exist")
                return 0
            
            if start < 0 or end > len(state.strings[string_name]) or start > end:
                state.add_error("Invalid substring range")
                return 0
            
            substring = state.strings[string_name][start:end]
            state.add_output(substring)
            return 3  # Consume string name, start, and end
        except ValueError:
            state.add_error("Start and end positions must be numbers")
            return 0
    
    @staticmethod
    def handle_dict_create(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create a new dictionary.
        Like creating an empty phone book to store names and numbers.
        Example: dict_create mydict creates an empty dictionary called mydict.
        """
        if index + 1 >= len(tokens):
            state.add_error("dict_create requires dictionary name. Use: dict_create <name>")
            return 0
        
        dict_name = tokens[index + 1]
        state.dictionaries[dict_name] = {}
        state.add_output(f"Dictionary '{dict_name}' created")
        return 1  # Consume dictionary name
    
    @staticmethod
    def handle_dict_set(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Store a key-value pair in a dictionary.
        Like writing someone's name and phone number in a phone book.
        Example: dict_set mydict "name" "Alice" stores "Alice" under the key "name".
        """
        if index + 3 >= len(tokens):
            state.add_error("dict_set requires dictionary name, key, and value. Use: dict_set <name> <key> <value>")
            return 0
        
        dict_name = tokens[index + 1]
        key = tokens[index + 2]
        value = tokens[index + 3]
        
        if dict_name not in state.dictionaries:
            state.add_error(f"Dictionary '{dict_name}' does not exist")
            return 0
        
        # Remove quotes from key and value if present
        if key.startswith('"') and key.endswith('"'):
            key = key[1:-1]
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        
        # Try to convert value to int if possible, otherwise keep as string
        try:
            value = int(value)
        except ValueError:
            pass  # Keep as string
        
        state.dictionaries[dict_name][key] = value
        return 3  # Consume dictionary name, key, and value
    
    @staticmethod
    def handle_dict_get(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get a value from a dictionary using its key.
        Like looking up someone's phone number by their name.
        Example: dict_get mydict "name" returns the value stored under "name".
        """
        if index + 2 >= len(tokens):
            state.add_error("dict_get requires dictionary name and key. Use: dict_get <name> <key>")
            return 0
        
        dict_name = tokens[index + 1]
        key = tokens[index + 2]
        
        if dict_name not in state.dictionaries:
            state.add_error(f"Dictionary '{dict_name}' does not exist")
            return 0
        
        # Remove quotes from key if present
        if key.startswith('"') and key.endswith('"'):
            key = key[1:-1]
        
        if key not in state.dictionaries[dict_name]:
            state.add_error(f"Key '{key}' not found in dictionary '{dict_name}'")
            return 0
        
        value = state.dictionaries[dict_name][key]
        state.add_output(str(value))
        return 2  # Consume dictionary name and key
    
    @staticmethod
    def handle_dict_keys(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get all the keys from a dictionary.
        Like getting a list of all the names in a phone book.
        Example: dict_keys mydict returns all the keys stored in mydict.
        """
        if index + 1 >= len(tokens):
            state.add_error("dict_keys requires dictionary name. Use: dict_keys <name>")
            return 0
        
        dict_name = tokens[index + 1]
        
        if dict_name not in state.dictionaries:
            state.add_error(f"Dictionary '{dict_name}' does not exist")
            return 0
        
        keys = list(state.dictionaries[dict_name].keys())
        state.add_output(f"Keys: {', '.join(keys)}")
        return 1  # Consume dictionary name
