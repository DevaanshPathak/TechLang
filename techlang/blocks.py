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
            if token in {"def", "if", "loop", "while", "switch", "match", "match_full", "try", "macro", "if_chain", "loop_else", "while_else", "protocol", "abstract_class"}:
                depth += 1
                block.append(token)
                i += 1
                
                # For 'if' statements, skip the condition tokens (var op value)
                # so that 'end' used as a variable name isn't treated as block terminator
                if token == "if" and i + 2 < len(tokens_list):
                    # Append the next 3 tokens (variable, operator, value) without interpreting them
                    block.append(tokens_list[i])      # variable
                    block.append(tokens_list[i + 1])  # operator
                    block.append(tokens_list[i + 2])  # value (could be 'end' as variable name!)
                    i += 3
                # For 'if_chain', skip tokens until we reach 'do'
                elif token == "if_chain":
                    while i < len(tokens_list) and tokens_list[i] != "do":
                        block.append(tokens_list[i])
                        i += 1
                    if i < len(tokens_list):
                        block.append(tokens_list[i])  # append 'do'
                        i += 1
                continue
                
            elif token == "struct":
                next_token = tokens_list[i + 1] if i + 1 < len(tokens_list) else ""
                if next_token not in {"new", "set", "get", "dump"}:
                    depth += 1
            elif token == "end":
                if depth == 0:
                    break
                depth -= 1
            
            block.append(token)
            i += 1
        
        return block, i
