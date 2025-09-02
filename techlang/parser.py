import re
from typing import List

def parse(code: str) -> List[str]:
    # Split source into tokens while keeping quoted strings intact
    commands: List[str] = []
    for line in code.strip().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Regex preserves quoted strings; everything else splits on whitespace
        parts = re.findall(r'"[^"]*"|\S+', line)
        commands.extend(parts)
    return commands
