from typing import List
from .core import InterpreterState


class MemoryOpsHandler:
    """A minimal memory allocator storing integer cells at integer addresses."""

    @staticmethod
    def _get_int(state: InterpreterState, token: str) -> int:
        try:
            return int(token)
        except ValueError:
            val = state.get_variable(token, None)
            if isinstance(val, int):
                return val
            raise ValueError(f"Expected number, got '{token}'")

    @staticmethod
    def handle_mem_alloc(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("mem_alloc requires size")
            return 0
        try:
            size = MemoryOpsHandler._get_int(state, tokens[index + 1])
            if size <= 0:
                state.add_error("mem_alloc size must be > 0")
                return 1
            base = state.next_address
            for offset in range(size):
                state.memory[base + offset] = 0
            state.next_address = base + size
            state.add_output(str(base))
            return 1
        except ValueError as e:
            state.add_error(str(e))
            return 0

    @staticmethod
    def handle_mem_free(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("mem_free requires address")
            return 0
        try:
            addr = MemoryOpsHandler._get_int(state, tokens[index + 1])
            # Remove only the single cell at address; simple model
            if addr in state.memory:
                del state.memory[addr]
                state.add_output(f"Freed {addr}")
            else:
                state.add_output(f"Address {addr} not allocated")
            return 1
        except ValueError as e:
            state.add_error(str(e))
            return 0

    @staticmethod
    def handle_mem_read(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("mem_read requires address")
            return 0
        try:
            addr = MemoryOpsHandler._get_int(state, tokens[index + 1])
            val = state.memory.get(addr, None)
            if val is None:
                state.add_error(f"Address {addr} not allocated")
                return 1
            state.add_output(str(val))
            return 1
        except ValueError as e:
            state.add_error(str(e))
            return 0

    @staticmethod
    def handle_mem_write(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 2 >= len(tokens):
            state.add_error("mem_write requires address and value")
            return 0
        try:
            addr = MemoryOpsHandler._get_int(state, tokens[index + 1])
            value = MemoryOpsHandler._get_int(state, tokens[index + 2])
            if addr not in state.memory:
                state.add_error(f"Address {addr} not allocated")
                return 2
            state.memory[addr] = value
            return 2
        except ValueError as e:
            state.add_error(str(e))
            return 0

    @staticmethod
    def handle_mem_dump(state: InterpreterState) -> None:
        if not state.memory:
            state.add_output("<empty>")
            return
        for addr in sorted(state.memory.keys()):
            state.add_output(f"{addr}: {state.memory[addr]}")


