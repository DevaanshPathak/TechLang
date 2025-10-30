# Debugging in TechLang

TechLang includes a powerful debugger that lets you pause execution, inspect state, and step through code to understand what your program is doing.

## Overview

The debugger provides several commands to help you track down bugs and understand program flow:

- **Breakpoints**: Pause execution at specific points
- **Stepping**: Execute one command at a time
- **Inspection**: View detailed state information
- **Watching**: Monitor specific variables

## Debugger Commands

### Setting Breakpoints

Use `breakpoint` to mark a point where execution should pause:

```techlang
set x 10
breakpoint        # Execution will pause here
set x 20
```

### Stepping Through Code

Enable step mode to pause after each command:

```techlang
step             # Enable step mode
set x 5
set y 10         # Will pause after each command
add x y
```

### Inspecting State

Use `inspect` to see detailed information about your program's current state:

```techlang
set counter 0
set max 100
array_create data 5
dict_create config
inspect          # Shows all state information
```

The `inspect` command displays:
- Current command number
- Stack contents
- Current value
- Variables (all or watched only)
- Arrays (names)
- Strings (names)
- Dictionaries (names)
- Active breakpoints
- Debug mode status

### Watching Variables

Monitor specific variables to see their values in inspect output:

```techlang
set x 0
watch x          # Add x to watch list
loop 10
    add x 1
end
inspect          # Shows watched variables
unwatch x        # Remove from watch list
```

### Continuing Execution

Resume from a paused state:

```techlang
continue         # Resume execution
```

### Clearing Breakpoints

Remove all breakpoints:

```techlang
clear_breakpoints    # Removes all breakpoints
```

## Practical Example

Here's a complete debugging session:

```techlang
# Enable watching
watch total
watch count

# Set initial values
set total 0
set count 0

# Set breakpoint before loop
breakpoint

# Process items
loop 5
    add count 1
    add total count
    inspect        # Check state each iteration
end

# Final inspection
print "Final values:"
inspect

# Cleanup
unwatch total
unwatch count
clear_breakpoints
```

## Debugging Strategies

### Finding Logic Errors

```techlang
def calculate_average
    set sum 0
    set count 0
    
    watch sum
    watch count
    
    loop 5
        add sum count
        add count 1
        inspect       # Check accumulation
    end
    
    div sum count
end

call calculate_average
```

### Tracking Variable Changes

```techlang
set x 10
watch x

# Multiple operations
mul x 2          # x = 20
add x 5          # x = 25  
sub x 3          # x = 22

inspect          # See final value
```

### Debugging Loops

```techlang
set i 0
watch i

breakpoint       # Stop before loop

loop 10
    add i 1
    inspect      # Check each iteration
end
```

### Debugging Functions

```techlang
def process_data
    set result 0
    watch result
    
    # Complex calculation
    set result 100
    mul result 2
    
    inspect      # Check intermediate state
end

call process_data
```

## Integration with Other Features

### With Threads

```techlang
def worker
    set value 0
    watch value
    
    loop 5
        add value 10
    end
    
    inspect
end

thread_create worker
thread_join 1
```

### With File I/O

```techlang
watch line_count

set line_count 0
file_read "data.txt" content

breakpoint       # Pause before processing

str_length content
inspect
```

### With Database Operations

```techlang
watch record_count

set record_count 0
db_select "users" "name"

inspect          # Check query results
```

## Command Counter

The debugger tracks each command executed with a counter. This helps you:

- Identify where breakpoints are set
- Track execution progress
- Correlate debug output with code position

```techlang
set x 1          # Command #1
set y 2          # Command #2
breakpoint       # Sets at #3
add x y          # Command #4
inspect          # Shows command count
```

## Best Practices

1. **Use watches for key variables**: Don't watch everything, focus on what matters
2. **Strategic breakpoints**: Set breakpoints before complex sections
3. **Inspect frequently**: Check state at decision points
4. **Clean up**: Remove watches and breakpoints when done
5. **Step carefully**: Use step mode for tricky bugs
6. **Document findings**: Add comments explaining what you discovered

## Limitations

- Breakpoints are per-command, not per-line in source file
- Step mode pauses after each command (can be verbose)
- Watched variables shown in inspect, not on each change
- No time-travel debugging (yet!)

## Example: Full Debugging Session

```techlang
boot
print "=== Debugging Session ==="

# Setup
watch x
watch y  
watch result

# Initialize
set x 10
set y 20
set result 0

# Checkpoint 1
breakpoint
inspect

# Calculate
add result x
add result y

# Checkpoint 2
breakpoint
inspect

# Process
mul result 2

# Final check
inspect

# Cleanup
unwatch x
unwatch y
unwatch result
clear_breakpoints

crash
```

---

See also:
- [Control Flow](control-flow.md) - For understanding execution order
- [Data Types](data-types.md) - For working with inspected data
- [Examples](examples.md) - For complete debugging examples
