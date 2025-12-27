"""
Walrus Operator := (Assignment Expressions) for TechLang.

Provides assignment expression support with:
- if_assign <var> := <expr> <op> <value> do ... end - Assignment in if condition
- while_assign <var> := <expr> do ... end - Assignment in while loop
- assign_expr <var> := <value> - Standalone assignment expression
"""

from typing import Dict, List, Optional, Any, Callable
from .core import InterpreterState
from .blocks import BlockCollector


class WalrusHandler:
    """Handles walrus operator (assignment expression) operations in TechLang."""
    
    @staticmethod
    def _resolve_value(state: InterpreterState, token: str) -> Any:
        """Resolve a token to its actual value."""
        # Check if it's a quoted string
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        
        # Check variables
        if token in state.variables:
            return state.variables[token]
        
        # Check strings
        if token in state.strings:
            return state.strings[token]
        
        # Try numeric parsing
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return token
    
    @staticmethod
    def _evaluate_expression(state: InterpreterState, expr_tokens: List[str], 
                            execute_block: Callable) -> Any:
        """
        Evaluate an expression and return its result.
        For simple cases, resolve directly. For commands, execute and capture.
        """
        if not expr_tokens:
            return 0
        
        # Single token - resolve directly
        if len(expr_tokens) == 1:
            return WalrusHandler._resolve_value(state, expr_tokens[0])
        
        # Handle common expression commands
        cmd = expr_tokens[0]
        
        if cmd == "str_length":
            if len(expr_tokens) >= 2:
                str_name = expr_tokens[1]
                if str_name in state.strings:
                    return len(state.strings[str_name])
                # Maybe it's a quoted string
                if str_name.startswith('"') and str_name.endswith('"'):
                    return len(str_name[1:-1])
            return 0
        
        if cmd == "array_length":
            if len(expr_tokens) >= 2:
                arr_name = expr_tokens[1]
                if arr_name in state.arrays:
                    return len(state.arrays[arr_name])
            return 0
        
        if cmd == "array_get":
            if len(expr_tokens) >= 3:
                arr_name = expr_tokens[1]
                idx = WalrusHandler._resolve_value(state, expr_tokens[2])
                if arr_name in state.arrays and isinstance(idx, int):
                    arr = state.arrays[arr_name]
                    if 0 <= idx < len(arr):
                        return arr[idx]
            return 0
        
        if cmd == "dict_get":
            if len(expr_tokens) >= 3:
                dict_name = expr_tokens[1]
                key = WalrusHandler._resolve_value(state, expr_tokens[2])
                if dict_name in state.dictionaries:
                    return state.dictionaries[dict_name].get(key, 0)
            return 0
        
        # For other commands, execute them and try to capture the result
        # This is a simplified approach - execute and check for new output
        before_len = len(state.output)
        execute_block(expr_tokens)
        
        # Check if output was added
        if len(state.output) > before_len:
            result_str = state.output[-1]
            # Try to parse as number
            try:
                return int(result_str)
            except ValueError:
                return result_str
        
        return 0
    
    @staticmethod
    def _check_condition(left: Any, op: str, right: Any) -> bool:
        """Check a condition between two values."""
        # Handle type coercion
        if isinstance(left, str) and isinstance(right, int):
            try:
                left = int(left)
            except ValueError:
                pass
        elif isinstance(left, int) and isinstance(right, str):
            try:
                right = int(right)
            except ValueError:
                pass
        
        if op in ("==", "eq"):
            return left == right
        elif op in ("!=", "ne"):
            return left != right
        elif op in (">", "gt"):
            return left > right
        elif op in ("<", "lt"):
            return left < right
        elif op in (">=", "ge"):
            return left >= right
        elif op in ("<=", "le"):
            return left <= right
        
        return False
    
    @staticmethod
    def handle_if_assign(state: InterpreterState, tokens: List[str], index: int,
                         execute_block: Callable) -> int:
        """
        Assignment expression in if condition:
        if_assign <var> := <expr> <op> <value> do ... end
        
        Example:
        if_assign n := str_length mystring > 10 do
            print "Long string with"
            print n
            print "characters"
        end
        """
        # Parse: if_assign <var> := <expr_cmd> [expr_args...] <op> <value> do ... end
        if index + 5 >= len(tokens):
            state.add_error("Invalid 'if_assign'. Use: if_assign <var> := <expr> <op> <value> do ... end")
            return 0
        
        var_name = tokens[index + 1]
        
        if tokens[index + 2] != ":=":
            state.add_error("if_assign requires ':=' after variable name.")
            return 2
        
        # Find 'do' keyword to determine structure
        do_index = None
        for i in range(index + 3, len(tokens)):
            if tokens[i] == "do":
                do_index = i
                break
        
        if do_index is None:
            state.add_error("if_assign requires 'do' keyword.")
            return 3
        
        # Tokens between ':=' and 'do' contain: expr_cmd [args...] op value
        expr_tokens = tokens[index + 3:do_index]
        
        if len(expr_tokens) < 3:
            state.add_error("if_assign requires expression, operator, and comparison value.")
            return do_index - index
        
        # Last two tokens are operator and comparison value
        compare_val_token = expr_tokens[-1]
        op = expr_tokens[-2]
        expr_cmd_tokens = expr_tokens[:-2]
        
        # Evaluate expression by executing it and capturing output or using a helper
        result = WalrusHandler._evaluate_expression(state, expr_cmd_tokens, execute_block)
        
        # Store result in variable
        if isinstance(result, str):
            state.strings[var_name] = result
        else:
            state.variables[var_name] = result
        
        # Evaluate condition
        compare_val = WalrusHandler._resolve_value(state, compare_val_token)
        condition_met = WalrusHandler._check_condition(result, op, compare_val)
        
        # Collect if block
        body_start = do_index + 1
        body, end_index = BlockCollector.collect_block(body_start, tokens)
        
        if condition_met:
            execute_block(body)
        
        return end_index - index
    
    @staticmethod
    def handle_while_assign(state: InterpreterState, tokens: List[str], index: int,
                            execute_block: Callable) -> int:
        """
        Assignment expression in while loop:
        while_assign <var> := <expr_cmd> [args...] do ... end
        
        The loop continues while expr returns a truthy value.
        
        Example:
        while_assign line := file_readline f do
            print line
        end
        """
        if index + 4 >= len(tokens):
            state.add_error("Invalid 'while_assign'. Use: while_assign <var> := <expr> do ... end")
            return 0
        
        var_name = tokens[index + 1]
        
        if tokens[index + 2] != ":=":
            state.add_error("while_assign requires ':=' after variable name.")
            return 2
        
        # Find 'do'
        do_index = None
        for i in range(index + 3, len(tokens)):
            if tokens[i] == "do":
                do_index = i
                break
        
        if do_index is None:
            state.add_error("while_assign requires 'do' keyword.")
            return 3
        
        expr_tokens = tokens[index + 3:do_index]
        body_start = do_index + 1
        body, end_index = BlockCollector.collect_block(body_start, tokens)
        
        max_iterations = 1000
        iteration = 0
        
        while iteration < max_iterations:
            # Evaluate expression
            result = WalrusHandler._evaluate_expression(state, expr_tokens, execute_block)
            
            # Check truthy
            if result is None or result == 0 or result == "" or result == []:
                break
            
            # Store result
            if isinstance(result, str):
                state.strings[var_name] = result
            else:
                state.variables[var_name] = result
            
            # Execute body
            execute_block(body)
            iteration += 1
        
        if iteration >= max_iterations:
            state.add_error(f"while_assign exceeded maximum iterations ({max_iterations}).")
        
        return end_index - index
    
    @staticmethod
    def handle_assign_expr(state: InterpreterState, tokens: List[str], index: int,
                           execute_block: Callable) -> int:
        """
        Standalone assignment expression:
        assign_expr <var> := <value_or_expr>
        
        Example:
        assign_expr x := 42
        assign_expr y := somevar
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'assign_expr'. Use: assign_expr <var> := <value>")
            return 0
        
        var_name = tokens[index + 1]
        
        if tokens[index + 2] != ":=":
            state.add_error("assign_expr requires ':=' operator.")
            return 2
        
        value_token = tokens[index + 3]
        value = WalrusHandler._resolve_value(state, value_token)
        
        if isinstance(value, str):
            state.strings[var_name] = value
        else:
            state.variables[var_name] = value
        
        # Also output the value (like Python's walrus)
        state.add_output(str(value))
        
        return 3
