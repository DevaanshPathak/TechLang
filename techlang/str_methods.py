"""
String Methods for TechLang.

Provides string operations:
- str_join <arr> <sep> <result> - Join array with separator
- str_zfill <str> <width> <result> - Zero-fill
- str_center <str> <width> <result> - Center
- str_ljust <str> <width> <result> - Left-justify
- str_rjust <str> <width> <result> - Right-justify
- str_title <str> <result> - Title case
- str_capitalize <str> <result> - Capitalize first char
- str_swapcase <str> <result> - Swap case
- str_isupper <str> <result> - Check uppercase (1/0)
- str_islower <str> <result> - Check lowercase (1/0)
- str_isspace <str> <result> - Check whitespace (1/0)
- str_lstrip <str> <result> - Strip left whitespace
- str_rstrip <str> <result> - Strip right whitespace
- str_strip_chars <str> <chars> <result> - Strip specific chars
"""

from typing import Dict, List, Optional, Any
from .core import InterpreterState


class StringMethodsHandler:
    """Handles string method operations in TechLang."""
    
    @staticmethod
    def _resolve_target_name(state: InterpreterState, token: str) -> str:
        """Resolve target variable name, handling -> prefix."""
        if token.startswith("->"):
            return token[2:]
        return token
    
    @staticmethod
    def handle_str_join(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Join array elements with separator, like Python's str.join().
        Syntax: str_join <array> <separator> <result>
        """
        if index + 3 >= len(tokens):
            state.add_error("str_join requires array, separator, and result. Use: str_join <arr> <sep> <result>")
            return 0
        
        arr_name = tokens[index + 1]
        sep_token = tokens[index + 2]
        result_name = StringMethodsHandler._resolve_target_name(state, tokens[index + 3])
        
        if arr_name not in state.arrays:
            state.add_error(f"Array '{arr_name}' does not exist")
            return 0
        
        # Resolve separator
        if sep_token.startswith('"') and sep_token.endswith('"'):
            separator = sep_token[1:-1]
        elif sep_token in state.strings:
            separator = state.strings[sep_token]
        else:
            separator = sep_token
        
        # Convert all elements to strings and join
        elements = [str(x) for x in state.arrays[arr_name]]
        result = separator.join(elements)
        state.strings[result_name] = result
        return 3
    
    @staticmethod
    def handle_str_zfill(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Zero-fill string to specified width, like Python's str.zfill().
        Syntax: str_zfill <string> <width> <result>
        """
        if index + 3 >= len(tokens):
            state.add_error("str_zfill requires string, width, and result. Use: str_zfill <str> <width> <result>")
            return 0
        
        str_name = tokens[index + 1]
        width_token = tokens[index + 2]
        result_name = StringMethodsHandler._resolve_target_name(state, tokens[index + 3])
        
        # Resolve string
        if str_name.startswith('"') and str_name.endswith('"'):
            string = str_name[1:-1]
        elif str_name in state.strings:
            string = state.strings[str_name]
        else:
            string = str(state.get_variable(str_name, str_name))
        
        # Resolve width
        try:
            width = int(width_token)
        except ValueError:
            width = state.get_variable(width_token, None)
            if not isinstance(width, int):
                state.add_error(f"str_zfill width must be integer, got '{width_token}'")
                return 0
        
        result = string.zfill(width)
        state.strings[result_name] = result
        return 3
    
    @staticmethod
    def handle_str_center(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Center string in specified width, like Python's str.center().
        Syntax: str_center <string> <width> <result> [fillchar]
        """
        if index + 3 >= len(tokens):
            state.add_error("str_center requires string, width, and result. Use: str_center <str> <width> <result> [fillchar]")
            return 0
        
        str_name = tokens[index + 1]
        width_token = tokens[index + 2]
        result_name = StringMethodsHandler._resolve_target_name(state, tokens[index + 3])
        
        # Optional fill character
        fillchar = ' '
        consumed = 3
        if index + 4 < len(tokens):
            fc_token = tokens[index + 4]
            if fc_token.startswith('"') and fc_token.endswith('"') and len(fc_token) == 3:
                fillchar = fc_token[1]
                consumed = 4
        
        # Resolve string
        if str_name.startswith('"') and str_name.endswith('"'):
            string = str_name[1:-1]
        elif str_name in state.strings:
            string = state.strings[str_name]
        else:
            string = str(state.get_variable(str_name, str_name))
        
        # Resolve width
        try:
            width = int(width_token)
        except ValueError:
            width = state.get_variable(width_token, None)
            if not isinstance(width, int):
                state.add_error(f"str_center width must be integer, got '{width_token}'")
                return 0
        
        result = string.center(width, fillchar)
        state.strings[result_name] = result
        return consumed
    
    @staticmethod
    def handle_str_ljust(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Left-justify string in specified width, like Python's str.ljust().
        Syntax: str_ljust <string> <width> <result> [fillchar]
        """
        if index + 3 >= len(tokens):
            state.add_error("str_ljust requires string, width, and result. Use: str_ljust <str> <width> <result>")
            return 0
        
        str_name = tokens[index + 1]
        width_token = tokens[index + 2]
        result_name = StringMethodsHandler._resolve_target_name(state, tokens[index + 3])
        
        fillchar = ' '
        consumed = 3
        if index + 4 < len(tokens):
            fc_token = tokens[index + 4]
            if fc_token.startswith('"') and fc_token.endswith('"') and len(fc_token) == 3:
                fillchar = fc_token[1]
                consumed = 4
        
        # Resolve string
        if str_name.startswith('"') and str_name.endswith('"'):
            string = str_name[1:-1]
        elif str_name in state.strings:
            string = state.strings[str_name]
        else:
            string = str(state.get_variable(str_name, str_name))
        
        # Resolve width
        try:
            width = int(width_token)
        except ValueError:
            width = state.get_variable(width_token, None)
            if not isinstance(width, int):
                state.add_error(f"str_ljust width must be integer, got '{width_token}'")
                return 0
        
        result = string.ljust(width, fillchar)
        state.strings[result_name] = result
        return consumed
    
    @staticmethod
    def handle_str_rjust(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Right-justify string in specified width, like Python's str.rjust().
        Syntax: str_rjust <string> <width> <result> [fillchar]
        """
        if index + 3 >= len(tokens):
            state.add_error("str_rjust requires string, width, and result. Use: str_rjust <str> <width> <result>")
            return 0
        
        str_name = tokens[index + 1]
        width_token = tokens[index + 2]
        result_name = StringMethodsHandler._resolve_target_name(state, tokens[index + 3])
        
        fillchar = ' '
        consumed = 3
        if index + 4 < len(tokens):
            fc_token = tokens[index + 4]
            if fc_token.startswith('"') and fc_token.endswith('"') and len(fc_token) == 3:
                fillchar = fc_token[1]
                consumed = 4
        
        # Resolve string
        if str_name.startswith('"') and str_name.endswith('"'):
            string = str_name[1:-1]
        elif str_name in state.strings:
            string = state.strings[str_name]
        else:
            string = str(state.get_variable(str_name, str_name))
        
        # Resolve width
        try:
            width = int(width_token)
        except ValueError:
            width = state.get_variable(width_token, None)
            if not isinstance(width, int):
                state.add_error(f"str_rjust width must be integer, got '{width_token}'")
                return 0
        
        result = string.rjust(width, fillchar)
        state.strings[result_name] = result
        return consumed
    
    @staticmethod
    def handle_str_title(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Convert string to title case, like Python's str.title().
        Syntax: str_title <string> <result>
        """
        if index + 2 >= len(tokens):
            state.add_error("str_title requires string and result. Use: str_title <str> <result>")
            return 0
        
        str_name = tokens[index + 1]
        result_name = StringMethodsHandler._resolve_target_name(state, tokens[index + 2])
        
        # Resolve string
        if str_name.startswith('"') and str_name.endswith('"'):
            string = str_name[1:-1]
        elif str_name in state.strings:
            string = state.strings[str_name]
        else:
            state.add_error(f"String '{str_name}' does not exist")
            return 0
        
        result = string.title()
        state.strings[result_name] = result
        return 2
    
    @staticmethod
    def handle_str_capitalize(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Capitalize first character, like Python's str.capitalize().
        Syntax: str_capitalize <string> <result>
        """
        if index + 2 >= len(tokens):
            state.add_error("str_capitalize requires string and result. Use: str_capitalize <str> <result>")
            return 0
        
        str_name = tokens[index + 1]
        result_name = StringMethodsHandler._resolve_target_name(state, tokens[index + 2])
        
        # Resolve string
        if str_name.startswith('"') and str_name.endswith('"'):
            string = str_name[1:-1]
        elif str_name in state.strings:
            string = state.strings[str_name]
        else:
            state.add_error(f"String '{str_name}' does not exist")
            return 0
        
        result = string.capitalize()
        state.strings[result_name] = result
        return 2
    
    @staticmethod
    def handle_str_swapcase(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Swap case of all characters, like Python's str.swapcase().
        Syntax: str_swapcase <string> <result>
        """
        if index + 2 >= len(tokens):
            state.add_error("str_swapcase requires string and result. Use: str_swapcase <str> <result>")
            return 0
        
        str_name = tokens[index + 1]
        result_name = StringMethodsHandler._resolve_target_name(state, tokens[index + 2])
        
        # Resolve string
        if str_name.startswith('"') and str_name.endswith('"'):
            string = str_name[1:-1]
        elif str_name in state.strings:
            string = state.strings[str_name]
        else:
            state.add_error(f"String '{str_name}' does not exist")
            return 0
        
        result = string.swapcase()
        state.strings[result_name] = result
        return 2
    
    @staticmethod
    def handle_str_isupper(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if all characters are uppercase, like Python's str.isupper().
        Syntax: str_isupper <string> <result>
        """
        if index + 2 >= len(tokens):
            state.add_error("str_isupper requires string and result. Use: str_isupper <str> <result>")
            return 0
        
        str_name = tokens[index + 1]
        result_name = StringMethodsHandler._resolve_target_name(state, tokens[index + 2])
        
        # Resolve string
        if str_name.startswith('"') and str_name.endswith('"'):
            string = str_name[1:-1]
        elif str_name in state.strings:
            string = state.strings[str_name]
        else:
            state.add_error(f"String '{str_name}' does not exist")
            return 0
        
        result = 1 if string.isupper() else 0
        state.set_variable(result_name, result)
        return 2
    
    @staticmethod
    def handle_str_islower(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if all characters are lowercase, like Python's str.islower().
        Syntax: str_islower <string> <result>
        """
        if index + 2 >= len(tokens):
            state.add_error("str_islower requires string and result. Use: str_islower <str> <result>")
            return 0
        
        str_name = tokens[index + 1]
        result_name = StringMethodsHandler._resolve_target_name(state, tokens[index + 2])
        
        # Resolve string
        if str_name.startswith('"') and str_name.endswith('"'):
            string = str_name[1:-1]
        elif str_name in state.strings:
            string = state.strings[str_name]
        else:
            state.add_error(f"String '{str_name}' does not exist")
            return 0
        
        result = 1 if string.islower() else 0
        state.set_variable(result_name, result)
        return 2
    
    @staticmethod
    def handle_str_isspace(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if all characters are whitespace, like Python's str.isspace().
        Syntax: str_isspace <string> <result>
        """
        if index + 2 >= len(tokens):
            state.add_error("str_isspace requires string and result. Use: str_isspace <str> <result>")
            return 0
        
        str_name = tokens[index + 1]
        result_name = StringMethodsHandler._resolve_target_name(state, tokens[index + 2])
        
        # Resolve string
        if str_name.startswith('"') and str_name.endswith('"'):
            string = str_name[1:-1]
        elif str_name in state.strings:
            string = state.strings[str_name]
        else:
            state.add_error(f"String '{str_name}' does not exist")
            return 0
        
        result = 1 if (string and string.isspace()) else 0
        state.set_variable(result_name, result)
        return 2
    
    @staticmethod
    def handle_str_lstrip(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Strip characters from left, like Python's str.lstrip().
        Syntax: str_lstrip <string> <result> [chars]
        """
        if index + 2 >= len(tokens):
            state.add_error("str_lstrip requires string and result. Use: str_lstrip <str> <result> [chars]")
            return 0
        
        str_name = tokens[index + 1]
        result_name = StringMethodsHandler._resolve_target_name(state, tokens[index + 2])
        
        chars = None
        consumed = 2
        if index + 3 < len(tokens):
            chars_token = tokens[index + 3]
            if chars_token.startswith('"') and chars_token.endswith('"'):
                chars = chars_token[1:-1]
                consumed = 3
        
        # Resolve string
        if str_name.startswith('"') and str_name.endswith('"'):
            string = str_name[1:-1]
        elif str_name in state.strings:
            string = state.strings[str_name]
        else:
            state.add_error(f"String '{str_name}' does not exist")
            return 0
        
        result = string.lstrip(chars)
        state.strings[result_name] = result
        return consumed
    
    @staticmethod
    def handle_str_rstrip(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Strip characters from right, like Python's str.rstrip().
        Syntax: str_rstrip <string> <result> [chars]
        """
        if index + 2 >= len(tokens):
            state.add_error("str_rstrip requires string and result. Use: str_rstrip <str> <result> [chars]")
            return 0
        
        str_name = tokens[index + 1]
        result_name = StringMethodsHandler._resolve_target_name(state, tokens[index + 2])
        
        chars = None
        consumed = 2
        if index + 3 < len(tokens):
            chars_token = tokens[index + 3]
            if chars_token.startswith('"') and chars_token.endswith('"'):
                chars = chars_token[1:-1]
                consumed = 3
        
        # Resolve string
        if str_name.startswith('"') and str_name.endswith('"'):
            string = str_name[1:-1]
        elif str_name in state.strings:
            string = state.strings[str_name]
        else:
            state.add_error(f"String '{str_name}' does not exist")
            return 0
        
        result = string.rstrip(chars)
        state.strings[result_name] = result
        return consumed
    
    @staticmethod
    def handle_str_strip_chars(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Strip specific characters from both ends, like Python's str.strip(chars).
        Syntax: str_strip_chars <string> <chars> <result>
        """
        if index + 3 >= len(tokens):
            state.add_error("str_strip_chars requires string, chars, and result. Use: str_strip_chars <str> <chars> <result>")
            return 0
        
        str_name = tokens[index + 1]
        chars_token = tokens[index + 2]
        result_name = StringMethodsHandler._resolve_target_name(state, tokens[index + 3])
        
        # Resolve string
        if str_name.startswith('"') and str_name.endswith('"'):
            string = str_name[1:-1]
        elif str_name in state.strings:
            string = state.strings[str_name]
        else:
            state.add_error(f"String '{str_name}' does not exist")
            return 0
        
        # Resolve chars
        if chars_token.startswith('"') and chars_token.endswith('"'):
            chars = chars_token[1:-1]
        elif chars_token in state.strings:
            chars = state.strings[chars_token]
        else:
            chars = chars_token
        
        result = string.strip(chars)
        state.strings[result_name] = result
        return 3
