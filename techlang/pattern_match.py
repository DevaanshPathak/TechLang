"""
Full Pattern Matching

Extends the basic match statement with Python 3.10+ style pattern matching:
- OR patterns: case 1 | 2 | 3
- Array/list patterns: case [x, y] or case [first, *rest]
- Dict patterns: case {"key": value}
- Wildcard: case _
- Guard clauses: case x if x > 0

Commands:
- match_full <value> ... end - Enhanced pattern matching block
- case_or <val1> <val2> ... do ... end - Match any of the values
- case_list <var1> <var2> ... do ... end - Destructure list
- case_dict <key1:var1> <key2:var2> ... do ... end - Destructure dict
"""

from typing import List, Dict, Any, Optional, Tuple
from .core import InterpreterState


class PatternMatchHandler:
    """Handler for full pattern matching commands."""
    
    @staticmethod
    def handle_match_full(state: InterpreterState, tokens: List[str], index: int, execute_block) -> int:
        """
        Enhanced pattern matching with Python 3.10+ features.
        
        Syntax:
            match_full <value>
                case_or 1 2 3 do
                    print "small number"
                end
                case_list x y do
                    print "pair"
                end
                case_dict type:t name:n do
                    print "dict pattern"
                end
                case _ do
                    print "default"
                end
            end
        """
        if index + 1 >= len(tokens):
            state.add_error("match_full requires a value. Use: match_full <value> ... end")
            return 0
        
        value_token = tokens[index + 1]
        
        # Check if value_token is a keyword (not a valid value)
        if value_token in ("case", "case_or", "case_list", "case_dict", "end", "do"):
            state.add_error("match_full requires a value. Use: match_full <value> ... end")
            return 0
        
        match_value = PatternMatchHandler._resolve_value(state, value_token)
        
        # Collect entire match_full body (until matching end)
        body, end_index = PatternMatchHandler._collect_match_body(tokens, index + 2)
        
        # Process cases
        i = 0
        matched = False
        
        while i < len(body) and not matched:
            token = body[i]
            
            if token == "case_or":
                # OR pattern: case_or val1 val2 val3 do ... end
                values = []
                j = i + 1
                while j < len(body) and body[j] != "do":
                    values.append(PatternMatchHandler._resolve_value(state, body[j]))
                    j += 1
                
                if j < len(body) and body[j] == "do":
                    j += 1  # skip "do"
                
                if match_value in values:
                    # Find and execute the block
                    block, block_end = PatternMatchHandler._collect_case_block(body, j)
                    execute_block(block)
                    matched = True
                    i = block_end + 1
                else:
                    # Skip to next case
                    _, block_end = PatternMatchHandler._collect_case_block(body, j)
                    i = block_end + 1
            
            elif token == "case_list":
                # List destructuring: case_list x y z do ... end
                var_names = []
                j = i + 1
                rest_var = None
                while j < len(body) and body[j] != "do":
                    var = body[j]
                    if var.startswith("*"):
                        rest_var = var[1:]
                    else:
                        var_names.append(var)
                    j += 1
                
                if j < len(body) and body[j] == "do":
                    j += 1  # skip "do"
                
                # Check if match_value is an array
                if isinstance(match_value, list):
                    if rest_var:
                        # Has *rest syntax
                        if len(match_value) >= len(var_names):
                            for idx, vn in enumerate(var_names):
                                state.variables[vn] = match_value[idx]
                            state.arrays[rest_var] = match_value[len(var_names):]
                            block, block_end = PatternMatchHandler._collect_case_block(body, j)
                            execute_block(block)
                            matched = True
                            i = block_end + 1
                        else:
                            _, block_end = PatternMatchHandler._collect_case_block(body, j)
                            i = block_end + 1
                    else:
                        # Exact match
                        if len(match_value) == len(var_names):
                            for idx, vn in enumerate(var_names):
                                state.variables[vn] = match_value[idx]
                            block, block_end = PatternMatchHandler._collect_case_block(body, j)
                            execute_block(block)
                            matched = True
                            i = block_end + 1
                        else:
                            _, block_end = PatternMatchHandler._collect_case_block(body, j)
                            i = block_end + 1
                else:
                    _, block_end = PatternMatchHandler._collect_case_block(body, j)
                    i = block_end + 1
            
            elif token == "case_dict":
                # Dict destructuring: case_dict key1:var1 key2:var2 do ... end
                bindings = {}
                j = i + 1
                while j < len(body) and body[j] != "do":
                    binding = body[j]
                    if ":" in binding:
                        key, var = binding.split(":", 1)
                        bindings[key] = var
                    j += 1
                
                if j < len(body) and body[j] == "do":
                    j += 1  # skip "do"
                
                # Check if match_value is a dict
                if isinstance(match_value, dict):
                    if all(k in match_value for k in bindings.keys()):
                        for key, var in bindings.items():
                            val = match_value[key]
                            if isinstance(val, str):
                                state.strings[var] = val
                            else:
                                state.variables[var] = val
                        block, block_end = PatternMatchHandler._collect_case_block(body, j)
                        execute_block(block)
                        matched = True
                        i = block_end + 1
                    else:
                        _, block_end = PatternMatchHandler._collect_case_block(body, j)
                        i = block_end + 1
                else:
                    _, block_end = PatternMatchHandler._collect_case_block(body, j)
                    i = block_end + 1
            
            elif token == "case":
                # Simple value match or wildcard
                if i + 1 < len(body):
                    pattern = body[i + 1]
                    j = i + 2
                    
                    # Find "do"
                    while j < len(body) and body[j] != "do":
                        j += 1
                    
                    if j < len(body) and body[j] == "do":
                        j += 1  # skip "do"
                    
                    if pattern in ("_", "default"):
                        # Wildcard - always matches
                        block, block_end = PatternMatchHandler._collect_case_block(body, j)
                        execute_block(block)
                        matched = True
                        i = block_end + 1
                    else:
                        pattern_value = PatternMatchHandler._resolve_value(state, pattern)
                        if match_value == pattern_value:
                            block, block_end = PatternMatchHandler._collect_case_block(body, j)
                            execute_block(block)
                            matched = True
                            i = block_end + 1
                        else:
                            _, block_end = PatternMatchHandler._collect_case_block(body, j)
                            i = block_end + 1
                else:
                    i += 1
            else:
                i += 1
        
        return end_index - index
    
    @staticmethod
    def _collect_match_body(tokens: List[str], start: int) -> Tuple[List[str], int]:
        """Collect entire body of match_full until final 'end', including all case blocks."""
        body = []
        depth = 1  # Start at depth 1 because we're inside match_full
        i = start
        
        while i < len(tokens):
            token = tokens[i]
            
            # Track depth for ALL block-starting tokens
            if token in ("if", "loop", "while", "def", "match", "match_full", "switch", "try", 
                         "if_chain", "loop_else", "while_else", "case_or", "case_list", "case_dict"):
                depth += 1
                body.append(token)
            elif token == "case":
                # 'case' followed by 'do' is a block (like 'case _ do' or 'case 42 do')
                depth += 1
                body.append(token)
            elif token == "end":
                depth -= 1
                if depth == 0:
                    # This is the closing 'end' for match_full
                    return body, i
                else:
                    body.append(token)
            else:
                body.append(token)
            i += 1
        
        return body, i
    
    @staticmethod
    def _collect_case_block(body: List[str], start: int) -> Tuple[List[str], int]:
        """Collect tokens until 'end' at the same depth level or next case."""
        block = []
        depth = 1  # We're inside a case...do block
        i = start
        while i < len(body):
            token = body[i]
            
            # Check for start of new case at depth 1 (same level)
            if depth == 1 and token in ("case", "case_or", "case_list", "case_dict"):
                return block, i - 1
            
            if token in ("if", "loop", "while", "def", "match", "match_full", "switch", "try", 
                         "if_chain", "loop_else", "while_else"):
                depth += 1
                block.append(token)
            elif token == "end":
                depth -= 1
                if depth == 0:
                    # End of this case block
                    return block, i
                block.append(token)
            else:
                block.append(token)
            i += 1
        return block, i - 1
    
    @staticmethod
    def _resolve_value(state: InterpreterState, token: str) -> Any:
        """Resolve a token to its actual value."""
        # Strip quotes
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        
        # Check arrays
        if token in state.arrays:
            return state.arrays[token]
        
        # Check dicts
        if token in state.dictionaries:
            return state.dictionaries[token]
        
        # Check strings
        if token in state.strings:
            return state.strings[token]
        
        # Check variables
        if token in state.variables:
            return state.variables[token]
        
        # Numeric literal
        try:
            if "." in token:
                return float(token)
            return int(token)
        except ValueError:
            return token
