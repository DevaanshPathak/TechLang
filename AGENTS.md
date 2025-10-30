# TechLang AI Agent Guide

This document serves as a comprehensive guide for AI agents working on the TechLang project. It provides architectural overview, development workflows, and best practices to ensure productive and consistent contributions.

---

## 🎯 Quick Start for AI Agents

**Before making any changes:**
1. Read `.github/copilot-instructions.md` for detailed architecture
2. Understand the execution pipeline: `parser.parse` → `MacroHandler` → `AliasHandler` → `CommandExecutor`
3. Review existing tests to understand patterns
4. Always run `python run_tests.py` before and after changes

**Core Principle:** TechLang is a stack-based, hacker-themed language with strict output discipline - all user-facing text MUST go through `InterpreterState.add_output()` / `add_error()`.

---

## 🏗️ Architecture Overview

### Execution Pipeline

```
Source Code → Parser → Macro Processing → Alias Expansion → Command Execution → Output
```

1. **Parser** (`techlang/parser.py`): Tokenizes source, handles comments, preserves quoted strings
2. **Macro Handler** (`techlang/macros.py`): Expands `macro ... do ... end` definitions with `$param` substitution
3. **Alias Handler** (`techlang/aliases.py`): Expands registered aliases before execution
4. **Command Executor** (`techlang/executor.py`): Routes tokens to domain-specific handlers
5. **Output System** (`InterpreterState.add_output()`): Centralized output for testability

### State Management

`InterpreterState` (in `core.py`) maintains:
- **Stack**: Main execution stack for operations
- **Variables**: Named numeric values (`vars`)
- **Strings**: Named text values (`strings`)
- **Arrays**: Named lists (`arrays`)
- **Dictionaries**: Named key-value pairs (`dicts`)
- **Structs**: Named structured types (`structs`)
- **Functions**: User-defined functions (`functions`)
- **Modules**: Loaded module namespaces (`modules`)
- **Threads**: Background thread tracking (`thread_results`, `threads`)
- **Memory**: Simulated memory cells (`memory`, `next_address`)
- **Processes**: System process tracking (`processes`)
- **Output**: Accumulated output lines (`output`)

### Command Routing

Commands are routed through `CommandExecutor.execute_block()` to specialized handlers:

| Handler Module | Commands | Purpose |
|---------------|----------|---------|
| `basic_commands.py` | `boot`, `ping`, `crash`, `print`, `upload`, `download`, `debug`, `hack`, `lag`, `sleep`, `yield` | Core language operations |
| `variables.py` | `set`, `add`, `sub`, `mul`, `div`, `input` | Variable operations |
| `control_flow.py` | `if`, `loop`, `while`, `switch`, `case`, `match`, `try`, `catch` | Control structures |
| `data_types.py` | `array_*`, `str_*`, `dict_*` | Data structure operations |
| `struct_ops.py` | `struct` | Structured types |
| `file_ops.py` | `file_*` | File I/O operations |
| `net_ops.py` | `http_*`, `server_*` | Network operations |
| `graphics_ops.py` | `graphics_*` | Graphics rendering |
| `database.py` | `db_*` | SQLite database operations |
| `memory_ops.py` | `mem_*` | Memory management |
| `math_ops.py` | `math_*`, `now`, `format_date` | Math and date utilities |
| `thread_ops.py` | `thread_*`, `async_*`, `mutex_*`, `queue_*` | Concurrency primitives |
| `system_ops.py` | `sys_*`, `proc_*` | System and process operations |
| `help_ops.py` | `help` | Help system |

---

## 🔧 Adding New Features

### Step-by-Step Process

1. **Design**: Determine command syntax and behavior
2. **Wire command**: Add to `BasicCommandHandler.KNOWN_COMMANDS` set
3. **Route**: Add handler call in `CommandExecutor.execute_block()`
4. **Implement**: Create handler function (signature: `state, tokens, index → consumed_count`)
5. **Test**: Write comprehensive tests in `tests/`
6. **Document**: Update `help_ops.HELP_TEXT`, relevant `docs/*.md`, and `README.md`
7. **Example**: Create demo in `examples/`
8. **Validate**: Run full test suite

