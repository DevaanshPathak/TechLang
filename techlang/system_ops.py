import os
import shlex
import subprocess
import time
import datetime as dt
from typing import List
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
    def handle_sys_time(state: InterpreterState) -> None:
        state.add_output(str(int(time.time())))

    @staticmethod
    def handle_sys_date(state: InterpreterState) -> None:
        state.add_output(dt.datetime.now().isoformat())

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
    @staticmethod
    def handle_proc_spawn(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("proc_spawn requires a quoted command")
            return 0
        cmd_token = tokens[index + 1]
        if not (cmd_token.startswith('"') and cmd_token.endswith('"')):
            state.add_error("proc_spawn requires a quoted command")
            return 0
        cmd = cmd_token[1:-1]
        try:
            args = shlex.split(cmd)
            p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            pid = state.next_process_id
            state.next_process_id += 1
            state.processes[pid] = p
            state.add_output(str(pid))
            return 1
        except Exception as e:
            state.add_error(f"proc_spawn failed: {e}")
            return 1

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
        p = state.processes.get(pid)
        if p is None:
            state.add_error(f"Unknown process {pid}")
            return 1
        try:
            out, err = p.communicate(timeout=30)
            if out:
                state.add_output(out.strip())
            if err:
                state.add_output(err.strip())
            state.set_variable(f"proc_{pid}_status", p.returncode)
            return 1
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
            return 1
        except Exception as e:
            state.add_error(f"proc_kill failed: {e}")
            return 1


