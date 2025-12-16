from typing import List, Optional
from string import Formatter
from .core import InterpreterState


class VariableHandler:
    """
    Handles variable operations in TechLang.
    This class manages storing values in variables and doing math with them.
    Think of it as the memory manager for your programs.
    """
    
    @staticmethod
    def handle_set(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 2 >= len(tokens):
            state.add_error("Invalid 'set' command. Use: set <variable_name> <number>")
            return 0
        
        varname = tokens[index + 1]
        value_token = tokens[index + 2]
        
        # Allow quoted string literals (mirrors input behavior, and enables tests for non-numeric vars)
        if value_token.startswith('"') and value_token.endswith('"'):
            state.set_variable(varname, value_token[1:-1])
            return 2

        # Try to resolve value_token as a variable first, then as a literal
        varvalue = state.get_variable(value_token, None)
        if varvalue is None:
            try:
                varvalue = int(value_token)
            except ValueError:
                state.add_error(f"Expected a number or variable for '{varname}', but got '{value_token}'. Please provide a valid integer or variable name.")
                return 0

        if not isinstance(varvalue, int):
            state.add_error(f"Value must be a number, but got type '{type(varvalue).__name__}'.")
            return 0

        state.set_variable(varname, varvalue)
        return 2  # Consume variable name and value
    
    @staticmethod
    def handle_math_operation(state: InterpreterState, tokens: List[str], index: int, operation: str) -> int:
        if index + 2 >= len(tokens):
            state.add_error(f"Invalid '{operation}' command. Use: {operation} <variable_name> <number>")
            return 0
        
        varname = tokens[index + 1]
        amount_token = tokens[index + 2]
        
        # Try to get the amount - could be a number or variable
        try:
            amount = int(amount_token)
        except ValueError:
            # Check if it's a variable
            if state.has_variable(amount_token):
                amount = state.get_variable(amount_token)
                if not isinstance(amount, int):
                    state.add_error(f"Variable '{amount_token}' is not a number. Cannot perform {operation} operation.")
                    return 0
            else:
                state.add_error(f"Expected a number or variable for {operation} operation, but got '{amount_token}'. Please provide a valid integer or variable name.")
                return 0
        
        if not state.has_variable(varname):
            state.add_error(f"Variable '{varname}' is not defined. Use 'set {varname} <value>' to create it first.")
            return 0
        
        current_value = state.get_variable(varname)
        if not isinstance(current_value, int):
            state.add_error(f"Variable '{varname}' is not a number. Cannot perform {operation} operation.")
            return 0
        
        if operation == "add":
            state.set_variable(varname, current_value + amount)
        elif operation == "mul":
            state.set_variable(varname, current_value * amount)
        elif operation == "sub":
            state.set_variable(varname, current_value - amount)
        elif operation == "div":
            if amount == 0:
                # Friendly guardrail for division by zero
                state.add_error("Cannot divide by zero. Please provide a non-zero number.")
                return 0
            state.set_variable(varname, current_value // amount)
        
        return 2  # Consume variable name and amount
    
    @staticmethod
    def handle_input(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'input' command. Use: input <variable_name>")
            return 0
        
        varname = tokens[index + 1]
        
        try:
            if state.has_input():
                value = state.get_input()
            else:
                value = input(f"Enter value for {varname}: ")
            
            state.set_variable(varname, value)
            return 1  # Consume variable name
        except (EOFError, IndexError):
            state.add_error(f"Input failed for variable '{varname}'. Please provide input when prompted.")
            return 0

    @staticmethod
    def _resolve_string_token(state: InterpreterState, token: str, description: str) -> Optional[str]:
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        if token in state.strings:
            return state.strings[token]
        if state.has_variable(token):
            value = state.get_variable(token)
            return value if isinstance(value, str) else str(value)
        state.add_error(f"{description} '{token}' is not defined. Create it first with str_create or set.")
        return None

    @staticmethod
    def handle_string_interpolate(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 2 >= len(tokens):
            state.add_error("string_interpolate requires target and template. Use: string_interpolate <name> <template>")
            return 0

        target = tokens[index + 1]
        template_token = tokens[index + 2]

        template = VariableHandler._resolve_string_token(state, template_token, "Template")
        if template is None:
            return 0

        formatter = Formatter()
        placeholders = set()
        for _, field_name, _, _ in formatter.parse(template):
            if field_name:
                placeholders.add(field_name)

        values = {}
        for name in placeholders:
            if name in state.strings:
                values[name] = state.strings[name]
            elif state.has_variable(name):
                values[name] = state.get_variable(name)
            else:
                state.add_error(f"Placeholder '{name}' is not defined for string_interpolate")
                return 0

        normalized = {key: (value if isinstance(value, str) else str(value)) for key, value in values.items()}

        try:
            result = formatter.vformat(template, (), normalized)
        except KeyError as exc:
            missing = exc.args[0]
            state.add_error(f"Placeholder '{missing}' is not defined for string_interpolate")
            return 0

        state.strings[target] = result
        return 2

    @staticmethod
    def handle_string_match(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 3 >= len(tokens):
            state.add_error("string_match requires pattern, subject, and target. Use: string_match <pattern> <subject> <result>")
            return 0

        try:
            import re  # type: ignore
        except ImportError:
            state.add_output("[Error: 're' library not available]")
            return 0

        pattern_token = tokens[index + 1]
        subject_token = tokens[index + 2]
        target = tokens[index + 3]

        pattern = VariableHandler._resolve_string_token(state, pattern_token, "Pattern")
        if pattern is None:
            return 0
        subject = VariableHandler._resolve_string_token(state, subject_token, "Subject")
        if subject is None:
            return 0

        try:
            found = re.search(pattern, subject) is not None  # type: ignore[attr-defined]
        except re.error as exc:  # type: ignore[attr-defined]
            state.add_error(f"Invalid regular expression: {exc}")
            return 0

        state.set_variable(target, 1 if found else 0)
        return 3
