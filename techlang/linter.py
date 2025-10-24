"""
TechLang linter for detecting common issues in .tl files.
"""

from typing import List, Dict, Set, Tuple
from dataclasses import dataclass
import re


@dataclass
class LintIssue:
    """Represents a linting issue found in code."""
    line: int
    column: int
    severity: str  # 'error', 'warning', 'info'
    code: str
    message: str
    
    def __str__(self):
        return f"Line {self.line}:{self.column} [{self.severity.upper()}] {self.code}: {self.message}"


class TechLangLinter:
    """Lint TechLang source code for common issues."""
    
    BLOCK_START_KEYWORDS = {'def', 'if', 'loop', 'while', 'switch', 'match', 'try', 'macro'}
    STRUCT_OPERATIONS = {'new', 'set', 'get', 'dump'}
    
    def __init__(self):
        """Initialize the linter."""
        self.issues: List[LintIssue] = []
    
    def lint(self, source: str, filepath: str = "<string>") -> List[LintIssue]:
        """
        Lint TechLang source code.
        
        Args:
            source: TechLang source code
            filepath: Optional filepath for better error messages
            
        Returns:
            List of LintIssue objects
        """
        self.issues = []
        self.filepath = filepath
        
        lines = source.splitlines()
        tokens_per_line = self._tokenize_lines(lines)
        
        # Run all lint checks
        self._check_block_balance(tokens_per_line)
        self._check_undefined_variables(tokens_per_line)
        self._check_unreachable_code(tokens_per_line)
        self._check_empty_blocks(tokens_per_line)
        self._check_duplicate_function_definitions(tokens_per_line)
        self._check_long_lines(lines)
        
        # Sort by line number
        self.issues.sort(key=lambda x: (x.line, x.column))
        
        return self.issues
    
    def _tokenize_lines(self, lines: List[str]) -> List[List[str]]:
        """Tokenize each line, returning list of token lists."""
        result = []
        for line in lines:
            # Strip comments
            stripped = line.strip()
            if '#' in stripped:
                # Simple comment removal (doesn't handle # in strings perfectly)
                parts = stripped.split('#', 1)
                stripped = parts[0].strip()
            
            if not stripped:
                result.append([])
            else:
                # Tokenize using regex to preserve quoted strings
                tokens = re.findall(r'"[^"]*"|\S+', stripped)
                result.append(tokens)
        
        return result
    
    def _check_block_balance(self, tokens_per_line: List[List[str]]) -> None:
        """Check that all blocks have matching 'end' keywords."""
        depth = 0
        block_stack = []  # Track which blocks are open
        
        for line_num, tokens in enumerate(tokens_per_line, start=1):
            for col, token in enumerate(tokens):
                if token in self.BLOCK_START_KEYWORDS:
                    depth += 1
                    block_stack.append((token, line_num, col))
                elif token == 'struct':
                    # Check if it's a type definition
                    next_token = tokens[col + 1] if col + 1 < len(tokens) else ""
                    if next_token not in self.STRUCT_OPERATIONS:
                        depth += 1
                        block_stack.append((token, line_num, col))
                elif token == 'end':
                    if depth == 0:
                        self.issues.append(LintIssue(
                            line=line_num,
                            column=col + 1,
                            severity='error',
                            code='E001',
                            message="Unmatched 'end' keyword (no corresponding block start)"
                        ))
                    else:
                        depth -= 1
                        block_stack.pop()
        
        # Check for unclosed blocks
        if depth > 0:
            for block_type, line, col in block_stack:
                self.issues.append(LintIssue(
                    line=line,
                    column=col + 1,
                    severity='error',
                    code='E002',
                    message=f"Unclosed '{block_type}' block (missing 'end')"
                ))
    
    def _check_undefined_variables(self, tokens_per_line: List[List[str]]) -> None:
        """Warn about potential use of undefined variables."""
        defined_vars = set()
        defined_functions = set()
        defined_arrays = set()
        defined_strings = set()
        defined_dicts = set()
        
        for line_num, tokens in enumerate(tokens_per_line, start=1):
            if not tokens:
                continue
            
            cmd = tokens[0]
            
            # Track variable definitions
            if cmd == 'set' and len(tokens) >= 2:
                defined_vars.add(tokens[1])
            elif cmd == 'def' and len(tokens) >= 2:
                defined_functions.add(tokens[1])
            elif cmd == 'array_create' and len(tokens) >= 2:
                defined_arrays.add(tokens[1])
            elif cmd == 'str_create' and len(tokens) >= 2:
                defined_strings.add(tokens[1])
            elif cmd == 'dict_create' and len(tokens) >= 2:
                defined_dicts.add(tokens[1])
            
            # Check for variable usage
            elif cmd in {'add', 'sub', 'mul', 'div'} and len(tokens) >= 2:
                var_name = tokens[1]
                if not var_name.isdigit() and var_name not in defined_vars:
                    self.issues.append(LintIssue(
                        line=line_num,
                        column=1,
                        severity='warning',
                        code='W001',
                        message=f"Variable '{var_name}' may be used before assignment"
                    ))
            elif cmd == 'call' and len(tokens) >= 2:
                func_name = tokens[1]
                # Skip module calls (foo.bar or foo::bar)
                if '.' not in func_name and '::' not in func_name and func_name not in defined_functions:
                    self.issues.append(LintIssue(
                        line=line_num,
                        column=1,
                        severity='warning',
                        code='W002',
                        message=f"Function '{func_name}' may not be defined"
                    ))
    
    def _check_unreachable_code(self, tokens_per_line: List[List[str]]) -> None:
        """Detect code after 'end' at depth 0 (unreachable in some contexts)."""
        # This is a simplified check - in reality, top-level code after functions is fine
        # But code after an 'end' that closes a block at depth 0 inside a function would be unreachable
        pass  # Skip this check for now as it requires more context
    
    def _check_empty_blocks(self, tokens_per_line: List[List[str]]) -> None:
        """Warn about empty blocks (block start immediately followed by end)."""
        for line_num, tokens in enumerate(tokens_per_line, start=1):
            if not tokens:
                continue
            
            # Check for block start
            if tokens[0] in self.BLOCK_START_KEYWORDS:
                # Look at next non-empty line
                found_end_immediately = False
                for offset in range(1, min(3, len(tokens_per_line) - line_num + 1)):
                    next_line_idx = line_num + offset - 1
                    if next_line_idx >= len(tokens_per_line):
                        break
                    next_tokens = tokens_per_line[next_line_idx]
                    if not next_tokens:
                        continue  # Skip empty lines
                    if next_tokens[0] == 'end':
                        found_end_immediately = True
                        break
                    else:
                        # Found a non-end token, so not empty
                        break
                
                if found_end_immediately:
                    self.issues.append(LintIssue(
                        line=line_num,
                        column=1,
                        severity='info',
                        code='I001',
                        message=f"Empty '{tokens[0]}' block"
                    ))
    
    def _check_duplicate_function_definitions(self, tokens_per_line: List[List[str]]) -> None:
        """Check for duplicate function definitions."""
        defined_functions = {}
        
        for line_num, tokens in enumerate(tokens_per_line, start=1):
            if tokens and tokens[0] == 'def' and len(tokens) >= 2:
                func_name = tokens[1]
                if func_name in defined_functions:
                    self.issues.append(LintIssue(
                        line=line_num,
                        column=1,
                        severity='warning',
                        code='W003',
                        message=f"Function '{func_name}' is defined multiple times (first defined at line {defined_functions[func_name]})"
                    ))
                else:
                    defined_functions[func_name] = line_num
    
    def _check_long_lines(self, lines: List[str]) -> None:
        """Warn about lines that are too long (> 100 characters)."""
        max_length = 100
        
        for line_num, line in enumerate(lines, start=1):
            if len(line) > max_length:
                self.issues.append(LintIssue(
                    line=line_num,
                    column=max_length + 1,
                    severity='info',
                    code='I002',
                    message=f"Line too long ({len(line)} > {max_length} characters)"
                ))


def lint_file(filepath: str) -> List[LintIssue]:
    """
    Lint a TechLang file.
    
    Args:
        filepath: Path to .tl file
        
    Returns:
        List of LintIssue objects
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    
    linter = TechLangLinter()
    return linter.lint(source, filepath=filepath)


def lint_string(source: str) -> List[LintIssue]:
    """
    Lint TechLang source code string.
    
    Args:
        source: TechLang source code
        
    Returns:
        List of LintIssue objects
    """
    linter = TechLangLinter()
    return linter.lint(source)
