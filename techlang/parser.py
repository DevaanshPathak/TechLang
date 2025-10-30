import re
from typing import List

def parse(code: str) -> List[str]:
    """
    Parse TechLang source code into tokens.
    
    Supports three comment styles:
    - # single-line comments (original)
    - // single-line comments (C-style)
    - /* multi-line comments */ (C-style)
    """
    # First, remove all multi-line comments /* ... */
    code = _remove_multiline_comments(code)
    
    # Split source into tokens while keeping quoted strings intact
    commands: List[str] = []
    for line in code.strip().splitlines():
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # Remove single-line comments (# or //)
        # Handle comments that appear after code on the same line
        line = _remove_inline_comments(line)
        line = line.strip()
        
        # Skip if line became empty after comment removal
        if not line:
            continue
        
        # Regex preserves quoted strings; everything else splits on whitespace
        parts = re.findall(r'"[^"]*"|\S+', line)
        commands.extend(parts)
    return commands


def _remove_multiline_comments(code: str) -> str:
    """Remove /* ... */ style multi-line comments from code."""
    result = []
    i = 0
    length = len(code)
    
    while i < length:
        # Check for start of multi-line comment
        if i < length - 1 and code[i:i+2] == '/*':
            # Find the end of the comment
            end = code.find('*/', i + 2)
            if end != -1:
                # Skip to after the closing */
                i = end + 2
            else:
                # Unclosed comment - skip rest of file
                break
        else:
            result.append(code[i])
            i += 1
    
    return ''.join(result)


def _remove_inline_comments(line: str) -> str:
    """
    Remove # or // comments from a line, but preserve them inside quoted strings.
    Returns the line with comments removed.
    """
    result = []
    i = 0
    length = len(line)
    in_string = False
    
    while i < length:
        char = line[i]
        
        # Toggle string state when we see unescaped quotes
        if char == '"' and (i == 0 or line[i-1] != '\\'):
            in_string = not in_string
            result.append(char)
            i += 1
            continue
        
        # If we're in a string, keep everything
        if in_string:
            result.append(char)
            i += 1
            continue
        
        # Check for // comment
        if i < length - 1 and line[i:i+2] == '//':
            # Rest of line is a comment
            break
        
        # Check for # comment
        if char == '#':
            # Rest of line is a comment
            break
        
        result.append(char)
        i += 1
    
    return ''.join(result)
