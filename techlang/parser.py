# techlang/parser.py

import re
from typing import List

def parse(code: str) -> List[str]:
    """
    Parses TechLang code into a list of commands.

    - Supports comments (lines starting with '#')
    - Ignores blank lines
    - Handles both space-separated and newline-separated commands
    - Preserves quoted strings as single tokens

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
        
        # Use regex to split by spaces but preserve quoted strings
        parts = re.findall(r'"[^"]*"|\S+', line)
        commands.extend(parts)
    return commands
