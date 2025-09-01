# techlang/interpreter.py

from techlang.parser import parse
import os
import time
from typing import List, Optional, Set, Dict, Any, Tuple

def run(code: str, inputs: Optional[List[str]] = None, loaded_files: Optional[Set[str]] = None) -> str:
    if loaded_files is None:
        loaded_files = set()

    tokens: List[str] = parse(code)
    value: int = 0
    stack: List[int] = []
    output: List[str] = []
    variables: Dict[str, Any] = {}
    functions: Dict[str, List[str]] = {}
    aliases: Dict[str, str] = {}
    input_queue: List[str] = inputs or []

    def handle_import(filename_token: str) -> List[str]:
        if not filename_token.endswith(".tl"):
            filename_token += ".tl"
        if filename_token in loaded_files:
            return []
        loaded_files.add(filename_token)
        try:
            with open(filename_token, "r") as f:
                imported_code: str = f.read()
            return parse(imported_code)
        except FileNotFoundError:
            return [f"[Error: File not found '{filename_token}']"]

    def collect_block(start_index: int, tokens_list: List[str]) -> Tuple[List[str], int]:
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

    # --- ALIAS PROCESSING ---
    i: int = 0
    while i < len(tokens):
        if tokens[i] == "alias" and i + 2 < len(tokens):
            aliases[tokens[i + 1]] = tokens[i + 2]
            i += 3
        else:
            i += 1

    # Fully expand aliases recursively
    def expand_alias(token: str) -> str:
        seen: Set[str] = set()
        while token in aliases:
            if token in seen:  # prevent infinite loop
                break
            seen.add(token)
            token = aliases[token]
        return token

    tokens = [expand_alias(token) for token in tokens if token != "alias"]

    # --- INTERNAL EXECUTE BLOCK FUNCTION ---
    def execute_block(block_tokens: List[str]):
        nonlocal value, stack, variables, functions, input_queue, output
        j = 0
        while j < len(block_tokens):
            token = block_tokens[j]

            if token == "boot":
                value = 0
            elif token == "ping":
                value += 1
            elif token == "crash":
                value -= 1
            elif token == "reboot":
                value = 0
            elif token == "print":
                lookahead: Optional[str] = block_tokens[j + 1] if j + 1 < len(block_tokens) else None
                known_commands: Set[str] = {
                    "boot", "ping", "crash", "reboot", "print", "upload",
                    "download", "debug", "hack", "lag", "fork", "set", "add",
                    "mul", "sub", "div", "loop", "end", "if", "def", "call", "input", "alias", "import"
                }
                if lookahead and lookahead.isalpha() and lookahead not in known_commands:
                    output.append(str(variables.get(lookahead, f"[Error: Undefined variable '{lookahead}']")))
                    j += 1
                else:
                    output.append(str(value))
            elif token == "set":
                if j + 2 < len(block_tokens):
                    varname: str = block_tokens[j + 1]
                    try:
                        varvalue: int = int(block_tokens[j + 2])
                        variables[varname] = varvalue
                        j += 2
                    except ValueError:
                        output.append(f"[Error: Expected a number, got '{block_tokens[j+2]}']")
                else:
                    output.append("[Error: Expected syntax 'set <var> <value>']")
            elif token in {"add", "mul", "sub", "div"}:
                if j + 2 < len(block_tokens):
                    varname: str = block_tokens[j + 1]
                    try:
                        amount: int = int(block_tokens[j + 2])
                        if varname in variables:
                            if token == "add":
                                variables[varname] += amount
                            elif token == "mul":
                                variables[varname] *= amount
                            elif token == "sub":
                                variables[varname] -= amount
                            elif token == "div":
                                if amount != 0:
                                    variables[varname] //= amount
                                else:
                                    output.append("[Error: Division by zero]")
                        else:
                            output.append(f"[Error: Undefined variable '{varname}']")
                        j += 2
                    except ValueError:
                        output.append(f"[Error: Expected a number, got '{block_tokens[j+2]}']")
                else:
                    output.append(f"[Error: Expected syntax '{token} <var> <value>']")
            elif token == "input":
                if j + 1 < len(block_tokens):
                    varname: str = block_tokens[j + 1]
                    if input_queue:
                        variables[varname] = input_queue.pop(0)
                    else:
                        try:
                            variables[varname] = input(f"Enter value for {varname}: ")
                        except EOFError:
                            output.append(f"[Error: Input failed for '{varname}']")
                    j += 1
                else:
                    output.append("[Error: Expected syntax 'input <varname>']")
            elif token == "upload":
                stack.append(value)
            elif token == "download":
                if stack:
                    value = stack.pop()
                else:
                    output.append("[Error: Stack is empty]")
            elif token == "debug":
                output.append(f"Stack: {stack}")
                output.append(f"Vars: {variables}")
            elif token == "hack":
                value *= 2
            elif token == "lag":
                time.sleep(1)
            elif token == "fork":
                stack.append(value)
            elif token == "loop":
                if j + 1 < len(block_tokens):
                    loop_count_token: str = block_tokens[j + 1]
                    j += 2
                    loop_block, end_index = collect_block(j, block_tokens)
                    j = end_index
                    try:
                        loop_count: int = int(loop_count_token)
                    except ValueError:
                        loop_count = variables.get(loop_count_token)
                        if loop_count is None:
                            output.append(f"[Error: Loop count must be a number or existing variable, got '{loop_count_token}']")
                            continue
                    for _ in range(loop_count):
                        execute_block(loop_block)
                else:
                    output.append("[Error: Expected syntax 'loop <count>']")
            elif token == "if":
                if j + 3 < len(block_tokens):
                    varname: str = block_tokens[j + 1]
                    op: str = block_tokens[j + 2]
                    try:
                        compare_val: int = int(block_tokens[j + 3])
                    except ValueError:
                        output.append(f"[Error: Expected a number for comparison, got '{block_tokens[j+3]}']")
                        break
                    var_value: int = variables.get(varname, 0)
                    condition_met: bool = (
                        (op == "==" and var_value == compare_val) or
                        (op == "!=" and var_value != compare_val) or
                        (op == ">" and var_value > compare_val) or
                        (op == "<" and var_value < compare_val) or
                        (op == ">=" and var_value >= compare_val) or
                        (op == "<=" and var_value <= compare_val)
                    )
                    j += 4
                    if_block, end_index = collect_block(j, block_tokens)
                    j = end_index
                    if condition_met:
                        execute_block(if_block)
                else:
                    output.append("[Error: Expected syntax 'if <var> <op> <value>']")
            elif token == "def":
                if j + 1 < len(block_tokens):
                    func_name: str = block_tokens[j + 1]
                    func_block, end_index = collect_block(j + 2, block_tokens)
                    functions[func_name] = func_block
                    j = end_index
                else:
                    output.append("[Error: Expected syntax 'def <name> ... end']")
            elif token == "call":
                if j + 1 < len(block_tokens):
                    func_name: str = block_tokens[j + 1]
                    if func_name in functions:
                        execute_block(functions[func_name])
                    else:
                        output.append(f"[Error: Undefined function '{func_name}']")
                    j += 1
                else:
                    output.append("[Error: Expected syntax 'call <function>']")
            elif token == "end":
                pass
            else:
                output.append(f"[Error: Unknown command '{token}']")

            j += 1

    # --- RUN MAIN TOKENS ---
    execute_block(tokens)

    return "\n".join(output)
