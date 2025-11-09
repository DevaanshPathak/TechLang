# TechLang REPL Guide

## Overview

TechLang's REPL (Read-Eval-Print Loop) provides an interactive environment for testing code, exploring features, and rapid prototyping.

## Starting the REPL

```bash
tl -i
```

You'll see:
```
TechLang REPL v1.1 - Enhanced Edition
Type ':help' for commands, ':quit' to exit
tl>
```

## Basic Usage

### Simple Commands
```
tl> set x 10
tl> print x
10
tl> add x 5
tl> print x
15
```

### Multi-line Blocks

The REPL automatically detects blocks and provides auto-indentation:

```
tl> def greet name do
...     print "Hello"
...     print name
... end
tl> call greet "Alice"
Hello
Alice
```

**Block Keywords**: `def`, `if`, `loop`, `while`, `switch`, `try`, `match`, `macro`, `struct`

## Persistent State

**NEW in v1.1**: State persists across commands within a session!

```
tl> set counter 0
tl> add counter 1
tl> print counter
1
tl> add counter 1
tl> print counter
2
```

Variables, strings, arrays, dicts, functions, and macros all persist until you `:reset` or exit.

## Meta-Commands

Meta-commands start with `:` and provide REPL management features.

### `:help` - Show Help
```
tl> :help
```
Displays all available meta-commands and their descriptions.

### `:state` - Show Current State
```
tl> set x 10
tl> set y 20
tl> str_set greeting "Hello"
tl> :state
=== Current Interpreter State ===

Variables:
  x = 10
  y = 20

Strings:
  greeting = "Hello"

Arrays:
  (none)

Dictionaries:
  (none)

Functions:
  (none)
```

Shows:
- All variables and their values
- All strings and their contents
- All arrays and their elements
- All dictionaries and their contents
- All defined functions

### `:macros` - List Macros
```
tl> macro greet name do
...     print "Hello"
...     print name
... end
tl> :macros
=== Defined Macros ===
  greet (parameters: name)
```

Shows all defined macros with their parameter names.

### `:reset` - Clear State
```
tl> set x 10
tl> print x
10
tl> :reset
[Interpreter state reset]
tl> print x
[Error: Undefined variable 'x'.]
```

Clears all:
- Variables
- Strings
- Arrays
- Dictionaries
- Functions
- Macros
- Loaded modules

Use this to start fresh without restarting the REPL.

### `:load <file>` - Load and Execute File
```
tl> :load examples/hello.tl
[Loaded examples/hello.tl]
[booting hacker system...]
[system online]
```

Loads and executes a TechLang file. State from the file persists in the REPL session.

**Example workflow:**
```
tl> :load examples/functions.tl
[Loaded examples/functions.tl]
tl> call square 5
25
```

### `:loadmacro <file>` - Load Macro Library
```
tl> :loadmacro examples/macros_library
[Loaded macros from examples/macros_library.tl]
tl> :macros
=== Defined Macros ===
  debug_log (parameters: if, debug_enabled, msg)
  repeat_cmd (parameters: times, cmd, arg)
  assert (parameters: condition, msg)
  ...
```

Loads macro definitions from a file **without executing the file**. Only macros are registered, no other commands run.

**Difference from `:load`:**
- `:load file.tl` - Executes all commands in file
- `:loadmacro file.tl` - Only registers macros, skips other commands

### `:history` - Show Command History
```
tl> set x 10
tl> add x 5
tl> :history
1: set x 10
2: add x 5
3: :history
```

Displays command history for the current session. History is persisted to `~/.techlang_history` and available across sessions.

### `:clear` - Clear Screen
```
tl> :clear
```

Clears the terminal screen. Useful for decluttering during long sessions.

### `:quit` - Exit REPL
```
tl> :quit
```

Exits the REPL. You can also use `Ctrl+C` or `Ctrl+D`.

## Command History

TechLang REPL includes full readline support:

### Navigation
- **Up/Down Arrows**: Navigate through command history
- **Ctrl+R**: Reverse search through history
- **Ctrl+A**: Move cursor to start of line
- **Ctrl+E**: Move cursor to end of line
- **Ctrl+K**: Delete from cursor to end of line
- **Ctrl+U**: Delete from cursor to start of line

### History File
Command history is saved to `~/.techlang_history` and persists across sessions.

## Auto-Indentation

The REPL automatically indents when entering blocks:

```
tl> def factorial n do
...     if n eq 1
...         # 4-space indent
...     end
...     # Back to 4-space
... end
```

**Indentation Rules:**
- 4 spaces per nesting level
- Automatically indented after block keywords
- Dedented after `end`

## Error Handling

Errors are displayed inline with context:

```
tl> invalid_command
[Error: Unknown command 'invalid_command'.]

tl> set x 10
tl> div x 0
[Error: Cannot divide by zero.]
```

The REPL continues after errors - state is preserved.

## Advanced Features

