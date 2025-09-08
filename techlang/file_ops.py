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
            state.add_error("file_write requires a path and a quoted string")
            return 0
        path_token = tokens[index + 1]
        text_token = tokens[index + 2]
        rel = FileOpsHandler._unquote(path_token)
        text = FileOpsHandler._unquote(text_token)
        path = os.path.join(base_dir, rel)
        try:
            os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
            state.add_output(f"Wrote {len(text)} bytes to '{rel}'")
            return 2
        except Exception as e:
            state.add_error(f"Failed to write file '{rel}': {e}")
            return 2

    @staticmethod
    def handle_file_append(state: InterpreterState, tokens: List[str], index: int, base_dir: str) -> int:
        if index + 2 >= len(tokens):
            state.add_error("file_append requires a path and a quoted string")
            return 0
        path_token = tokens[index + 1]
        text_token = tokens[index + 2]
        rel = FileOpsHandler._unquote(path_token)
        text = FileOpsHandler._unquote(text_token)
        path = os.path.join(base_dir, rel)
        try:
            os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
            with open(path, 'a', encoding='utf-8') as f:
                f.write(text)
            state.add_output(f"Appended {len(text)} bytes to '{rel}'")
            return 2
        except Exception as e:
            state.add_error(f"Failed to append file '{rel}': {e}")
            return 2

    @staticmethod
    def handle_file_exists(state: InterpreterState, tokens: List[str], index: int, base_dir: str) -> int:
        if index + 1 >= len(tokens):
            state.add_error("file_exists requires a path")
            return 0
        rel = FileOpsHandler._unquote(tokens[index + 1])
        path = os.path.join(base_dir, rel)
        state.add_output("true" if os.path.exists(path) else "false")
        return 1

    @staticmethod
    def handle_file_delete(state: InterpreterState, tokens: List[str], index: int, base_dir: str) -> int:
        if index + 1 >= len(tokens):
            state.add_error("file_delete requires a path")
            return 0
        rel = FileOpsHandler._unquote(tokens[index + 1])
        path = os.path.join(base_dir, rel)
        try:
            if os.path.isdir(path):
                state.add_error(f"'{rel}' is a directory; file_delete only removes files")
                return 1
            if os.path.exists(path):
                os.remove(path)
                state.add_output(f"Deleted '{rel}'")
            else:
                state.add_output(f"Not found '{rel}'")
            return 1
        except Exception as e:
            state.add_error(f"Failed to delete '{rel}': {e}")
            return 1

    @staticmethod
    def handle_file_list(state: InterpreterState, tokens: List[str], index: int, base_dir: str) -> int:
        if index + 1 >= len(tokens):
            state.add_error("file_list requires a directory path")
            return 0
        rel = FileOpsHandler._unquote(tokens[index + 1])
        path = os.path.join(base_dir, rel)
        try:
            if not os.path.isdir(path):
                state.add_error(f"'{rel}' is not a directory")
                return 1
            entries = sorted(os.listdir(path))
            for name in entries:
                state.add_output(name)
            return 1
        except Exception as e:
            state.add_error(f"Failed to list '{rel}': {e}")
            return 1

