# TechLang agent guide

## Core architecture
- `techlang.interpreter.run(code, inputs=None, loaded_files=None, base_dir=None)` is the entrypoint; the CLI (`cli.py` / `tl`) sets `base_dir` to the file folder and streams the captured output.
- Execution pipeline: `parser.parse` → `MacroHandler.process_macros` → `AliasHandler.process_aliases` → `CommandExecutor.execute_block`. Every block terminates with the literal `end` (no braces/indent inference).
- `blocks.BlockCollector.collect_block` handles nested depth tracking for `def`, `if`, `loop`, `while`, `switch`, `match`, `try`, `macro`, and `struct` (except `struct new/set/get/dump`).
- `executor.CommandExecutor.execute_block` fans out to handlers like `basic_commands.py`, `memory_ops.py`, `database.py`, `thread_ops.py`; keep new tokens in those modules.
- All user-visible text must go through `InterpreterState.add_output` / `add_error`; tests assert prefixes and ordering, so never `print()` directly.

## State & data conventions
- `InterpreterState` (in `core.py`) carries stack, vars, strings, arrays, dicts, structs, plus bookkeeping (`thread_results`, `processes`, `mutexes`, `queues`, `memory`, `next_address`). Update these containers instead of ad-hoc fields.
- `print <name>` resolves strings before numeric vars; struct values render as `Type{field: value}` (see `struct_ops.py`). Match that formatting when extending structs.
- File commands resolve paths relative to `base_dir` and expect quoted literals: `file_write "path" "text"`, `file_read "path" var`. Path traversal outside `base_dir` is blocked for security.
- The `debug` command prints: Stack, Vars, Arrays, Strings, Dictionaries, Structs (in that exact order). Changing labels or sequence will break `tests/test_interpreter.py`.

## Modules, macros, aliases
- `package use foo` loads `foo.tl` relative to `base_dir`, runs it in a child state (with `parent_state` fallback), then registers aliases/functions under `state.modules['foo']`; invoke with `call foo.bar` or `call foo::bar` (see `tests/test_modules.py`).
- `import foo` inlines tokens from `foo.tl` once (tracked via `state.loaded_files`) and enforces sandbox boundaries.
- `aliases.AliasHandler.process_aliases` expands alias tokens pre-execution; prefer touching `aliases.py` instead of sprinkling manual replacements.
- Macros live in `macros.py`; they expand at compile-time using `$param` placeholders and emit real TechLang tokens so downstream handlers stay unchanged.

## Adding or tweaking commands
- Wire new keywords in three spots: 
  1. Add to `basic_commands.BasicCommandHandler.KNOWN_COMMANDS` set
  2. Route in `CommandExecutor.execute_block` with `elif token == "newcmd": consumed = Handler.handle_newcmd(...)`
  3. Document in `help_ops.HELP_TEXT` dict (also update `tests/test_help.py`)
- Handlers should follow the existing signature (state, tokens, index), mutate state, and push textual results via `state.add_output(...)` / `add_error(...)` before returning.
- Return consumed token count (usually 0 for no-args, 1+ for multi-token commands) to advance the executor index correctly.
- Use lowercase TechLang tokens with Python handlers named `handle_<token>` for clarity and discoverability.

## Persistence, I/O, and external deps
- `database.DatabaseHandler` is a singleton pointing at `techlang.db`; `db_connect` swaps the active file. Keep SQL output wording identical to maintain snapshot-based tests.
- Network helpers rely on `requests`; graphics need `Pillow`. On missing deps, emit the exact pattern `[Error: 'requests' library not available]` / `[Error: 'Pillow' library not available]` so tests pass.
- Thread/process primitives stash results inside state (`thread_ops.py`, `system_ops.py`); update those maps when introducing new async behaviors.
- Graphics output saves to `techlang_canvas.png` in the working directory.

## Tooling & tests
- Run the full suite with `python run_tests.py` (pytest wrapper calling `pytest.main(["tests", "-v", "--maxfail=1", "--disable-warnings"])`). Tests assert literal output lines—match spacing, casing, and prefixes exactly.
- Test pattern: `assert run(code).strip() == "expected"` or `assert run(code).strip().splitlines() == ["line1", "line2"]`
- Formatter/linter: `python format_tl.py --check file.tl` (check formatting), `--fix` (reformat in place), `--lint` (detect issues like unclosed blocks, undefined vars). CI enforces formatting on all .tl files via `.github/workflows/techlang-format.yml`.
- Sync examples (`examples/`) and docs (`docs/*.md`) whenever you add or rename commands so the CLI, GUI (`playground/gui.py`), and web app (`techlang_web/app.py`) stay aligned.
- CLI modes: `tl file.tl` (run file), `tl -i` (REPL), `tl -v file.tl` (verbose—streams each command before execution, helpful for tracing parser vs executor).

## Debugging & workflows
- When troubleshooting modules or macros, write minimal `.tl` repros in `examples/` and run them through `python cli.py example.tl` for consistent `base_dir` handling.
- REPL (`tl -i`) features enhanced interactive mode: command history persisted to `~/.techlang_history`, auto-indentation (4 spaces per block depth), and meta-commands (`:load file.tl`, `:help`, `:clear`, `:history`).
- REPL block detection: tracks depth across `def`, `if`, `loop`, `while`, `switch`, `try`, `match`, `macro`, `struct` (but not `struct new/set/get/dump`), executes when depth returns to zero.
- Use `ProcessOpsHandler.prime_cached_streams(state)` before execution to capture subprocess output correctly.