### Testing Snippets
```
tl> # Test a function quickly
tl> def double x do
...     mul x 2
... end
tl> call double 5
10
tl> call double 10
20
```

### Debugging
```
tl> set debug 1
tl> macro log if debug msg do
...     print "[DEBUG]"
...     print $msg
... end
tl> inline log "Testing"
[DEBUG]
Testing
```

### Module Development
```
tl> :load stl/validation
[Loaded stl/validation.tl]
tl> call stl.validation.is_positive 10
1
tl> call stl.validation.is_positive -5
0
```

### Macro Prototyping
```
tl> macro safe_div num denom result do
...     if $denom eq 0
...         print "Division by zero"
...         set $result 0
...     else
...         set $result $num
...         div $result $denom
...     end
... end
tl> set a 10
tl> set b 2
tl> set c 0
tl> inline safe_div a b c
tl> print c
5
```

## Tips and Tricks

### 1. Use `:state` for Debugging
```
tl> set x 10
tl> :state
# See all variables at a glance
```

### 2. Reset When Stuck
```
tl> :reset
# Start fresh without restarting
```

### 3. Load Libraries Once
```
tl> :loadmacro examples/macros_library
# Now all macros available for session
```

### 4. Test Functions Interactively
```
tl> :load mycode.tl
tl> call my_function test_input
# See results immediately
```

### 5. Use History Search
Press `Ctrl+R` and type to search command history:
```
(reverse-i-search)`def': def greet name do
```

### 6. Multi-line Editing
Use `\` to continue long commands (though blocks auto-detect):
```
tl> set long_var 123
```

### 7. Verbose Mode
Start REPL with verbose flag to see detailed execution:
```bash
tl -i -v
```

## Common Workflows

### Workflow 1: Function Development
```
tl> # Write function
tl> def calculate x y do
...     add x y
...     mul x 2
... end

tl> # Test it
tl> call calculate 5 3
16

tl> # Debug if needed
tl> :state
tl> # Check variable values

tl> # Refine and test again
tl> :reset
tl> def calculate x y do
...     # Improved version
... end
```

### Workflow 2: Macro Library Development
```
tl> # Create macros
tl> macro log_info msg do
...     print "[INFO]"
...     print $msg
... end

tl> # Test them
tl> inline log_info "Test message"
[INFO]
Test message

tl> # Save to file (outside REPL)
# Create mylib.tl with macro definitions

tl> # Load in future sessions
tl> :loadmacro mylib
```

### Workflow 3: Module Testing
```
tl> # Load module
tl> :load stl/math

tl> # Check what's available
tl> :state
# See exported functions

tl> # Test functions
tl> call stl.math.abs -5
5

tl> call stl.math.max 10 20
20
```

### Workflow 4: Debugging Issues
```
tl> :load problematic_code.tl
[Error: ...]

tl> # Check state
tl> :state

tl> # Try commands manually
tl> set test_var 10
tl> # ... reproduce issue ...

tl> # Reset and try again
tl> :reset
tl> # ... test fix ...
```

## Keyboard Shortcuts Summary

| Shortcut | Action |
|----------|--------|
| `Up/Down` | Navigate history |
| `Ctrl+R` | Reverse search |
| `Ctrl+C` | Interrupt/Exit |
| `Ctrl+D` | Exit REPL |
| `Ctrl+A` | Start of line |
| `Ctrl+E` | End of line |
| `Ctrl+K` | Kill to end |
| `Ctrl+U` | Kill to start |
| `Tab` | (Future: auto-complete) |

## Configuration

### History File Location
- Linux/Mac: `~/.techlang_history`
- Windows: `%USERPROFILE%\.techlang_history`

### History Size
Default: 1000 commands

## Troubleshooting

### Issue: Commands Not Persisting
**Problem:** Variables disappear between commands

**Solution:** This was fixed in v1.1. If you're using an older version, upgrade:
```bash
git pull
```

### Issue: Block Not Detected
**Problem:** `end` keyword doesn't close block

**Solution:** Ensure block keyword is recognized:
- Valid: `def`, `if`, `loop`, `while`, `switch`, `try`, `match`, `macro`, `struct`
- Not valid: `struct new`, `struct set` (these are single commands)

### Issue: History Not Saving
**Problem:** Command history lost between sessions

**Solution:** Check permissions on `~/.techlang_history`:
```bash
chmod 644 ~/.techlang_history
```

### Issue: Macros Not Loading
**Problem:** `:loadmacro` fails

**Solution:** 
1. Check file path is relative to current directory
2. Ensure file has `.tl` extension
3. Verify file contains valid macro definitions

## See Also

- [General Documentation](general.md) - TechLang syntax basics
- [Macro Guide](macros-advanced.md) - Advanced macro features
- [Examples](../examples/) - Sample TechLang programs
- [CLI Help](help-cli.md) - Command-line options

## Version History

- **v1.0**: Basic REPL with block detection and history
- **v1.1**: Added persistent state, `:state`, `:macros`, `:reset`, `:loadmacro` commands
