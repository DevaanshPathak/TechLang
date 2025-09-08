from typing import List, Tuple, Callable
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
        while i < len(try_body):
            t = try_body[i]
            if t in {"def", "if", "loop", "while", "switch", "try"}:
                nested_depth += 1
            elif t == "end" and nested_depth > 0:
                nested_depth -= 1
            if t == "catch" and nested_depth == 0 and not found_catch:
                found_catch = True
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
        error_emitted = any(line.startswith("[Error:") for line in state.output[before_len:])
        if error_emitted and catch_block:
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
        
        if func_name in state.functions:
            execute_block(state.functions[func_name])
        else:
            state.add_error(f"Function '{func_name}' is not defined. Use 'def {func_name} ... end' to define it first.")
        
        return 1  # Consume function name
    
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
