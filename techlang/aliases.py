# techlang/aliases.py

from typing import List, Set
from .core import InterpreterState


class AliasHandler:
    """Handles alias processing in TechLang."""
    
    @staticmethod
    def process_aliases(tokens: List[str], state: InterpreterState) -> List[str]:
        """
        Process alias definitions and expand aliases in tokens.
        
        Args:
            tokens: List of tokens to process
            state: The interpreter state
            
        Returns:
            List of tokens with aliases expanded
        """
        # First pass: collect alias definitions
        AliasHandler._collect_aliases(tokens, state)
        
        # Second pass: expand aliases
        return AliasHandler._expand_aliases(tokens, state)
    
    @staticmethod
    def _collect_aliases(tokens: List[str], state: InterpreterState) -> None:
        """
        Collect alias definitions from tokens.
        
        Args:
            tokens: List of tokens
            state: The interpreter state
        """
        i = 0
        while i < len(tokens):
            if tokens[i] == "alias" and i + 2 < len(tokens):
                state.aliases[tokens[i + 1]] = tokens[i + 2]
                i += 3
            else:
                i += 1
    
    @staticmethod
    def _expand_aliases(tokens: List[str], state: InterpreterState) -> List[str]:
        """
        Expand aliases in tokens, handling recursive aliases.
        
        Args:
            tokens: List of tokens
            state: The interpreter state
            
        Returns:
            List of tokens with aliases expanded
        """
        expanded_tokens = []
        
        for token in tokens:
            if token != "alias":
                expanded_token = AliasHandler._expand_single_alias(token, state)
                expanded_tokens.append(expanded_token)
        
        return expanded_tokens
    
    @staticmethod
    def _expand_single_alias(token: str, state: InterpreterState) -> str:
        """
        Expand a single alias token, handling recursive aliases.
        
        Args:
            token: The token to expand
            state: The interpreter state
            
        Returns:
            The expanded token value
        """
        seen: Set[str] = set()
        current_token = token
        
        while current_token in state.aliases:
            if current_token in seen:  # Prevent infinite loop
                break
            seen.add(current_token)
            current_token = state.aliases[current_token]
        
        return current_token
