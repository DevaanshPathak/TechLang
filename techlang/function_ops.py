"""
First-Class Functions and Closures support for TechLang.

This module implements:
- Functions as first-class values (store in variables, pass as arguments)
- Closures that capture outer scope
- Higher-order functions (functions returning functions)
- Partial function application
"""

from typing import Dict, List, Optional, Union, Any, Callable
from .core import InterpreterState


class FunctionValue:
    """Represents a first-class function value in TechLang."""
    
    def __init__(self, name: str, params: List[str], body: List[str], 
                 captured_scope: Optional[Dict[str, Any]] = None):
        self.name = name
        self.params = params
        self.body = body
        self.captured_scope = captured_scope or {}  # Closure: captured variables
    
    def __repr__(self):
        return f"<function {self.name}({', '.join(self.params)})>"


class PartialFunction:
    """Represents a partially applied function."""
    
    def __init__(self, base_func: Union[FunctionValue, str], bound_args: Dict[str, Any]):
        self.base_func = base_func
        self.bound_args = bound_args  # param_name -> value
    
    def __repr__(self):
        if isinstance(self.base_func, FunctionValue):
            return f"<partial {self.base_func.name}(...)>"
        return f"<partial {self.base_func}(...)>"


class FunctionOpsHandler:
    """Handles first-class function operations in TechLang."""
    
    @staticmethod
    def handle_fn(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create an anonymous function (closure):
        fn <name> [params...] do ... end
        
        Creates a function value that captures the current scope.
        """
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'fn' command. Use: fn <name> [params...] do ... end")
            return 0
        
        func_name = tokens[index + 1]
        cursor = index + 2
        
        # Collect parameters (until 'do')
        params = []
        while cursor < len(tokens) and tokens[cursor] != "do":
            params.append(tokens[cursor])
            cursor += 1
        
        if cursor >= len(tokens) or tokens[cursor] != "do":
            state.add_error("Expected 'do' in function definition")
            return cursor - index
        
        cursor += 1  # Skip 'do'
        
        # Find matching 'end'
        body_start = cursor
        depth = 1
        while cursor < len(tokens):
            t = tokens[cursor]
            if t in {"fn", "def", "if", "loop", "while", "switch", "try", "match", "do"}:
                depth += 1
            elif t == "end":
                depth -= 1
                if depth == 0:
                    break
            cursor += 1
        
        if cursor >= len(tokens):
            state.add_error("Function definition missing 'end'")
            return cursor - index
        
        body = tokens[body_start:cursor]
        
        # Capture current scope for closure
        captured = {}
        for var_name, value in state.variables.items():
            captured[var_name] = ('var', value)
        for str_name, value in state.strings.items():
            captured[str_name] = ('str', value)
        
        # Create function value
        func_value = FunctionValue(func_name, params, body, captured)
        state.fn_values[func_name] = func_value
        
        return cursor - index
    
    @staticmethod
    def handle_fn_ref(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get a reference to an existing function:
        fn_ref <func_name> <target>
        
        Stores a reference to the function in target for later use.
        """
        if index + 2 >= len(tokens):
            state.add_error("Invalid 'fn_ref' command. Use: fn_ref <func_name> <target>")
            return 0
        
        func_name = tokens[index + 1]
        target = tokens[index + 2]
        
        # Check if it's a fn_value first
        if func_name in state.fn_values:
            state.fn_values[target] = state.fn_values[func_name]
            return 2
        
        # Check if it's a regular function
        if func_name in state.functions:
            func_def = state.functions[func_name]
            if isinstance(func_def, dict):
                params = func_def.get('params', [])
                body = func_def.get('body', [])
            else:
                params = []
                body = func_def
            
            # Capture current scope
            captured = {}
            for var_name, value in state.variables.items():
                captured[var_name] = ('var', value)
            for str_name, value in state.strings.items():
                captured[str_name] = ('str', value)
            
            func_value = FunctionValue(func_name, params, body, captured)
            state.fn_values[target] = func_value
            return 2
        
        # Check lambda
        if func_name in state.lambdas:
            state.fn_values[target] = state.lambdas[func_name]
            return 2
        
        state.add_error(f"Function '{func_name}' is not defined.")
        return 2
    
    @staticmethod
    def handle_fn_call(state: InterpreterState, tokens: List[str], index: int, 
                      execute_block: Callable) -> int:
        """
        Call a function value:
        fn_call <fn_var> [args...] [-> return_vars...]
        """
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'fn_call' command. Use: fn_call <fn_var> [args...] [-> return_vars...]")
            return 0
        
        fn_name = tokens[index + 1]
        
        # Find the function value
        func_value = None
        if fn_name in state.fn_values:
            func_value = state.fn_values[fn_name]
        elif fn_name in state.lambdas:
            # Lambda is a simplified function
            func_value = state.lambdas[fn_name]
        
        if func_value is None:
            state.add_error(f"Function value '{fn_name}' not found.")
            return 1
        
        # Handle PartialFunction
        if isinstance(func_value, PartialFunction):
            return FunctionOpsHandler._call_partial(state, func_value, tokens, index, execute_block)
        
        # Handle FunctionValue
        if isinstance(func_value, FunctionValue):
            return FunctionOpsHandler._call_fn_value(state, func_value, tokens, index, execute_block)
        
        # Handle dict (lambda or composed)
        if isinstance(func_value, dict):
            if func_value.get('type') == 'composed':
                return FunctionOpsHandler._call_composed(state, func_value, tokens, index, execute_block)
            else:
                return FunctionOpsHandler._call_lambda(state, func_value, tokens, index)
        
        state.add_error(f"'{fn_name}' is not a callable function value.")
        return 1
    
    @staticmethod
    def _call_composed(state: InterpreterState, composed: Dict,
                      tokens: List[str], index: int, execute_block: Callable) -> int:
        """Execute a composed function f(g(x))."""
        f_name = composed.get('f_name')
        g_name = composed.get('g_name')
        
        # Collect argument
        consumed = 1
        arg_value = 0
        from .basic_commands import BasicCommandHandler
        
        if index + 2 < len(tokens):
            arg_token = tokens[index + 2]
            if arg_token not in BasicCommandHandler.KNOWN_COMMANDS and arg_token != "->":
                arg_value = FunctionOpsHandler._resolve_arg(state, arg_token)
                consumed += 1
        
        # Collect return var (after optional ->)
        return_vars = []
        if index + 1 + consumed < len(tokens) and tokens[index + 1 + consumed] == "->":
            consumed += 1
            while index + 1 + consumed < len(tokens):
                ret_token = tokens[index + 1 + consumed]
                if ret_token in BasicCommandHandler.KNOWN_COMMANDS:
                    break
                return_vars.append(ret_token)
                consumed += 1
        
        # Apply g first, then f: f(g(x))
        g_result = FunctionOpsHandler._apply_fn_to_value(state, g_name, arg_value, execute_block)
        f_result = FunctionOpsHandler._apply_fn_to_value(state, f_name, g_result, execute_block)
        
        # Store result
        if return_vars:
            target = return_vars[0]
            if isinstance(f_result, str):
                state.strings[target] = f_result
            else:
                state.variables[target] = f_result
        else:
            state.add_output(str(f_result))
        
        return consumed
    
    @staticmethod
    def _call_fn_value(state: InterpreterState, func_value: FunctionValue, 
                      tokens: List[str], index: int, execute_block: Callable) -> int:
        """Execute a FunctionValue with closure support."""
        params = func_value.params
        body = func_value.body
        captured = func_value.captured_scope
        
        # Collect arguments
        args = []
        consumed = 1  # fn_name
        from .basic_commands import BasicCommandHandler
        
        # Check for arrow to separate args from return vars
        arrow_pos = -1
        for j in range(index + 2, len(tokens)):
            if tokens[j] == "->":
                arrow_pos = j
                break
            if tokens[j] in BasicCommandHandler.KNOWN_COMMANDS:
                break
        
        # Collect args (up to arrow or param count)
        for i in range(len(params)):
            if index + 1 + consumed >= len(tokens):
                break
            arg_token = tokens[index + 1 + consumed]
            if arg_token == "->" or arg_token in BasicCommandHandler.KNOWN_COMMANDS:
                break
            args.append(arg_token)
            consumed += 1
        
        # Collect return vars (after arrow)
        return_vars = []
        if arrow_pos >= 0:
            consumed += 1  # Skip arrow
            while index + 1 + consumed < len(tokens):
                ret_token = tokens[index + 1 + consumed]
                if ret_token in BasicCommandHandler.KNOWN_COMMANDS:
                    break
                return_vars.append(ret_token)
                consumed += 1
        
        # Save current state
        saved_vars = dict(state.variables)
        saved_strings = dict(state.strings)
        
        # Restore captured scope (closure)
        for name, (kind, value) in captured.items():
            if kind == 'var':
                state.variables[name] = value
            elif kind == 'str':
                state.strings[name] = value
        
        # Bind arguments to parameters
        for i, param in enumerate(params):
            if i < len(args):
                arg_value = FunctionOpsHandler._resolve_arg(state, args[i])
                if isinstance(arg_value, str):
                    state.strings[param] = arg_value
                else:
                    state.variables[param] = arg_value
        
        # Clear return values
        state.return_values.clear()
        state.should_return = False
        
        # Execute function body
        execute_block(body)
        
        # Store return values
        if return_vars:
            for i, var_name in enumerate(return_vars):
                if i < len(state.return_values):
                    ret_val = state.return_values[i]
                    if isinstance(ret_val, str):
                        state.strings[var_name] = ret_val
                    else:
                        state.variables[var_name] = ret_val
        
        # Restore state (but update captured scope for mutable closures)
        # Update captured scope with any changes made during execution
        for name in captured:
            if name in state.variables and captured[name][0] == 'var':
                captured[name] = ('var', state.variables[name])
            elif name in state.strings and captured[name][0] == 'str':
                captured[name] = ('str', state.strings[name])
        
        state.variables = saved_vars
        state.strings = saved_strings
        
        # Copy return values to caller's scope
        if return_vars:
            for i, var_name in enumerate(return_vars):
                if i < len(state.return_values):
                    ret_val = state.return_values[i]
                    if isinstance(ret_val, str):
                        state.strings[var_name] = ret_val
                    else:
                        state.variables[var_name] = ret_val
        
        state.should_return = False
        
        return consumed
    
    @staticmethod
    def _call_partial(state: InterpreterState, partial: PartialFunction,
                     tokens: List[str], index: int, execute_block: Callable) -> int:
        """Execute a partially applied function."""
        base = partial.base_func
        bound = partial.bound_args
        
        if isinstance(base, str):
            # It's a reference to a function name
            if base in state.fn_values:
                base = state.fn_values[base]
            elif base in state.functions:
                func_def = state.functions[base]
                if isinstance(func_def, dict):
                    base = FunctionValue(base, func_def.get('params', []), func_def.get('body', []))
                else:
                    base = FunctionValue(base, [], func_def)
        
        if not isinstance(base, FunctionValue):
            state.add_error("Cannot call partial: base function not found")
            return 1
        
        # Collect remaining arguments
        remaining_params = [p for p in base.params if p not in bound]
        args = []
        consumed = 1
        from .basic_commands import BasicCommandHandler
        
        for _ in range(len(remaining_params)):
            if index + 1 + consumed >= len(tokens):
                break
            arg_token = tokens[index + 1 + consumed]
            if arg_token == "->" or arg_token in BasicCommandHandler.KNOWN_COMMANDS:
                break
            args.append(arg_token)
            consumed += 1
        
        # Collect return vars
        return_vars = []
        if index + 1 + consumed < len(tokens) and tokens[index + 1 + consumed] == "->":
            consumed += 1
            while index + 1 + consumed < len(tokens):
                ret_token = tokens[index + 1 + consumed]
                if ret_token in BasicCommandHandler.KNOWN_COMMANDS:
                    break
                return_vars.append(ret_token)
                consumed += 1
        
        # Save state
        saved_vars = dict(state.variables)
        saved_strings = dict(state.strings)
        
        # Restore closure
        for name, (kind, value) in base.captured_scope.items():
            if kind == 'var':
                state.variables[name] = value
            elif kind == 'str':
                state.strings[name] = value
        
        # Bind pre-bound arguments
        for param, value in bound.items():
            if isinstance(value, str):
                state.strings[param] = value
            else:
                state.variables[param] = value
        
        # Bind new arguments to remaining parameters
        for i, param in enumerate(remaining_params):
            if i < len(args):
                arg_value = FunctionOpsHandler._resolve_arg(state, args[i])
                if isinstance(arg_value, str):
                    state.strings[param] = arg_value
                else:
                    state.variables[param] = arg_value
        
        # Execute
        state.return_values.clear()
        state.should_return = False
        execute_block(base.body)
        
        # Store return values
        ret_values = list(state.return_values)
        
        # Restore state
        state.variables = saved_vars
        state.strings = saved_strings
        
        if return_vars:
            for i, var_name in enumerate(return_vars):
                if i < len(ret_values):
                    ret_val = ret_values[i]
                    if isinstance(ret_val, str):
                        state.strings[var_name] = ret_val
                    else:
                        state.variables[var_name] = ret_val
        
        state.should_return = False
        return consumed
    
    @staticmethod
    def _call_lambda(state: InterpreterState, lambda_def: Dict,
                    tokens: List[str], index: int) -> int:
        """Execute a lambda (simple expression function)."""
        param = lambda_def.get('param', 'x')
        expr = lambda_def.get('expr', 'x')
        
        # Get argument
        consumed = 1
        arg_value = 0
        if index + 2 < len(tokens):
            arg_token = tokens[index + 2]
            from .basic_commands import BasicCommandHandler
            if arg_token not in BasicCommandHandler.KNOWN_COMMANDS:
                arg_value = FunctionOpsHandler._resolve_arg(state, arg_token)
                consumed += 1
        
        # Evaluate expression
        result = FunctionOpsHandler._eval_lambda_expr(arg_value, expr, param)
        
        # Get target if specified
        if index + 1 + consumed < len(tokens):
            target = tokens[index + 1 + consumed]
            from .basic_commands import BasicCommandHandler
            if target not in BasicCommandHandler.KNOWN_COMMANDS:
                state.variables[target] = result
                consumed += 1
            else:
                state.add_output(str(result))
        else:
            state.add_output(str(result))
        
        return consumed
    
    @staticmethod
    def handle_partial(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create a partially applied function:
        partial <fn_name> <target> <param>=<value> [<param>=<value>...]
        """
        if index + 2 >= len(tokens):
            state.add_error("Invalid 'partial' command. Use: partial <fn_name> <target> <param>=<value>...")
            return 0
        
        fn_name = tokens[index + 1]
        target = tokens[index + 2]
        
        # Find base function
        base_func = None
        if fn_name in state.fn_values:
            base_func = state.fn_values[fn_name]
        elif fn_name in state.functions:
            func_def = state.functions[fn_name]
            if isinstance(func_def, dict):
                # Capture scope
                captured = {}
                for var_name, value in state.variables.items():
                    captured[var_name] = ('var', value)
                base_func = FunctionValue(fn_name, func_def.get('params', []), 
                                         func_def.get('body', []), captured)
            else:
                base_func = FunctionValue(fn_name, [], func_def, {})
        
        if base_func is None:
            state.add_error(f"Function '{fn_name}' not found.")
            return 2
        
        # Collect bound arguments
        bound_args = {}
        consumed = 2
        from .basic_commands import BasicCommandHandler
        
        while index + 1 + consumed < len(tokens):
            token = tokens[index + 1 + consumed]
            if token in BasicCommandHandler.KNOWN_COMMANDS:
                break
            
            if "=" in token:
                parts = token.split("=", 1)
                param_name = parts[0]
                value_str = parts[1]
                
                # Resolve value
                value = FunctionOpsHandler._resolve_arg(state, value_str)
                bound_args[param_name] = value
                consumed += 1
            else:
                break
        
        # Create partial function
        partial_func = PartialFunction(base_func, bound_args)
        state.fn_values[target] = partial_func
        
        return consumed
    
    @staticmethod
    def handle_compose(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Compose two functions: f ∘ g means f(g(x))
        compose <f> <g> <target>
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'compose' command. Use: compose <f> <g> <target>")
            return 0
        
        f_name = tokens[index + 1]
        g_name = tokens[index + 2]
        target = tokens[index + 3]
        
        # Get functions
        f_func = state.fn_values.get(f_name) or state.lambdas.get(f_name)
        g_func = state.fn_values.get(g_name) or state.lambdas.get(g_name)
        
        if f_func is None:
            state.add_error(f"Function '{f_name}' not found.")
            return 3
        
        if g_func is None:
            state.add_error(f"Function '{g_name}' not found.")
            return 3
        
        # Create composed function
        # For simplicity, we create a special composed function value
        composed = {
            'type': 'composed',
            'f': f_func,
            'g': g_func,
            'f_name': f_name,
            'g_name': g_name
        }
        state.fn_values[target] = composed
        
        return 3
    
    @staticmethod
    def handle_map_fn(state: InterpreterState, tokens: List[str], index: int,
                     execute_block: Callable) -> int:
        """
        Map a function over an array:
        map_fn <array> <fn> <result>
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'map_fn' command. Use: map_fn <array> <fn> <result>")
            return 0
        
        array_name = tokens[index + 1]
        fn_name = tokens[index + 2]
        result_name = tokens[index + 3]
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist.")
            return 3
        
        source = state.arrays[array_name]
        result = []
        
        for item in source:
            # Call function with item
            mapped = FunctionOpsHandler._apply_fn_to_value(state, fn_name, item, execute_block)
            result.append(mapped)
        
        state.arrays[result_name] = result
        return 3
    
    @staticmethod
    def handle_filter_fn(state: InterpreterState, tokens: List[str], index: int,
                        execute_block: Callable) -> int:
        """
        Filter an array using a predicate function:
        filter_fn <array> <fn> <result>
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'filter_fn' command. Use: filter_fn <array> <fn> <result>")
            return 0
        
        array_name = tokens[index + 1]
        fn_name = tokens[index + 2]
        result_name = tokens[index + 3]
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist.")
            return 3
        
        source = state.arrays[array_name]
        result = []
        
        for item in source:
            # Call predicate function
            keep = FunctionOpsHandler._apply_fn_to_value(state, fn_name, item, execute_block)
            if keep and keep != 0:
                result.append(item)
        
        state.arrays[result_name] = result
        return 3
    
    @staticmethod
    def handle_reduce_fn(state: InterpreterState, tokens: List[str], index: int,
                        execute_block: Callable) -> int:
        """
        Reduce an array using a binary function:
        reduce_fn <array> <fn> <initial> <result>
        """
        if index + 4 >= len(tokens):
            state.add_error("Invalid 'reduce_fn' command. Use: reduce_fn <array> <fn> <initial> <result>")
            return 0
        
        array_name = tokens[index + 1]
        fn_name = tokens[index + 2]
        initial_token = tokens[index + 3]
        result_name = tokens[index + 4]
        
        if array_name not in state.arrays:
            state.add_error(f"Array '{array_name}' does not exist.")
            return 4
        
        source = state.arrays[array_name]
        accumulator = FunctionOpsHandler._resolve_arg(state, initial_token)
        
        for item in source:
            # Call binary function with (accumulator, item)
            accumulator = FunctionOpsHandler._apply_binary_fn(
                state, fn_name, accumulator, item, execute_block
            )
        
        if isinstance(accumulator, str):
            state.strings[result_name] = accumulator
        else:
            state.variables[result_name] = accumulator
        
        return 4
    
    @staticmethod
    def _apply_fn_to_value(state: InterpreterState, fn_name: str, value: Any,
                          execute_block: Callable) -> Any:
        """Apply a function to a single value and return the result."""
        # Check lambda first (simpler)
        if fn_name in state.lambdas:
            lambda_def = state.lambdas[fn_name]
            param = lambda_def.get('param', 'x')
            expr = lambda_def.get('expr', 'x')
            return FunctionOpsHandler._eval_lambda_expr(value, expr, param)
        
        # Check fn_values
        if fn_name in state.fn_values:
            func_value = state.fn_values[fn_name]
            
            if isinstance(func_value, FunctionValue):
                # Save state
                saved_vars = dict(state.variables)
                saved_strings = dict(state.strings)
                
                # Bind value to first param
                if func_value.params:
                    param = func_value.params[0]
                    if isinstance(value, str):
                        state.strings[param] = value
                    else:
                        state.variables[param] = value
                
                state.return_values.clear()
                state.should_return = False
                execute_block(func_value.body)
                
                result = state.return_values[0] if state.return_values else value
                
                state.variables = saved_vars
                state.strings = saved_strings
                state.should_return = False
                
                return result
            
            # Handle composed function
            if isinstance(func_value, dict) and func_value.get('type') == 'composed':
                g_result = FunctionOpsHandler._apply_fn_to_value(
                    state, func_value['g_name'], value, execute_block
                )
                return FunctionOpsHandler._apply_fn_to_value(
                    state, func_value['f_name'], g_result, execute_block
                )
        
        # Check regular functions
        if fn_name in state.functions:
            func_def = state.functions[fn_name]
            if isinstance(func_def, dict):
                params = func_def.get('params', [])
                body = func_def.get('body', [])
            else:
                params = []
                body = func_def
            
            saved_vars = dict(state.variables)
            saved_strings = dict(state.strings)
            
            if params:
                param = params[0]
                if isinstance(value, str):
                    state.strings[param] = value
                else:
                    state.variables[param] = value
            
            state.return_values.clear()
            state.should_return = False
            execute_block(body)
            
            result = state.return_values[0] if state.return_values else value
            
            state.variables = saved_vars
            state.strings = saved_strings
            state.should_return = False
            
            return result
        
        return value
    
    @staticmethod
    def _apply_binary_fn(state: InterpreterState, fn_name: str, 
                        acc: Any, item: Any, execute_block: Callable) -> Any:
        """Apply a binary function f(accumulator, item) and return result."""
        # Check fn_values
        if fn_name in state.fn_values:
            func_value = state.fn_values[fn_name]
            
            if isinstance(func_value, FunctionValue) and len(func_value.params) >= 2:
                saved_vars = dict(state.variables)
                saved_strings = dict(state.strings)
                
                # Bind parameters
                p1, p2 = func_value.params[0], func_value.params[1]
                if isinstance(acc, str):
                    state.strings[p1] = acc
                else:
                    state.variables[p1] = acc
                if isinstance(item, str):
                    state.strings[p2] = item
                else:
                    state.variables[p2] = item
                
                state.return_values.clear()
                state.should_return = False
                execute_block(func_value.body)
                
                result = state.return_values[0] if state.return_values else acc
                
                state.variables = saved_vars
                state.strings = saved_strings
                state.should_return = False
                
                return result
        
        # Check regular functions
        if fn_name in state.functions:
            func_def = state.functions[fn_name]
            if isinstance(func_def, dict):
                params = func_def.get('params', [])
                body = func_def.get('body', [])
            else:
                params = []
                body = func_def
            
            if len(params) >= 2:
                saved_vars = dict(state.variables)
                saved_strings = dict(state.strings)
                
                p1, p2 = params[0], params[1]
                if isinstance(acc, str):
                    state.strings[p1] = acc
                else:
                    state.variables[p1] = acc
                if isinstance(item, str):
                    state.strings[p2] = item
                else:
                    state.variables[p2] = item
                
                state.return_values.clear()
                state.should_return = False
                execute_block(body)
                
                result = state.return_values[0] if state.return_values else acc
                
                state.variables = saved_vars
                state.strings = saved_strings
                state.should_return = False
                
                return result
        
        # Fallback: just return accumulator
        return acc
    
    @staticmethod
    def _resolve_arg(state: InterpreterState, token: str) -> Union[int, str, float]:
        """Resolve an argument token to its value."""
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        if token in state.strings:
            return state.strings[token]
        if token in state.variables:
            return state.variables[token]
        try:
            return int(token)
        except ValueError:
            pass
        try:
            return float(token)
        except ValueError:
            pass
        return token
    
    @staticmethod
    def _eval_lambda_expr(x: Any, expr: str, param: str = 'x') -> Any:
        """Evaluate a simple lambda expression with value x."""
        # Replace parameter with value
        expr_with_value = expr.replace(param, str(x))
        
        try:
            # Safe evaluation of simple math expressions
            # Support: +, -, *, /, %, **, abs(), int(), str()
            allowed_names = {
                'abs': abs,
                'int': int,
                'str': str,
                'float': float,
                'min': min,
                'max': max,
                'round': round,
            }
            result = eval(expr_with_value, {"__builtins__": {}}, allowed_names)
            return result
        except Exception:
            return x
