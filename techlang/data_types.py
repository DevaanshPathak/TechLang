import json
from typing import List, Dict, Union, Optional
from .core import InterpreterState
from .system_ops import ProcessOpsHandler
from .basic_commands import BasicCommandHandler


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
    def _resolve_target_name(state: InterpreterState, token: str) -> str:
        # Resolve a token intended to represent a *target name*.
        # STL module functions often pass target names through string parameters.
        if token in state.strings:
            return state.strings[token]
        if state.has_variable(token):
            value = state.get_variable(token, None)
            if isinstance(value, str):
                return value
        return token

    @staticmethod
    def _resolve_existing_name(state: InterpreterState, token: str) -> str:
        # Resolve a token intended to represent an *existing* object name.
        # Only indirect if the resolved value points at an existing container/var.
        if token in state.strings:
            candidate = state.strings[token]
            if (
                candidate in state.dictionaries
                or candidate in state.arrays
                or candidate in state.strings
                or state.has_variable(candidate)
            ):
                return candidate
        if state.has_variable(token):
            value = state.get_variable(token, None)
            if isinstance(value, str):
                candidate = value
                if (
                    candidate in state.dictionaries
                    or candidate in state.arrays
                    or candidate in state.strings
                    or state.has_variable(candidate)
                ):
                    return candidate
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
        if index + 1 >= len(tokens):
            state.add_error("array_create requires array name. Use: array_create <name> [size]")
            return 0

        array_name = DataTypesHandler._resolve_target_name(state, tokens[index + 1])

        # Optional size argument. If omitted (or next token is clearly another command), create a dynamic array.
        size_token: Optional[str] = None
        if index + 2 < len(tokens) and tokens[index + 2] not in BasicCommandHandler.KNOWN_COMMANDS:
            size_token = tokens[index + 2]

        if size_token is None:
            state.arrays[array_name] = []
            state.dynamic_arrays.add(array_name)
            return 1

        size = DataTypesHandler._resolve_int_token(state, size_token, "Array size")
        if size is None:
            return 0
        if size < 0:
            state.add_error("Array size must be non-negative")
            return 0
        state.arrays[array_name] = [0] * size
        state.dynamic_arrays.discard(array_name)
        state.add_output(f"Array '{array_name}' created with size {size}")
        return 2
    
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
        
        array_name = DataTypesHandler._resolve_existing_name(state, tokens[index + 1])
        
        array_index = DataTypesHandler._resolve_int_token(state, tokens[index + 2], "Array index")
        if array_index is None:
            return 0
        
        value = tokens[index + 3]
        
        if array_name not in state.arrays and not ProcessOpsHandler.hydrate_stream_array(state, array_name):
            state.add_error(f"Array '{array_name}' does not exist")
            return 0
        
        if array_index < 0:
            state.add_error(f"Array index {array_index} out of bounds for array '{array_name}'")
            return 0

        # Dynamic arrays grow on demand.
        if array_name in state.dynamic_arrays and array_index >= len(state.arrays[array_name]):
            state.arrays[array_name].extend([0] * (array_index - len(state.arrays[array_name]) + 1))

        if array_index >= len(state.arrays[array_name]):
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
            state.add_error("array_get requires array name and index. Use: array_get <name> <index> [target]")
            return 0

        array_name = DataTypesHandler._resolve_existing_name(state, tokens[index + 1])
        array_index = DataTypesHandler._resolve_int_token(state, tokens[index + 2], "Array index")
        if array_index is None:
            return 0

        target: Optional[str] = None
        if index + 3 < len(tokens) and tokens[index + 3] not in BasicCommandHandler.KNOWN_COMMANDS:
            candidate = tokens[index + 3]
            if not (candidate.startswith('"') and candidate.endswith('"')):
                target = candidate

        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 0

        if array_index < 0:
            state.add_error(f"Array index {array_index} out of bounds for array '{array_name}'")
            return 0

        out_of_bounds = array_index >= len(state.arrays[array_name])
        if out_of_bounds:
            if target is not None and array_name in state.dynamic_arrays:
                # STL-style sentinel for dynamic arrays
                state.variables.pop(target, None)
                state.strings.pop(target, None)
                state.set_variable(target, 0)
                return 3
            state.add_error(f"Array index {array_index} out of bounds for array '{array_name}'")
            return 0

        value = state.arrays[array_name][array_index]

        if target is None:
            state.add_output(str(value))
            return 2

        # Store result in target without producing output
        if isinstance(value, str):
            state.variables.pop(target, None)
            state.strings[target] = value
        else:
            state.strings.pop(target, None)
            state.set_variable(target, int(value))
        return 3
    
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

    # ========== Array Sort/Reverse/Find/Unique Commands ==========

    @staticmethod
    def handle_array_sort(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Sort an array in place.
        Example: array_sort nums — sorts ascending
        Example: array_sort nums asc — sorts ascending
        Example: array_sort nums desc — sorts descending
        """
        if index + 1 >= len(tokens):
            state.add_error("array_sort requires array name. Use: array_sort <name> [asc|desc]")
            return 0
        
        array_name = DataTypesHandler._resolve_existing_name(state, tokens[index + 1])
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 0
        
        # Check for optional direction
        direction = "asc"
        consumed = 1
        if index + 2 < len(tokens) and tokens[index + 2] in ("asc", "desc"):
            direction = tokens[index + 2]
            consumed = 2
        
        arr = state.arrays[array_name]
        
        # Check if array contains mixed types
        has_numbers = any(isinstance(x, (int, float)) for x in arr)
        has_strings = any(isinstance(x, str) for x in arr)
        
        if has_numbers and has_strings:
            state.add_error(f"Cannot sort array '{array_name}' with mixed types (numbers and strings)")
            return 0
        
        try:
            reverse = (direction == "desc")
            state.arrays[array_name] = sorted(arr, reverse=reverse)
            state.add_output(f"Sorted array '{array_name}' ({direction}ending, {len(arr)} items)")
        except TypeError as e:
            state.add_error(f"Cannot sort array '{array_name}': {str(e)}")
            return 0
        
        return consumed

    @staticmethod
    def handle_array_reverse(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Reverse an array in place.
        Example: array_reverse nums
        """
        if index + 1 >= len(tokens):
            state.add_error("array_reverse requires array name. Use: array_reverse <name>")
            return 0
        
        array_name = DataTypesHandler._resolve_existing_name(state, tokens[index + 1])
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 0
        
        state.arrays[array_name] = list(reversed(state.arrays[array_name]))
        state.add_output(f"Reversed array '{array_name}' ({len(state.arrays[array_name])} items)")
        return 1

    @staticmethod
    def handle_array_find(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Find the index of a value in an array.
        Example: array_find nums 42 result — stores index in result (-1 if not found)
        """
        if index + 3 >= len(tokens):
            state.add_error("array_find requires array name, value, and target. Use: array_find <name> <value> <target>")
            return 0
        
        array_name = DataTypesHandler._resolve_existing_name(state, tokens[index + 1])
        search_value = DataTypesHandler._resolve_value_token(state, tokens[index + 2])
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 0
        
        arr = state.arrays[array_name]
        try:
            idx = arr.index(search_value)
        except ValueError:
            idx = -1
        
        state.set_variable(target, idx)
        return 3

    @staticmethod
    def handle_array_unique(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Remove duplicate elements from an array in place, preserving order.
        Example: array_unique nums
        """
        if index + 1 >= len(tokens):
            state.add_error("array_unique requires array name. Use: array_unique <name>")
            return 0
        
        array_name = DataTypesHandler._resolve_existing_name(state, tokens[index + 1])
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 0
        
        arr = state.arrays[array_name]
        original_len = len(arr)
        
        # Preserve order while removing duplicates
        seen = set()
        unique = []
        for item in arr:
            # Handle unhashable types by converting to string for comparison
            key = item if isinstance(item, (int, float, str)) else str(item)
            if key not in seen:
                seen.add(key)
                unique.append(item)
        
        state.arrays[array_name] = unique
        removed = original_len - len(unique)
        state.add_output(f"Removed {removed} duplicate(s) from array '{array_name}' ({len(unique)} items remaining)")
        return 1

    @staticmethod
    def handle_array_join(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Join array elements into a string with a delimiter.
        Example: array_join nums "," result — joins with comma into string 'result'
        """
        if index + 3 >= len(tokens):
            state.add_error("array_join requires array name, delimiter, and target. Use: array_join <name> <delimiter> <target>")
            return 0
        
        array_name = DataTypesHandler._resolve_existing_name(state, tokens[index + 1])
        delimiter = DataTypesHandler._resolve_string_token(state, tokens[index + 2], "delimiter")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 0
        
        if delimiter is None:
            return 0
        
        arr = state.arrays[array_name]
        result = delimiter.join(str(item) for item in arr)
        state.strings[target] = result
        return 3
    
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
            state.add_error("str_length requires string name. Use: str_length <name> [target]")
            return 0

        string_name = tokens[index + 1]

        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0

        target: Optional[str] = None
        if index + 2 < len(tokens) and tokens[index + 2] not in BasicCommandHandler.KNOWN_COMMANDS:
            candidate = tokens[index + 2]
            if not (candidate.startswith('"') and candidate.endswith('"')):
                target = candidate

        length = len(state.strings[string_name])

        if target is None:
            state.add_output(str(length))
            return 1

        state.strings.pop(target, None)
        state.set_variable(target, length)
        return 2
    
    @staticmethod
    def handle_str_substring(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Extract part of a string.
        Like cutting out a piece of text from a sentence.
        Example: str_substring mystring 0 5 gets characters 0 through 4 from mystring.
        """
        if index + 3 >= len(tokens):
            state.add_error("str_substring requires string name, start, and end. Use: str_substring <name> <start> <end> [target]")
            return 0

        string_name = tokens[index + 1]
        start = DataTypesHandler._resolve_int_token(state, tokens[index + 2], "Start position")
        if start is None:
            return 0
        end = DataTypesHandler._resolve_int_token(state, tokens[index + 3], "End position")
        if end is None:
            return 0

        target: Optional[str] = None
        if index + 4 < len(tokens) and tokens[index + 4] not in BasicCommandHandler.KNOWN_COMMANDS:
            candidate = tokens[index + 4]
            if not (candidate.startswith('"') and candidate.endswith('"')):
                target = candidate

        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0

        if start < 0 or end > len(state.strings[string_name]) or start > end:
            state.add_error("Invalid substring range")
            return 0

        substring = state.strings[string_name][start:end]
        if target is None:
            state.add_output(substring)
            return 3

        state.variables.pop(target, None)
        state.strings[target] = substring
        return 4
    
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
            state.add_error("str_contains requires string name and substring. Use: str_contains <string> <substring> [target]")
            return 0
        
        string_name = tokens[index + 1]
        substring_token = tokens[index + 2]
        
        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0
        
        # Resolve substring:
        # - if it's a string variable name, use its content
        # - else if quoted literal, unquote
        # - else treat as literal token
        if substring_token in state.strings:
            substring = state.strings[substring_token]
        elif substring_token.startswith('"') and substring_token.endswith('"'):
            substring = substring_token[1:-1]
        else:
            substring = substring_token
        
        target: Optional[str] = None
        if index + 3 < len(tokens) and tokens[index + 3] not in BasicCommandHandler.KNOWN_COMMANDS:
            candidate = tokens[index + 3]
            if not (candidate.startswith('"') and candidate.endswith('"')):
                target = candidate

        result = 1 if substring in state.strings[string_name] else 0
        if target is None:
            state.add_output(str(result))
            return 2

        state.strings.pop(target, None)
        state.set_variable(target, result)
        return 3
    
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
        target_name = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        # Get the JSON string
        json_str = None
        if source_name in state.strings:
            json_str = state.strings[source_name]
        elif state.has_variable(source_name) and isinstance(state.get_variable(source_name, None), str):
            json_str = state.get_variable(source_name)
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
        
        source_name = DataTypesHandler._resolve_existing_name(state, tokens[index + 1])
        target_name = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
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
        target_name = DataTypesHandler._resolve_target_name(state, tokens[index + 2])

        # Allow path to be provided via a string/variable value.
        file_path = DataTypesHandler._resolve_target_name(state, file_path)
        
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
        
        source_name = DataTypesHandler._resolve_existing_name(state, tokens[index + 1])
        file_path = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
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
    # ========== Type Checking Commands ==========

    @staticmethod
    def handle_type_of(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get the type of a variable/data structure.
        Example: type_of myvar result — stores "number", "string", "array", "dict", or "struct" in result
        """
        if index + 2 >= len(tokens):
            state.add_error("type_of requires name and target. Use: type_of <name> <target>")
            return 0
        
        name = tokens[index + 1]
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        # Check each type in order of specificity
        type_name = "undefined"
        
        # Check structs first (more specific)
        if name in state.structs:
            # Get the struct type name if available
            struct_instance = state.structs[name]
            if isinstance(struct_instance, dict) and 'type' in struct_instance:
                type_name = f"struct:{struct_instance['type']}"
            else:
                type_name = "struct"
        elif name in state.dictionaries:
            type_name = "dict"
        elif name in state.arrays:
            type_name = "array"
        elif name in state.strings:
            type_name = "string"
        elif state.has_variable(name):
            val = state.get_variable(name)
            if isinstance(val, bool):
                type_name = "bool"
            elif isinstance(val, int):
                type_name = "number"
            elif isinstance(val, float):
                type_name = "float"
            elif isinstance(val, str):
                type_name = "string"
            else:
                type_name = "unknown"
        
        # Store result in target string
        state.strings[target] = type_name
        return 2

    @staticmethod
    def handle_is_number(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if a name refers to a numeric variable.
        Example: is_number myvar result — stores 1 or 0 in result
        """
        if index + 2 >= len(tokens):
            state.add_error("is_number requires name and target. Use: is_number <name> <target>")
            return 0
        
        name = tokens[index + 1]
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        result = 0
        if state.has_variable(name):
            val = state.get_variable(name)
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                result = 1
        
        state.set_variable(target, result)
        return 2

    @staticmethod
    def handle_is_string(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if a name refers to a string.
        Example: is_string myvar result — stores 1 or 0 in result
        """
        if index + 2 >= len(tokens):
            state.add_error("is_string requires name and target. Use: is_string <name> <target>")
            return 0
        
        name = tokens[index + 1]
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        result = 1 if name in state.strings else 0
        
        state.set_variable(target, result)
        return 2

    @staticmethod
    def handle_is_array(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if a name refers to an array.
        Example: is_array myvar result — stores 1 or 0 in result
        """
        if index + 2 >= len(tokens):
            state.add_error("is_array requires name and target. Use: is_array <name> <target>")
            return 0
        
        name = tokens[index + 1]
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        result = 1 if name in state.arrays else 0
        
        state.set_variable(target, result)
        return 2

    @staticmethod
    def handle_is_dict(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if a name refers to a dictionary.
        Example: is_dict myvar result — stores 1 or 0 in result
        """
        if index + 2 >= len(tokens):
            state.add_error("is_dict requires name and target. Use: is_dict <name> <target>")
            return 0
        
        name = tokens[index + 1]
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        result = 1 if name in state.dictionaries else 0
        
        state.set_variable(target, result)
        return 2

    @staticmethod
    def handle_is_struct(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if a name refers to a struct instance.
        Example: is_struct myvar result — stores 1 or 0 in result
        """
        if index + 2 >= len(tokens):
            state.add_error("is_struct requires name and target. Use: is_struct <name> <target>")
            return 0
        
        name = tokens[index + 1]
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        result = 1 if name in state.structs else 0
        
        state.set_variable(target, result)
        return 2

    @staticmethod
    def handle_is_set(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if a name refers to a set.
        Example: is_set myvar result — stores 1 or 0 in result
        """
        if index + 2 >= len(tokens):
            state.add_error("is_set requires name and target. Use: is_set <name> <target>")
            return 0
        
        name = tokens[index + 1]
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        result = 1 if name in state.sets else 0
        
        state.set_variable(target, result)
        return 2

    # ========== Generator Commands ==========

    @staticmethod
    def handle_generator_create(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create a generator from an array - iterates through values one at a time.
        Syntax: generator_create <name> <array>
        Like Python's iter(list).
        """
        if index + 2 >= len(tokens):
            state.add_error("generator_create requires name and source array. Use: generator_create <name> <array>")
            return 0
        
        gen_name = tokens[index + 1]
        source = tokens[index + 2]
        
        # Get values from source array
        if source not in state.arrays:
            state.add_error(f"Array '{source}' does not exist")
            return 0
        
        values = list(state.arrays[source])  # Copy values
        state.generators[gen_name] = {
            'values': values,
            'index': 0,
            'exhausted': False
        }
        return 2

    @staticmethod
    def handle_generator_next(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get the next value from a generator.
        Syntax: generator_next <generator> <value_var> <done_var>
        Sets done_var to 1 when generator is exhausted, 0 otherwise.
        Like Python's next().
        """
        if index + 3 >= len(tokens):
            state.add_error("generator_next requires generator, value_var, and done_var. Use: generator_next <gen> <value> <done>")
            return 0
        
        gen_name = tokens[index + 1]
        value_var = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        done_var = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if gen_name not in state.generators:
            state.add_error(f"Generator '{gen_name}' does not exist")
            return 0
        
        gen = state.generators[gen_name]
        
        if gen['exhausted'] or gen['index'] >= len(gen['values']):
            gen['exhausted'] = True
            state.set_variable(done_var, 1)
            state.set_variable(value_var, 0)  # Default value when exhausted
            return 3
        
        # Get next value
        value = gen['values'][gen['index']]
        gen['index'] += 1
        
        # Store value appropriately
        if isinstance(value, str):
            state.strings[value_var] = value
        else:
            state.set_variable(value_var, value)
        
        state.set_variable(done_var, 0)
        return 3

    @staticmethod
    def handle_generator_reset(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Reset a generator to the beginning.
        Syntax: generator_reset <generator>
        """
        if index + 1 >= len(tokens):
            state.add_error("generator_reset requires generator name. Use: generator_reset <gen>")
            return 0
        
        gen_name = tokens[index + 1]
        
        if gen_name not in state.generators:
            state.add_error(f"Generator '{gen_name}' does not exist")
            return 0
        
        state.generators[gen_name]['index'] = 0
        state.generators[gen_name]['exhausted'] = False
        return 1

    @staticmethod
    def handle_generator_to_array(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Collect remaining generator values into an array.
        Syntax: generator_to_array <generator> <array>
        Like Python's list(generator).
        """
        if index + 2 >= len(tokens):
            state.add_error("generator_to_array requires generator and target array. Use: generator_to_array <gen> <array>")
            return 0
        
        gen_name = tokens[index + 1]
        array_name = tokens[index + 2]
        
        if gen_name not in state.generators:
            state.add_error(f"Generator '{gen_name}' does not exist")
            return 0
        
        gen = state.generators[gen_name]
        
        # Collect remaining values
        remaining = gen['values'][gen['index']:]
        state.arrays[array_name] = list(remaining)
        
        # Mark generator as exhausted
        gen['index'] = len(gen['values'])
        gen['exhausted'] = True
        return 2

    @staticmethod
    def handle_generator_from_range(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create a generator from a range - lazily generates values.
        Syntax: generator_from_range <name> <start> <end> [step]
        Like Python's range() as a generator.
        """
        if index + 3 >= len(tokens):
            state.add_error("generator_from_range requires name, start, end. Use: generator_from_range <name> <start> <end> [step]")
            return 0
        
        gen_name = tokens[index + 1]
        
        # Get start and end
        try:
            start = int(tokens[index + 2])
        except ValueError:
            if state.has_variable(tokens[index + 2]):
                start = state.get_variable(tokens[index + 2])
            else:
                state.add_error(f"Invalid start value: {tokens[index + 2]}")
                return 0
        
        try:
            end = int(tokens[index + 3])
        except ValueError:
            if state.has_variable(tokens[index + 3]):
                end = state.get_variable(tokens[index + 3])
            else:
                state.add_error(f"Invalid end value: {tokens[index + 3]}")
                return 0
        
        # Check for optional step
        step = 1
        consumed = 3
        if index + 4 < len(tokens):
            try:
                step = int(tokens[index + 4])
                consumed = 4
            except ValueError:
                if state.has_variable(tokens[index + 4]):
                    step = state.get_variable(tokens[index + 4])
                    consumed = 4
        
        if step == 0:
            state.add_error("Step cannot be 0")
            return 0
        
        # Generate values lazily (but we store them for simplicity)
        values = list(range(start, end, step))
        state.generators[gen_name] = {
            'values': values,
            'index': 0,
            'exhausted': False
        }
        return consumed

    @staticmethod
    def handle_generator_take(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Take N values from a generator into an array.
        Syntax: generator_take <generator> <n> <array>
        Like Python's itertools.islice().
        """
        if index + 3 >= len(tokens):
            state.add_error("generator_take requires generator, count, and array. Use: generator_take <gen> <n> <array>")
            return 0
        
        gen_name = tokens[index + 1]
        
        try:
            n = int(tokens[index + 2])
        except ValueError:
            if state.has_variable(tokens[index + 2]):
                n = state.get_variable(tokens[index + 2])
            else:
                state.add_error(f"Invalid count: {tokens[index + 2]}")
                return 0
        
        array_name = tokens[index + 3]
        
        if gen_name not in state.generators:
            state.add_error(f"Generator '{gen_name}' does not exist")
            return 0
        
        gen = state.generators[gen_name]
        
        # Take up to n values
        result = []
        for _ in range(n):
            if gen['exhausted'] or gen['index'] >= len(gen['values']):
                gen['exhausted'] = True
                break
            result.append(gen['values'][gen['index']])
            gen['index'] += 1
        
        state.arrays[array_name] = result
        return 3

    @staticmethod
    def handle_is_generator(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if a name refers to a generator.
        Example: is_generator mygen result — stores 1 or 0 in result
        """
        if index + 2 >= len(tokens):
            state.add_error("is_generator requires name and target. Use: is_generator <name> <target>")
            return 0
        
        name = tokens[index + 1]
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        result = 1 if name in state.generators else 0
        
        state.set_variable(target, result)
        return 2

    # ========== Regex Commands ==========

    @staticmethod
    def handle_regex_match(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Test if a regex pattern matches a string.
        Example: regex_match "\\d+" text result — stores 1 if matches, 0 otherwise
        """
        import re
        
        if index + 3 >= len(tokens):
            state.add_error("regex_match requires pattern, subject, and target. Use: regex_match <pattern> <subject> <target>")
            return 0
        
        pattern = DataTypesHandler._resolve_string_token(state, tokens[index + 1], "pattern")
        subject = DataTypesHandler._resolve_string_token(state, tokens[index + 2], "subject")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if pattern is None or subject is None:
            return 0
        
        try:
            match = re.search(pattern, subject)
            state.set_variable(target, 1 if match else 0)
        except re.error as e:
            state.add_error(f"Invalid regex pattern: {str(e)}")
            return 0
        
        return 3

    @staticmethod
    def handle_regex_find(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Find all matches of a regex pattern and store in an array.
        Example: regex_find "\\d+" text matches — stores all matches in array 'matches'
        """
        import re
        
        if index + 3 >= len(tokens):
            state.add_error("regex_find requires pattern, subject, and target array. Use: regex_find <pattern> <subject> <array>")
            return 0
        
        pattern = DataTypesHandler._resolve_string_token(state, tokens[index + 1], "pattern")
        subject = DataTypesHandler._resolve_string_token(state, tokens[index + 2], "subject")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if pattern is None or subject is None:
            return 0
        
        try:
            matches = re.findall(pattern, subject)
            state.arrays[target] = list(matches)
            state.add_output(f"Found {len(matches)} match(es)")
        except re.error as e:
            state.add_error(f"Invalid regex pattern: {str(e)}")
            return 0
        
        return 3

    @staticmethod
    def handle_regex_replace(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Replace all matches of a regex pattern with a replacement string.
        Example: regex_replace "\\d+" text "X" result — replaces all digits with X
        """
        import re
        
        if index + 4 >= len(tokens):
            state.add_error("regex_replace requires pattern, subject, replacement, and target. Use: regex_replace <pattern> <subject> <replacement> <target>")
            return 0
        
        pattern = DataTypesHandler._resolve_string_token(state, tokens[index + 1], "pattern")
        subject = DataTypesHandler._resolve_string_token(state, tokens[index + 2], "subject")
        replacement = DataTypesHandler._resolve_string_token(state, tokens[index + 3], "replacement")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 4])
        
        if pattern is None or subject is None or replacement is None:
            return 0
        
        try:
            result = re.sub(pattern, replacement, subject)
            state.strings[target] = result
        except re.error as e:
            state.add_error(f"Invalid regex pattern: {str(e)}")
            return 0
        
        return 4

    @staticmethod
    def handle_regex_split(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Split a string by a regex pattern into an array.
        Example: regex_split "\\s+" text parts — splits by whitespace
        """
        import re
        
        if index + 3 >= len(tokens):
            state.add_error("regex_split requires pattern, subject, and target array. Use: regex_split <pattern> <subject> <array>")
            return 0
        
        pattern = DataTypesHandler._resolve_string_token(state, tokens[index + 1], "pattern")
        subject = DataTypesHandler._resolve_string_token(state, tokens[index + 2], "subject")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if pattern is None or subject is None:
            return 0
        
        try:
            parts = re.split(pattern, subject)
            state.arrays[target] = parts
            state.add_output(f"Split into {len(parts)} part(s)")
        except re.error as e:
            state.add_error(f"Invalid regex pattern: {str(e)}")
            return 0
        
        return 3

    # ========== Crypto/Encoding Commands ==========

    @staticmethod
    def handle_base64_encode(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Encode a string to base64.
        Example: base64_encode text result
        """
        import base64
        
        if index + 2 >= len(tokens):
            state.add_error("base64_encode requires source and target. Use: base64_encode <source> <target>")
            return 0
        
        source = DataTypesHandler._resolve_string_token(state, tokens[index + 1], "source")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        if source is None:
            return 0
        
        encoded = base64.b64encode(source.encode('utf-8')).decode('utf-8')
        state.strings[target] = encoded
        return 2

    @staticmethod
    def handle_base64_decode(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Decode a base64 string.
        Example: base64_decode encoded result
        """
        import base64
        
        if index + 2 >= len(tokens):
            state.add_error("base64_decode requires source and target. Use: base64_decode <source> <target>")
            return 0
        
        source = DataTypesHandler._resolve_string_token(state, tokens[index + 1], "source")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        if source is None:
            return 0
        
        try:
            decoded = base64.b64decode(source.encode('utf-8')).decode('utf-8')
            state.strings[target] = decoded
        except Exception as e:
            state.add_error(f"Invalid base64 string: {str(e)}")
            return 0
        
        return 2

    @staticmethod
    def handle_md5(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Compute MD5 hash of a string.
        Example: md5 text result
        """
        import hashlib
        
        if index + 2 >= len(tokens):
            state.add_error("md5 requires source and target. Use: md5 <source> <target>")
            return 0
        
        source = DataTypesHandler._resolve_string_token(state, tokens[index + 1], "source")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        if source is None:
            return 0
        
        hash_result = hashlib.md5(source.encode('utf-8')).hexdigest()
        state.strings[target] = hash_result
        return 2

    @staticmethod
    def handle_sha256(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Compute SHA256 hash of a string.
        Example: sha256 text result
        """
        import hashlib
        
        if index + 2 >= len(tokens):
            state.add_error("sha256 requires source and target. Use: sha256 <source> <target>")
            return 0
        
        source = DataTypesHandler._resolve_string_token(state, tokens[index + 1], "source")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        if source is None:
            return 0
        
        hash_result = hashlib.sha256(source.encode('utf-8')).hexdigest()
        state.strings[target] = hash_result
        return 2

    @staticmethod
    def handle_sha512(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Compute SHA512 hash of a string.
        Example: sha512 text result
        """
        import hashlib
        
        if index + 2 >= len(tokens):
            state.add_error("sha512 requires source and target. Use: sha512 <source> <target>")
            return 0
        
        source = DataTypesHandler._resolve_string_token(state, tokens[index + 1], "source")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        if source is None:
            return 0
        
        hash_result = hashlib.sha512(source.encode('utf-8')).hexdigest()
        state.strings[target] = hash_result
        return 2

    @staticmethod
    def handle_uuid(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Generate a random UUID.
        Example: uuid result — generates a UUID like "550e8400-e29b-41d4-a716-446655440000"
        """
        import uuid as uuid_module
        
        if index + 1 >= len(tokens):
            state.add_error("uuid requires target. Use: uuid <target>")
            return 0
        
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 1])
        state.strings[target] = str(uuid_module.uuid4())
        return 1

    @staticmethod
    def handle_hex_encode(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Encode a string to hexadecimal.
        Example: hex_encode text result
        """
        if index + 2 >= len(tokens):
            state.add_error("hex_encode requires source and target. Use: hex_encode <source> <target>")
            return 0
        
        source = DataTypesHandler._resolve_string_token(state, tokens[index + 1], "source")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        if source is None:
            return 0
        
        encoded = source.encode('utf-8').hex()
        state.strings[target] = encoded
        return 2

    @staticmethod
    def handle_hex_decode(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Decode a hexadecimal string.
        Example: hex_decode encoded result
        """
        if index + 2 >= len(tokens):
            state.add_error("hex_decode requires source and target. Use: hex_decode <source> <target>")
            return 0
        
        source = DataTypesHandler._resolve_string_token(state, tokens[index + 1], "source")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        if source is None:
            return 0
        
        try:
            decoded = bytes.fromhex(source).decode('utf-8')
            state.strings[target] = decoded
        except Exception as e:
            state.add_error(f"Invalid hex string: {str(e)}")
            return 0
        
        return 2

    # ========== Assert Command ==========

    @staticmethod
    def handle_assert(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Assert that a condition is true, otherwise fail with an error message.
        Example: assert x > 5 "x must be greater than 5"
        Supported operators: ==, !=, <, <=, >, >=, eq, ne, lt, le, gt, ge
        """
        if index + 3 >= len(tokens):
            state.add_error("assert requires variable, operator, value, and optional message. Use: assert <var> <op> <value> [message]")
            return 0
        
        var_name = tokens[index + 1]
        operator = tokens[index + 2]
        compare_token = tokens[index + 3]
        
        # Check for optional message
        message = "Assertion failed"
        consumed = 3
        if index + 4 < len(tokens):
            msg_token = tokens[index + 4]
            if msg_token.startswith('"') and msg_token.endswith('"'):
                message = msg_token[1:-1]
                consumed = 4
            elif msg_token in state.strings:
                message = state.strings[msg_token]
                consumed = 4
        
        # Get the variable value
        var_value = None
        if state.has_variable(var_name):
            var_value = state.get_variable(var_name)
        elif var_name in state.strings:
            var_value = state.strings[var_name]
        else:
            state.add_error(f"assert: variable '{var_name}' is not defined")
            return 0
        
        # Get the comparison value
        compare_value = None
        if compare_token.startswith('"') and compare_token.endswith('"'):
            compare_value = compare_token[1:-1]
        elif state.has_variable(compare_token):
            compare_value = state.get_variable(compare_token)
        elif compare_token in state.strings:
            compare_value = state.strings[compare_token]
        else:
            try:
                compare_value = int(compare_token)
            except ValueError:
                try:
                    compare_value = float(compare_token)
                except ValueError:
                    compare_value = compare_token
        
        # Normalize operator
        op_map = {"eq": "==", "ne": "!=", "lt": "<", "le": "<=", "gt": ">", "ge": ">="}
        operator = op_map.get(operator, operator)
        
        # Perform comparison
        result = False
        try:
            if operator == "==":
                result = var_value == compare_value
            elif operator == "!=":
                result = var_value != compare_value
            elif operator == "<":
                result = var_value < compare_value
            elif operator == "<=":
                result = var_value <= compare_value
            elif operator == ">":
                result = var_value > compare_value
            elif operator == ">=":
                result = var_value >= compare_value
            else:
                state.add_error(f"assert: unknown operator '{operator}'. Use ==, !=, <, <=, >, >=")
                return 0
        except TypeError as e:
            state.add_error(f"assert: cannot compare {type(var_value).__name__} with {type(compare_value).__name__}")
            return 0
        
        if not result:
            state.add_error(f"[AssertionError] {message}: {var_name} ({var_value}) {operator} {compare_value}")
            return 0
        
        return consumed

    # ========== Bitwise Operations ==========

    @staticmethod
    def handle_bit_and(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Bitwise AND of two values.
        Example: bit_and a b result — stores a & b in result
        """
        if index + 3 >= len(tokens):
            state.add_error("bit_and requires two operands and target. Use: bit_and <a> <b> <target>")
            return 0
        
        a = DataTypesHandler._resolve_int_token(state, tokens[index + 1], "first operand")
        b = DataTypesHandler._resolve_int_token(state, tokens[index + 2], "second operand")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if a is None or b is None:
            return 0
        
        state.set_variable(target, a & b)
        return 3

    @staticmethod
    def handle_bit_or(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Bitwise OR of two values.
        Example: bit_or a b result — stores a | b in result
        """
        if index + 3 >= len(tokens):
            state.add_error("bit_or requires two operands and target. Use: bit_or <a> <b> <target>")
            return 0
        
        a = DataTypesHandler._resolve_int_token(state, tokens[index + 1], "first operand")
        b = DataTypesHandler._resolve_int_token(state, tokens[index + 2], "second operand")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if a is None or b is None:
            return 0
        
        state.set_variable(target, a | b)
        return 3

    @staticmethod
    def handle_bit_xor(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Bitwise XOR of two values.
        Example: bit_xor a b result — stores a ^ b in result
        """
        if index + 3 >= len(tokens):
            state.add_error("bit_xor requires two operands and target. Use: bit_xor <a> <b> <target>")
            return 0
        
        a = DataTypesHandler._resolve_int_token(state, tokens[index + 1], "first operand")
        b = DataTypesHandler._resolve_int_token(state, tokens[index + 2], "second operand")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if a is None or b is None:
            return 0
        
        state.set_variable(target, a ^ b)
        return 3

    @staticmethod
    def handle_bit_not(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Bitwise NOT of a value.
        Example: bit_not a result — stores ~a in result
        """
        if index + 2 >= len(tokens):
            state.add_error("bit_not requires operand and target. Use: bit_not <a> <target>")
            return 0
        
        a = DataTypesHandler._resolve_int_token(state, tokens[index + 1], "operand")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        if a is None:
            return 0
        
        state.set_variable(target, ~a)
        return 2

    @staticmethod
    def handle_bit_shift_left(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Bitwise left shift.
        Example: bit_shift_left val n result — stores val << n in result
        """
        if index + 3 >= len(tokens):
            state.add_error("bit_shift_left requires value, shift amount, and target. Use: bit_shift_left <val> <n> <target>")
            return 0
        
        val = DataTypesHandler._resolve_int_token(state, tokens[index + 1], "value")
        n = DataTypesHandler._resolve_int_token(state, tokens[index + 2], "shift amount")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if val is None or n is None:
            return 0
        
        if n < 0:
            state.add_error("bit_shift_left: shift amount must be non-negative")
            return 0
        
        state.set_variable(target, val << n)
        return 3

    @staticmethod
    def handle_bit_shift_right(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Bitwise right shift.
        Example: bit_shift_right val n result — stores val >> n in result
        """
        if index + 3 >= len(tokens):
            state.add_error("bit_shift_right requires value, shift amount, and target. Use: bit_shift_right <val> <n> <target>")
            return 0
        
        val = DataTypesHandler._resolve_int_token(state, tokens[index + 1], "value")
        n = DataTypesHandler._resolve_int_token(state, tokens[index + 2], "shift amount")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if val is None or n is None:
            return 0
        
        if n < 0:
            state.add_error("bit_shift_right: shift amount must be non-negative")
            return 0
        
        state.set_variable(target, val >> n)
        return 3

    # ========== Python-like Array Operations ==========

    @staticmethod
    def handle_array_slice(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Slice an array like Python's list[start:end].
        Example: array_slice nums 1 4 result — copies nums[1:4] into result array
        Supports negative indices like Python.
        """
        if index + 4 >= len(tokens):
            state.add_error("array_slice requires array, start, end, and target. Use: array_slice <array> <start> <end> <target>")
            return 0
        
        array_name = tokens[index + 1]
        start = DataTypesHandler._resolve_int_token(state, tokens[index + 2], "start index")
        end = DataTypesHandler._resolve_int_token(state, tokens[index + 3], "end index")
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 4])
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 0
        
        if start is None or end is None:
            return 0
        
        arr = state.arrays[array_name]
        length = len(arr)
        
        # Handle negative indices like Python
        if start < 0:
            start = max(0, length + start)
        if end < 0:
            end = max(0, length + end)
        
        # Clamp to bounds
        start = min(start, length)
        end = min(end, length)
        
        # Create the slice
        sliced = list(arr[start:end])
        state.arrays[target] = sliced
        return 4

    @staticmethod
    def handle_range(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Generate a range of numbers into an array, like Python's range().
        Syntax:
          range <end> <target>           — creates [0, 1, ..., end-1]
          range <start> <end> <target>   — creates [start, start+1, ..., end-1]
          range <start> <end> <step> <target> — creates [start, start+step, ...]
        """
        if index + 2 >= len(tokens):
            state.add_error("range requires at least end and target. Use: range <end> <target> or range <start> <end> <target>")
            return 0
        
        # Try to parse arguments - could be 2, 3, or 4 args
        first = DataTypesHandler._resolve_int_token(state, tokens[index + 1], "first argument")
        if first is None:
            return 0
        
        # Check if next token is a number or variable (more args) or a name (target)
        second_token = tokens[index + 2]
        second = DataTypesHandler._resolve_int_token(state, second_token, "")
        
        if second is None:
            # Only 2 args: range <end> <target>
            target = DataTypesHandler._resolve_target_name(state, second_token)
            state.arrays[target] = list(range(first))
            return 2
        
        # At least 3 args
        if index + 3 >= len(tokens):
            state.add_error("range requires target array name")
            return 0
        
        third_token = tokens[index + 3]
        third = DataTypesHandler._resolve_int_token(state, third_token, "")
        
        if third is None:
            # 3 args: range <start> <end> <target>
            target = DataTypesHandler._resolve_target_name(state, third_token)
            state.arrays[target] = list(range(first, second))
            return 3
        
        # 4 args: range <start> <end> <step> <target>
        if index + 4 >= len(tokens):
            state.add_error("range requires target array name")
            return 0
        
        target = DataTypesHandler._resolve_target_name(state, tokens[index + 4])
        
        if third == 0:
            state.add_error("range step cannot be zero")
            return 0
        
        state.arrays[target] = list(range(first, second, third))
        return 4

    @staticmethod
    def handle_array_comprehend(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Apply a simple expression to each element, like Python list comprehension.
        Example: array_comprehend source target "x * 2"
        Supported operations: x * n, x + n, x - n, x / n, x // n, x % n, x ** n
        Also supports: -x, abs(x), str(x), int(x), float(x)
        """
        if index + 3 >= len(tokens):
            state.add_error("array_comprehend requires source, target, and expression. Use: array_comprehend <source> <target> \"expr\"")
            return 0
        
        source_name = tokens[index + 1]
        target_name = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        expr_token = tokens[index + 3]
        
        if source_name not in state.arrays:
            state.add_error(f"Array '{source_name}' does not exist")
            return 0
        
        # Parse expression (strip quotes if present)
        expr = expr_token
        if expr.startswith('"') and expr.endswith('"'):
            expr = expr[1:-1]
        
        source = state.arrays[source_name]
        result = []
        
        for x in source:
            try:
                value = DataTypesHandler._evaluate_comprehension_expr(x, expr, state)
                if value is None:
                    return 0
                result.append(value)
            except Exception as e:
                state.add_error(f"array_comprehend error: {e}")
                return 0
        
        state.arrays[target_name] = result
        return 3

    @staticmethod
    def _evaluate_comprehension_expr(x, expr: str, state: InterpreterState):
        """
        Evaluate a simple comprehension expression for a value x.
        Supports: x * n, x + n, x - n, x / n, x // n, x % n, x ** n
        Also: -x, abs(x), str(x), int(x), float(x), x (identity)
        """
        expr = expr.strip()
        
        # Identity
        if expr == "x":
            return x
        
        # Negation
        if expr == "-x":
            return -x
        
        # Built-in functions
        if expr == "abs(x)":
            return abs(x)
        if expr == "str(x)":
            return str(x)
        if expr == "int(x)":
            return int(x)
        if expr == "float(x)":
            return float(x)
        
        # Binary operations: x op n
        import re
        
        # Match patterns like "x * 2", "x + 10", "x ** 2", "x // 3"
        patterns = [
            (r'^x\s*\*\*\s*(.+)$', lambda x, n: x ** n),  # Power (must be before *)
            (r'^x\s*//\s*(.+)$', lambda x, n: x // n),   # Floor div (must be before /)
            (r'^x\s*\*\s*(.+)$', lambda x, n: x * n),    # Multiply
            (r'^x\s*/\s*(.+)$', lambda x, n: x / n),     # Divide
            (r'^x\s*\+\s*(.+)$', lambda x, n: x + n),    # Add
            (r'^x\s*-\s*(.+)$', lambda x, n: x - n),     # Subtract
            (r'^x\s*%\s*(.+)$', lambda x, n: x % n),     # Modulo
        ]
        
        for pattern, op in patterns:
            match = re.match(pattern, expr)
            if match:
                n_str = match.group(1).strip()
                try:
                    # Try to parse as int first, then float
                    try:
                        n = int(n_str)
                    except ValueError:
                        n = float(n_str)
                    return op(x, n)
                except (ValueError, ZeroDivisionError) as e:
                    state.add_error(f"Invalid expression operand '{n_str}': {e}")
                    return None
        
        # Reverse patterns: n op x
        reverse_patterns = [
            (r'^(.+)\s*\*\*\s*x$', lambda n, x: n ** x),
            (r'^(.+)\s*//\s*x$', lambda n, x: n // x),
            (r'^(.+)\s*\*\s*x$', lambda n, x: n * x),
            (r'^(.+)\s*/\s*x$', lambda n, x: n / x),
            (r'^(.+)\s*\+\s*x$', lambda n, x: n + x),
            (r'^(.+)\s*-\s*x$', lambda n, x: n - x),
            (r'^(.+)\s*%\s*x$', lambda n, x: n % x),
        ]
        
        for pattern, op in reverse_patterns:
            match = re.match(pattern, expr)
            if match:
                n_str = match.group(1).strip()
                try:
                    try:
                        n = int(n_str)
                    except ValueError:
                        n = float(n_str)
                    return op(n, x)
                except (ValueError, ZeroDivisionError) as e:
                    state.add_error(f"Invalid expression operand '{n_str}': {e}")
                    return None
        
        state.add_error(f"Unsupported comprehension expression: '{expr}'. Use: x * n, x + n, x - n, x / n, x // n, x % n, x ** n, -x, abs(x), str(x), int(x), float(x)")
        return None

    # ========== Enumerate Command ==========

    @staticmethod
    def handle_enumerate(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create index-value pairs from an array, like Python's enumerate().
        Syntax: enumerate <array> <indices_array> <values_array>
        Example: enumerate items idxs vals — creates parallel arrays of indices and values
        """
        if index + 3 >= len(tokens):
            state.add_error("enumerate requires array, indices target, and values target. Use: enumerate <array> <indices> <values>")
            return 0
        
        array_name = tokens[index + 1]
        indices_target = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        values_target = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 0
        
        arr = state.arrays[array_name]
        
        # Create parallel arrays for indices and values
        state.arrays[indices_target] = list(range(len(arr)))
        state.arrays[values_target] = list(arr)
        
        return 3

    # ========== Zip Arrays Command ==========

    @staticmethod
    def handle_array_zip(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Zip two arrays together like Python's zip().
        Syntax: array_zip <arr1> <arr2> <result1> <result2>
        Creates two result arrays with paired elements (truncates to shorter length).
        
        Alternative: array_zip <arr1> <arr2> <result_pairs>
        Creates array of "a,b" string pairs.
        """
        if index + 3 >= len(tokens):
            state.add_error("array_zip requires at least arr1, arr2, and result. Use: array_zip <arr1> <arr2> <result>")
            return 0
        
        arr1_name = tokens[index + 1]
        arr2_name = tokens[index + 2]
        
        if arr1_name not in state.arrays:
            state.add_error(f"Array '{arr1_name}' does not exist")
            return 0
        if arr2_name not in state.arrays:
            state.add_error(f"Array '{arr2_name}' does not exist")
            return 0
        
        arr1 = state.arrays[arr1_name]
        arr2 = state.arrays[arr2_name]
        min_len = min(len(arr1), len(arr2))
        
        # Check if we have 4 args (two result arrays) or 3 args (single pairs array)
        result1_token = tokens[index + 3]
        
        if index + 4 < len(tokens):
            # Check if 4th token looks like a target name (not a command)
            potential_result2 = tokens[index + 4]
            # Simple heuristic: if it's not a known command and doesn't have special chars
            if (not potential_result2.startswith('"') and 
                potential_result2 not in BasicCommandHandler.KNOWN_COMMANDS):
                # 4 args: two separate result arrays
                result1 = DataTypesHandler._resolve_target_name(state, result1_token)
                result2 = DataTypesHandler._resolve_target_name(state, potential_result2)
                
                state.arrays[result1] = list(arr1[:min_len])
                state.arrays[result2] = list(arr2[:min_len])
                return 4
        
        # 3 args: single array of tuples (stored as nested arrays)
        result = DataTypesHandler._resolve_target_name(state, result1_token)
        pairs = []
        for i in range(min_len):
            # Store each pair as a small array
            pairs.append([arr1[i], arr2[i]])
        state.arrays[result] = pairs
        return 3

    # ========== Lambda/Anonymous Functions ==========

    @staticmethod
    def handle_lambda(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create a named lambda function for use with array operations.
        Syntax: lambda <name> <param> "expression"
        Example: lambda double x "x * 2"
        
        The lambda can then be used with array_apply: array_apply <array> <lambda> <result>
        """
        if index + 3 >= len(tokens):
            state.add_error("lambda requires name, parameter, and expression. Use: lambda <name> <param> \"expr\"")
            return 0
        
        lambda_name = tokens[index + 1]
        param = tokens[index + 2]
        expr_token = tokens[index + 3]
        
        # Parse expression (strip quotes if present)
        expr = expr_token
        if expr.startswith('"') and expr.endswith('"'):
            expr = expr[1:-1]
        
        # Store lambda definition
        if not hasattr(state, 'lambdas'):
            state.lambdas = {}
        
        state.lambdas[lambda_name] = {
            'param': param,
            'expr': expr
        }
        
        return 3

    @staticmethod
    def handle_array_apply(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Apply a lambda function to each element of an array.
        Syntax: array_apply <array> <lambda_name> <result>
        Example: array_apply nums double squared
        """
        if index + 3 >= len(tokens):
            state.add_error("array_apply requires array, lambda name, and result. Use: array_apply <array> <lambda> <result>")
            return 0
        
        array_name = tokens[index + 1]
        lambda_name = tokens[index + 2]
        result_name = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 0
        
        if not hasattr(state, 'lambdas') or lambda_name not in state.lambdas:
            state.add_error(f"Lambda '{lambda_name}' does not exist")
            return 0
        
        lambda_def = state.lambdas[lambda_name]
        expr = lambda_def['expr']
        source = state.arrays[array_name]
        result = []
        
        for x in source:
            try:
                value = DataTypesHandler._evaluate_comprehension_expr(x, expr, state)
                if value is None:
                    return 0
                result.append(value)
            except Exception as e:
                state.add_error(f"array_apply error: {e}")
                return 0
        
        state.arrays[result_name] = result
        return 3

    @staticmethod
    def handle_lambda_call(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Call a lambda function with a single value and store result.
        Syntax: lambda_call <lambda_name> <value> <result_var>
        Example: lambda_call double 5 result — stores 10 in result
        """
        if index + 3 >= len(tokens):
            state.add_error("lambda_call requires lambda name, value, and result variable. Use: lambda_call <lambda> <value> <result>")
            return 0
        
        lambda_name = tokens[index + 1]
        value_token = tokens[index + 2]
        result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if not hasattr(state, 'lambdas') or lambda_name not in state.lambdas:
            state.add_error(f"Lambda '{lambda_name}' does not exist")
            return 0
        
        # Resolve value
        value = DataTypesHandler._resolve_value_token(state, value_token)
        if isinstance(value, str):
            try:
                value = float(value) if '.' in value else int(value)
            except ValueError:
                pass  # Keep as string
        
        lambda_def = state.lambdas[lambda_name]
        expr = lambda_def['expr']
        
        try:
            result = DataTypesHandler._evaluate_comprehension_expr(value, expr, state)
            if result is None:
                return 0
            state.set_variable(result_var, result)
        except Exception as e:
            state.add_error(f"lambda_call error: {e}")
            return 0
        
        return 3

    # ========== Any/All Functions ==========

    @staticmethod
    def handle_any(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if any element in array is truthy (non-zero), like Python's any().
        Syntax: any <array> <result_var>
        Stores 1 if any element is truthy, 0 otherwise.
        """
        if index + 2 >= len(tokens):
            state.add_error("any requires array and result variable. Use: any <array> <result>")
            return 0
        
        array_name = tokens[index + 1]
        result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 0
        
        arr = state.arrays[array_name]
        
        # Check if any element is truthy
        result = 1 if any(bool(x) for x in arr) else 0
        state.set_variable(result_var, result)
        return 2

    @staticmethod
    def handle_all(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if all elements in array are truthy (non-zero), like Python's all().
        Syntax: all <array> <result_var>
        Stores 1 if all elements are truthy, 0 otherwise.
        Empty array returns 1 (like Python).
        """
        if index + 2 >= len(tokens):
            state.add_error("all requires array and result variable. Use: all <array> <result>")
            return 0
        
        array_name = tokens[index + 1]
        result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 0
        
        arr = state.arrays[array_name]
        
        # Check if all elements are truthy (empty array returns True like Python)
        result = 1 if all(bool(x) for x in arr) else 0
        state.set_variable(result_var, result)
        return 2

    # ========== Min/Max with Key ==========

    @staticmethod
    def handle_array_min(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Find minimum value in array, like Python's min().
        Syntax: array_min <array> <result_var>
        Also supports: array_min <array> <key_lambda> <result_var> for custom key function
        """
        if index + 2 >= len(tokens):
            state.add_error("array_min requires array and result variable. Use: array_min <array> <result>")
            return 0
        
        array_name = tokens[index + 1]
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 0
        
        arr = state.arrays[array_name]
        if len(arr) == 0:
            state.add_error("array_min: cannot find min of empty array")
            return 0
        
        # Check if we have a key function (3 args) or just result (2 args)
        second_token = tokens[index + 2]
        
        # Check if second token is a lambda name
        if hasattr(state, 'lambdas') and second_token in state.lambdas:
            if index + 3 >= len(tokens):
                state.add_error("array_min with key requires result variable. Use: array_min <array> <key> <result>")
                return 0
            
            key_lambda = second_token
            result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
            
            # Find min using key function
            lambda_def = state.lambdas[key_lambda]
            expr = lambda_def['expr']
            
            min_val = arr[0]
            min_key = DataTypesHandler._evaluate_comprehension_expr(arr[0], expr, state)
            if min_key is None:
                return 0
            
            for item in arr[1:]:
                key = DataTypesHandler._evaluate_comprehension_expr(item, expr, state)
                if key is None:
                    return 0
                if key < min_key:
                    min_key = key
                    min_val = item
            
            state.set_variable(result_var, min_val)
            return 3
        else:
            # No key function, just find min directly
            result_var = DataTypesHandler._resolve_target_name(state, second_token)
            state.set_variable(result_var, min(arr))
            return 2

    @staticmethod
    def handle_array_max(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Find maximum value in array, like Python's max().
        Syntax: array_max <array> <result_var>
        Also supports: array_max <array> <key_lambda> <result_var> for custom key function
        """
        if index + 2 >= len(tokens):
            state.add_error("array_max requires array and result variable. Use: array_max <array> <result>")
            return 0
        
        array_name = tokens[index + 1]
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 0
        
        arr = state.arrays[array_name]
        if len(arr) == 0:
            state.add_error("array_max: cannot find max of empty array")
            return 0
        
        # Check if we have a key function (3 args) or just result (2 args)
        second_token = tokens[index + 2]
        
        # Check if second token is a lambda name
        if hasattr(state, 'lambdas') and second_token in state.lambdas:
            if index + 3 >= len(tokens):
                state.add_error("array_max with key requires result variable. Use: array_max <array> <key> <result>")
                return 0
            
            key_lambda = second_token
            result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
            
            # Find max using key function
            lambda_def = state.lambdas[key_lambda]
            expr = lambda_def['expr']
            
            max_val = arr[0]
            max_key = DataTypesHandler._evaluate_comprehension_expr(arr[0], expr, state)
            if max_key is None:
                return 0
            
            for item in arr[1:]:
                key = DataTypesHandler._evaluate_comprehension_expr(item, expr, state)
                if key is None:
                    return 0
                if key > max_key:
                    max_key = key
                    max_val = item
            
            state.set_variable(result_var, max_val)
            return 3
        else:
            # No key function, just find max directly
            result_var = DataTypesHandler._resolve_target_name(state, second_token)
            state.set_variable(result_var, max(arr))
            return 2

    # ========== Sorted Copy ==========

    @staticmethod
    def handle_array_sorted(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create a sorted copy of array (non-mutating), like Python's sorted().
        Syntax: array_sorted <array> <result>
        Also supports: array_sorted <array> <result> desc — for descending order
        Also supports: array_sorted <array> <key_lambda> <result> [desc] — with key function
        """
        if index + 2 >= len(tokens):
            state.add_error("array_sorted requires array and result. Use: array_sorted <array> <result>")
            return 0
        
        array_name = tokens[index + 1]
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 0
        
        arr = state.arrays[array_name]
        second_token = tokens[index + 2]
        
        # Check if second token is a lambda name (key function)
        if hasattr(state, 'lambdas') and second_token in state.lambdas:
            if index + 3 >= len(tokens):
                state.add_error("array_sorted with key requires result. Use: array_sorted <array> <key> <result>")
                return 0
            
            key_lambda = second_token
            result_name = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
            
            # Check for desc flag
            reverse = False
            consumed = 3
            if index + 4 < len(tokens) and tokens[index + 4].lower() == "desc":
                reverse = True
                consumed = 4
            
            # Sort using key function
            lambda_def = state.lambdas[key_lambda]
            expr = lambda_def['expr']
            
            def key_func(x):
                return DataTypesHandler._evaluate_comprehension_expr(x, expr, state)
            
            try:
                sorted_arr = sorted(arr, key=key_func, reverse=reverse)
                state.arrays[result_name] = sorted_arr
            except Exception as e:
                state.add_error(f"array_sorted error: {e}")
                return 0
            
            return consumed
        else:
            # No key function
            result_name = DataTypesHandler._resolve_target_name(state, second_token)
            
            # Check for desc flag
            reverse = False
            consumed = 2
            if index + 3 < len(tokens) and tokens[index + 3].lower() == "desc":
                reverse = True
                consumed = 3
            
            try:
                sorted_arr = sorted(arr, reverse=reverse)
                state.arrays[result_name] = sorted_arr
            except TypeError:
                # Mixed types that can't be compared
                state.add_error("array_sorted: cannot compare elements of different types")
                return 0
            
            return consumed

    # ========== String Formatting (str_format) ==========

    @staticmethod
    def handle_str_format(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Format string with placeholders, like Python's str.format() or f-strings.
        Syntax: str_format <result> "template with {} placeholders" arg1 arg2 ...
        Example: str_format msg "Hello, {}! You have {} messages." name count
        Also supports named: str_format msg "Hello, {name}!" name
        """
        if index + 2 >= len(tokens):
            state.add_error("str_format requires result name and template. Use: str_format <result> \"template\" [args...]")
            return 0
        
        result_name = DataTypesHandler._resolve_target_name(state, tokens[index + 1])
        template_token = tokens[index + 2]
        
        # Parse template (strip quotes if present)
        template = template_token
        if template.startswith('"') and template.endswith('"'):
            template = template[1:-1]
        
        # Collect arguments
        args = []
        consumed = 2
        i = index + 3
        
        while i < len(tokens):
            token = tokens[i]
            # Stop if we hit a known command
            if token in BasicCommandHandler.KNOWN_COMMANDS:
                break
            
            # Resolve argument value
            if token.startswith('"') and token.endswith('"'):
                args.append(token[1:-1])
            elif token in state.strings:
                args.append(state.strings[token])
            elif state.has_variable(token):
                args.append(state.get_variable(token))
            else:
                try:
                    args.append(int(token))
                except ValueError:
                    try:
                        args.append(float(token))
                    except ValueError:
                        args.append(token)
            
            consumed += 1
            i += 1
        
        # Format the string
        try:
            # Try positional format first
            result = template.format(*args)
        except (IndexError, KeyError) as e:
            state.add_error(f"str_format error: {e}")
            return 0
        
        state.strings[result_name] = result
        return consumed

    # ========== String Methods ==========

    @staticmethod
    def handle_str_startswith(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if string starts with prefix, like Python's str.startswith().
        Syntax: str_startswith <string> <prefix> <result>
        Stores 1 if true, 0 if false.
        """
        if index + 3 >= len(tokens):
            state.add_error("str_startswith requires string, prefix, and result. Use: str_startswith <string> <prefix> <result>")
            return 0
        
        string_name = tokens[index + 1]
        prefix_token = tokens[index + 2]
        result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0
        
        string = state.strings[string_name]
        prefix = DataTypesHandler._resolve_string_token(state, prefix_token, "prefix")
        if prefix is None:
            return 0
        
        result = 1 if string.startswith(prefix) else 0
        state.set_variable(result_var, result)
        return 3

    @staticmethod
    def handle_str_endswith(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if string ends with suffix, like Python's str.endswith().
        Syntax: str_endswith <string> <suffix> <result>
        Stores 1 if true, 0 if false.
        """
        if index + 3 >= len(tokens):
            state.add_error("str_endswith requires string, suffix, and result. Use: str_endswith <string> <suffix> <result>")
            return 0
        
        string_name = tokens[index + 1]
        suffix_token = tokens[index + 2]
        result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0
        
        string = state.strings[string_name]
        suffix = DataTypesHandler._resolve_string_token(state, suffix_token, "suffix")
        if suffix is None:
            return 0
        
        result = 1 if string.endswith(suffix) else 0
        state.set_variable(result_var, result)
        return 3

    @staticmethod
    def handle_str_count(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Count occurrences of substring, like Python's str.count().
        Syntax: str_count <string> <substring> <result>
        """
        if index + 3 >= len(tokens):
            state.add_error("str_count requires string, substring, and result. Use: str_count <string> <substring> <result>")
            return 0
        
        string_name = tokens[index + 1]
        substr_token = tokens[index + 2]
        result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0
        
        string = state.strings[string_name]
        substr = DataTypesHandler._resolve_string_token(state, substr_token, "substring")
        if substr is None:
            return 0
        
        count = string.count(substr)
        state.set_variable(result_var, count)
        return 3

    @staticmethod
    def handle_str_find(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Find first occurrence of substring, like Python's str.find().
        Syntax: str_find <string> <substring> <result>
        Returns -1 if not found.
        """
        if index + 3 >= len(tokens):
            state.add_error("str_find requires string, substring, and result. Use: str_find <string> <substring> <result>")
            return 0
        
        string_name = tokens[index + 1]
        substr_token = tokens[index + 2]
        result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0
        
        string = state.strings[string_name]
        substr = DataTypesHandler._resolve_string_token(state, substr_token, "substring")
        if substr is None:
            return 0
        
        pos = string.find(substr)
        state.set_variable(result_var, pos)
        return 3

    @staticmethod
    def handle_str_rfind(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Find last occurrence of substring, like Python's str.rfind().
        Syntax: str_rfind <string> <substring> <result>
        Returns -1 if not found.
        """
        if index + 3 >= len(tokens):
            state.add_error("str_rfind requires string, substring, and result. Use: str_rfind <string> <substring> <result>")
            return 0
        
        string_name = tokens[index + 1]
        substr_token = tokens[index + 2]
        result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0
        
        string = state.strings[string_name]
        substr = DataTypesHandler._resolve_string_token(state, substr_token, "substring")
        if substr is None:
            return 0
        
        pos = string.rfind(substr)
        state.set_variable(result_var, pos)
        return 3

    @staticmethod
    def handle_str_isdigit(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if string contains only digits, like Python's str.isdigit().
        Syntax: str_isdigit <string> <result>
        """
        if index + 2 >= len(tokens):
            state.add_error("str_isdigit requires string and result. Use: str_isdigit <string> <result>")
            return 0
        
        string_name = tokens[index + 1]
        result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0
        
        string = state.strings[string_name]
        result = 1 if string.isdigit() else 0
        state.set_variable(result_var, result)
        return 2

    @staticmethod
    def handle_str_isalpha(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if string contains only letters, like Python's str.isalpha().
        Syntax: str_isalpha <string> <result>
        """
        if index + 2 >= len(tokens):
            state.add_error("str_isalpha requires string and result. Use: str_isalpha <string> <result>")
            return 0
        
        string_name = tokens[index + 1]
        result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0
        
        string = state.strings[string_name]
        result = 1 if string.isalpha() else 0
        state.set_variable(result_var, result)
        return 2

    @staticmethod
    def handle_str_isalnum(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if string contains only alphanumeric chars, like Python's str.isalnum().
        Syntax: str_isalnum <string> <result>
        """
        if index + 2 >= len(tokens):
            state.add_error("str_isalnum requires string and result. Use: str_isalnum <string> <result>")
            return 0
        
        string_name = tokens[index + 1]
        result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        if string_name not in state.strings:
            state.add_error(f"String '{string_name}' does not exist")
            return 0
        
        string = state.strings[string_name]
        result = 1 if string.isalnum() else 0
        state.set_variable(result_var, result)
        return 2

    # ========== Dict Methods ==========

    @staticmethod
    def handle_dict_values(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get all values from dictionary as an array, like Python's dict.values().
        Syntax: dict_values <dict> <result_array>
        """
        if index + 2 >= len(tokens):
            state.add_error("dict_values requires dict and result array. Use: dict_values <dict> <result>")
            return 0
        
        dict_name = tokens[index + 1]
        result_name = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        if dict_name not in state.dictionaries:
            state.add_error(f"Dictionary '{dict_name}' does not exist")
            return 0
        
        values = list(state.dictionaries[dict_name].values())
        state.arrays[result_name] = values
        return 2

    @staticmethod
    def handle_dict_items(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get all key-value pairs from dictionary, like Python's dict.items().
        Syntax: dict_items <dict> <keys_array> <values_array>
        Creates two parallel arrays for keys and values.
        """
        if index + 3 >= len(tokens):
            state.add_error("dict_items requires dict, keys array, and values array. Use: dict_items <dict> <keys> <values>")
            return 0
        
        dict_name = tokens[index + 1]
        keys_name = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        values_name = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if dict_name not in state.dictionaries:
            state.add_error(f"Dictionary '{dict_name}' does not exist")
            return 0
        
        d = state.dictionaries[dict_name]
        state.arrays[keys_name] = list(d.keys())
        state.arrays[values_name] = list(d.values())
        return 3

    @staticmethod
    def handle_dict_update(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Update dictionary with another dictionary, like Python's dict.update().
        Syntax: dict_update <target_dict> <source_dict>
        """
        if index + 2 >= len(tokens):
            state.add_error("dict_update requires target and source dicts. Use: dict_update <target> <source>")
            return 0
        
        target_name = tokens[index + 1]
        source_name = tokens[index + 2]
        
        if target_name not in state.dictionaries:
            state.add_error(f"Dictionary '{target_name}' does not exist")
            return 0
        if source_name not in state.dictionaries:
            state.add_error(f"Dictionary '{source_name}' does not exist")
            return 0
        
        state.dictionaries[target_name].update(state.dictionaries[source_name])
        return 2

    @staticmethod
    def handle_dict_pop(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Remove key from dictionary and store its value, like Python's dict.pop().
        Syntax: dict_pop <dict> <key> <result>
        If key doesn't exist, stores empty string and doesn't error.
        """
        if index + 3 >= len(tokens):
            state.add_error("dict_pop requires dict, key, and result. Use: dict_pop <dict> <key> <result>")
            return 0
        
        dict_name = tokens[index + 1]
        key_token = tokens[index + 2]
        result_name = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if dict_name not in state.dictionaries:
            state.add_error(f"Dictionary '{dict_name}' does not exist")
            return 0
        
        key = DataTypesHandler._resolve_string_token(state, key_token, "key")
        if key is None:
            return 0
        
        value = state.dictionaries[dict_name].pop(key, "")
        state.strings[result_name] = str(value)
        return 3

    @staticmethod
    def handle_dict_get_default(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get value from dictionary with default, like Python's dict.get().
        Syntax: dict_get_default <dict> <key> <default> <result>
        """
        if index + 4 >= len(tokens):
            state.add_error("dict_get_default requires dict, key, default, and result. Use: dict_get_default <dict> <key> <default> <result>")
            return 0
        
        dict_name = tokens[index + 1]
        key_token = tokens[index + 2]
        default_token = tokens[index + 3]
        result_name = DataTypesHandler._resolve_target_name(state, tokens[index + 4])
        
        if dict_name not in state.dictionaries:
            state.add_error(f"Dictionary '{dict_name}' does not exist")
            return 0
        
        key = DataTypesHandler._resolve_string_token(state, key_token, "key")
        if key is None:
            return 0
        
        default = DataTypesHandler._resolve_string_token(state, default_token, "default")
        if default is None:
            default = default_token  # Use raw token as default
        
        value = state.dictionaries[dict_name].get(key, default)
        state.strings[result_name] = str(value)
        return 4

    @staticmethod
    def handle_dict_has_key(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if key exists in dictionary, like Python's 'key in dict'.
        Syntax: dict_has_key <dict> <key> <result>
        Stores 1 if key exists, 0 otherwise.
        """
        if index + 3 >= len(tokens):
            state.add_error("dict_has_key requires dict, key, and result. Use: dict_has_key <dict> <key> <result>")
            return 0
        
        dict_name = tokens[index + 1]
        key_token = tokens[index + 2]
        result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if dict_name not in state.dictionaries:
            state.add_error(f"Dictionary '{dict_name}' does not exist")
            return 0
        
        key = DataTypesHandler._resolve_string_token(state, key_token, "key")
        if key is None:
            return 0
        
        result = 1 if key in state.dictionaries[dict_name] else 0
        state.set_variable(result_var, result)
        return 3

    @staticmethod
    def handle_dict_clear(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Remove all items from dictionary, like Python's dict.clear().
        Syntax: dict_clear <dict>
        """
        if index + 1 >= len(tokens):
            state.add_error("dict_clear requires dict name. Use: dict_clear <dict>")
            return 0
        
        dict_name = tokens[index + 1]
        
        if dict_name not in state.dictionaries:
            state.add_error(f"Dictionary '{dict_name}' does not exist")
            return 0
        
        state.dictionaries[dict_name].clear()
        return 1

    @staticmethod
    def handle_dict_len(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get number of items in dictionary, like Python's len(dict).
        Syntax: dict_len <dict> <result>
        """
        if index + 2 >= len(tokens):
            state.add_error("dict_len requires dict and result. Use: dict_len <dict> <result>")
            return 0
        
        dict_name = tokens[index + 1]
        result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        if dict_name not in state.dictionaries:
            state.add_error(f"Dictionary '{dict_name}' does not exist")
            return 0
        
        state.set_variable(result_var, len(state.dictionaries[dict_name]))
        return 2

    # ========== SET OPERATIONS (Python-like) ==========
    
    @staticmethod
    def handle_set_create(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create a new set, like Python's set().
        Syntax: set_create <name>
        """
        if index + 1 >= len(tokens):
            state.add_error("set_create requires a name. Use: set_create <name>")
            return 0
        
        set_name = tokens[index + 1]
        state.sets[set_name] = set()
        state.add_output(f"Set '{set_name}' created")
        return 1

    @staticmethod
    def handle_set_add(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Add an item to a set, like Python's set.add().
        Syntax: set_add <set> <value>
        """
        if index + 2 >= len(tokens):
            state.add_error("set_add requires set and value. Use: set_add <set> <value>")
            return 0
        
        set_name = tokens[index + 1]
        value_token = tokens[index + 2]
        
        if set_name not in state.sets:
            state.add_error(f"Set '{set_name}' does not exist")
            return 0
        
        # Resolve value
        value = DataTypesHandler._resolve_value_token(state, value_token)
        state.sets[set_name].add(value)
        return 2

    @staticmethod
    def handle_set_remove(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Remove an item from a set, like Python's set.remove().
        Syntax: set_remove <set> <value>
        """
        if index + 2 >= len(tokens):
            state.add_error("set_remove requires set and value. Use: set_remove <set> <value>")
            return 0
        
        set_name = tokens[index + 1]
        value_token = tokens[index + 2]
        
        if set_name not in state.sets:
            state.add_error(f"Set '{set_name}' does not exist")
            return 0
        
        value = DataTypesHandler._resolve_value_token(state, value_token)
        state.sets[set_name].discard(value)  # discard doesn't error if not present
        return 2

    @staticmethod
    def handle_set_contains(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if set contains a value, like Python's 'in' operator.
        Syntax: set_contains <set> <value> <result>
        Stores 1 if value in set, 0 otherwise.
        """
        if index + 3 >= len(tokens):
            state.add_error("set_contains requires set, value, and result. Use: set_contains <set> <value> <result>")
            return 0
        
        set_name = tokens[index + 1]
        value_token = tokens[index + 2]
        result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if set_name not in state.sets:
            state.add_error(f"Set '{set_name}' does not exist")
            return 0
        
        value = DataTypesHandler._resolve_value_token(state, value_token)
        result = 1 if value in state.sets[set_name] else 0
        state.set_variable(result_var, result)
        return 3

    @staticmethod
    def handle_set_len(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get number of items in set, like Python's len(set).
        Syntax: set_len <set> <result>
        """
        if index + 2 >= len(tokens):
            state.add_error("set_len requires set and result. Use: set_len <set> <result>")
            return 0
        
        set_name = tokens[index + 1]
        result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        if set_name not in state.sets:
            state.add_error(f"Set '{set_name}' does not exist")
            return 0
        
        state.set_variable(result_var, len(state.sets[set_name]))
        return 2

    @staticmethod
    def handle_set_clear(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Remove all items from set, like Python's set.clear().
        Syntax: set_clear <set>
        """
        if index + 1 >= len(tokens):
            state.add_error("set_clear requires set name. Use: set_clear <set>")
            return 0
        
        set_name = tokens[index + 1]
        
        if set_name not in state.sets:
            state.add_error(f"Set '{set_name}' does not exist")
            return 0
        
        state.sets[set_name].clear()
        return 1

    @staticmethod
    def handle_set_union(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create union of two sets, like Python's set.union().
        Syntax: set_union <set1> <set2> <result>
        """
        if index + 3 >= len(tokens):
            state.add_error("set_union requires set1, set2, and result. Use: set_union <set1> <set2> <result>")
            return 0
        
        set1_name = tokens[index + 1]
        set2_name = tokens[index + 2]
        result_name = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if set1_name not in state.sets:
            state.add_error(f"Set '{set1_name}' does not exist")
            return 0
        if set2_name not in state.sets:
            state.add_error(f"Set '{set2_name}' does not exist")
            return 0
        
        state.sets[result_name] = state.sets[set1_name] | state.sets[set2_name]
        return 3

    @staticmethod
    def handle_set_intersection(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create intersection of two sets, like Python's set.intersection().
        Syntax: set_intersection <set1> <set2> <result>
        """
        if index + 3 >= len(tokens):
            state.add_error("set_intersection requires set1, set2, and result. Use: set_intersection <set1> <set2> <result>")
            return 0
        
        set1_name = tokens[index + 1]
        set2_name = tokens[index + 2]
        result_name = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if set1_name not in state.sets:
            state.add_error(f"Set '{set1_name}' does not exist")
            return 0
        if set2_name not in state.sets:
            state.add_error(f"Set '{set2_name}' does not exist")
            return 0
        
        state.sets[result_name] = state.sets[set1_name] & state.sets[set2_name]
        return 3

    @staticmethod
    def handle_set_difference(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create difference of two sets, like Python's set.difference().
        Syntax: set_difference <set1> <set2> <result>
        """
        if index + 3 >= len(tokens):
            state.add_error("set_difference requires set1, set2, and result. Use: set_difference <set1> <set2> <result>")
            return 0
        
        set1_name = tokens[index + 1]
        set2_name = tokens[index + 2]
        result_name = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if set1_name not in state.sets:
            state.add_error(f"Set '{set1_name}' does not exist")
            return 0
        if set2_name not in state.sets:
            state.add_error(f"Set '{set2_name}' does not exist")
            return 0
        
        state.sets[result_name] = state.sets[set1_name] - state.sets[set2_name]
        return 3

    @staticmethod
    def handle_set_symmetric_difference(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create symmetric difference of two sets, like Python's set.symmetric_difference().
        Syntax: set_symmetric_difference <set1> <set2> <result>
        """
        if index + 3 >= len(tokens):
            state.add_error("set_symmetric_difference requires set1, set2, and result. Use: set_symmetric_difference <set1> <set2> <result>")
            return 0
        
        set1_name = tokens[index + 1]
        set2_name = tokens[index + 2]
        result_name = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if set1_name not in state.sets:
            state.add_error(f"Set '{set1_name}' does not exist")
            return 0
        if set2_name not in state.sets:
            state.add_error(f"Set '{set2_name}' does not exist")
            return 0
        
        state.sets[result_name] = state.sets[set1_name] ^ state.sets[set2_name]
        return 3

    @staticmethod
    def handle_set_issubset(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if set1 is subset of set2, like Python's set.issubset().
        Syntax: set_issubset <set1> <set2> <result>
        Stores 1 if set1 is subset of set2, 0 otherwise.
        """
        if index + 3 >= len(tokens):
            state.add_error("set_issubset requires set1, set2, and result. Use: set_issubset <set1> <set2> <result>")
            return 0
        
        set1_name = tokens[index + 1]
        set2_name = tokens[index + 2]
        result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if set1_name not in state.sets:
            state.add_error(f"Set '{set1_name}' does not exist")
            return 0
        if set2_name not in state.sets:
            state.add_error(f"Set '{set2_name}' does not exist")
            return 0
        
        result = 1 if state.sets[set1_name] <= state.sets[set2_name] else 0
        state.set_variable(result_var, result)
        return 3

    @staticmethod
    def handle_set_issuperset(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if set1 is superset of set2, like Python's set.issuperset().
        Syntax: set_issuperset <set1> <set2> <result>
        Stores 1 if set1 is superset of set2, 0 otherwise.
        """
        if index + 3 >= len(tokens):
            state.add_error("set_issuperset requires set1, set2, and result. Use: set_issuperset <set1> <set2> <result>")
            return 0
        
        set1_name = tokens[index + 1]
        set2_name = tokens[index + 2]
        result_var = DataTypesHandler._resolve_target_name(state, tokens[index + 3])
        
        if set1_name not in state.sets:
            state.add_error(f"Set '{set1_name}' does not exist")
            return 0
        if set2_name not in state.sets:
            state.add_error(f"Set '{set2_name}' does not exist")
            return 0
        
        result = 1 if state.sets[set1_name] >= state.sets[set2_name] else 0
        state.set_variable(result_var, result)
        return 3

    @staticmethod
    def handle_set_to_array(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Convert set to array, like Python's list(set).
        Syntax: set_to_array <set> <result_array>
        """
        if index + 2 >= len(tokens):
            state.add_error("set_to_array requires set and result array. Use: set_to_array <set> <result>")
            return 0
        
        set_name = tokens[index + 1]
        result_name = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        if set_name not in state.sets:
            state.add_error(f"Set '{set_name}' does not exist")
            return 0
        
        state.arrays[result_name] = list(state.sets[set_name])
        return 2

    @staticmethod
    def handle_array_to_set(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Convert array to set (removes duplicates), like Python's set(list).
        Syntax: array_to_set <array> <result_set>
        """
        if index + 2 >= len(tokens):
            state.add_error("array_to_set requires array and result set. Use: array_to_set <array> <result>")
            return 0
        
        array_name = tokens[index + 1]
        result_name = DataTypesHandler._resolve_target_name(state, tokens[index + 2])
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist")
            return 0
        
        # Convert array elements to set (handles mixed types)
        state.sets[result_name] = set(state.arrays[array_name])
        return 2
