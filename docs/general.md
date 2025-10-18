# General Rules & Syntax in TechLang

This document outlines the fundamental syntax rules and conventions that govern the TechLang programming language.

## Basic Syntax Rules

| Topic | Details |
|------|---------|
| Case Sensitivity | Commands are lowercase (`print`, `set`, `add`); variables are case-sensitive (`counter` and `Counter` are different variables) |
| Statement Termination | One command per line; no semicolons required |
| Strings | Double quotes only: `"text"` (single quotes are not supported) |
| Comments | Use `#` for single-line comments; no multi-line comment syntax |
| Blocks | Begin with a keyword (`loop`, `if`, `def`, `while`, `switch`, `match`, `try`, `macro`) and end with `end` |
| Whitespace | Whitespace is used for separation but is otherwise ignored |
| Errors | Printed as `[Error: message]` (non-fatal); execution continues |
| Inputs | `input <var>` reads queued inputs (CLI/tests) or prompts user in interactive mode |

## Modules

Use `package use <module>` to execute another `.tl` file in a namespaced scope. Modules are resolved relative to the current script’s `base_dir`, so `package use utils/helpers` loads `utils/helpers.tl` next to the caller. Any functions defined inside the module are invoked with a qualified name:

```techlang
package use utils.helpers
call utils.helpers::greet
call utils.helpers.greet   # double-colon or dot both work
```

Modules run in a child `InterpreterState` that shares variables, strings, arrays, dictionaries, structs, and output with the caller. The runtime keeps `state.modules` / `state.loaded_modules` so each module is evaluated once per run.

## Macros

Use `macro <name> [params...] do ... end` to capture reusable snippets that expand before execution. Inside the body, reference parameters with `$param`. Invoke the macro with `inline <name> <args...>`; the generated tokens are inserted directly into the surrounding code. Recursive macro expansion is prevented to avoid infinite loops.

## Variables and Data Types

### Variable Naming

Variables in TechLang:
- Must start with a letter or underscore
- Can contain letters, numbers, and underscores
- Are case-sensitive
- Cannot use reserved keywords

```techlang
set counter 1      # Valid
set Counter 2      # Different from 'counter'
set _temp 3        # Valid
set 1st_value 4    # Invalid - cannot start with a number
```

### Data Types

TechLang supports these basic data types:

- **Integers**: Whole numbers (`42`, `-7`)
- **Strings**: Text data (`"Hello, world!"`)
- **Floats**: Decimal numbers (`3.14`, `-0.5`)
- **Booleans**: `true` or `false`
- **Arrays**: Ordered collections (`[1, 2, 3]`)
- **Maps**: Key-value pairs (`{"name": "Alice", "age": 30}`)

```techlang
set age 30                     # Integer
set name "Alice"               # String
set pi 3.14159                 # Float
set is_active true             # Boolean
set numbers [1, 2, 3, 4, 5]    # Array
set person {"name": "Bob", "age": 25}  # Map
```

## Code Blocks and Structure

### Block Structure

All blocks in TechLang follow this pattern:
```techlang
keyword [condition] {
    # code inside block
}
```

Examples of different blocks:

```techlang
# If block
if x > 5 {
    print "x is greater than 5"
}

# While loop
while counter < 10 {
    add counter 1
    print counter
}

# Function definition
fn greet(name) {
    print "Hello, " + name
}
```

### Nesting Blocks

Blocks can be nested within other blocks:

```techlang
if x > 0 {
    print "Positive"
    if x > 10 {
        print "Greater than 10"
    } else {
        print "Not greater than 10"
    }
} else {
    print "Non-positive"
}
```

## Error Handling

Errors in TechLang are non-fatal by default:

```techlang
print 10 / 0  # [Error: Division by zero]
print "Program continues"  # This still executes
```

Use try-catch blocks for explicit error handling:

```techlang
try {
    print 10 / 0
} catch error {
    print "Caught error: " + error
}
```

`catch` can optionally bind two identifiers: the first receives the error message without the `[Error:` prefix, and the second (if provided) receives a stringified snapshot of the operand stack.

## Input and Output

### Basic Input

```techlang
print "What is your name?"
input name
print "Hello, " + name
```

### Input Modes

- **Interactive Mode**: Prompts the user for input
- **Script Mode**: Reads from predefined inputs provided at runtime
- **Test Mode**: Uses inputs specified in test cases

### Output Formatting

```techlang
set name "Alice"
set age 30
print name + " is " + string(age) + " years old"

# Format strings
print "Name: ${name}, Age: ${age}"
```

## Comments and Documentation

### Single-line Comments

```techlang
# This is a comment
print "Hello"  # This is an end-of-line comment
```

### Documentation Style

Good practice for documenting functions:

```techlang
# Calculate the factorial of a number
# Params:
#   n: The number to calculate factorial for
# Returns:
#   The factorial of n
fn factorial(n) {
    if n <= 1 {
        return 1
    }
    return n * factorial(n - 1)
}
```

## Advanced Syntax Features

### One-liners

For simple conditions and loops, you can use one-line syntax:

```techlang
if x > 10 { print "Greater than 10" }
for i in 1..5 { print i }
```

### Chained Commands

Some commands can be chained for conciseness:

```techlang
# Instead of:
set x 5
add x 3
print x

# You can write:
set x 5 add x 3 print x  # Output: 8
```

### Implicit Value Usage

Some commands operate on an implicit current value:

```techlang
boot ping ping print   # Output: 2
```

## Best Practices

1. **Consistent Indentation**: Use 2 or 4 spaces for indentation inside blocks
2. **Meaningful Variable Names**: Use descriptive names that indicate purpose
3. **Comment Complex Logic**: Add comments to explain non-obvious code
4. **Modular Structure**: Break large programs into smaller, reusable functions
5. **Error Checking**: Validate inputs and handle potential errors gracefully

## Complete Example

```techlang
# Simple temperature converter program

print "Temperature Converter"
print "---------------------"
print "1. Celsius to Fahrenheit"
print "2. Fahrenheit to Celsius"
print "Enter your choice (1 or 2):"

input choice
set choice int(choice)

if choice == 1 {
    print "Enter temperature in Celsius:"
    input celsius
    set celsius float(celsius)
    set fahrenheit (celsius * 9/5) + 32
    print string(celsius) + "°C = " + string(fahrenheit) + "°F"
} else if choice == 2 {
    print "Enter temperature in Fahrenheit:"
    input fahrenheit
    set fahrenheit float(fahrenheit)
    set celsius (fahrenheit - 32) * 5/9
    print string(fahrenheit) + "°F = " + string(celsius) + "°C"
} else {
    print "Invalid choice!"
}
```

---

See the [Examples Index](examples.md) for more code samples.