# System & Processes in TechLang

TechLang includes a small set of system utilities for running external commands, reading environment variables, and managing subprocesses.

## System Utilities

* `sys_exec "command"` — Runs the command without a shell, streaming stdout/stderr into the TechLang output. The exit code is stored in `_status`.
* `sys_env VAR_NAME` — Prints the value of an environment variable (empty string if missing).
* `sys_time` / `sys_date` — Emit the current UNIX timestamp or ISO-8601 datetime.
* `sys_sleep <milliseconds>` — Blocks the interpreter for the requested duration.
* `sys_cwd` — Prints the interpreter's current working directory.
* `sys_exit [code]` — Records the requested exit code in `_exit`; the outer host decides whether to terminate.

Example:

```techlang
sys_exec "\"python\" -c \"print('hi')\""
sys_env PATH
sys_sleep 100
sys_cwd
```

## Subprocess Management

The process commands let you start a long-running program and interact with it later:

* `proc_spawn "command"` — Launches the process and returns an id.
* `proc_status <id>` — Prints `running` while the process is alive; once it exits the exit code is printed and cached in `proc_<id>_status`.
* `proc_wait <id>` — Waits for completion (30s timeout), streams stdout/stderr, and stores the exit code in `proc_<id>_status`.
* `proc_kill <id>` — Terminates the process.

Commands that accept a path or command string must use double quotes. All commands run relative to the interpreter's base directory, so you can reference project scripts directly.

```techlang
proc_spawn "\"python\" -c \"import time; time.sleep(1)\""
proc_status 1    # running
sys_sleep 1100
proc_status 1    # 0
```

---

See the [Examples Index](examples.md) for additional demonstrations.