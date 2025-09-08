import threading
from typing import List
from .core import InterpreterState

try:
    import requests  # type: ignore
except Exception:  # pragma: no cover
    requests = None


class NetOpsHandler:
    """HTTP client commands for TechLang."""

    @staticmethod
    def _unquote(token: str) -> str:
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        return token

    @staticmethod
    def handle_http_get(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 2 >= len(tokens):
            state.add_error("http_get requires a URL and a response name")
            return 0
        if requests is None:
            state.add_error("'requests' library not available")
            return 2
        url = NetOpsHandler._unquote(tokens[index + 1])
        name = tokens[index + 2]
        try:
            resp = requests.get(url, timeout=10)
            state.strings[name] = resp.text
            state.set_variable(f"{name}_status", resp.status_code)
            return 2
        except Exception as e:
            state.add_error(f"HTTP GET failed: {e}")
            return 2

    @staticmethod
    def handle_http_post(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 2 >= len(tokens):
            state.add_error("http_post requires a URL and data token")
            return 0
        if requests is None:
            state.add_error("'requests' library not available")
            return 2
        url = NetOpsHandler._unquote(tokens[index + 1])
        data_token = tokens[index + 2]
        # Resolve data: prefer string var, then quoted literal, then numeric var
        if data_token in state.strings:
            data = state.strings[data_token]
        elif data_token.startswith('"') and data_token.endswith('"'):
            data = data_token[1:-1]
        else:
            val = state.get_variable(data_token, None)
            data = str(val) if val is not None else data_token
        try:
            resp = requests.post(url, data=data, timeout=10)
            state.strings["response"] = resp.text
            state.set_variable("response_status", resp.status_code)
            return 2
        except Exception as e:
            state.add_error(f"HTTP POST failed: {e}")
            return 2

    @staticmethod
    def handle_http_status(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("http_status requires a response name")
            return 0
        name = tokens[index + 1]
        code = state.get_variable(f"{name}_status", None)
        if code is None:
            state.add_error(f"No status for '{name}'")
            return 1
        state.add_output(str(code))
        return 1


class NetServerHandler:
    """Stubs for server commands (not a full server implementation)."""

    _server_thread = None

    @staticmethod
    def handle_server_start(state: InterpreterState, tokens: List[str], index: int) -> int:
        # For now, just acknowledge start to avoid breaking scripts
        state.add_output("Server started (stub)")
        return 1 if index + 1 < len(tokens) else 0

    @staticmethod
    def handle_server_route(state: InterpreterState, tokens: List[str], index: int) -> int:
        # Route registration stub
        state.add_output("Route registered (stub)")
        return 2 if index + 2 < len(tokens) else 0

    @staticmethod
    def handle_server_stop(state: InterpreterState) -> None:
        state.add_output("Server stopped (stub)")


