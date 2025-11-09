# Enhanced Macro System Documentation

## Overview

TechLang's enhanced macro system provides powerful compile-time code generation with conditional expansion, nested macros, and macro libraries.

## Basic Macro Definition

```techlang
macro name param1 param2 do
    # Macro body with $param1 and $param2 placeholders
    print $param1
    add $param2 1
end
```

## Conditional Macros

Macros can have conditional expansion based on variable values:

```techlang
set debug_enabled 1

macro debug_log if debug_enabled msg do
    print "[DEBUG]"
    print $msg
end

# This will expand when debug_enabled != 0
inline debug_log "Starting process"

# Disable debugging
set debug_enabled 0

# This will NOT expand (silently skipped)
inline debug_log "This won't appear"
```

### Conditional Syntax

```
macro <name> if <condition_var> <param1> <param2> ... do
    <body>
end
```

- `condition_var`: Variable name to check (expands if non-zero)
- Condition is checked at expansion time
- If condition is false/zero, expansion is skipped silently

## Nested Macro Expansion

Macros can invoke other macros:

```techlang
macro inner value do
    print $value
end

macro outer text do
    print "Outer:"
    inline inner $text
    print "Done"
end

inline outer "Hello"
```

**Output:**
```
Outer:
Hello
Done
```

### Recursion Detection

The macro system detects recursive expansion and reports errors:

```techlang
macro infinite do
    inline infinite
end

inline infinite  # Error: Recursive macro expansion detected
```

## Macro Libraries

### Creating a Macro Library

Create a `.tl` file with macro definitions:

```techlang
# mylib.tl
macro log_info msg do
    print "[INFO]"
    print $msg
end

macro log_error msg do
    print "[ERROR]"
    print $msg
end
```

### Loading Macro Libraries

#### In REPL:
```
tl> :loadmacro mylib
[Loaded macros from mylib.tl]
tl> inline log_info "System started"
[INFO]
System started
```

#### Programmatically:
```python
from techlang.macros import MacroHandler
from techlang.core import InterpreterState

state = InterpreterState()
MacroHandler.load_macro_library("mylib", state, base_dir="./")
```

## Advanced Examples

### 1. Debug Logging System

```techlang
# Enable/disable debug output
set debug 1

macro debug_log if debug msg do
    print "[DEBUG]"
    print $msg
end

macro debug_var if debug name val do
    print "[DEBUG]"
    print $name
    print $val
end

# Use it
set x 42
inline debug_log "Processing data"
inline debug_var "x = " x

# Disable debug
set debug 0
inline debug_log "This won't print"
```

### 2. Assertion Macros

```techlang
macro assert condition msg do
    if $condition eq 0
        print "[ASSERTION FAILED]"
        print $msg
    end
end

set x 5
set y 10
inline assert x "x should be positive"  # Passes (5 != 0)

set z 0
inline assert z "z should be non-zero"  # Fails
```

### 3. Code Patterns

```techlang
# Repeat pattern
macro repeat_n times cmd arg do
    loop $times
        $cmd $arg
    end
end

set counter 0
inline repeat_n 5 add counter

# counter is now 5
```

### 4. Safe Operations

```techlang
macro safe_div num denom result do
    if $denom eq 0
        print "[Error: Division by zero]"
        set $result 0
    else
        set $result $num
        div $result $denom
    end
end

set a 10
set b 2
set c 0

inline safe_div a b c
print c  # 5

set b 0
inline safe_div a b c  # Prints error, c = 0
```

## Best Practices

### 1. Use Descriptive Names
```techlang
# Good
macro validate_input value min max do
    ...
end

# Bad
macro chk v m n do
    ...
end
```

### 2. Document Macro Parameters
```techlang
# Calculate percentage
# $value: The value to convert
# $total: The total amount
# $result: Variable to store percentage
macro calc_percent value total result do
    set $result $value
    mul $result 100
    div $result $total
end
```

### 3. Use Conditionals for Optional Features
```techlang
set enable_logging 1
set enable_profiling 0

macro log if enable_logging msg do
    print $msg
end

macro profile if enable_profiling name do
    print "Profiling:"
    print $name
end
```

### 4. Create Macro Libraries for Reusable Code
Organize related macros into library files:
- `logging_macros.tl` - Logging utilities
- `math_macros.tl` - Math operations
- `validation_macros.tl` - Input validation
- `debug_macros.tl` - Debugging helpers

### 5. Test Macros Thoroughly
```techlang
# Test conditional expansion
set test_mode 1
macro test_log if test_mode msg do
    print "[TEST]"
    print $msg
end

inline test_log "Starting tests"
# ... run tests ...
inline test_log "Tests complete"
```

## Limitations

1. **No runtime expansion**: Macros are expanded at compile/parse time only
2. **Simple condition checking**: Conditional macros only check if variable is non-zero
3. **No macro overloading**: Cannot define multiple macros with same name
4. **Parameter substitution only**: Cannot do arithmetic in macro parameters
5. **No variadic macros**: Fixed number of parameters per macro

## Common Patterns

### Toggle Features
```techlang
set feature_a 1
set feature_b 0

macro feature_a_code if feature_a do
    # Feature A implementation
end

macro feature_b_code if feature_b do
    # Feature B implementation
end
```

### Platform-Specific Code
```techlang
set is_windows 1
set is_linux 0

macro windows_init if is_windows do
    print "Windows initialization"
end

macro linux_init if is_linux do
    print "Linux initialization"
end
```

### Development vs Production
```techlang
set development 1
set production 0

macro dev_log if development msg do
    print "[DEV]"
    print $msg
end

macro prod_log if production msg do
    # Log to file in production
    file_append "app.log" $msg
end
```

## See Also

- [Macro Examples](../examples/macros_library.tl) - Common macro library
- [Language Reference](general.md) - Basic macro syntax
- [REPL Guide](help-cli.md) - Using `:loadmacro` in REPL
