"""
Chained Comparisons for TechLang.

Provides chained comparison support with:
- if_chain <val1> <op1> <val2> <op2> <val3> ... do ... end
"""

from typing import Dict, List, Optional, Any, Callable
from .core import InterpreterState
from .blocks import BlockCollector


class ChainedComparisonHandler:
    """Handles chained comparison operations in TechLang."""
    
    @staticmethod
    def _resolve_value(state: InterpreterState, token: str) -> Any:
        """Resolve a token to its actual value."""
        # Quoted string
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        
        # Check variables first
        if state.has_variable(token):
            return state.get_variable(token)
        
        # Check strings
        if token in state.strings:
            return state.strings[token]
        
        # Try as integer
        try:
            return int(token)
        except ValueError:
            pass
        
        # Try as float
        try:
            return float(token)
        except ValueError:
            pass
        
        # Check if it's a variable name that just doesn't exist yet
        # Return 0 as default for non-existent variables (consistent with TechLang behavior)
        return 0
    
    @staticmethod
    def _check_condition(left: Any, op: str, right: Any) -> bool:
        """Check a condition between two values."""
        # Type coercion for comparisons
        if isinstance(left, str) and isinstance(right, (int, float)):
            try:
                left = float(left) if '.' in left else int(left)
            except ValueError:
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
    def handle_if_chain(state: InterpreterState, tokens: List[str], index: int, 
                        execute_block: Callable) -> int:
        """
        Handle chained comparisons like: if_chain 0 < x < 100 do ... end
        Syntax: if_chain <val1> <op1> <val2> <op2> <val3> [<op> <val>...] do ... end
        
        Example:
            if_chain 0 < x < 100 do
                print "x is in range"
            end
        """
        if index + 5 >= len(tokens):
            state.add_error("if_chain requires at least: if_chain <v1> <op1> <v2> <op2> <v3> do ... end")
            return 0
        
        cursor = index + 1
        values = []
        operators = []
        
        # Parse alternating values and operators until we hit 'do'
        while cursor < len(tokens):
            tok = tokens[cursor]
            if tok == "do":
                break
            
            if len(values) == len(operators):
                # Expecting a value
                values.append(ChainedComparisonHandler._resolve_value(state, tok))
            else:
                # Expecting an operator
                operators.append(tok)
            cursor += 1
        
        if cursor >= len(tokens) or tokens[cursor] != "do":
            state.add_error("if_chain requires 'do' before block")
            return 0
        
        if len(values) < 2 or len(operators) < 1:
            state.add_error("if_chain needs at least 2 values and 1 operator")
            return 0
        
        if len(values) != len(operators) + 1:
            state.add_error("if_chain has mismatched values and operators")
            return 0
        
        # Skip 'do'
        cursor += 1
        
        # Collect the block
        block, end_index = BlockCollector.collect_block(cursor, tokens)
        
        # Evaluate all chained comparisons (a op1 b AND b op2 c AND ...)
        all_true = True
        for i in range(len(operators)):
            left = values[i]
            op = operators[i]
            right = values[i + 1]
            
            if not ChainedComparisonHandler._check_condition(left, op, right):
                all_true = False
                break
        
        # Execute block if all conditions are true
        if all_true:
            execute_block(block)
        
        return end_index - index
