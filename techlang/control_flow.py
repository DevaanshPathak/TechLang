# techlang/control_flow.py

from typing import List, Tuple, Callable
from .core import InterpreterState
from .blocks import BlockCollector


class ControlFlowHandler:
    """Handles control flow operations in TechLang."""
    
    @staticmethod
    def handle_loop(state: InterpreterState, tokens: List[str], index: int, execute_block: Callable) -> int:
        """
        Handle the 'loop' command to repeat a block of code.
        
        Args:
            state: The interpreter state
            tokens: List of tokens
            index: Current token index
            execute_block: Function to execute code blocks
            
        Returns:
            Number of tokens consumed
        """
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'loop' command. Use: loop <count> ... end")
            return 0
        
        loop_count_token = tokens[index + 1]
        start_index = index + 2  # Start after 'loop' and count token
        
        # Collect the loop block
        loop_block, end_index = BlockCollector.collect_block(start_index, tokens)
        
        # Determine loop count
        try:
            loop_count = int(loop_count_token)
        except ValueError:
            # Try to get from variables
            loop_count = state.get_variable(loop_count_token)
            if not isinstance(loop_count, int):
                state.add_error(f"Loop count must be a number or existing variable, but got '{loop_count_token}'. Please provide a valid integer or variable name.")
                return 0
        
        # Execute the loop
        for _ in range(loop_count):
            execute_block(loop_block)
        
        # Return total tokens consumed: 'loop' + count + block + 'end'
        return end_index - index
    
    @staticmethod
    def handle_if(state: InterpreterState, tokens: List[str], index: int, execute_block: Callable) -> int:
        """
        Handle the 'if' command for conditional execution.
        
        Args:
            state: The interpreter state
            tokens: List of tokens
            index: Current token index
            execute_block: Function to execute code blocks
            
        Returns:
            Number of tokens consumed
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'if' command. Use: if <variable> <operator> <value> ... end")
            return 0
        
        varname = tokens[index + 1]
        op = tokens[index + 2]
        
        try:
            compare_val = int(tokens[index + 3])
        except ValueError:
            state.add_error(f"Expected a number for comparison, but got '{tokens[index + 3]}'. Please provide a valid integer.")
            return 0
        
        start_index = index + 4  # Start after 'if', variable, operator, and value
        
        # Get variable value for comparison
        var_value = state.get_variable(varname, 0)
        if not isinstance(var_value, int):
            state.add_error(f"Variable '{varname}' is not a number. Cannot perform comparison.")
            return 0
        
        # Check condition
        condition_met = ControlFlowHandler._evaluate_condition(var_value, op, compare_val)
        
        # Collect the if block
        if_block, end_index = BlockCollector.collect_block(start_index, tokens)
        
        # Execute block if condition is met
        if condition_met:
            execute_block(if_block)
        
        # Return total tokens consumed: 'if' + var + op + val + block + 'end'
        return end_index - index
    
    @staticmethod
    def handle_def(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Handle the 'def' command to define functions.
        
        Args:
            state: The interpreter state
            tokens: List of tokens
            index: Current token index
            
        Returns:
            Number of tokens consumed
        """
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'def' command. Use: def <function_name> ... end")
            return 0
        
        func_name = tokens[index + 1]
        start_index = index + 2  # Start after 'def' and function name
        
        # Collect the function block (but don't execute it)
        func_block, end_index = BlockCollector.collect_block(start_index, tokens)
        
        # Store the function body (the tokens inside the function)
        state.functions[func_name] = func_block
        
        # Return total tokens consumed: 'def' + func_name + func_body + 'end'
        return end_index - index
    
    @staticmethod
    def handle_call(state: InterpreterState, tokens: List[str], index: int, execute_block: Callable) -> int:
        """
        Handle the 'call' command to execute functions.
        
        Args:
            state: The interpreter state
            tokens: List of tokens
            index: Current token index
            execute_block: Function to execute code blocks
            
        Returns:
            Number of tokens consumed
        """
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'call' command. Use: call <function_name>")
            return 0
        
        func_name = tokens[index + 1]
        
        if func_name in state.functions:
            execute_block(state.functions[func_name])
        else:
            state.add_error(f"Function '{func_name}' is not defined. Use 'def {func_name} ... end' to define it first.")
        
        return 1  # Consume function name
    
    @staticmethod
    def _evaluate_condition(var_value: int, op: str, compare_val: int) -> bool:
        """
        Evaluate a comparison condition.
        
        Args:
            var_value: The variable value to compare
            op: The comparison operator
            compare_val: The value to compare against
            
        Returns:
            True if condition is met, False otherwise
        """
        if op == "==":
            return var_value == compare_val
        elif op == "!=":
            return var_value != compare_val
        elif op == ">":
            return var_value > compare_val
        elif op == "<":
            return var_value < compare_val
        elif op == ">=":
            return var_value >= compare_val
        elif op == "<=":
            return var_value <= compare_val
        else:
            return False  # Unknown operator
