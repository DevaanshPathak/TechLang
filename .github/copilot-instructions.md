# TechLang agent guide

## Core architecture
- `techlang.interpreter.run(code, inputs=None, loaded_files=None, base_dir=None)` is the entrypoint; the CLI (`cli.py` / `tl`) sets `base_dir` to the file folder and streams the captured output.
- `parser.parse` and `blocks.collect_blocks` break `.tl` source into tokens; every block terminates with the literal `end` (no braces/indent inference).
- `executor.CommandExecutor.execute_block` fans out to handlers like `basic_commands.py`, `memory_ops.py`, `database.py`, `thread_ops.py`; keep new tokens in those modules.
- All user-visible text must go through `InterpreterState.add_output` / `add_error`; tests assert prefixes and ordering, so never `print()` directly.

## State & data conventions
- `InterpreterState` carries stack, vars, strings, arrays, dicts, structs, plus bookkeeping (`_status`, `proc_<pid>_status`, `thread_results`). Update these containers instead of ad-hoc fields.
- `print <name>` resolves strings before numeric vars; struct values render as `Type{field: value}` (see `struct_ops.py`). Match that formatting when extending structs.
- File commands resolve paths relative to `base_dir` and expect quoted literals: `file_write "path" "text"`, `file_read "path" var`.

## Modules, macros, aliases
- `package use foo` loads `foo.tl` relative to `base_dir`, runs it in a child state, then registers aliases/functions under `state.modules['foo']`; invoke with `call foo.bar` or `call foo::bar` (see `tests/test_modules.py`).
- `aliases.AliasHandler` expands alias tokens pre-execution; prefer touching `aliases.py` instead of sprinkling manual replacements.
- Macros live in `macros.py`; emit real TechLang tokens so downstream handlers stay unchanged.

## Adding or tweaking commands
- Wire new keywords in three spots: add to `basic_commands.BasicCommandHandler.KNOWN_COMMANDS`, route in `CommandExecutor.execute_block`, and document in `help_ops.HELP_TEXT` (also update `tests/test_help.py`).
- Handlers should follow the existing signature, mutate state, and push textual results via `state.add_output(...)` / `add_error(...)` before returning.
- Use lowercase TechLang tokens with Python handlers named `handle_<token>` for clarity and discoverability.

## Persistence, I/O, and external deps
- `database.DatabaseHandler` is a singleton pointing at `techlang.db`; `db_connect` swaps the active file. Keep SQL output wording identical to maintain snapshot-based tests.
- Network helpers rely on `requests`; graphics need `Pillow`. On missing deps, emit the exact pattern `[Error: 'requests' library not available]` / `[Error: 'Pillow' library not available]` so tests pass.
- Thread/process primitives stash results inside state (`thread_ops.py`, `system_ops.py`); update those maps when introducing new async behaviors.

## Tooling & tests
- Run the full suite with `python run_tests.py` (pytest wrapper). Tests assert literal output lines—match spacing, casing, and prefixes exactly.
- Sync examples (`examples/`) and docs (`docs/*.md`) whenever you add or rename commands so the CLI, GUI (`playground/gui.py`), and web app (`techlang_web/app.py`) stay aligned.
- Verbose CLI mode `tl -v path.tl` streams each command before execution—helpful when you need to trace parser vs executor behavior.

## Debugging
- The `debug` command prints stack, vars, arrays, strings, dicts, structs in that order; changing labels or sequence will break `tests/test_interpreter.py`.
- When troubleshooting modules or macros, write minimal `.tl` repros in `examples/` and run them through `python cli.py example.tl` for consistent `base_dir` handling.