### Example: Adding a New Command

```python
# 1. Add to KNOWN_COMMANDS (basic_commands.py)
KNOWN_COMMANDS = {
    # ... existing commands ...
    "my_new_cmd",
}

# 2. Route in executor (executor.py)
elif token == "my_new_cmd":
    consumed = MyHandler.handle_my_new_cmd(state, tokens, i)
    i += consumed

# 3. Implement handler (my_handler.py)
class MyHandler:
    @staticmethod
    def handle_my_new_cmd(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("my_new_cmd requires an argument")
            return 0
        
        arg = tokens[index + 1]
        # ... do work ...
        state.add_output(f"Result: {result}")
        return 1  # consumed 1 token (arg)

# 4. Add help text (help_ops.py)
HELP_TEXT = {
    # ... existing help ...
    "my_new_cmd": "my_new_cmd <arg> — description of what it does",
}

# 5. Write tests (tests/test_my_feature.py)
def test_my_new_cmd():
    code = "my_new_cmd foo"
    assert run(code).strip() == "Result: foo"
```

---

## ✅ Testing Guidelines

### Test Structure

- **Location**: `tests/test_*.py`
- **Runner**: `python run_tests.py` (calls pytest with strict options)
- **Assertions**: Test exact output including whitespace, prefixes, and ordering

### Test Patterns

```python
from techlang.interpreter import run

# Simple output test
def test_simple():
    code = "set x 5\nprint x"
    assert run(code).strip() == "5"

# Multi-line output test
def test_multiline():
    code = "print 1\nprint 2\nprint 3"
    output = run(code).strip().splitlines()
    assert output == ["1", "2", "3"]

# Error message test
def test_error():
    code = "invalid_command"
    output = run(code).strip()
    assert "[Error: Unknown command 'invalid_command'" in output

# Integration test
def test_with_files(tmp_path):
    # Use tmp_path for file operations
    code = f'file_write "test.txt" "hello"'
    run(code, base_dir=str(tmp_path))
    # ... assertions ...
```

### Critical Test Requirements

- **Output discipline**: Never use `print()` directly - always `state.add_output()`
- **Exact matching**: Tests assert exact prefixes and formatting
- **Base directory**: Use `base_dir` parameter for file operations
- **Cleanup**: Use pytest fixtures (`tmp_path`) for file system tests

---

## 📝 Documentation Standards

### Files to Update

1. **`help_ops.py`**: Add command to `HELP_TEXT` dict
2. **`docs/*.md`**: Update relevant documentation file (general, control-flow, data-types, etc.)
3. **`README.md`**: Add to feature highlights and quick reference sections
4. **`DOCUMENTATION.md`**: Ensure master index is current
5. **`examples/`**: Create standalone `.tl` demo file

### Documentation Format

```markdown
## Command Name

Brief description of what it does.

### Syntax

\`\`\`techlang
command_name arg1 arg2
\`\`\`

### Parameters

- `arg1` - Description of first argument
- `arg2` - Description of second argument

### Example

\`\`\`techlang
set x 10
command_name x 5
print x
\`\`\`

### Notes

- Special behaviors or edge cases
- Limitations or requirements
```

---

## 🎨 Code Style

### Python Conventions

- **Type hints**: Use for all function parameters and returns
- **Naming**: 
  - TechLang tokens: lowercase (`set`, `print`, `array_create`)
  - Python functions: `snake_case` (`handle_print`, `get_value`)
  - Classes: `PascalCase` (`InterpreterState`, `CommandExecutor`)
- **Docstrings**: Add to all public functions and classes
- **Imports**: Group stdlib, third-party, local; sort alphabetically

### TechLang Conventions

- **Block terminators**: Always use literal `end` keyword
- **Strings**: Double quotes only (`"text"`)
- **Case sensitivity**: Commands lowercase, variables case-sensitive
- **Whitespace**: Space-separated tokens on single lines

---

## 🚨 Common Pitfalls

### 1. Output Discipline Violations

❌ **Wrong:**
```python
def handle_cmd(state):
    print("Hello")  # NEVER do this!
```

