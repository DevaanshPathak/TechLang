import json
from typing import List, Dict, Union, Optional
from .core import InterpreterState
from .system_ops import ProcessOpsHandler


class DataTypesHandler:
    """
    Handles advanced data types in TechLang.
    This class manages arrays (lists), strings (text), and dictionaries (key-value pairs).
    Think of it as the toolbox for working with complex data structures.
    """
    @staticmethod
    def _resolve_int_token(state: InterpreterState, token: str, description: str) -> Optional[int]:
        try:
            return int(token)
        except ValueError:
            if state.has_variable(token):
                value = state.get_variable(token)
                if isinstance(value, (int, float)):
                    return int(value)
                if isinstance(value, str):
                    try:
                        return int(value)
                    except ValueError:
                        state.add_error(f"{description} must be numeric; variable '{token}' is not numeric")
                        return None
                state.add_error(f"{description} must be numeric; variable '{token}' is not numeric")
                return None
            if token in state.strings:
                try:
                    return int(state.strings[token])
                except ValueError:
                    state.add_error(f"{description} must be numeric; string '{token}' is not numeric")
                    return None
            state.add_error(f"{description} must be numeric; got '{token}'")
            return None

    @staticmethod
    def _resolve_value_token(state: InterpreterState, token: str) -> Union[int, str]:
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        if token in state.strings:
            return state.strings[token]
        if state.has_variable(token):
            return state.get_variable(token)
        try:
            return int(token)
        except ValueError:
            return token

    @staticmethod
    def _resolve_string_token(state: InterpreterState, token: str, description: str) -> Optional[str]:
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        if token in state.strings:
            return state.strings[token]
        if state.has_variable(token):
            value = state.get_variable(token)
            if isinstance(value, str):
                return value
            state.add_error(f"{description} must be a string; variable '{token}' is not a string")
            return None
        return token

    @staticmethod
    def _format_descriptor(name: str, argument: Optional[str]) -> str:
        return name if argument is None else f"{name} {argument}"
    
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
        
        if array_name not in state.arrays and not ProcessOpsHandler.hydrate_stream_array(state, array_name):
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
    def handle_array_map(state: InterpreterState, tokens: List[str], index: int) -> int:
        """Apply a simple transformation to every element in an array."""
        if index + 3 >= len(tokens):
            state.add_error("array_map requires source, target, and operation. Use: array_map <source> <target> <op> [value]")
            return 0

        source_name = tokens[index + 1]
        target_name = tokens[index + 2]
        operation = tokens[index + 3]

        if source_name not in state.arrays:
            state.add_error(f"Array '{source_name}' does not exist")
            return 0

        source_values = list(state.arrays[source_name])
        op_requires_arg = {"add", "mul"}
        arg_token: Optional[str] = None
        consumed = 3

        if operation in op_requires_arg:
            if index + 4 >= len(tokens):
                state.add_error(f"array_map {operation} requires a value. Use: array_map <source> <target> {operation} <number|var>")
                return 0
            arg_token = tokens[index + 4]
            consumed = 4

        result: List[Union[int, str]] = []

        def ensure_numeric(value: Union[int, str], idx: int) -> Optional[int]:
            if isinstance(value, int):
                return value
            state.add_error(f"array_map {operation} requires numeric elements; index {idx} in '{source_name}' is not numeric")
            return None

        numeric_arg: Optional[int] = None
        if arg_token is not None:
            numeric_arg = DataTypesHandler._resolve_int_token(state, arg_token, f"array_map {operation} value")
            if numeric_arg is None:
                return 0

        for idx, value in enumerate(source_values):
            if operation == "identity":
                result.append(value)
            elif operation == "negate":
                numeric_value = ensure_numeric(value, idx)
                if numeric_value is None:
                    return 0
                result.append(-numeric_value)
            elif operation == "double":
                numeric_value = ensure_numeric(value, idx)
                if numeric_value is None:
                    return 0
                result.append(numeric_value * 2)
            elif operation == "square":
                numeric_value = ensure_numeric(value, idx)
                if numeric_value is None:
                    return 0
                result.append(numeric_value * numeric_value)
            elif operation == "abs":
                numeric_value = ensure_numeric(value, idx)
                if numeric_value is None:
                    return 0
                result.append(abs(numeric_value))
            elif operation == "add":
                numeric_value = ensure_numeric(value, idx)
                if numeric_value is None or numeric_arg is None:
                    return 0
                result.append(numeric_value + numeric_arg)
            elif operation == "mul":
                numeric_value = ensure_numeric(value, idx)
                if numeric_value is None or numeric_arg is None:
                    return 0
                result.append(numeric_value * numeric_arg)
            else:
                state.add_error("Unknown array_map operation. Supported: identity, add, mul, negate, double, square, abs")
                return 0

        state.arrays[target_name] = result
        descriptor = DataTypesHandler._format_descriptor(operation, arg_token)
        state.add_output(f"Mapped array '{source_name}' into '{target_name}' with op {descriptor} (items: {len(result)})")
        return consumed

    @staticmethod
    def handle_array_filter(state: InterpreterState, tokens: List[str], index: int) -> int:
        """Filter array elements into a new array based on simple predicates."""
        if index + 3 >= len(tokens):
            state.add_error("array_filter requires source, target, and predicate. Use: array_filter <source> <target> <predicate> [value]")
            return 0

        source_name = tokens[index + 1]
        target_name = tokens[index + 2]
        predicate = tokens[index + 3]

        if source_name not in state.arrays:
            state.add_error(f"Array '{source_name}' does not exist")
            return 0

        predicates_with_value = {"gt", "ge", "lt", "le", "eq", "ne", "contains"}
        value_token: Optional[str] = None
        consumed = 3

        if predicate in predicates_with_value:
            if index + 4 >= len(tokens):
                state.add_error(f"array_filter {predicate} requires a value. Use: array_filter <source> <target> {predicate} <value>")
                return 0
            value_token = tokens[index + 4]
            consumed = 4

        source_values = list(state.arrays[source_name])
        result: List[Union[int, str]] = []

        numeric_predicates = {"even", "odd", "positive", "negative", "nonzero", "gt", "ge", "lt", "le"}
        comparator_value: Optional[int] = None
        comparison_target: Optional[Union[int, str]] = None
        contains_term: Optional[str] = None

        if predicate in {"gt", "ge", "lt", "le"}:
            comparator_value = DataTypesHandler._resolve_int_token(state, value_token or "", f"array_filter {predicate} value")
            if comparator_value is None:
                return 0
        elif predicate in {"eq", "ne"}:
            comparison_target = DataTypesHandler._resolve_value_token(state, value_token or "")
        elif predicate == "contains":
            contains_term = DataTypesHandler._resolve_string_token(state, value_token or "", "array_filter contains value")
            if contains_term is None:
                return 0

        for idx, value in enumerate(source_values):
            if predicate in numeric_predicates:
                if not isinstance(value, int):
                    state.add_error(f"array_filter {predicate} requires numeric elements; index {idx} in '{source_name}' is not numeric")
                    return 0

            match = False
            if predicate == "even":
                match = value % 2 == 0  # type: ignore[arg-type]
            elif predicate == "odd":
                match = value % 2 != 0  # type: ignore[arg-type]
            elif predicate == "positive":
                match = value > 0  # type: ignore[arg-type]
            elif predicate == "negative":
                match = value < 0  # type: ignore[arg-type]
            elif predicate == "nonzero":
                match = value != 0  # type: ignore[arg-type]
            elif predicate == "gt":
                match = value > comparator_value  # type: ignore[operator]
            elif predicate == "ge":
                match = value >= comparator_value  # type: ignore[operator]
            elif predicate == "lt":
                match = value < comparator_value  # type: ignore[operator]
            elif predicate == "le":
                match = value <= comparator_value  # type: ignore[operator]
            elif predicate == "eq":
                match = value == comparison_target
            elif predicate == "ne":
                match = value != comparison_target
            elif predicate == "contains":
                match = contains_term in str(value)
            else:
                state.add_error("Unknown array_filter predicate. Supported: even, odd, positive, negative, nonzero, gt, ge, lt, le, eq, ne, contains")
                return 0

            if match:
                result.append(value)

        state.arrays[target_name] = result
        descriptor = DataTypesHandler._format_descriptor(predicate, value_token)
        state.add_output(
            f"Filtered array '{source_name}' into '{target_name}' with predicate {descriptor} (kept {len(result)}/{len(source_values)})"
        )
        return consumed
    
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
    def handle_str_split(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Split a string into an array using a delimiter.
        Like cutting a sentence into words.
        Example: str_split mystring " " myarray splits mystring by spaces into myarray.
        """
        if index + 3 >= len(tokens):
            state.add_error("str_split requires string name, delimiter, and target array name. Use: str_split <string> <delimiter> <array>")
            return 0
        
        string_name = tokens[index + 1]
        delimiter = tokens[index + 2]
        array_name = tokens[index + 3]
        
        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0
        
        # Remove quotes from delimiter if present
        if delimiter.startswith('"') and delimiter.endswith('"'):
            delimiter = delimiter[1:-1]
        
        # Perform the split
        parts = state.strings[string_name].split(delimiter)
        state.arrays[array_name] = parts
        state.add_output(f"String split into {len(parts)} parts")
        return 3  # Consume string name, delimiter, and array name
    
    @staticmethod
    def handle_str_replace(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Replace all occurrences of a substring with another.
        Like using find-and-replace in a text editor.
        Example: str_replace mystring "old" "new" replaces all "old" with "new" in mystring.
        """
        if index + 3 >= len(tokens):
            state.add_error("str_replace requires string name, old value, and new value. Use: str_replace <string> <old> <new>")
            return 0
        
        string_name = tokens[index + 1]
        old_value = tokens[index + 2]
        new_value = tokens[index + 3]
        
        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0
        
        # Remove quotes if present
        if old_value.startswith('"') and old_value.endswith('"'):
            old_value = old_value[1:-1]
        if new_value.startswith('"') and new_value.endswith('"'):
            new_value = new_value[1:-1]
        
        # Perform the replacement
        state.strings[string_name] = state.strings[string_name].replace(old_value, new_value)
        return 3  # Consume string name, old value, and new value
    
    @staticmethod
    def handle_str_trim(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Remove whitespace from both ends of a string.
        Like trimming the edges of a piece of paper.
        Example: str_trim mystring removes leading and trailing spaces from mystring.
        """
        if index + 1 >= len(tokens):
            state.add_error("str_trim requires string name. Use: str_trim <string>")
            return 0
        
        string_name = tokens[index + 1]
        
        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0
        
        state.strings[string_name] = state.strings[string_name].strip()
        return 1  # Consume string name
    
    @staticmethod
    def handle_str_upper(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Convert a string to uppercase.
        Like turning all letters into capital letters.
        Example: str_upper mystring converts mystring to all uppercase.
        """
        if index + 1 >= len(tokens):
            state.add_error("str_upper requires string name. Use: str_upper <string>")
            return 0
        
        string_name = tokens[index + 1]
        
        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0
        
        state.strings[string_name] = state.strings[string_name].upper()
        return 1  # Consume string name
    
    @staticmethod
    def handle_str_lower(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Convert a string to lowercase.
        Like turning all letters into small letters.
        Example: str_lower mystring converts mystring to all lowercase.
        """
        if index + 1 >= len(tokens):
            state.add_error("str_lower requires string name. Use: str_lower <string>")
            return 0
        
        string_name = tokens[index + 1]
        
        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0
        
        state.strings[string_name] = state.strings[string_name].lower()
        return 1  # Consume string name
    
    @staticmethod
    def handle_str_contains(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if a string contains a substring.
        Like checking if a sentence includes a specific word.
        Example: str_contains mystring "hello" prints 1 if "hello" is in mystring, 0 otherwise.
        """
        if index + 2 >= len(tokens):
            state.add_error("str_contains requires string name and substring. Use: str_contains <string> <substring>")
            return 0
        
        string_name = tokens[index + 1]
        substring = tokens[index + 2]
        
        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0
        
        # Remove quotes from substring if present
        if substring.startswith('"') and substring.endswith('"'):
            substring = substring[1:-1]
        
        result = 1 if substring in state.strings[string_name] else 0
        state.add_output(str(result))
        return 2  # Consume string name and substring
    
    @staticmethod
    def handle_str_reverse(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Reverse the characters in a string.
        Like reading text backwards.
        Example: str_reverse mystring reverses the order of characters in mystring.
        """
        if index + 1 >= len(tokens):
            state.add_error("str_reverse requires string name. Use: str_reverse <string>")
            return 0
        
        string_name = tokens[index + 1]
        
        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0
        
        state.strings[string_name] = state.strings[string_name][::-1]
        return 1  # Consume string name
    
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
        
        keys = sorted(state.dictionaries[dict_name].keys())
        if not keys:
            state.add_output("Keys[0]: (empty)")
        else:
            state.add_output(f"Keys[{len(keys)}]: {', '.join(keys)}")
        return 1  # Consume dictionary name
    
    @staticmethod
    def handle_json_parse(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Parse a JSON string into a TechLang data structure.
        Converts JSON objects to dictionaries and JSON arrays to arrays.
        Example: json_parse jsonString result
        """
        if index + 2 >= len(tokens):
            state.add_error("json_parse requires source string and target name. Use: json_parse <source> <target>")
            return 0
        
        source_name = tokens[index + 1]
        target_name = tokens[index + 2]
        
        # Get the JSON string
        json_str = None
        if source_name in state.strings:
            json_str = state.strings[source_name]
        elif source_name.startswith('"') and source_name.endswith('"'):
            json_str = source_name[1:-1]
        else:
            state.add_error(f"Source '{source_name}' is not a valid string")
            return 0
        
        # Parse the JSON
        try:
            parsed = json.loads(json_str)
            
            # Store based on type
            # NOTE: Check bool before int/float since bool is a subclass of int in Python
            if isinstance(parsed, bool):
                state.variables[target_name] = 1 if parsed else 0
                state.add_output(f"Parsed JSON boolean into variable '{target_name}'")
            elif isinstance(parsed, dict):
                state.dictionaries[target_name] = parsed
                state.add_output(f"Parsed JSON object into dictionary '{target_name}'")
            elif isinstance(parsed, list):
                state.arrays[target_name] = parsed
                state.add_output(f"Parsed JSON array into array '{target_name}'")
            elif isinstance(parsed, str):
                state.strings[target_name] = parsed
                state.add_output(f"Parsed JSON string into string '{target_name}'")
            elif isinstance(parsed, (int, float)):
                state.variables[target_name] = parsed
                state.add_output(f"Parsed JSON number into variable '{target_name}'")
            elif parsed is None:
                state.variables[target_name] = 0
                state.add_output(f"Parsed JSON null into variable '{target_name}' (0)")
            else:
                state.add_error(f"Unsupported JSON type: {type(parsed).__name__}")
                return 0
            
            return 2  # Consume source and target
            
        except json.JSONDecodeError as e:
            state.add_error(f"Invalid JSON: {str(e)}")
            return 0
    
    @staticmethod
    def handle_json_stringify(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Convert a TechLang data structure to a JSON string.
        Works with dictionaries, arrays, strings, and numbers.
        Example: json_stringify myDict jsonString
        """
        if index + 2 >= len(tokens):
            state.add_error("json_stringify requires source name and target string. Use: json_stringify <source> <target>")
            return 0
        
        source_name = tokens[index + 1]
        target_name = tokens[index + 2]
        
        # Determine what to stringify
        obj = None
        if source_name in state.dictionaries:
            obj = state.dictionaries[source_name]
        elif source_name in state.arrays:
            obj = state.arrays[source_name]
        elif source_name in state.strings:
            obj = state.strings[source_name]
        elif state.has_variable(source_name):
            obj = state.get_variable(source_name)
        else:
            state.add_error(f"Source '{source_name}' does not exist")
            return 0
        
        # Convert to JSON
        try:
            json_str = json.dumps(obj, ensure_ascii=False, separators=(',', ':'))
            state.strings[target_name] = json_str
            state.add_output(f"Stringified to JSON in '{target_name}'")
            return 2  # Consume source and target
            
        except (TypeError, ValueError) as e:
            state.add_error(f"Cannot stringify to JSON: {str(e)}")
            return 0
    
    @staticmethod
    def handle_json_read(state: InterpreterState, tokens: List[str], index: int, base_dir: str = None) -> int:
        """
        Read JSON from a file and parse it into a TechLang data structure.
        Example: json_read "data.json" myDict
        """
        if index + 2 >= len(tokens):
            state.add_error("json_read requires file path and target name. Use: json_read <path> <target>")
            return 0
        
        file_path = tokens[index + 1]
        target_name = tokens[index + 2]
        
        # Remove quotes from path if present
        if file_path.startswith('"') and file_path.endswith('"'):
            file_path = file_path[1:-1]
        
        # Resolve path relative to base_dir
        if base_dir:
            from pathlib import Path
            full_path = Path(base_dir) / file_path
            
            # Security check - prevent path traversal
            try:
                full_path = full_path.resolve()
                base_resolved = Path(base_dir).resolve()
                if not str(full_path).startswith(str(base_resolved)):
                    state.add_error(f"Access denied: path outside base directory")
                    return 0
            except Exception as e:
                state.add_error(f"Invalid path: {str(e)}")
                return 0
        else:
            from pathlib import Path
            full_path = Path(file_path)
        
        # Read and parse the file
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            parsed = json.loads(content)
            
            # Store based on type
            if isinstance(parsed, dict):
                state.dictionaries[target_name] = parsed
                state.add_output(f"Read JSON object from file into dictionary '{target_name}'")
            elif isinstance(parsed, list):
                state.arrays[target_name] = parsed
                state.add_output(f"Read JSON array from file into array '{target_name}'")
            else:
                state.add_error(f"JSON file must contain an object or array at root level")
                return 0
            
            return 2  # Consume path and target
            
        except FileNotFoundError:
            state.add_error(f"File not found: {file_path}")
            return 0
        except json.JSONDecodeError as e:
            state.add_error(f"Invalid JSON in file: {str(e)}")
            return 0
        except Exception as e:
            state.add_error(f"Error reading file: {str(e)}")
            return 0
    
    @staticmethod
    def handle_json_write(state: InterpreterState, tokens: List[str], index: int, base_dir: str = None) -> int:
        """
        Write a data structure to a JSON file.
        Example: json_write myDict "data.json"
        """
        if index + 2 >= len(tokens):
            state.add_error("json_write requires source name and file path. Use: json_write <source> <path>")
            return 0
        
        source_name = tokens[index + 1]
        file_path = tokens[index + 2]
        
        # Get the data to write
        obj = None
        if source_name in state.dictionaries:
            obj = state.dictionaries[source_name]
        elif source_name in state.arrays:
            obj = state.arrays[source_name]
        else:
            state.add_error(f"Source '{source_name}' must be a dictionary or array")
            return 0
        
        # Remove quotes from path if present
        if file_path.startswith('"') and file_path.endswith('"'):
            file_path = file_path[1:-1]
        
        # Resolve path relative to base_dir
        if base_dir:
            from pathlib import Path
            full_path = Path(base_dir) / file_path
            
            # Security check - prevent path traversal
            try:
                full_path = full_path.resolve()
                base_resolved = Path(base_dir).resolve()
                if not str(full_path).startswith(str(base_resolved)):
                    state.add_error(f"Access denied: path outside base directory")
                    return 0
            except Exception as e:
                state.add_error(f"Invalid path: {str(e)}")
                return 0
        else:
            from pathlib import Path
            full_path = Path(file_path)
        
        # Write to file
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(obj, f, ensure_ascii=False, indent=2)
            
            state.add_output(f"Wrote JSON to file: {file_path}")
            return 2  # Consume source and path
            
        except Exception as e:
            state.add_error(f"Error writing file: {str(e)}")
            return 0
