import os
from typing import List, Optional
from .core import InterpreterState


class FileOpsHandler:
    """
    File I/O commands for TechLang.
    Commands:
      - file_read "path" varname
      - file_write "path" "text"
      - file_append "path" "text"
      - file_exists "path"
      - file_delete "path"
      - file_list "dirpath"
    """

    @staticmethod
    def _unquote(token: str) -> str:
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        return token

    @staticmethod
    def _resolve_text(state: InterpreterState, token: str) -> Optional[str]:
        # Accept either a quoted literal or a string stored in vars/strings.
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        if token in state.strings:
            return state.strings[token]
        if state.has_variable(token):
            value = state.get_variable(token)
            if isinstance(value, str):
                return value
        return None

    @staticmethod
    def _resolve_stringish(state: InterpreterState, token: str) -> str:
        # Accept quoted literals, string vars, or string-valued variables.
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        if token in state.strings:
            return state.strings[token]
        if state.has_variable(token):
            value = state.get_variable(token)
            if isinstance(value, str):
                return value
        return token

    @staticmethod
    def _is_possible_name_token(token: str) -> bool:
        # Optional target/output names must not be quoted and must not be a command.
        if token.startswith('"') and token.endswith('"'):
            return False
        from .basic_commands import BasicCommandHandler

        if token in BasicCommandHandler.KNOWN_COMMANDS:
            return False
        if token in {"end", "case", "default", "catch", "else"}:
            return False
        return True

    @staticmethod
    def handle_file_read(state: InterpreterState, tokens: List[str], index: int, base_dir: str) -> int:
        if index + 2 >= len(tokens):
            state.add_error("file_read requires a path and a variable name")
            return 0
        path_token = tokens[index + 1]
        varname = tokens[index + 2]
        rel = FileOpsHandler._unquote(path_token)
        path = os.path.join(base_dir, rel)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            state.set_variable(varname, content)
            return 2
        except Exception as e:
            state.add_error(f"Failed to read file '{rel}': {e}")
            return 2

    @staticmethod
    def handle_file_write(state: InterpreterState, tokens: List[str], index: int, base_dir: str) -> int:
        if index + 2 >= len(tokens):
            state.add_error("file_write requires a path and text")
            return 0
        path_token = tokens[index + 1]
        text_token = tokens[index + 2]
        ok_var: Optional[str] = None
        if index + 3 < len(tokens):
            candidate = tokens[index + 3]
            if FileOpsHandler._is_possible_name_token(candidate):
                ok_var = candidate
        rel = FileOpsHandler._unquote(path_token)
        text = FileOpsHandler._resolve_text(state, text_token)
        if text is None:
            state.add_error("file_write requires text as a quoted string or a string variable")
            return 0
        path = os.path.join(base_dir, rel)
        try:
            os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
            if ok_var is not None:
                state.variables[ok_var] = 1
                return 3
            state.add_output(f"Wrote {len(text)} bytes to '{rel}'")
            return 2
        except Exception as e:
            if ok_var is not None:
                state.variables[ok_var] = 0
                return 3
            state.add_error(f"Failed to write file '{rel}': {e}")
            return 2

    @staticmethod
    def handle_file_append(state: InterpreterState, tokens: List[str], index: int, base_dir: str) -> int:
        if index + 2 >= len(tokens):
            state.add_error("file_append requires a path and text")
            return 0
        path_token = tokens[index + 1]
        text_token = tokens[index + 2]
        ok_var: Optional[str] = None
        if index + 3 < len(tokens):
            candidate = tokens[index + 3]
            if FileOpsHandler._is_possible_name_token(candidate):
                ok_var = candidate
        rel = FileOpsHandler._unquote(path_token)
        text = FileOpsHandler._resolve_text(state, text_token)
        if text is None:
            state.add_error("file_append requires text as a quoted string or a string variable")
            return 0
        path = os.path.join(base_dir, rel)
        try:
            os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
            with open(path, 'a', encoding='utf-8') as f:
                f.write(text)
            if ok_var is not None:
                state.variables[ok_var] = 1
                return 3
            state.add_output(f"Appended {len(text)} bytes to '{rel}'")
            return 2
        except Exception as e:
            if ok_var is not None:
                state.variables[ok_var] = 0
                return 3
            state.add_error(f"Failed to append file '{rel}': {e}")
            return 2

    @staticmethod
    def handle_file_exists(state: InterpreterState, tokens: List[str], index: int, base_dir: str) -> int:
        if index + 1 >= len(tokens):
            state.add_error("file_exists requires a path")
            return 0
        rel = FileOpsHandler._unquote(tokens[index + 1])
        path = os.path.join(base_dir, rel)
        exists = os.path.exists(path)

        # Optional store form: file_exists "path" <targetVar>
        if index + 2 < len(tokens):
            target = tokens[index + 2]
            if FileOpsHandler._is_possible_name_token(target):
                state.variables[target] = 1 if exists else 0
                return 2

        state.add_output("true" if exists else "false")
        return 1

    @staticmethod
    def handle_file_delete(state: InterpreterState, tokens: List[str], index: int, base_dir: str) -> int:
        if index + 1 >= len(tokens):
            state.add_error("file_delete requires a path")
            return 0
        rel = FileOpsHandler._unquote(tokens[index + 1])
        path = os.path.join(base_dir, rel)
        ok_var: Optional[str] = None
        if index + 2 < len(tokens):
            candidate = tokens[index + 2]
            if FileOpsHandler._is_possible_name_token(candidate):
                ok_var = candidate
        try:
            if os.path.isdir(path):
                if ok_var is not None:
                    state.variables[ok_var] = 0
                    return 2
                state.add_error(f"'{rel}' is a directory; file_delete only removes files")
                return 1
            if os.path.exists(path):
                os.remove(path)
                if ok_var is not None:
                    state.variables[ok_var] = 1
                    return 2
                state.add_output(f"Deleted '{rel}'")
            else:
                if ok_var is not None:
                    state.variables[ok_var] = 0
                    return 2
                state.add_output(f"Not found '{rel}'")
            return 1
        except Exception as e:
            if ok_var is not None:
                state.variables[ok_var] = 0
                return 2
            state.add_error(f"Failed to delete '{rel}': {e}")
            return 1

    @staticmethod
    def handle_file_list(state: InterpreterState, tokens: List[str], index: int, base_dir: str) -> int:
        if index + 1 >= len(tokens):
            state.add_error("file_list requires a directory path")
            return 0
        rel = FileOpsHandler._unquote(tokens[index + 1])
        path = os.path.join(base_dir, rel)

        out_arr: Optional[str] = None
        ok_var: Optional[str] = None
        if index + 2 < len(tokens):
            candidate = tokens[index + 2]
            if FileOpsHandler._is_possible_name_token(candidate):
                out_arr = candidate
        if out_arr is not None and index + 3 < len(tokens):
            candidate = tokens[index + 3]
            if FileOpsHandler._is_possible_name_token(candidate):
                ok_var = candidate
        try:
            if not os.path.isdir(path):
                if out_arr is not None:
                    state.arrays[out_arr] = []
                    if ok_var is not None:
                        state.variables[ok_var] = 0
                    return 2 if ok_var is None else 3
                state.add_error(f"'{rel}' is not a directory")
                return 1
            entries = sorted(os.listdir(path))
            if out_arr is not None:
                state.arrays[out_arr] = entries
                if ok_var is not None:
                    state.variables[ok_var] = 1
                    return 3
                return 2
            for name in entries:
                state.add_output(name)
            return 1
        except Exception as e:
            if out_arr is not None:
                state.arrays[out_arr] = []
                if ok_var is not None:
                    state.variables[ok_var] = 0
                    return 3
                return 2
            state.add_error(f"Failed to list '{rel}': {e}")
            return 1

    @staticmethod
    def handle_path_join(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 3 >= len(tokens):
            state.add_error("path_join requires a, b, and a target string name")
            return 0
        a = FileOpsHandler._resolve_stringish(state, tokens[index + 1])
        b = FileOpsHandler._resolve_stringish(state, tokens[index + 2])
        target = tokens[index + 3]
        state.strings[target] = os.path.join(a, b)
        return 3

    @staticmethod
    def handle_path_basename(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 2 >= len(tokens):
            state.add_error("path_basename requires a path and a target string name")
            return 0
        p = FileOpsHandler._resolve_stringish(state, tokens[index + 1])
        target = tokens[index + 2]
        state.strings[target] = os.path.basename(p)
        return 2

    @staticmethod
    def handle_path_dirname(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 2 >= len(tokens):
            state.add_error("path_dirname requires a path and a target string name")
            return 0
        p = FileOpsHandler._resolve_stringish(state, tokens[index + 1])
        target = tokens[index + 2]
        state.strings[target] = os.path.dirname(p)
        return 2

    @staticmethod
    def handle_path_extname(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 2 >= len(tokens):
            state.add_error("path_extname requires a path and a target string name")
            return 0
        p = FileOpsHandler._resolve_stringish(state, tokens[index + 1])
        target = tokens[index + 2]
        _root, ext = os.path.splitext(p)
        state.strings[target] = ext
        return 2

