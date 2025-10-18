# Core Commands in TechLang

This document covers the fundamental commands that form the backbone of TechLang programming. These core commands provide essential functionality for variable manipulation, arithmetic operations, input/output, and program flow.

## Command Reference

| Command | Syntax | Description | Example |
|--------|--------|-------------|---------|
| boot | `boot` | Reset the current value to 0. This is often used to initialize a calculation or reset the program state. | `boot print  # 0` |
| ping | `ping` | Increment current value by 1. This command adds 1 to the implicit current value maintained by the interpreter. | `boot ping ping print  # 2` |
| crash | `crash` | Decrement current value by 1. This command subtracts 1 from the implicit current value. | `boot ping crash print  # 0` |
| print | `print [arg]` | Print the current value, variable, or quoted text to the console. If no argument is provided, it prints the current value. | `print "Hello, TechLang!"` → Hello, TechLang! |
| set | `set <var> <int>` | Assign an integer value to a variable. Creates the variable if it doesn't exist, or updates it if it does. | `set counter 5` |
| add | `add <var> <int\|var>` | Add a value (integer or another variable's value) to a variable. | `set x 10 add x 5 print x  # 15` |
| sub | `sub <var> <int\|var>` | Subtract a value from a variable. | `set x 10 sub x 3 print x  # 7` |
| mul | `mul <var> <int\|var>` | Multiply a variable by a value. | `set x 4 mul x 6 print x  # 24` |
| div | `div <var> <int\|var>` | Divide a variable by a value using integer division. Automatically handles division by zero by producing an error. | `set x 9 div x 2 print x  # 4` |
| input | `input <var>` | Read the next input from the user and store it in a variable. In non-interactive mode, reads from predefined inputs. | `input name print "Hello, " print name` |
| upload | `upload` | Push the current value onto the stack for later retrieval. The stack can store multiple values in LIFO (Last In, First Out) order. | `boot ping upload boot ping ping download print  # 1` |
| download | `download` | Pop the top value from the stack and set it as the current value. Produces an error if the stack is empty. | `boot ping upload boot download print  # 1` |
| debug | `debug` | Print the current state of the program, including stack contents, variable values, and data types. Useful for troubleshooting. | `set x 5 set y 10 debug` |
| alias | `alias <short> <command>` | Create a shorthand name for a command. Useful for creating custom commands or simplifying repetitive operations. | `alias inc ping alias dec crash inc inc print  # 2` |
| import | `import <name>` | Load and execute a TechLang file (`name.tl`). Each file is imported only once, even if the command is called multiple times. | `import math_utils` |

### String Utilities

| Command | Syntax | Description | Example |
|--------|--------|-------------|---------|
| string_interpolate | `string_interpolate <name> "template"` | Fill `{placeholders}` using string or numeric variables and store the resolved string under `<name>`. | `str_create name "Ada" string_interpolate welcome "Hello {name}!" print welcome` → Hello Ada! |
| string_match | `string_match "pattern" <subject> <resultVar>` | Run a regular expression match; stores `1` on success or `0` on failure. Errors if the pattern is invalid or the optional regex dependency is missing. | `str_create msg "hello123" string_match "\\d+" msg has_digits print has_digits` → 1 |

## Detailed Examples

### Value Manipulation

```techlang
# Basic value manipulation
boot             # Reset to 0
ping ping ping   # Increment three times (value is now 3)
print            # Output: 3

# Using crash to decrement
boot ping ping ping   # Value is 3
crash crash           # Decrement twice (value is now 1)
print                 # Output: 1
```

### Variable Operations

```techlang
# Setting and manipulating variables
set counter 10
print counter         # Output: 10
add counter 5
print counter         # Output: 15
sub counter 3
print counter         # Output: 12
mul counter 2
print counter         # Output: 24
div counter 6
print counter         # Output: 4

# Using variables with other variables
set x 5
set y 3
add x y               # x = x + y
print x               # Output: 8
```

### Input and Output

```techlang
# Basic input and output
print "What is your name?"
input user_name
print "Hello, "
print user_name

# Combining input with arithmetic
print "Enter a number:"
input num
set num int(num)      # Convert string input to integer
mul num 2
print "Double your number is: "
print num
```

### Stack Operations

```techlang
# Using the stack to save and restore values
boot ping ping        # Value is 2
upload                # Save 2 to the stack
boot                  # Reset to 0
ping ping ping ping   # Value is 4
upload                # Save 4 to the stack
boot                  # Reset to 0
download              # Pop 4 from stack, value is now 4
print                 # Output: 4
download              # Pop 2 from stack, value is now 2
print                 # Output: 2
```

### Creating Aliases

```techlang
# Define custom commands with alias
alias increment ping
alias decrement crash
alias double "mul current 2"

set current 5
increment
increment
print current         # Output: 7
double
print current         # Output: 14
decrement
print current         # Output: 13
```

### Importing Files

```techlang
# main.tl
import utils          # Loads utils.tl
print "Main program"
print counter         # Uses variable defined in utils.tl

# utils.tl
set counter 0
alias increment "add counter 1"
print "Utils loaded"
```

## Common Patterns and Techniques

### Counter Pattern

```techlang
# Initialize counter
set counter 0

# Increment in a loop
set i 0
while i < 10 {
    add counter 1
    add i 1
}
print counter    # Output: 10
```

### Accumulator Pattern

```techlang
# Sum a list of numbers
set sum 0
set numbers [5, 10, 15, 20, 25]

for num in numbers {
    add sum num
}
print "The sum is: "
print sum        # Output: 75
```

### Value Swapping

```techlang
# Swap two variables using the stack
set x 10
set y 20

# Traditional swap
set temp x
set x y
set y temp

print x          # Output: 20
print y          # Output: 10

# Swap using stack
set x 10
set y 20
boot
set current x
upload
set current y
set x current
download
set y current
print x          # Output: 20
print y          # Output: 10
```

## Tips and Best Practices

1. **Initialize Variables**: Always initialize variables before using them with the `set` command.

2. **Use Aliases for Clarity**: Create meaningful aliases for common operations to make your code more readable.

3. **Stack Management**: Be careful with stack operations - always ensure you download the same number of values that you upload.

4. **Error Handling**: Prevent division by zero errors by checking values before using the `div` command.

5. **Modularity**: Use `import` to organize your code into reusable modules.

## Advanced Usage

### Custom Function Simulation

```techlang
# Define a "function" using aliases
alias start_square "set temp current upload"
alias end_square "download mul temp temp set current temp"

# Usage
set current 5
start_square
# Do other operations...
end_square
print current    # Output: 25
```

### Debug-Driven Development

```techlang
# Use debug to inspect program state
set counter 0
add counter 5
debug            # Shows all variables and their values
mul counter 2
debug            # Check the result of multiplication
```

---

See the [Examples Index](examples.md) for more code samples.