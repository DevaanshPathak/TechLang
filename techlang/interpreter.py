from techlang.parser import parse

def run(code: str) -> str:
    """
    Interprets and runs TechLang code.
    Returns output as a string.
    """
    tokens = parse(code)
    value = 0
    stack = []
    output = []
    variables = {}

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token == "boot":
            value = 0

        elif token == "ping":
            value += 1

        elif token == "crash":
            value -= 1

        elif token == "reboot":
            value = 0

        elif token == "print":
            # Safely check if next token is a variable (not a known command)
            if i + 1 < len(tokens):
                lookahead = tokens[i + 1]
                known_commands = {
                    "boot", "ping", "crash", "reboot", "print", "upload",
                    "download", "debug", "hack", "lag", "fork", "set", "add"
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

        elif token == "add":
            if i + 2 < len(tokens):
                varname = tokens[i + 1]
                try:
                    amount = int(tokens[i + 2])
                    if varname in variables:
                        variables[varname] += amount
                    else:
                        output.append(f"[undefined variable: {varname}]")
                    i += 2
                except ValueError:
                    output.append(f"[invalid number: {tokens[i+2]}]")
            else:
                output.append("[syntax error: add <var> <value>]")

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

        else:
            output.append(f"[unknown command: {token}]")

        i += 1

    return "\n".join(output)
