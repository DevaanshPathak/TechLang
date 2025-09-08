from typing import List, Optional
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
        try:
            varvalue = int(tokens[index + 2])
            state.set_variable(varname, varvalue)
            return 2  # Consume variable name and value
        except ValueError:
            state.add_error(f"Expected a number for variable '{varname}', but got '{tokens[index + 2]}'. Please provide a valid integer.")
            return 0
    
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
