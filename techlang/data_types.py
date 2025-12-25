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
