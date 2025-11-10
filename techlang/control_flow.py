from typing import Callable, List, Optional, Tuple, Union
from .core import InterpreterState
from .blocks import BlockCollector


class ControlFlowHandler:
    """
    Handles control flow in TechLang.
    This class manages loops, conditions, and functions - the logic that controls
    how your program flows from one part to another.
    """
    
    @staticmethod
    def handle_loop(state: InterpreterState, tokens: List[str], index: int, execute_block: Callable) -> int:
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'loop' command. Use: loop <count> ... end")
            return 0
        
        loop_count_token = tokens[index + 1]
        start_index = index + 2  # Start after 'loop' and count token
        
        # Grab the block of tokens to be repeated
        loop_block, end_index = BlockCollector.collect_block(start_index, tokens)
        
        # Determine loop count
        try:
            loop_count = int(loop_count_token)
        except ValueError:
            # Fallback: allow using a variable as the loop count
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
    def handle_while(state: InterpreterState, tokens: List[str], index: int, execute_block: Callable) -> int:
        """
        Handle while loops in TechLang.
        Keeps repeating a block of code as long as a condition is true.
        Like saying "keep doing this while this condition is true".
        Example: while x > 0 ... end
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'while' command. Use: while <variable> <operator> <value> ... end")
            return 0
        
        varname = tokens[index + 1]
        op = tokens[index + 2]
        compare_token = tokens[index + 3]
        
        # Try to get comparison value - could be a number or variable
        try:
            compare_val = int(compare_token)
        except ValueError:
            # Check if it's a variable
            if state.has_variable(compare_token):
                compare_val = state.get_variable(compare_token)
                if not isinstance(compare_val, int):
                    state.add_error(f"Variable '{compare_token}' is not a number. Cannot perform comparison.")
                    return 0
            else:
                state.add_error(f"Expected a number or variable for comparison, but got '{compare_token}'. Please provide a valid integer or variable name.")
                return 0
        
        start_index = index + 4  # Start after 'while', variable, operator, and value
        
        # Collect the while block
        while_block, end_index = BlockCollector.collect_block(start_index, tokens)
        
        # Keep executing the block while the condition is true
        # Add safety limit to prevent infinite loops
        max_iterations = 1000
        iteration_count = 0
        
        while iteration_count < max_iterations:
            # Get current variable value for comparison
            var_value = state.get_variable(varname, 0)
            if not isinstance(var_value, int):
                state.add_error(f"Variable '{varname}' is not a number. Cannot perform comparison.")
                return 0
            
            # Check if condition is still true
            condition_met = ControlFlowHandler._evaluate_condition(var_value, op, compare_val)
            
            if not condition_met:
                # Condition is false, exit the loop
                break
            
            # Execute the block
            execute_block(while_block)
            iteration_count += 1
            
            # Check if we've hit the safety limit
            if iteration_count >= max_iterations:
                state.add_error(f"While loop exceeded maximum iterations ({max_iterations}). This might be an infinite loop.")
                break
        
        # Return total tokens consumed: 'while' + var + op + val + block + 'end'
        return end_index - index
    
    @staticmethod
    def handle_if(state: InterpreterState, tokens: List[str], index: int, execute_block: Callable) -> int:
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'if' command. Use: if <variable> <operator> <value> ... end")
            return 0
        
        varname = tokens[index + 1]
        op = tokens[index + 2]
        compare_token = tokens[index + 3]
        
        # Try to resolve compare_token as a variable first, then as a literal
        compare_val = state.get_variable(compare_token, None)
        if compare_val is None:
            try:
                compare_val = int(compare_token)
            except ValueError:
                state.add_error(f"Expected a number or variable for comparison, but got '{compare_token}'. Please provide a valid integer or variable name.")
                return 0
        
        start_index = index + 4  # Start after 'if', variable, operator, and value
        
        # Get variable value for comparison
        var_value = state.get_variable(varname, 0)
        if not isinstance(var_value, int):
            state.add_error(f"Variable '{varname}' is not a number. Cannot perform comparison.")
            return 0
        
        # Ensure compare_val is an integer
        if not isinstance(compare_val, int):
            state.add_error(f"Comparison value must be a number, but got type '{type(compare_val).__name__}'.")
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
    def handle_switch(state: InterpreterState, tokens: List[str], index: int, execute_block: Callable) -> int:
        """
        switch <variable> ... case <value> ... default ... end
        Executes the matching case block, or default if none match. Only one block runs.
        """
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'switch' command. Use: switch <variable> ... end")
            return 0
        varname = tokens[index + 1]
        start_index = index + 2
        # Collect entire switch body
        switch_body, end_index = BlockCollector.collect_block(start_index, tokens)

        # Read selector value
        selector = state.get_variable(varname, 0)

        # Parse switch body into case/default segments
        i = 0
        active_block: List[str] = []
        have_match = False
        default_block: List[str] = []
        while i < len(switch_body):
            t = switch_body[i]
            if t == "case":
                # case <number>
                if i + 1 >= len(switch_body):
                    state.add_error("Invalid 'case' usage. Use: case <number>")
                    return end_index - index
                case_token = switch_body[i + 1]
                try:
                    case_value = int(case_token)
                except ValueError:
                    state.add_error(f"Case value must be a number, got '{case_token}'")
                    return end_index - index
                # Collect case block until next case/default/end of switch_body
                block_start = i + 2
                j = block_start
                nested_depth = 0
                case_block: List[str] = []
                while j < len(switch_body):
                    tt = switch_body[j]
                    if tt in {"def", "if", "loop", "while", "switch", "try"}:
                        nested_depth += 1
                    elif tt in {"case", "default"} and nested_depth == 0:
                        break
                    elif tt == "end" and nested_depth > 0:
                        nested_depth -= 1
                    case_block.append(tt)
                    j += 1
                if not have_match and selector == case_value:
                    active_block = case_block
                    have_match = True
                i = j
                continue
            elif t == "default":
                # Collect default block similarly
                block_start = i + 1
                j = block_start
                nested_depth = 0
                tmp_block: List[str] = []
                while j < len(switch_body):
                    tt = switch_body[j]
                    if tt in {"def", "if", "loop", "while", "switch", "try"}:
                        nested_depth += 1
                    elif tt in {"case", "default"} and nested_depth == 0:
                        break
                    elif tt == "end" and nested_depth > 0:
                        nested_depth -= 1
                    tmp_block.append(tt)
                    j += 1
                default_block = tmp_block
                i = j
                continue
            else:
                # Skip stray tokens (e.g., whitespace already tokenized out)
                i += 1
        # Execute matching block
        if have_match:
            execute_block(active_block)
        elif default_block:
            execute_block(default_block)
        return end_index - index

    @staticmethod
    def handle_match(state: InterpreterState, tokens: List[str], index: int, execute_block: Callable) -> int:
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'match' command. Use: match <expression> ... end")
            return 0

        selector_token = tokens[index + 1]
        selector_resolved = ControlFlowHandler._resolve_match_value(state, selector_token)
        if selector_resolved is None:
            return 0

        selector_value = selector_resolved
        start_index = index + 2
        match_body, end_index = BlockCollector.collect_block(start_index, tokens)

        i = 0
        matched_block: Optional[List[str]] = None
        default_block: Optional[List[str]] = None

        while i < len(match_body):
            token = match_body[i]
            if token != "case":
                i += 1
                continue

            if i + 1 >= len(match_body):
                state.add_error("Invalid 'case' usage in match. Use: case <pattern>")
                return end_index - index

            pattern_token = match_body[i + 1]
            operator = "=="
            value_token: Optional[str] = None
            cursor = i + 2

            if pattern_token in {"default", "_"}:
                block_start = cursor
                value_token = None
                operator = "default"
            else:
                if pattern_token in {"==", "!=", ">", "<", ">=", "<="}:
                    if cursor >= len(match_body):
                        state.add_error("Invalid pattern for match case. Expected value after operator.")
                        return end_index - index
                    operator = pattern_token
                    value_token = match_body[cursor]
                    cursor += 1
                else:
                    value_token = pattern_token

                block_start = cursor

            case_block: List[str] = []
            nested_depth = 0
            j = block_start
            while j < len(match_body):
                current = match_body[j]
                if current in {"def", "if", "loop", "while", "switch", "match", "try"}:
                    nested_depth += 1
                elif current == "case" and nested_depth == 0:
                    break
                elif current == "end" and nested_depth > 0:
                    nested_depth -= 1
                case_block.append(current)
                j += 1

            if operator == "default":
                default_block = case_block
            else:
                pattern_value = ControlFlowHandler._resolve_match_value(state, value_token)
                if pattern_value is None:
                    return end_index - index
                condition_met, valid = ControlFlowHandler._evaluate_match(selector_value, operator, pattern_value, state)
                if not valid:
                    return end_index - index
                if condition_met and matched_block is None:
                    matched_block = case_block

            i = j

        if matched_block is not None:
            execute_block(matched_block)
        elif default_block is not None:
            execute_block(default_block)

        return end_index - index

    @staticmethod
    def handle_try(state: InterpreterState, tokens: List[str], index: int, execute_block: Callable) -> int:
        """
        try ... catch ... end
        Execute try block; if any error is emitted inside, suppress it and run catch.
        We detect errors by inspecting output lines appended during try.
        """
        start_index = index + 1
        try_body, end_index = BlockCollector.collect_block(start_index, tokens)

        # Split try_body by top-level 'catch'
        i = 0
        nested_depth = 0
        try_block: List[str] = []
        catch_block: List[str] = []
        found_catch = False
        catch_error_var: Optional[str] = None
        catch_stack_var: Optional[str] = None
        from .basic_commands import BasicCommandHandler  # local import to avoid circular dependency

        reserved_tokens = {"case", "catch", "default", "def", "end", "if", "loop", "match", "switch", "try", "while"}
        reserved_tokens.update(BasicCommandHandler.KNOWN_COMMANDS)
        while i < len(try_body):
            t = try_body[i]
            if t in {"def", "if", "loop", "while", "switch", "try"}:
                nested_depth += 1
            elif t == "end" and nested_depth > 0:
                nested_depth -= 1
            if t == "catch" and nested_depth == 0 and not found_catch:
                found_catch = True
                if i + 1 < len(try_body) and try_body[i + 1] not in reserved_tokens:
                    catch_error_var = try_body[i + 1]
                    i += 1
                    if i + 1 < len(try_body) and try_body[i + 1] not in reserved_tokens:
                        catch_stack_var = try_body[i + 1]
                        i += 1
                i += 1
                continue
            if not found_catch:
                try_block.append(t)
            else:
                catch_block.append(t)
            i += 1

        # Snapshot output length; if an [Error: ...] is added during try, run catch
        before_len = len(state.output)
        execute_block(try_block)
        new_lines = state.output[before_len:]
        error_lines = [line for line in new_lines if line.startswith("[Error:")]
        error_emitted = bool(error_lines)
        if error_emitted and catch_block:
            if catch_error_var:
                message = ControlFlowHandler._extract_error_message(error_lines[0])
                state.set_variable(catch_error_var, message)
            if catch_stack_var:
                state.set_variable(catch_stack_var, str(state.stack))
            execute_block(catch_block)
        return end_index - index
    def handle_def(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'def' command. Use: def <function_name> [params...] ... end")
            return 0
        
        func_name = tokens[index + 1]
        
        # Collect parameter names (everything between func_name and the function body)
        params = []
        param_index = index + 2
        
        # Parameters are tokens before the function body starts
        # We need to find where params end and body begins
        # Body starts when we encounter tokens that look like commands or we run out of simple identifiers
        # Note: 'end' can be a valid parameter name, so we don't stop at 'end'
        while param_index < len(tokens):
            token = tokens[param_index]
            # If we hit a known command (except 'end') or quoted string, that's the start of the body
            from .basic_commands import BasicCommandHandler
            if (token in BasicCommandHandler.KNOWN_COMMANDS and token != "end") or token.startswith('"'):
                break
            # Otherwise it's a parameter name
            params.append(token)
            param_index += 1
        
        # Now collect the function body from where params ended
        start_index = param_index
        func_block, end_index = BlockCollector.collect_block(start_index, tokens)
        
        # Store function with both params and body
        state.functions[func_name] = {
            'params': params,
            'body': func_block
        }
        
        # Return total tokens consumed: 'def' + func_name + params + func_body + 'end'
        return end_index - index
    
    @staticmethod
    def handle_call(state: InterpreterState, tokens: List[str], index: int, execute_block: Callable) -> int:
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'call' command. Use: call <function_name> [args...] [return_vars...]")
            return 0
        
        func_name = tokens[index + 1]

        module_call = ControlFlowHandler._split_module_call(func_name)
        if module_call is not None:
            module_name, inner_name = module_call
            from .imports import ModuleHandler  # local import to avoid circular dependencies

            # Collect arguments and return variables for module function call
            # First, get the module and function to see how many params it needs
            normalized_name = module_name.replace("::", ".").replace("/", ".")
            # Support 'stdlib' as alias for 'stl'
            if normalized_name.startswith("stdlib.") or normalized_name == "stdlib":
                normalized_name = normalized_name.replace("stdlib", "stl", 1)
            module_info = state.modules.get(normalized_name)
            if module_info is None:
                state.add_error(f"Module '{module_name}' is not loaded. Use 'package use {module_name}' first.")
                return 1
            
            module_state = module_info.state
            func_data = module_state.functions.get(inner_name)
            if func_data is None:
                state.add_error(f"Module '{module_name}' has no function '{inner_name}'.")
                return 1
            
            # Determine parameter count
            if isinstance(func_data, dict):
                param_count = len(func_data.get('params', []))
            else:
                param_count = 0
            
            # Collect arguments - collect exactly param_count arguments
            # Don't stop early for KNOWN_COMMANDS since variables can have those names
            args = []
            consumed = 1  # function name
            for _ in range(param_count):
                if index + 1 + consumed >= len(tokens):
                    break
                arg_token = tokens[index + 1 + consumed]
                args.append(arg_token)
                consumed += 1
            
            # Collect return variable names (rest of tokens until next command)
            return_vars = []
            while index + 1 + consumed < len(tokens):
                ret_token = tokens[index + 1 + consumed]
                from .basic_commands import BasicCommandHandler
                if ret_token in BasicCommandHandler.KNOWN_COMMANDS:
                    break
                return_vars.append(ret_token)
                consumed += 1
            
            # Call module function with args and returns
            ModuleHandler.call_module_function(state, module_name, inner_name, args, return_vars, execute_block)
            return consumed
        
        # Find the function definition
        func_def = None
        if func_name in state.functions:
            func_def = state.functions[func_name]
        elif state.parent_state and func_name in state.parent_state.functions:
            func_def = state.parent_state.functions[func_name]
        else:
            state.add_error(f"Function '{func_name}' is not defined. Use 'def {func_name} ... end' to define it first.")
            return 1
        
        # Handle both old format (list of tokens) and new format (dict with params/body)
        if isinstance(func_def, list):
            # Old format: just execute the body
            execute_block(func_def)
            return 1
        
        # New format with parameters
        params = func_def['params']
        body = func_def['body']
        
        # Collect arguments (tokens after function name, before return variable names)
        # We need to figure out how many are args vs return vars
        # Args come first, return vars come after all args
        args = []
        return_var_names = []
        consumed = 1  # Start at 1 for function name
        
        # Collect arguments (same number as parameters)
        # Don't stop early for KNOWN_COMMANDS since variables can have those names
        for i in range(len(params)):
            if index + 1 + consumed >= len(tokens):
                break
            arg_token = tokens[index + 1 + consumed]
            args.append(arg_token)
            consumed += 1
        
        # Remaining tokens are return variable names
        while index + 1 + consumed < len(tokens):
            token = tokens[index + 1 + consumed]
            from .basic_commands import BasicCommandHandler
            if token in BasicCommandHandler.KNOWN_COMMANDS:
                break
            return_var_names.append(token)
            consumed += 1
        
        # Save current variable state (for local scope)
        saved_vars = {}
        saved_strings = {}
        for param in params:
            if param in state.variables:
                saved_vars[param] = state.variables[param]
            if param in state.strings:
                saved_strings[param] = state.strings[param]
        
        # Bind arguments to parameters
        for i, param in enumerate(params):
            if i < len(args):
                # Resolve argument value
                arg_token = args[i]
                # If the argument is a string variable, bind it as a string
                if arg_token in state.strings:
                    state.strings[param] = state.strings[arg_token]
                else:
                    arg_value = ControlFlowHandler._resolve_arg_value(state, arg_token)
                    state.variables[param] = arg_value
            else:
                # Not enough arguments provided
                state.add_error(f"Function '{func_name}' expects {len(params)} arguments, got {len(args)}")
                return consumed
        
        # Clear return values before executing
        state.return_values.clear()
        
        # Clear should_return flag for this function call
        state.should_return = False
        
        # Execute the function body
        execute_block(body)
        
        # Clear should_return flag after function execution
        state.should_return = False
        
        # Restore parameter variables (clean up local scope)
        for param in params:
            if param in saved_vars:
                state.variables[param] = saved_vars[param]
            else:
                state.variables.pop(param, None)
            
            if param in saved_strings:
                state.strings[param] = saved_strings[param]
            else:
                state.strings.pop(param, None)
        
        # Assign return values to return variables
        for i, var_name in enumerate(return_var_names):
            if i < len(state.return_values):
                value = state.return_values[i]
                # If it's a string, store in strings; if numeric, store in variables
                if isinstance(value, str):
                    try:
                        # Try to parse as number
                        state.variables[var_name] = int(value)
                    except ValueError:
                        # It's a string
                        state.strings[var_name] = value
                else:
                    state.variables[var_name] = value
            else:
                # Not enough return values - set to 0/empty
                state.variables[var_name] = 0
        
        return consumed

    @staticmethod
    def _resolve_arg_value(state: InterpreterState, token: str) -> Union[int, str]:
        """Resolve an argument token to its actual value."""
        # Check if it's a quoted string
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        
        # Check if it's a string variable
        if token in state.strings:
            return state.strings[token]
        
        # Check if it's a numeric variable
        if token in state.variables:
            return state.variables[token]
        
        # Try to parse as integer
        try:
            return int(token)
        except ValueError:
            pass
        
        # Try to parse as float and convert to int
        try:
            return int(float(token))
        except ValueError:
            pass
        
        # If we can't resolve it, treat as 0
        return 0
    
    @staticmethod
    def _split_module_call(func_name: str) -> Optional[Tuple[str, str]]:
        if "::" in func_name:
            parts = func_name.rsplit("::", 1)
        elif "." in func_name:
            parts = func_name.rsplit(".", 1)
        else:
            return None

        if len(parts) != 2 or not parts[0] or not parts[1]:
            return None
        return parts[0], parts[1]

    @staticmethod
    def _resolve_match_value(state: InterpreterState, token: Optional[str]) -> Optional[object]:
        if token is None:
            return None
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        try:
            return int(token)
        except ValueError:
            pass

        if token in state.strings:
            return state.strings[token]
        if state.has_variable(token):
            return state.get_variable(token)

        state.add_error(f"Unknown identifier or value '{token}' in match expression.")
        return None

    @staticmethod
    def _evaluate_match(selector: object, operator: str, pattern: object, state: InterpreterState) -> Tuple[bool, bool]:
        if operator in {"==", "!="}:
            if operator == "==":
                return selector == pattern, True
            return selector != pattern, True

        if not isinstance(selector, int) or not isinstance(pattern, int):
            state.add_error("Numeric comparison in match requires integer operands.")
            return False, False

        if operator == ">":
            return selector > pattern, True
        if operator == "<":
            return selector < pattern, True
        if operator == ">=":
            return selector >= pattern, True
        if operator == "<=":
            return selector <= pattern, True

        state.add_error(f"Unsupported match operator '{operator}'.")
        return False, False

    @staticmethod
    def _extract_error_message(line: str) -> str:
        prefix = "[Error: "
        if line.startswith(prefix) and line.endswith("]"):
            return line[len(prefix):-1].strip()
        if line.startswith(prefix):
            return line[len(prefix):].strip()
        return line
    
    @staticmethod
    def _evaluate_condition(var_value: int, op: str, compare_val: int) -> bool:
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
