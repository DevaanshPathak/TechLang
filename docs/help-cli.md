# Help & CLI in TechLang

TechLang includes a command-line interface (CLI) for running scripts, exploring code interactively, and accessing built-in documentation.

## Running Scripts

Execute a TechLang script file:

```bash
# Using Python
python cli.py examples/hello.tl

# Or using the tl command (if installed)
tl examples/hello.tl
```

## Interactive REPL

Start an interactive Read-Eval-Print Loop (REPL) session:

```bash
python cli.py -i
# or
tl -i
```

The REPL includes these features:
- **Command history**: Persisted to `~/.techlang_history`
- **Auto-indentation**: Automatically indents block content (4 spaces per depth)
- **Block detection**: Executes when block depth returns to zero
- **Meta-commands**: Special commands starting with `:`

### REPL Meta-Commands

| Command | Description |
|---------|-------------|
| `:load file.tl` | Load and execute a TechLang file |
| `:help` | Show help information |
| `:clear` | Clear the screen |
| `:history` | Show command history |
| `:quit` | Exit the REPL |

## Verbose Mode

Run files with verbose output to see each command before execution:

```bash
python cli.py -v examples/hello.tl
# or
tl -v examples/hello.tl
```

Verbose mode shows:
- Each command token before execution
- Helpful for debugging parser vs executor issues

## Built-In Help System

TechLang includes a comprehensive help system accessible from within programs:

### List All Commands

```techlang
help
```

Output shows all available commands with brief descriptions.

### Get Specific Command Help

```techlang
help print
help array_create
help json_parse
```

### Help Categories

Commands are organized into categories:
- Core & variables
- Control flow
- Data types (arrays, strings, dicts, structs)
- JSON operations
- File I/O
- Network & HTTP
- Graphics
- Math & date/time
- Database operations
- Memory management
- Concurrency & threading
- System & processes
- Debugging
- Modules & macros

## Exit Codes

Set the exit code for your script:

```techlang
sys_exit 0   # Success
sys_exit 1   # Error
```

The exit code is stored in the `_exit` variable and returned when the script ends.

## File Paths and Base Directory

When running a script file, TechLang sets the `base_dir` to the folder containing the script. All relative file operations resolve from this directory:

```techlang
# If running examples/database.tl, base_dir is examples/
file_write "output.txt" "Hello"  # Creates examples/output.txt
```

For security, path traversal outside `base_dir` is blocked.

## Running Tests

Run the full test suite:

```bash
python run_tests.py
```

Run specific test files:

```bash
python -m pytest tests/test_json.py -v
python -m pytest tests/test_debugger.py::test_breakpoint_sets_breakpoint -v
```

## Code Formatting

Format TechLang code:

```bash
# Check formatting (CI mode)
python format_tl.py --check examples/

# Fix formatting automatically
python format_tl.py --fix examples/hello.tl

# Lint code for issues
python format_tl.py --lint examples/
```

The formatter handles:
- Proper indentation for blocks
- Consistent spacing
- Preserves comments and quoted strings

## Example: Complete Workflow

```bash
# 1. Create a new script
echo "set x 10" > myscript.tl
echo "print x" >> myscript.tl

# 2. Format it
python format_tl.py --fix myscript.tl

# 3. Run it
python cli.py myscript.tl

# 4. Debug it interactively
python cli.py -i
> :load myscript.tl
> help set
> :quit
```

---

See the [Examples Index](examples.md) for more code samples.