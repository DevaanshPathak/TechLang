from typing import List, Tuple


class BlockCollector:
    # Collect tokens until a matching 'end', supporting nested blocks (def/if/loop/while)
    
    @staticmethod
    def collect_block(start_index: int, tokens_list: List[str]) -> Tuple[List[str], int]:
        block: List[str] = []
        depth: int = 0
        i: int = start_index
        
        while i < len(tokens_list):
            token: str = tokens_list[i]
            
            # Any of these tokens start a nested block
            if token in {"def", "if", "loop", "while", "switch", "try"}:
                depth += 1
            elif token == "end":
                if depth == 0:
                    break
                depth -= 1
            
            block.append(token)
            i += 1
        
        return block, i
