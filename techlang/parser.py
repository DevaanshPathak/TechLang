# techlang/parser.py

from typing import List

def parse(code: str) -> List[str]:
    """
    Parses TechLang code into a list of commands.

    - Supports comments (lines starting with '#')
    - Ignores blank lines
    - Handles both space-separated and newline-separated commands

    Args:
        code (str): The TechLang source code as a string.

    Returns:
        List[str]: A flat list of command tokens.
    """
    commands: List[str] = []
    for line in code.strip().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue  # skip empty or commented lines
        parts = line.split()  # split by spaces
        commands.extend(parts)
    return commands
