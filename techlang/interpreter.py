from techlang.parser import parse
import os

def run(code: str, inputs: list[str] = None, loaded_files: set[str] = None) -> str:
    if loaded_files is None:
        loaded_files = set()

    tokens = parse(code)
    value = 0
    stack = []
    output = []
    variables = {}
    functions = {}
    aliases = {}
    input_queue = inputs or []

    def handle_import(filename_token):
        if not filename_token.endswith(".tl"):
            filename_token += ".tl"
        if filename_token in loaded_files:
            return []
        loaded_files.add(filename_token)
        try:
            with open(filename_token, "r") as f:
                imported_code = f.read()
            return parse(imported_code)
        except FileNotFoundError:
            return [f"[import error: file not found {filename_token}]"]

    # First pass: extract alias definitions
    i = 0
    while i < len(tokens):
        if tokens[i] == "alias" and i + 2 < len(tokens):
            aliases[tokens[i + 1]] = tokens[i + 2]
            i += 3
        else:
            i += 1

    # Second pass: expand aliases
    tokens = [aliases.get(token, token) for token in tokens if token != "alias"]

    def collect_block(start_index):
        block = []
        depth = 0
        i = start_index
        while i < len(tokens):
            token = tokens[i]
            if token == "def":
                depth += 1
            elif token == "end":
                if depth == 0:
                    break
                depth -= 1
            block.append(token)
            i += 1
        return block, i

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token == "import" and i + 1 < len(tokens):
            filename = tokens[i + 1]
            imported_tokens = handle_import(filename)
            tokens = tokens[:i] + imported_tokens + tokens[i + 2:]
            continue

        if token == "boot":
            value = 0

        elif token == "ping":
            value += 1

        elif token == "crash":
            value -= 1

        elif token == "reboot":
            value = 0

        elif token == "print":
            if i + 1 < len(tokens):
                lookahead = tokens[i + 1]
                known_commands = {
                    "boot", "ping", "crash", "reboot", "print", "upload",
                    "download", "debug", "hack", "lag", "fork", "set", "add",
                    "mul", "sub", "div", "loop", "end", "if", "def", "call", "input", "alias", "import"
                }
                if lookahead.isalpha() and lookahead not in known_commands:
                    output.append(str(variables.get(lookahead, f"[undefined variable: {lookahead}]")))
                    i += 1
                else:
                    output.append(str(value))
            else:
                output.append(str(value))

        elif token == "set":
            if i + 2 < len(tokens):
                varname = tokens[i + 1]
                try:
                    varvalue = int(tokens[i + 2])
                    variables[varname] = varvalue
                    i += 2
                except ValueError:
                    output.append(f"[invalid number: {tokens[i+2]}]")
            else:
                output.append("[syntax error: set <var> <value>]")

        elif token in {"add", "mul", "sub", "div"}:
            if i + 2 < len(tokens):
                varname = tokens[i + 1]
                try:
                    amount = int(tokens[i + 2])
                    if varname in variables:
                        if token == "add":
                            variables[varname] += amount
                        elif token == "mul":
                            variables[varname] *= amount
                        elif token == "sub":
                            variables[varname] -= amount
                        elif token == "div":
                            variables[varname] //= amount
                    else:
                        output.append(f"[undefined variable: {varname}]")
                    i += 2
                except ValueError:
                    output.append(f"[invalid number: {tokens[i+2]}]")
            else:
                output.append(f"[syntax error: {token} <var> <value>]")

        elif token == "input":
            if i + 1 < len(tokens):
                varname = tokens[i + 1]
                if input_queue:
                    variables[varname] = input_queue.pop(0)
                else:
                    try:
                        variables[varname] = input(f"Enter value for {varname}: ")
                    except EOFError:
                        output.append(f"[input error: {varname}]")
                i += 1
            else:
                output.append("[syntax error: input <varname>]")

        elif token == "loop":
            if i + 1 < len(tokens):
                loop_count_token = tokens[i + 1]
                i += 2
                block = []
                while i < len(tokens) and tokens[i] != "end":
                    block.append(tokens[i])
                    i += 1
                if i < len(tokens) and tokens[i] == "end":
                    i += 1
                else:
                    output.append("[syntax error: missing 'end' for loop]")
                    break

                try:
                    loop_count = int(loop_count_token)
                except ValueError:
                    loop_count = variables.get(loop_count_token, 0)

                for _ in range(loop_count):
                    inner_i = 0
                    while inner_i < len(block):
                        inner_token = block[inner_i]
                        if inner_token == "ping":
                            value += 1
                        elif inner_token == "crash":
                            value -= 1
                        elif inner_token == "print":
                            output.append(str(value))
                        elif inner_token == "upload":
                            stack.append(value)
                        elif inner_token == "download":
                            if stack:
                                value = stack.pop()
                            else:
                                output.append("[stack empty]")
                        elif inner_token == "set":
                            if inner_i + 2 < len(block):
                                var = block[inner_i + 1]
                                try:
                                    val = int(block[inner_i + 2])
                                    variables[var] = val
                                except:
                                    output.append(f"[invalid number in loop: {block[inner_i+2]}]")
                                inner_i += 2
                        elif inner_token in {"add", "mul", "sub", "div"}:
                            if inner_i + 2 < len(block):
                                var = block[inner_i + 1]
                                try:
                                    amt = int(block[inner_i + 2])
                                    if var in variables:
                                        if inner_token == "add":
                                            variables[var] += amt
                                        elif inner_token == "mul":
                                            variables[var] *= amt
                                        elif inner_token == "sub":
                                            variables[var] -= amt
                                        elif inner_token == "div":
                                            variables[var] //= amt
                                    else:
                                        output.append(f"[undefined variable: {var}]")
                                except:
                                    output.append(f"[invalid number in loop: {block[inner_i+2]}]")
                                inner_i += 2
                        inner_i += 1
            else:
                output.append("[syntax error: loop <count>]")

        elif token == "if":
            if i + 3 < len(tokens):
                varname = tokens[i + 1]
                op = tokens[i + 2]
                try:
                    compare_val = int(tokens[i + 3])
                except ValueError:
                    output.append(f"[invalid number in if: {tokens[i+3]}]")
                    break

                var_value = variables.get(varname, 0)
                condition_met = (
                    (op == "==" and var_value == compare_val) or
                    (op == "!=" and var_value != compare_val) or
                    (op == ">" and var_value > compare_val) or
                    (op == "<" and var_value < compare_val) or
                    (op == ">=" and var_value >= compare_val) or
                    (op == "<=" and var_value <= compare_val)
                )

                i += 4
                block = []
                while i < len(tokens) and tokens[i] != "end":
                    block.append(tokens[i])
                    i += 1
                if i < len(tokens) and tokens[i] == "end":
                    i += 1
                else:
                    output.append("[syntax error: missing 'end' for if]")
                    break

                if condition_met:
                    output.extend(run(" ".join(block), inputs=input_queue, loaded_files=loaded_files).splitlines())
            else:
                output.append("[syntax error: if <var> <op> <value>]")

        elif token == "def":
            if i + 1 < len(tokens):
                func_name = tokens[i + 1]
                block, end_index = collect_block(i + 2)
                functions[func_name] = block
                i = end_index
            else:
                output.append("[syntax error: def <name> ... end]")

        elif token == "call":
            if i + 1 < len(tokens):
                func_name = tokens[i + 1]
                if func_name in functions:
                    func_tokens = functions[func_name]
                    tokens = tokens[:i + 2] + func_tokens + tokens[i + 2:]
                else:
                    output.append(f"[undefined function: {func_name}]")
                i += 1
            else:
                output.append("[syntax error: call <function>]")

        elif token == "upload":
            stack.append(value)

        elif token == "download":
            if stack:
                value = stack.pop()
            else:
                output.append("[stack empty]")

        elif token == "debug":
            output.append(f"Stack: {stack}")
            output.append(f"Vars: {variables}")

        elif token == "hack":
            value *= 2

        elif token == "lag":
            import time
            time.sleep(1)

        elif token == "fork":
            stack.append(value)

        elif token == "end":
            pass

        else:
            output.append(f"[unknown command: {token}]")

        i += 1

    return "\n".join(output)
