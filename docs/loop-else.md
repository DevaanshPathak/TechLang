# Loop Else

Loop else blocks execute when a loop completes without encountering a `break` statement. This is useful for search patterns where you want to handle the "not found" case. Like Python's `for/else` and `while/else`.

## Syntax

### For Loop Else

```techlang
loop_else <count> do
    # loop body
    if <condition>
        break    # Skip else block
    end
else
    # Runs if loop completes without break
end
```

### While Loop Else

```techlang
while_else <var> <op> <value> do
    # loop body
    if <condition>
        break    # Skip else block
    end
else
    # Runs if loop completes without break
end
```

## Commands

| Command | Description |
|---------|-------------|
| `loop_else <count> do ... else ... end` | Loop with else block |
| `while_else <var> <op> <val> do ... else ... end` | While with else block |
| `break` | Exit innermost loop, skip else block |
| `continue` | Skip to next iteration |

## Examples

### Search Pattern (Not Found)

```techlang
set found 0
set i 0
loop_else 10 do
    if i == 999
        set found 1
        break
    end
    add i 1
else
    print "Item not found"
end
```

### Search Pattern (Found)

```techlang
set counter 0
loop_else 10 do
    add counter 1
    if counter == 3
        print "Found at 3!"
        break
    end
else
    print "This won't print because we broke"
end
```

### Loop Completes Normally

```techlang
set i 0
while_else i < 5 do
    print i
    add i 1
else
    print "Loop completed without break!"
end
```

### Search in Array

```techlang
array_create data
array_push data 10
array_push data 20
array_push data 30
array_push data 40

set target 25
set i 0
loop_else 4 do
    array_get data i val
    if val == target
        print "Found!"
        break
    end
    add i 1
else
    print "Not found in array"
end
```

## Implementation

- Handler: `techlang/loop_else.py`
- Tests: `tests/test_loop_else.py`
- Example: `examples/loop_else.tl`

## See Also

- [Control Flow](control-flow.md) - Standard loops
- [Chained Comparisons](chained-comparisons.md) - Multiple comparisons
