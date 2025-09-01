# techlang/blocks.py

from typing import List, Tuple


class BlockCollector:
    """Handles collection of code blocks in TechLang."""
    
    @staticmethod
    def collect_block(start_index: int, tokens_list: List[str]) -> Tuple[List[str], int]:
        """
        Collect a block of tokens between 'def' and 'end' or 'loop' and 'end'.
        
        Args:
            start_index: Starting index in the tokens list
            tokens_list: List of all tokens
            
        Returns:
            Tuple of (block_tokens, end_index) where block_tokens is the collected tokens
            and end_index is the position after the block
        """
        block: List[str] = []
        depth: int = 0
        i: int = start_index
        
        while i < len(tokens_list):
            token: str = tokens_list[i]
            
            if token == "def":
                depth += 1
            elif token == "end":
                if depth == 0:
                    break
                depth -= 1
            
            block.append(token)
            i += 1
        
        return block, i