✅ **Correct:**
```python
def handle_cmd(state):
    state.add_output("Hello")
```

### 2. Block Depth Tracking

Blocks that affect depth (must have `end`):
- `def`, `if`, `loop`, `while`, `switch`, `match`, `try`, `macro`, `struct` (type definitions)

Commands that DON'T affect depth:
- `struct new`, `struct set`, `struct get`, `struct dump`

### 3. Path Resolution

Always resolve file paths relative to `base_dir`:
```python
from pathlib import Path

def handle_file_op(state, path_str):
    if not state.base_dir:
        state.add_error("Cannot resolve path without base_dir")
        return
    
    full_path = Path(state.base_dir) / path_str
    # ... validate and use full_path ...
```

### 4. Dependency Handling

Check for optional dependencies gracefully:
```python
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

def handle_http_get(state, tokens, index):
    if not HAS_REQUESTS:
        state.add_error("[Error: 'requests' library not available]")
        return 0
    # ... proceed with requests ...
```

---

## 🔍 Debugging Tips

### Verbose Mode

Run files with `-v` flag to see each command before execution:
```bash
tl -v examples/debug_me.tl
```

### REPL for Quick Testing

Use interactive mode to test snippets:
```bash
tl -i
```

REPL features:
- Command history (persisted to `~/.techlang_history`)
- Auto-indentation for blocks
- Meta-commands: `:load`, `:help`, `:clear`, `:history`, `:quit`

### Test Isolation

Run specific test file or function:
```bash
python -m pytest tests/test_specific.py -v
python -m pytest tests/test_file.py::test_function_name -v
```

---

## 📦 Module System

### Using Modules

```techlang
package use utils.helpers
call utils.helpers::greet
call utils.helpers.greet   # both :: and . work
```

### Module Resolution

- Modules resolved relative to caller's `base_dir`
- `package use foo` loads `foo.tl` in same directory
- `package use utils/bar` loads `utils/bar.tl` subdirectory
- Loaded once per run (tracked in `state.loaded_modules`)

### Module State

- Runs in child `InterpreterState` with `parent_state` fallback
- Shares variables, strings, arrays, dicts, structs, output
- Functions registered under `state.modules['module_name']`

---

## 🧪 CI/CD Workflows

### GitHub Actions

1. **`python-app.yml`**: Runs full test suite on push/PR
2. **`techlang-format.yml`**: Validates `.tl` file formatting

### Pre-Commit Checklist

- [ ] All tests pass (`python run_tests.py`)
- [ ] New features have tests (minimum 3 test cases)
- [ ] Documentation updated (help text, docs, README)
- [ ] Example file created in `examples/`
- [ ] No `print()` statements (use `state.add_output()`)
- [ ] Code follows style guidelines
- [ ] No regressions in existing functionality

---

## 📚 Key Resources

- **Architecture**: `.github/copilot-instructions.md` (most detailed)
- **Examples**: `examples/*.tl` (runnable demonstrations)
- **Documentation**: `docs/*.md` (user-facing guides)
- **Tests**: `tests/*.py` (behavioral specifications)
- **CLI**: `cli.py` (entry point, REPL implementation)

---

## Template for Future Entries

When documenting changes, add entries below in this format:

```markdown
## YYYY-MM-DD: Feature Name

**Status:** 🚧 In Progress / ✅ Completed / ❌ Deprecated

### Summary
Brief description of the feature/change

### Motivation
Why this was needed

### Implementation Details
Technical details, design decisions, code changes

### Files Modified
- List of changed files

### Files Created
- List of new files

### Validation
Test results and verification steps

### Known Limitations
Any edge cases or constraints

### Future Enhancements
Potential improvements or follow-ups
```

---

## Contributing Guidelines for Agents

When adding new features to TechLang:

1. **Follow the architecture** - Review `.github/copilot-instructions.md` first
2. **Parser → Handler → Executor** - Understand the pipeline
3. **Output discipline** - Always use `state.add_output()` / `state.add_error()`
4. **Test coverage** - Write comprehensive tests before declaring complete
5. **Documentation** - Update relevant docs (general.md, README.md, help text)
6. **Examples** - Create `.tl` files in `examples/` demonstrating the feature
7. **Run full test suite** - Ensure no regressions (`python run_tests.py`)
8. **Update this file** - Document your changes here for future agents

