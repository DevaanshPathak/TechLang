from typing import Callable, List, Optional, Tuple
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
            state.add_error("Invalid 'def' command. Use: def <function_name> ... end")
            return 0
        
        func_name = tokens[index + 1]
        start_index = index + 2  # Start after 'def' and function name
        
        # Store the function body tokens for later calls
        func_block, end_index = BlockCollector.collect_block(start_index, tokens)
        
        state.functions[func_name] = func_block
        
        # Return total tokens consumed: 'def' + func_name + func_body + 'end'
        return end_index - index
    
    @staticmethod
    def handle_call(state: InterpreterState, tokens: List[str], index: int, execute_block: Callable) -> int:
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'call' command. Use: call <function_name>")
            return 0
        
        func_name = tokens[index + 1]

        module_call = ControlFlowHandler._split_module_call(func_name)
        if module_call is not None:
            module_name, inner_name = module_call
            from .imports import ModuleHandler  # local import to avoid circular dependencies

            ModuleHandler.call_module_function(state, module_name, inner_name)
            return 1
        
        if func_name in state.functions:
            execute_block(state.functions[func_name])
        elif state.parent_state and func_name in state.parent_state.functions:
            execute_block(state.parent_state.functions[func_name])
        else:
            state.add_error(f"Function '{func_name}' is not defined. Use 'def {func_name} ... end' to define it first.")
        
        return 1  # Consume function name

    @staticmethod
    def _split_module_call(func_name: str) -> Optional[Tuple[str, str]]:
        if "::" in func_name:
            parts = func_name.split("::", 1)
        elif "." in func_name:
            parts = func_name.split(".", 1)
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
