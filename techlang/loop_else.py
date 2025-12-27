"""
Loop Else (with break/continue) for TechLang.

Provides loop-else support with:
- loop_else <count> do ... else ... end - Loop with else (runs if no break)
- while_else <var> <op> <val> do ... else ... end - While with else
- break - Exit loop (prevents else from running)
- continue - Skip to next iteration
"""

from typing import Dict, List, Optional, Any, Callable
from .core import InterpreterState


class LoopElseHandler:
    """Handles loop-else operations in TechLang."""
    
    @staticmethod
    def _check_condition(left: Any, op: str, right: Any) -> bool:
        """Check a condition between two values."""
        # Type coercion for comparisons
        if isinstance(left, str) and isinstance(right, (int, float)):
            try:
                left = float(left) if '.' in str(left) and '.' in left else int(left)
            except (ValueError, TypeError):
                pass
        elif isinstance(left, (int, float)) and isinstance(right, str):
            try:
                right = float(right) if '.' in right else int(right)
            except ValueError:
                pass
        
        op_map = {
            "eq": "==", "ne": "!=", "gt": ">", "lt": "<", "ge": ">=", "le": "<="
        }
        op = op_map.get(op, op)
        
        if op == "==":
            return left == right
        elif op == "!=":
            return left != right
        elif op == ">":
            return left > right
        elif op == "<":
            return left < right
        elif op == ">=":
            return left >= right
        elif op == "<=":
            return left <= right
        
        return False
    
    @staticmethod
    def handle_break(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Handle break command to exit loops.
        Syntax: break
        
        Sets state.loop_break = True to signal loop handlers to exit.
        """
        state.loop_break = True
        return 0
    
    @staticmethod
    def handle_continue(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Handle continue command to skip to next iteration.
        Syntax: continue
        
        Sets state.loop_continue = True to signal loop handlers to skip.
        """
        state.loop_continue = True
        return 0
    
    @staticmethod
    def handle_loop_else(state: InterpreterState, tokens: List[str], index: int, 
                         execute_block: Callable) -> int:
        """
        Handle loop with else block that runs if loop completes without break.
        Syntax: loop_else <count> do ... else ... end
        
        Example:
            loop_else 10 do
                if i == target
                    print "Found!"
                    break
                end
            else
                print "Not found"
            end
        """
        if index + 2 >= len(tokens):
            state.add_error("loop_else requires count. Use: loop_else <count> do ... else ... end")
            return 0
        
        count_token = tokens[index + 1]
        
        # Resolve count
        try:
            count = int(count_token)
        except ValueError:
            count = state.get_variable(count_token, None)
            if not isinstance(count, (int, float)):
                state.add_error(f"loop_else count must be a number, got '{count_token}'")
                return 0
            count = int(count)
        
        cursor = index + 2
        
        # Skip optional 'do'
        if cursor < len(tokens) and tokens[cursor] == "do":
            cursor += 1
        
        # Find 'else' and 'end', collecting loop block and else block
        loop_block = []
        else_block = []
        depth = 1
        in_else = False
        
        while cursor < len(tokens) and depth > 0:
            tok = tokens[cursor]
            
            # Track block depth
            if tok in ("loop_else", "while_else", "if", "loop", "while", "def", "switch", "try", "match", "if_chain"):
                if in_else:
                    else_block.append(tok)
                else:
                    loop_block.append(tok)
                depth += 1
            elif tok == "end":
                depth -= 1
                if depth == 0:
                    break
                if in_else:
                    else_block.append(tok)
                else:
                    loop_block.append(tok)
            elif tok == "else" and depth == 1:
                in_else = True
            else:
                if in_else:
                    else_block.append(tok)
                else:
                    loop_block.append(tok)
            cursor += 1
        
        end_index = cursor + 1  # Include 'end'
        
        # Initialize loop control flags
        old_break = getattr(state, 'loop_break', False)
        state.loop_break = False
        loop_broken = False
        
        # Execute loop
        for i in range(count):
            # Set loop variable 'i' 
            state.set_variable('i', i)
            
            # Check for continue from previous iteration
            if hasattr(state, 'loop_continue'):
                state.loop_continue = False
            
            execute_block(loop_block)
            
            # Check for break
            if getattr(state, 'loop_break', False):
                loop_broken = True
                state.loop_break = False  # Reset for nested loops
                break
                
            # Check for continue
            if getattr(state, 'loop_continue', False):
                state.loop_continue = False
                continue
        
        # Execute else block if loop completed without break
        if not loop_broken and else_block:
            execute_block(else_block)
        
        # Restore break flag
        state.loop_break = old_break
        
        # Return consumed count (executor adds 1, so we return end_index - index - 1)
        return end_index - index - 1
    
    @staticmethod
    def handle_while_else(state: InterpreterState, tokens: List[str], index: int, 
                          execute_block: Callable) -> int:
        """
        Handle while loop with else block that runs if loop completes without break.
        Syntax: while_else <var> <op> <val> do ... else ... end
        
        Example:
            set i 0
            while_else i < 10 do
                if arr[i] == target
                    print "Found!"
                    break
                end
                add i 1
            else
                print "Not found"
            end
        """
        if index + 4 >= len(tokens):
            state.add_error("while_else requires: while_else <var> <op> <val> do ... else ... end")
            return 0
        
        varname = tokens[index + 1]
        op = tokens[index + 2]
        compare_token = tokens[index + 3]
        
        cursor = index + 4
        
        # Skip optional 'do'
        if cursor < len(tokens) and tokens[cursor] == "do":
            cursor += 1
        
        # Resolve comparison value
        try:
            compare_val = int(compare_token)
        except ValueError:
            compare_val = state.get_variable(compare_token, None)
            if compare_val is None:
                state.add_error(f"while_else compare value must be a number or variable, got '{compare_token}'")
                return 0
        
        # Find 'else' and 'end', collecting while block and else block
        while_block = []
        else_block = []
        depth = 1
        in_else = False
        
        while cursor < len(tokens) and depth > 0:
            tok = tokens[cursor]
            
            if tok in ("loop_else", "while_else", "if", "loop", "while", "def", "switch", "try", "match", "if_chain"):
                if in_else:
                    else_block.append(tok)
                else:
                    while_block.append(tok)
                depth += 1
            elif tok == "end":
                depth -= 1
                if depth == 0:
                    break
                if in_else:
                    else_block.append(tok)
                else:
                    while_block.append(tok)
            elif tok == "else" and depth == 1:
                in_else = True
            else:
                if in_else:
                    else_block.append(tok)
                else:
                    while_block.append(tok)
            cursor += 1
        
        end_index = cursor + 1
        
        # Initialize loop control flags
        old_break = getattr(state, 'loop_break', False)
        state.loop_break = False
        loop_broken = False
        
        # Execute while loop
        max_iterations = 10000
        iterations = 0
        
        while iterations < max_iterations:
            # Check condition
            var_value = state.get_variable(varname, 0)
            if not LoopElseHandler._check_condition(var_value, op, compare_val):
                break
            
            # Reset continue flag
            if hasattr(state, 'loop_continue'):
                state.loop_continue = False
            
            execute_block(while_block)
            iterations += 1
            
            # Check for break
            if getattr(state, 'loop_break', False):
                loop_broken = True
                state.loop_break = False  # Reset for nested loops
                break
            
            # Check for continue
            if getattr(state, 'loop_continue', False):
                state.loop_continue = False
                continue
        
        if iterations >= max_iterations:
            state.add_error(f"while_else exceeded maximum iterations ({max_iterations})")
        
        # Execute else block if loop completed without break
        if not loop_broken and else_block:
            execute_block(else_block)
        
        # Restore break flag
        state.loop_break = old_break
        
        # Return consumed count (executor adds 1, so we return end_index - index - 1)
        return end_index - index - 1