### Code Style
- Use type hints in Python code
- Follow existing naming conventions (lowercase for TechLang tokens, snake_case for Python)
- Add docstrings to new functions/classes
- Keep handlers focused (single responsibility)

### Testing Philosophy
- Test happy paths AND edge cases
- Verify error messages match expected format exactly
- Test integration with existing features
- Include performance/security tests when relevant

### Documentation Standards
- Update inline help text in `help_ops.py`
- Add examples to relevant `docs/*.md` files
- Create standalone example in `examples/` directory
- Update `README.md` feature list
- Keep `DOCUMENTATION.md` index current

---

## 📋 Feature Additions Log

### 2025-01-XX: JSON Support

**Status:** ✅ Completed

**Summary:**  
Added comprehensive JSON support for modern application development with 4 new commands: `json_parse`, `json_stringify`, `json_read`, and `json_write`.

**Motivation:**  
JSON is critical for modern applications - APIs, config files, data exchange. TechLang needed native JSON support to be practical for real-world use cases.

**Implementation:**
- **Commands added:** 
  - `json_parse <source> <target>` - Parse JSON strings into TechLang structures
  - `json_stringify <source> <target>` - Convert structures to JSON strings
  - `json_read <path> <target>` - Read and parse JSON files
  - `json_write <source> <path>` - Write structures to JSON files

- **Type mapping:**
  - JSON objects ↔ TechLang dictionaries
  - JSON arrays ↔ TechLang arrays
  - JSON strings ↔ TechLang strings
  - JSON numbers ↔ TechLang variables
  - JSON booleans → 1/0 (true/false)
  - JSON null → 0

- **Key features:**
  - Unicode support (emoji, international characters)
  - Nested structures (objects within arrays/objects)
  - Path security (prevents directory traversal)
  - Roundtrip fidelity
  - Pretty-printed output (2-space indentation)

**Files Modified:**
- `techlang/data_types.py`: Added 4 JSON handler functions (~200 lines)
- `techlang/basic_commands.py`: Added JSON commands to KNOWN_COMMANDS
- `techlang/executor.py`: Routed JSON commands (passed base_dir for file ops)
- `techlang/help_ops.py`: Added help text for 4 JSON commands

**Files Created:**
- `tests/test_json.py`: 29 comprehensive tests
- `examples/json_demo.tl`: Full demonstration of JSON features
- `docs/data-types.md`: Added JSON operations section

**Validation:**
- ✅ All 29 JSON tests passing
- ✅ Full test suite: 233 tests passing (no regressions)
- ✅ Example file runs successfully
- ✅ Documentation updated

**Technical Notes:**
- Initially attempted string escaping approach but TechLang parser doesn't handle `\"` inside strings
- Solution: Use file-based tests to avoid parser escaping issues
- Boolean type check must come before int/float (bool is subclass of int in Python)
- File operations require `base_dir` parameter passed from executor to handlers
- Used `getattr(state, 'base_dir', None)` pattern initially but proper approach is passing as parameter

**Known Limitations:**
- JSON strings in TechLang code require simple content (no escaped quotes)
- For complex JSON, use file operations instead
- No pretty-print control (always 2-space indent)

**Future Enhancements:**
- Add `json_validate` command for schema validation
- Support JSON streaming for large files
- Add JSON pointer/path query support (e.g., `json_get data "user.address.city"`)

---

### 2025-01-XX: String Operations

**Status:** ✅ Completed  
Added 7 string manipulation commands: `str_split`, `str_replace`, `str_trim`, `str_upper`, `str_lower`, `str_contains`, `str_reverse`.  
35 tests passing.

### 2025-01-XX: Comment Support  

**Status:** ✅ Completed  
Added 3 comment styles: `#` (hash), `//` (C-style), `/* */` (multi-line).  
19 tests passing.

---

**Last Updated:** 2025-01-XX  
**Total Features Added:** 3  
**Total Tests:** 233
