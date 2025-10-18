# TechLang agent playbook (short)

Quick, actionable points to get an AI coding agent productive in this repository.
# TechLang agent playbook

- Entrypoint & CLI
	- Interpreter entrypoint: `techlang.interpreter.run(code, inputs=None, loaded_files=None, base_dir=None)`.
	- CLI wrapper: `cli.py` exposes `tl`-style behavior; it sets `base_dir` to the script file's folder when running files and prints the collected output.

- Runtime pipeline (high-level)
	- Parsing: `parser.parse` produces tokens.
	- Alias expansion: `aliases.AliasHandler` collects/expands aliases.
	- Execution dispatch: `executor.CommandExecutor.execute_block` routes tokens to handler modules (e.g., `basic_commands.py`, `memory_ops.py`, `database.py`).
	- All output must flow through the `InterpreterState` instance (`InterpreterState.add_output` / `add_error`) — tests rely on exact output prefixes and ordering.

- Important concepts & files
	- `techlang/interpreter.py`: orchestrates the run loop and constructs `InterpreterState`.
	- `techlang/parser.py` and `techlang/blocks.py`: block collection (every block ends with literal `end`) and tokenization — do not assume brace-based blocks.
	- `techlang/imports.py`: `ImportHandler` still splices tokens inline; `ModuleHandler` backs the new `package use <module>` namespace loader and stores module states in `state.modules`/`loaded_modules`.
	- `techlang/variables.py`, `data_types.py`, `struct_ops.py`, `stack.py`: value containers (scalars, arrays, strings, dictionaries, structs, memory) and debugging helpers.
	- `techlang/database.py`: singleton `DatabaseHandler` uses `techlang.db` by default; `db_connect` changes the file.
	- `techlang/help_ops.py`: canonical `help` text — keep it in sync with command handlers and `tests/test_help.py`.

- Project-specific conventions (examples)
	- New commands must be wired in three places: add dispatch in `CommandExecutor.execute_block`, include token in `BasicCommandHandler.KNOWN_COMMANDS` (see `basic_commands.py`), and document text in `help_ops.HELP_TEXT`.
	- `package use foo` resolves `foo.tl` relative to `base_dir`, executes it in a child `InterpreterState`, and registers functions/aliases under the module key; invoke module functions with `call foo.bar` or `call foo::bar`. Tests live in `tests/test_modules.py`.
	- `struct <Type> ... end` defines field metadata; `struct new/set/get/dump` live in `struct_ops.py` and write into `state.struct_defs` / `state.structs`. Printing prefers struct instances before numeric variables so `print person` formats as `Type{field: value}`. See `tests/test_structs.py` for expected wording.
	- File paths are resolved relative to the `base_dir` argument passed to `run()` (the CLI sets this). File command arguments are quoted string literals (e.g., `file_write "path" "text"`) and tests assert exact response strings like `Wrote X bytes`.
	- Thread/process results are stored in state keys: processes use `_status` / `proc_<pid>_status`; threads put outputs into `state.thread_results`. Use those keys when adding synchronization primitives.

- External deps & graceful degradation
	- Optional: `requests` for network helpers; `Pillow` for graphics. Handlers emit a specific `[Error: 'requests' library not available]` or similar message when a dependency is missing — tests accept this pattern. Mirror that wording.

- Tests & workflows
	- Run quick checks: `python run_tests.py` (runs pytest with recommended flags). Unit tests in `tests/` are the source of truth for behavior — new suites `test_modules.py` and `test_structs.py` pin module + struct expectations.
	- Examples: `.tl` programs live in `examples/`; modify examples + tests when adding new language features.

- Debugging and output formatting
	- `debug` command prints internal structures in a fixed order (stack, vars, arrays, strings, dictionaries, structs); tests assert literal lines. Avoid reformatting those outputs or changing label names.
	- `print <name>` looks up `state.strings` before numeric variables — preserve lookup precedence when introducing new containers.

If anything here is unclear or you'd like more examples wired into specific files (tests or new command scaffolding), tell me which area to expand and I'll iterate.

```
