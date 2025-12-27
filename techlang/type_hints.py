"""
Static Typing / Type Hints

Provides optional type annotations for function parameters and return values,
with optional runtime type checking like Python's type hints.

Commands:
- typed_def <name> <params:types> -> <return_type> do ... end
- typecheck <on|off> - Enable/disable runtime type checking
- type_assert <value> <type> - Assert that value matches type at runtime
"""

from typing import List, Dict, Optional, Any
from .core import InterpreterState


class TypeHintsHandler:
    """Handler for type hints and type checking commands."""
    
    # Valid type names
    VALID_TYPES = {"int", "str", "float", "bool", "array", "dict", "any", "none"}
    
    @staticmethod
    def handle_typed_def(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Define a function with type hints.
        
        Syntax: typed_def <name> <param:type>... -> <return_type> do ... end
        
        Example:
            typed_def add a:int b:int -> int do
                set result a
                add result b
                return result
            end
        """
        if index + 1 >= len(tokens):
            state.add_error("typed_def requires a function name")
            return 0
        
        func_name = tokens[index + 1]
        
        # Parse parameters with types and find the -> and do
        cursor = index + 2
        params = []
        param_types = {}
        return_type = "any"
        
        while cursor < len(tokens):
            token = tokens[cursor]
            
            if token == "->":
                # Next token is return type
                if cursor + 1 < len(tokens):
                    return_type = tokens[cursor + 1].lower()
                    cursor += 2
                else:
                    state.add_error("Expected return type after '->'")
                    return 0
            elif token == "do":
                cursor += 1
                break
            else:
                # Parse param:type or just param
                if ":" in token:
                    parts = token.split(":", 1)
                    param_name = parts[0]
                    param_type = parts[1].lower() if len(parts) > 1 else "any"
                    params.append(param_name)
                    param_types[param_name] = param_type
                else:
                    params.append(token)
                    param_types[token] = "any"
                cursor += 1
        
        # Find the end of the function body
        depth = 1
        body_start = cursor
        while cursor < len(tokens) and depth > 0:
            t = tokens[cursor]
            if t in {"if", "loop", "while", "def", "typed_def", "match", "switch", "try", "class", "for"}:
                depth += 1
            elif t == "end":
                depth -= 1
            cursor += 1
        
        body_end = cursor - 1  # Before final 'end'
        body = tokens[body_start:body_end]
        
        # Store the function with type information
        state.functions[func_name] = {
            "params": params,
            "body": body,
            "param_types": param_types,
            "return_type": return_type,
            "typed": True
        }
        
        return cursor - index - 1
    
    @staticmethod
    def handle_typecheck(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Enable or disable runtime type checking.
        
        Syntax: typecheck <on|off>
        
        When enabled, typed functions will check argument and return types at runtime.
        
        Example:
            typecheck on
            # Now typed functions will raise errors for type mismatches
        """
        if index + 1 >= len(tokens):
            state.add_error("typecheck requires: typecheck <on|off>")
            return 0
        
        mode = tokens[index + 1].lower()
        
        if mode == "on":
            state.typecheck_enabled = True
            state.add_output("[Type checking enabled]")
        elif mode == "off":
            state.typecheck_enabled = False
            state.add_output("[Type checking disabled]")
        else:
            state.add_error(f"Invalid typecheck mode '{mode}'. Use: on or off")
            return 0
        
        return 1
    
    @staticmethod
    def handle_type_assert(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Assert that a value matches the expected type.
        
        Syntax: type_assert <value_or_var> <expected_type>
        
        Raises an error if the value does not match the expected type.
        
        Example:
            set x 42
            type_assert x int    # Passes
            type_assert x str    # Raises error
        """
        if index + 2 >= len(tokens):
            state.add_error("type_assert requires: type_assert <value> <type>")
            return 0
        
        value_token = tokens[index + 1]
        expected_type = tokens[index + 2].lower()
        
        # Get the actual value
        actual_value, actual_type = TypeHintsHandler._resolve_value_and_type(state, value_token)
        
        # Check type
        if not TypeHintsHandler._type_matches(actual_value, actual_type, expected_type):
            state.add_error(f"Type assertion failed: expected {expected_type}, got {actual_type}")
            return 0
        
        return 2
    
    @staticmethod
    def handle_type_of(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get the type of a value/variable.
        
        Syntax: type_of <value> <result>
        
        Stores the type name (int, str, array, dict, etc.) in result variable.
        
        Example:
            set x 42
            type_of x t
            print t  # Outputs: int
        """
        if index + 2 >= len(tokens):
            state.add_error("type_of requires: type_of <value> <result>")
            return 0
        
        value_token = tokens[index + 1]
        result_name = tokens[index + 2]
        
        _, type_name = TypeHintsHandler._resolve_value_and_type(state, value_token)
        state.strings[result_name] = type_name
        
        return 2
    
    @staticmethod
    def _resolve_value_and_type(state: InterpreterState, token: str) -> tuple:
        """Resolve a token to its value and type name."""
        # Check arrays
        if token in state.arrays:
            return state.arrays[token], "array"
        
        # Check dictionaries
        if token in state.dictionaries:
            return state.dictionaries[token], "dict"
        
        # Check sets
        if hasattr(state, 'sets') and token in state.sets:
            return state.sets[token], "set"
        
        # Check strings
        if token in state.strings:
            return state.strings[token], "str"
        
        # Check variables
        if token in state.variables:
            val = state.variables[token]
            if isinstance(val, bool):
                return val, "bool"
            elif isinstance(val, int):
                return val, "int"
            elif isinstance(val, float):
                return val, "float"
            return val, "any"
        
        # Check class instances
        if hasattr(state, 'instances') and token in state.instances:
            return state.instances[token], state.instances[token].class_name
        
        # Check dataclass instances
        if hasattr(state, 'dataclass_instances') and token in state.dataclass_instances:
            return state.dataclass_instances[token], state.dataclass_instances[token].class_name
        
        # Literal string
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1], "str"
        
        # Literal number
        try:
            if "." in token:
                return float(token), "float"
            return int(token), "int"
        except ValueError:
            pass
        
        return None, "none"
    
    @staticmethod
    def _type_matches(value: Any, actual_type: str, expected_type: str) -> bool:
        """Check if actual type matches expected type."""
        if expected_type == "any":
            return True
        if expected_type == "none":
            return value is None
        if expected_type == "int" and actual_type == "int":
            return True
        if expected_type == "float" and actual_type in ("int", "float"):
            return True
        if expected_type == "str" and actual_type == "str":
            return True
        if expected_type == "bool" and actual_type == "bool":
            return True
        if expected_type == "array" and actual_type == "array":
            return True
        if expected_type == "dict" and actual_type == "dict":
            return True
        if expected_type == "set" and actual_type == "set":
            return True
        # Custom class types
        if expected_type == actual_type:
            return True
        return False
