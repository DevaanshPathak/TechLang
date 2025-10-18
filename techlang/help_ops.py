from typing import List, Dict
from .core import InterpreterState


HELP_TEXT: Dict[str, str] = {
    "boot": "Reset current value to 0",
    "ping": "Increment current value by 1",
    "crash": "Decrement current value by 1",
    "print": "Print current value, a variable, or a quoted string",
    "set": "set <var> <number> — assign an integer to a variable",
    "add": "add <var> <number|var> — add to a variable",
    "sub": "sub <var> <number|var> — subtract from a variable",
    "mul": "mul <var> <number|var> — multiply a variable",
    "div": "div <var> <number|var> — integer divide (safe error on 0)",
    "loop": "loop <count|var> ... end — repeat a block",
    "while": "while <var> <op> <number|var> ... end — conditional loop",
    "if": "if <var> <op> <number> ... end — conditional block",
    "def": "def <name> ... end — define a function",
    "call": "call <name> — call a function",
    "macro": "macro <name> [params...] do ... end — define compile-time macro using $param placeholders",
    "inline": "inline <name> <args...> — expand a macro inline before execution",
    "upload": "Push current value to the stack",
    "download": "Pop value from the stack into current value",
    "debug": "Print stack, variables, arrays/strings/dicts",
    "lag": "lag — pause for 1 second (blocking)",
    "sleep": "sleep <ms> — pause execution for the given milliseconds",
    "yield": "yield — yield control with no delay (scheduler-friendly)",
    "alias": "alias <short> <command> — create shorthand",
    "import": "import <name> — load name.tl once",
    "package": "package use <module> — load a module with namespaced calls",
    "match": "match <expr> ... case [op] <value> ... end — pattern guards with ==, !=, <, <=, >, >=",
    "db_create": "db_create <table> \"cols\" — create table",
    "db_insert": "db_insert <table> \"values\" — insert row",
    "db_select": "db_select \"SQL\" — run SELECT and print rows",
    "db_update": "db_update \"SQL\" — run UPDATE",
    "db_delete": "db_delete \"SQL\" — run DELETE",
    "db_execute": "db_execute \"SQL\" — run any SQL",
    "db_begin": "Begin transaction",
    "db_commit": "Commit current transaction",
    "db_rollback": "Roll back current transaction",
    "db_tables": "List tables",
    "db_schema": "db_schema <table> — show columns",
    "db_indexes": "db_indexes <table> — list indexes",
    "db_connect": "db_connect \"path\" — set current DB",
    "db_disconnect": "Disconnect all DBs",
    "array_create": "array_create <name> <size>",
    "array_set": "array_set <name> <idx> <value|var>",
    "array_get": "array_get <name> <idx>",
    "array_push": "array_push <name> <value|var>",
    "array_pop": "array_pop <name>",
    "array_map": "array_map <source> <target> <op> [value] — transform items (identity, add, mul, negate, double, square, abs)",
    "array_filter": "array_filter <source> <target> <predicate> [value] — keep items (even, odd, positive, negative, nonzero, gt, ge, lt, le, eq, ne, contains)",
    "str_create": "str_create <name> \"text\"",
    "str_concat": "str_concat <name> <stringVar|\"text\">",
    "str_length": "str_length <name>",
    "str_substring": "str_substring <name> <start> <end>",
    "dict_create": "dict_create <name>",
    "dict_set": "dict_set <name> \"key\" \"val\"",
    "dict_get": "dict_get <name> \"key\"",
    "dict_keys": "dict_keys <name> — print sorted keys with counts",
    "struct": "struct <Type> <fields...> end / struct new|set|get|dump — manage records",
    "file_read": "file_read \"path\" <var>",
    "file_write": "file_write \"path\" \"text\"",
    "file_append": "file_append \"path\" \"text\"",
    "file_exists": "file_exists \"path\"",
    "file_delete": "file_delete \"path\"",
    "file_list": "file_list \"dir\"",
    "http_get": "http_get \"url\" <respVar> — store body/status",
    "http_post": "http_post \"url\" <dataToken> — store response",
    "http_status": "http_status <respVar> — print saved status",
    "server_start": "server_start <port> — stub",
    "server_route": "server_route \"/path\" <handler> — stub",
    "server_stop": "Stop server (stub)",
    "graphics_init": "graphics_init <w> <h> — prepare canvas",
    "graphics_draw_line": "graphics_draw_line x1 y1 x2 y2",
    "graphics_draw_circle": "graphics_draw_circle x y r",
    "graphics_draw_text": "graphics_draw_text x y \"text\"",
    "graphics_show": "Save canvas to techlang_canvas.png",
    "math_sin": "math_sin <deg>",
    "math_cos": "math_cos <deg>",
    "math_sqrt": "math_sqrt <n>",
    "math_pow": "math_pow <b> <e>",
    "math_random": "math_random <lo> <hi>",
    "math_pi": "Print π",
    "math_e": "Print e",
    "mem_alloc": "mem_alloc <size> — allocate integer cells (returns base address)",
    "mem_free": "mem_free <addr>",
    "mem_read": "mem_read <addr>",
    "mem_write": "mem_write <addr> <value>",
    "mem_dump": "Print memory contents",
    "try": "try ... catch [errVar [stackVar]] ... end — run catch if [Error:] is emitted",
    "thread_create": "thread_create <fn> — run function in a background interpreter",
    "thread_join": "thread_join <id> — wait for thread output",
    "thread_sleep": "thread_sleep <ms> — pause execution",
    "thread_status": "thread_status <id> — report if a thread is running or finished",
    "thread_result": "thread_result <id> — fetch cached thread output without joining",
    "thread_list": "thread_list — list currently tracked thread ids",
    "thread_wait_all": "thread_wait_all — join every active thread and emit their outputs",
    "async_start": "async_start <fn> — alias for thread_create",
    "async_wait": "async_wait <id> — alias for thread_join",
    "mutex_create": "mutex_create <name> — create a named mutex",
    "mutex_lock": "mutex_lock <name> — acquire a mutex (30s timeout)",
    "mutex_unlock": "mutex_unlock <name> — release a mutex",
    "queue_push": "queue_push <queue> <value> — enqueue resolved value (auto-creates queue)",
    "queue_pop": "queue_pop <queue> <var> — dequeue into string/variable (waits up to 30s)",
    "sys_exec": "sys_exec \"cmd\" — run command",
    "sys_env": "sys_env <VAR> — print environment variable",
    "sys_time": "sys_time — unix timestamp",
    "sys_date": "sys_date — ISO timestamp",
    "sys_sleep": "sys_sleep <ms> — sleep for the given milliseconds",
    "sys_cwd": "sys_cwd — print current working directory",
    "sys_exit": "sys_exit [code] — store exit code in _exit",
    "proc_spawn": "proc_spawn \"cmd\" — start subprocess (returns id)",
    "proc_kill": "proc_kill <id> — terminate subprocess",
    "proc_wait": "proc_wait <id> [timeout] — wait, stream output lines, update arrays",
    "proc_status": "proc_status <id> — report running state or exit code",
}


class HelpOpsHandler:
    @staticmethod
    def handle_help(state: InterpreterState, tokens: List[str], index: int, known: List[str]) -> int:
        # help or help <command>
        if index + 1 < len(tokens) and tokens[index + 1] not in known:
            # If next token is quoted, ignore — not a command name
            pass
        if index + 1 >= len(tokens):
            # General help
            state.add_output("Commands:")
            for name in sorted(known):
                if name in {"end", "case", "default", "catch"}:
                    continue
                desc = HELP_TEXT.get(name, "")
                state.add_output(f"- {name}{': ' + desc if desc else ''}")
            state.add_output("Use: help <command> for details")
            return 0
        command = tokens[index + 1]
        desc = HELP_TEXT.get(command, None)
        if desc is None:
            state.add_output(f"No help available for '{command}'")
        else:
            state.add_output(f"{command}: {desc}")
        return 1


