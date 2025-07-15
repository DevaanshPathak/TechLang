# techlang/parser.py

def parse(code: str) -> list:
    """
    Parses TechLang code into a list of commands.
    - Supports comments (lines starting with '#')
    - Ignores blank lines
    - Handles both space-separated and newline-separated commands
    """
    commands = []
    for line in code.strip().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue  # skip empty or commented lines
        parts = line.split()  # split by spaces
        commands.extend(parts)
    return commands
