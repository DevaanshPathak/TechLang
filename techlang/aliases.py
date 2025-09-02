from typing import List, Set
from .core import InterpreterState


class AliasHandler:
    # Two-pass aliasing: collect definitions, then expand recursively
    
    @staticmethod
    def process_aliases(tokens: List[str], state: InterpreterState) -> List[str]:
        # First pass: collect alias definitions
        AliasHandler._collect_aliases(tokens, state)
        
        # Second pass: expand aliases
        return AliasHandler._expand_aliases(tokens, state)
    
    @staticmethod
    def _collect_aliases(tokens: List[str], state: InterpreterState) -> None:
        i = 0
        while i < len(tokens):
            if tokens[i] == "alias" and i + 2 < len(tokens):
                state.aliases[tokens[i + 1]] = tokens[i + 2]
                i += 3
            else:
                i += 1
    
    @staticmethod
    def _expand_aliases(tokens: List[str], state: InterpreterState) -> List[str]:
        expanded_tokens = []
        
        for token in tokens:
            if token != "alias":
                expanded_token = AliasHandler._expand_single_alias(token, state)
                expanded_tokens.append(expanded_token)
        
        return expanded_tokens
    
    @staticmethod
    def _expand_single_alias(token: str, state: InterpreterState) -> str:
        # Detect cycles to avoid infinite expansion
        seen: Set[str] = set()
        current_token = token
        
        while current_token in state.aliases:
            if current_token in seen:  # Prevent infinite loop
                break
            seen.add(current_token)
            current_token = state.aliases[current_token]
        
        return current_token
