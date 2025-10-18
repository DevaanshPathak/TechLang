import threading
import time
from typing import List
from .core import InterpreterState


class ThreadOpsHandler:
    @staticmethod
    def handle_thread_create(state: InterpreterState, tokens: List[str], index: int, base_dir: str) -> int:
        if index + 1 >= len(tokens):
            state.add_error("thread_create requires a function name to call")
            return 0
        func_name = tokens[index + 1]

        # Create thread to run the function. Re-emit the function body into the worker code
        func_block = state.functions.get(func_name)
        if func_block is None:
            state.add_error(f"Function '{func_name}' is not defined. Use 'def {func_name} ... end' to define it first.")
            return 1
        func_body = ' '.join(func_block)
        code = f"def {func_name} {func_body} end\ncall {func_name}"
        thread_id = state.next_thread_id
        state.next_thread_id += 1

        def worker():
            try:
                # Import here to avoid circular import at module load time
                from .interpreter import run as run_code
                out = run_code(code, base_dir=base_dir)
            except Exception as e:
                out = f"[Thread error: {e}]"
            state.thread_results[thread_id] = out

        t = threading.Thread(target=worker, daemon=True)
        state.threads[thread_id] = t
        t.start()
        state.add_output(str(thread_id))
        return 1

    @staticmethod
    def handle_thread_join(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("thread_join requires thread_id")
            return 0
        try:
            tid = int(tokens[index + 1])
        except ValueError:
            state.add_error("thread_id must be an integer")
            return 0
        t = state.threads.get(tid)
        if t is None:
            state.add_error(f"Unknown thread {tid}")
            return 1
        t.join(timeout=30)
        out = state.thread_results.get(tid, "")
        state.add_output(out)
        return 1

    @staticmethod
    def handle_thread_sleep(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("thread_sleep requires milliseconds")
            return 0
        try:
            ms = int(tokens[index + 1])
        except ValueError:
            state.add_error("milliseconds must be an integer")
            return 0
        time.sleep(ms / 1000.0)
        return 1

    @staticmethod
    def handle_async_start(state: InterpreterState, tokens: List[str], index: int, base_dir: str) -> int:
        # Alias to thread_create for now
        return ThreadOpsHandler.handle_thread_create(state, tokens, index, base_dir)

    @staticmethod
    def handle_async_wait(state: InterpreterState, tokens: List[str], index: int) -> int:
        # Alias to thread_join for now
        return ThreadOpsHandler.handle_thread_join(state, tokens, index)

    @staticmethod
    def handle_thread_status(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("thread_status requires thread_id")
            return 0
        try:
            tid = int(tokens[index + 1])
        except ValueError:
            state.add_error("thread_id must be an integer")
            return 0
        thread = state.threads.get(tid)
        if thread is None:
            state.add_error(f"Unknown thread {tid}")
            return 1
        status = "running" if thread.is_alive() else "finished"
        state.add_output(status)
        return 1

    @staticmethod
    def handle_thread_result(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("thread_result requires thread_id")
            return 0
        try:
            tid = int(tokens[index + 1])
        except ValueError:
            state.add_error("thread_id must be an integer")
            return 0
        if tid not in state.threads:
            state.add_error(f"Unknown thread {tid}")
            return 1
        result = state.thread_results.get(tid, "")
        state.add_output(result)
        return 1

    @staticmethod
    def handle_thread_list(state: InterpreterState) -> int:
        order = " ".join(str(tid) for tid in state.threads.keys())
        state.add_output(order)
        return 0


