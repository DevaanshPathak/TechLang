import os
import shlex
import subprocess
import sys
import time
import datetime as dt
from typing import Dict, List
from .core import InterpreterState


class SystemOpsHandler:
    @staticmethod
    def handle_sys_exec(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("sys_exec requires a quoted command")
            return 0
        cmd_token = tokens[index + 1]
        if not (cmd_token.startswith('"') and cmd_token.endswith('"')):
            state.add_error("sys_exec requires a quoted command string")
            return 0
        cmd = cmd_token[1:-1]
        try:
            # Safe execution without shell; split args
            args = shlex.split(cmd)
            res = subprocess.run(args, capture_output=True, text=True, timeout=10)
            if res.stdout:
                state.add_output(res.stdout.strip())
            if res.stderr:
                state.add_output(res.stderr.strip())
            state.set_variable("_status", res.returncode)
            return 1
        except Exception as e:
            state.add_error(f"sys_exec failed: {e}")
            return 1

    @staticmethod
    def handle_sys_env(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("sys_env requires a variable name")
            return 0
        key = tokens[index + 1]
        state.add_output(os.environ.get(key, ""))
        return 1

    @staticmethod
    def handle_sys_time(state: InterpreterState, tokens: List[str], index: int) -> int:
        value = int(time.time())

        # Optional store form: sys_time <targetVar>
        if index + 1 < len(tokens):
            target = tokens[index + 1]
            from .basic_commands import BasicCommandHandler

            if not (target.startswith('"') and target.endswith('"')) and target not in BasicCommandHandler.KNOWN_COMMANDS:
                state.variables[target] = value
                return 1

        state.add_output(str(value))
        return 0

    @staticmethod
    def handle_sys_date(state: InterpreterState) -> None:
        state.add_output(dt.datetime.now().isoformat())
    
    @staticmethod
    def handle_sys_sleep(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("sys_sleep requires milliseconds")
            return 0
        try:
            ms = int(tokens[index + 1])
        except ValueError:
            state.add_error("sys_sleep expects an integer number of milliseconds")
            return 0
        if ms < 0:
            state.add_error("sys_sleep requires a non-negative duration")
            return 0
        time.sleep(ms / 1000.0)
        return 1

    @staticmethod
    def handle_sys_cwd(state: InterpreterState) -> int:
        state.add_output(os.getcwd())
        return 0

    @staticmethod
    def handle_sys_exit(state: InterpreterState, tokens: List[str], index: int) -> int:
        # Record desired exit code into variable; actual process exit is up to the caller
        code = 0
        if index + 1 < len(tokens):
            try:
                code = int(tokens[index + 1])
            except ValueError:
                code = 1
        state.set_variable("_exit", code)
        state.add_output(f"Exit code set to {code}")
        return 1 if index + 1 < len(tokens) else 0


class ProcessOpsHandler:
    _stream_cache: Dict[str, List[str]] = {}

    @staticmethod
    def handle_proc_spawn(state: InterpreterState, tokens: List[str], index: int) -> int:
        from .basic_commands import BasicCommandHandler  # Local import to avoid circular dependency

        cursor = index + 1
        cmd_parts: List[str] = []
        stop_tokens = BasicCommandHandler.KNOWN_COMMANDS.union({"end"})
        while cursor < len(tokens):
            token = tokens[cursor]
            if cmd_parts and token in stop_tokens:
                break
            cmd_parts.append(token)
            cursor += 1

        if not cmd_parts:
            state.add_error("proc_spawn requires a command")
            return 0

        cmd_text = " ".join(cmd_parts)
        if cmd_text.startswith('"') and cmd_text.endswith('"') and cmd_text.count('"') == 2:
            cmd = cmd_text[1:-1]
        else:
            cmd = cmd_text
        try:
            args = shlex.split(cmd)

            # On Windows, `python` may resolve to an App Execution Alias (Store shim).
            # Prefer the interpreter running TechLang to keep behavior deterministic.
            if args:
                exe = os.path.basename(args[0]).lower()
                if exe in {"python", "python.exe"}:
                    args[0] = sys.executable
            p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            pid = state.next_process_id
            state.next_process_id += 1
            state.processes[pid] = p
            state.process_start_times[pid] = time.monotonic()
            # Reset any cached output for this pid (ids restart each interpreter run)
            out_key = f"proc_{pid}_out"
            err_key = f"proc_{pid}_err"
            state.arrays.pop(out_key, None)
            state.arrays.pop(err_key, None)
            ProcessOpsHandler._stream_cache.pop(out_key, None)
            ProcessOpsHandler._stream_cache.pop(err_key, None)
            state.add_output(str(pid))
            return len(cmd_parts)
        except Exception as e:
            state.add_error(f"proc_spawn failed: {e}")
            return len(cmd_parts)

    @staticmethod
    def handle_proc_wait(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("proc_wait requires process_id")
            return 0
        try:
            pid = int(tokens[index + 1])
        except ValueError:
            state.add_error("process_id must be an integer")
            return 0
        timeout_seconds = 30.0
        if index + 2 < len(tokens):
            try:
                timeout_seconds = float(tokens[index + 2])
            except ValueError:
                state.add_error("proc_wait timeout must be a number of seconds")
                return 1
        p = state.processes.get(pid)
        if p is None:
            state.add_error(f"Unknown process {pid}")
            return 1
        try:
            out, err = p.communicate(timeout=timeout_seconds)
            ProcessOpsHandler._stream_process_output(state, pid, out, is_stdout=True)
            ProcessOpsHandler._stream_process_output(state, pid, err, is_stdout=False)
            state.set_variable(f"proc_{pid}_status", p.returncode)
            state.process_start_times.pop(pid, None)
            return 1 if index + 2 >= len(tokens) else 2
        except subprocess.TimeoutExpired:
            state.add_error("proc_wait timeout")
            return 1

    @staticmethod
    def handle_proc_kill(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("proc_kill requires process_id")
            return 0
        try:
            pid = int(tokens[index + 1])
        except ValueError:
            state.add_error("process_id must be an integer")
            return 0
        p = state.processes.get(pid)
        if p is None:
            state.add_error(f"Unknown process {pid}")
            return 1
        try:
            p.kill()
            state.add_output(f"Killed {pid}")
            state.process_start_times.pop(pid, None)
            return 1
        except Exception as e:
            state.add_error(f"proc_kill failed: {e}")
            return 1

    @staticmethod
    def handle_proc_status(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("proc_status requires process_id")
            return 0
        try:
            pid = int(tokens[index + 1])
        except ValueError:
            state.add_error("process_id must be an integer")
            return 0
        p = state.processes.get(pid)
        if p is None:
            state.add_error(f"Unknown process {pid}")
            return 1
        code = p.poll()
        if code is None:
            # On Windows, process startup can be slow (especially for Python).
            # If the process has been alive for a bit, do a short wait to reduce flakiness.
            started = state.process_start_times.get(pid)
            if started is not None:
                elapsed = time.monotonic() - started
                if elapsed >= 0.15:
                    try:
                        code = p.wait(timeout=1.0)
                    except subprocess.TimeoutExpired:
                        code = None
        if code is None:
            state.add_output("running")
        else:
            state.set_variable(f"proc_{pid}_status", code)
            state.add_output(str(code))
            state.process_start_times.pop(pid, None)
        return 1

    @staticmethod
    def _stream_process_output(state: InterpreterState, pid: int, data: str, *, is_stdout: bool) -> None:
        if not data:
            return
        lines = [line for line in data.splitlines() if line]
        for line in lines:
            state.add_output(line)
        array_name = f"proc_{pid}_{'out' if is_stdout else 'err'}"
        existing = state.arrays.get(array_name, [])
        existing.extend(lines)
        state.arrays[array_name] = existing
        ProcessOpsHandler._stream_cache[array_name] = list(existing)

    @classmethod
    def hydrate_stream_array(cls, state: InterpreterState, array_name: str) -> bool:
        if array_name in state.arrays:
            return True
        cached = cls._stream_cache.get(array_name)
        if cached is None:
            return False
        state.arrays[array_name] = list(cached)
        return True

    @classmethod
    def prime_cached_streams(cls, state: InterpreterState) -> None:
        if not cls._stream_cache:
            return
        for name, lines in cls._stream_cache.items():
            if name not in state.arrays:
                state.arrays[name] = list(lines)


