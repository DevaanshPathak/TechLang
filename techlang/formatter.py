"""
TechLang code formatter.

Tokenizes .tl files using parser.parse() and reflows blocks with consistent indentation.
"""

from typing import List, Tuple
import re


class TechLangFormatter:
    """Format TechLang source code with consistent indentation and spacing."""
    
    INDENT = "    "  # 4 spaces per level
    BLOCK_START_KEYWORDS = {'def', 'if', 'loop', 'while', 'switch', 'match', 'try', 'macro'}
    STRUCT_OPERATIONS = {'new', 'set', 'get', 'dump'}
    
    def __init__(self, indent_size: int = 4):
        """Initialize formatter with configurable indent size."""
        self.INDENT = " " * indent_size
    
    def format(self, source: str) -> str:
        """
        Format TechLang source code.
        
        Args:
            source: Raw TechLang source code
            
        Returns:
            Formatted source code with consistent indentation
        """
        lines = self._preprocess_lines(source)
        tokens = self._tokenize_with_context(lines)
        formatted_lines = self._format_tokens(tokens)
        return "\n".join(formatted_lines)
    
    def _preprocess_lines(self, source: str) -> List[Tuple[str, str]]:
        """
        Extract lines with their comments preserved.
        
        Returns list of (code, comment) tuples.
        """
        result = []
        for line in source.splitlines():
            # Preserve leading/trailing whitespace info but get clean content
            stripped = line.strip()
            
            if not stripped:
                result.append(("", ""))
                continue
            
            # Check for comments
            if stripped.startswith('#'):
                result.append(("", stripped))
                continue
            
            # Split inline comments (but not inside strings)
            code_part = stripped
            comment_part = ""
            
            # Simple approach: look for # outside of quoted strings
            in_string = False
            for i, char in enumerate(stripped):
                if char == '"' and (i == 0 or stripped[i-1] != '\\'):
                    in_string = not in_string
                elif char == '#' and not in_string:
                    code_part = stripped[:i].strip()
                    comment_part = stripped[i:].strip()
                    break
            
            result.append((code_part, comment_part))
        
        return result
    
    def _tokenize_with_context(self, lines: List[Tuple[str, str]]) -> List[Tuple[List[str], str]]:
        """
        Tokenize each line while preserving comments.
        
        Returns list of (tokens, comment) tuples.
        """
        result = []
        for code, comment in lines:
            if not code and not comment:
                result.append(([], ""))
            elif not code:
                result.append(([], comment))
            else:
                # Use regex to split while keeping quoted strings intact
                tokens = re.findall(r'"[^"]*"|\S+', code)
                result.append((tokens, comment))
        
        return result
    
    def _format_tokens(self, token_lines: List[Tuple[List[str], str]]) -> List[str]:
        """
        Format tokenized lines with proper indentation.
        
        Args:
            token_lines: List of (tokens, comment) tuples
            
        Returns:
            List of formatted lines
        """
        formatted = []
        depth = 0
        i = 0
        
        while i < len(token_lines):
            tokens, comment = token_lines[i]
            
            # Handle blank lines and comment-only lines
            if not tokens:
                if comment:
                    formatted.append(comment)
                else:
                    formatted.append("")
                i += 1
                continue
            
            # Calculate indentation for this line
            line_indent = depth
            first_token = tokens[0]
            
            # Dedent 'end' keyword
            if first_token == 'end':
                line_indent = max(0, depth - 1)
                depth = line_indent
            # 'case' and 'catch' should be at the same level as their parent (match/try)
            elif first_token in {'case', 'catch'}:
                line_indent = max(0, depth - 1)
            
            # Format the line
            line_tokens = tokens.copy()
            formatted_line = self._format_line(line_tokens, line_indent)
            
            # Append inline comment if present
            if comment:
                formatted_line += "  " + comment
            
            formatted.append(formatted_line)
            
            # Update depth for next line (after formatting current line)
            new_depth = self._calculate_depth_after_line(tokens, depth, first_token)
            depth = new_depth
            
            i += 1
        
        return formatted
    
    def _format_line(self, tokens: List[str], indent_level: int) -> str:
        """
        Format a single line of tokens with proper spacing.
        
        Args:
            tokens: List of tokens for this line
            indent_level: Current indentation level
            
        Returns:
            Formatted line string
        """
        indent = self.INDENT * indent_level
        
        # Special formatting for different constructs
        if not tokens:
            return indent
        
        # Add appropriate spacing between tokens
        formatted_tokens = []
        for j, token in enumerate(tokens):
            formatted_tokens.append(token)
            
            # Add spacing rules
            if j < len(tokens) - 1:
                next_token = tokens[j + 1]
                
                # No space before/after certain tokens
                if token in {',', '::'} or next_token in {',', '::'}:
                    continue
                
                # Add space between most tokens
                formatted_tokens.append(' ')
        
        return indent + ''.join(formatted_tokens).rstrip()
    
    def _calculate_new_depth(self, tokens: List[str], current_depth: int) -> int:
        """
        Calculate the new indentation depth after processing tokens.
        
        Args:
            tokens: Tokens from the current line
            current_depth: Current indentation depth
            
        Returns:
            New indentation depth
        """
        depth = current_depth
        i = 0
        
        while i < len(tokens):
            token = tokens[i]
            
            # Block start keywords
            if token in self.BLOCK_START_KEYWORDS:
                depth += 1
            elif token == 'struct':
                # Check if it's a type definition (creates block) or operation (doesn't)
                next_token = tokens[i + 1] if i + 1 < len(tokens) else ""
                if next_token not in self.STRUCT_OPERATIONS:
                    depth += 1
            elif token == 'case':
                # case starts a block that ends with next case or end
                depth += 1
            elif token == 'catch':
                # catch starts a block
                depth += 1
            elif token == 'end':
                depth = max(0, depth - 1)
            
            i += 1
        
        return depth
    
    def _calculate_depth_after_line(self, tokens: List[str], current_depth: int, first_token: str) -> int:
        """
        Calculate depth for the next line after current line.
        
        Handles special cases like 'case' and 'catch' which reset to parent level
        then increment.
        """
        depth = current_depth
        
        # If this line starts with 'end', depth was already decremented
        if first_token == 'end':
            return depth
        
        # If this line starts with 'case' or 'catch', we're at parent level
        # and need to increment for the body
        if first_token in {'case', 'catch'}:
            # We're at parent level, increment for the body
            return current_depth + 1
        
        # For other lines, calculate based on all tokens
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # Block start keywords
            if token in self.BLOCK_START_KEYWORDS:
                depth += 1
            elif token == 'struct':
                next_token = tokens[i + 1] if i + 1 < len(tokens) else ""
                if next_token not in self.STRUCT_OPERATIONS:
                    depth += 1
            elif token == 'end':
                depth = max(0, depth - 1)
            
            i += 1
        
        return depth


def format_file(filepath: str, indent_size: int = 4) -> str:
    """
    Format a TechLang file.
    
    Args:
        filepath: Path to .tl file
        indent_size: Number of spaces per indent level
        
    Returns:
        Formatted source code
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    
    formatter = TechLangFormatter(indent_size=indent_size)
    return formatter.format(source)


def format_string(source: str, indent_size: int = 4) -> str:
    """
    Format TechLang source code string.
    
    Args:
        source: TechLang source code
        indent_size: Number of spaces per indent level
        
    Returns:
        Formatted source code
    """
    formatter = TechLangFormatter(indent_size=indent_size)
    return formatter.format(source)
