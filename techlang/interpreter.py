# techlang/interpreter.py

from techlang.parser import parse

def run(code: str) -> str:
    """
    Interprets and runs TechLang code.
    Returns output as a string.
    """
    value = 0
    stack = []
    output = []

    for cmd in parse(code):
        if cmd == "boot":
            value = 0
        elif cmd == "ping":
            value += 1
        elif cmd == "crash":
            value -= 1
        elif cmd == "reboot":
            value = 0
        elif cmd == "print":
            output.append(str(value))
        elif cmd == "upload":
            stack.append(value)
        elif cmd == "download":
            if stack:
                value = stack.pop()
            else:
                output.append("[stack empty]")
        elif cmd == "debug":
            output.append(f"Stack: {stack}")
        elif cmd == "hack":
            value *= 2
        elif cmd == "lag":
            import time
            time.sleep(1)
        elif cmd == "fork":
            stack.append(value)
        else:
            output.append(f"[unknown command: {cmd}]")

    return "\n".join(output)

if __name__ == "__main__":
    code = "boot ping ping upload ping print download print debug"
    print(run(code))
