# Chained Comparisons

Chained comparisons allow multiple comparison operators in a single expression, evaluated left-to-right with AND semantics. Like Python's `0 < x < 100`.

## Syntax

```techlang
if_chain <val1> <op1> <val2> <op2> <val3> ... do
    # code block
end
```

## Supported Operators

- `<` - less than
- `>` - greater than
- `<=` - less than or equal
- `>=` - greater than or equal
- `==` - equal
- `!=` - not equal

## Examples

### Range Check

```techlang
set x 50
if_chain 0 < x < 100 do
    print "x is in range 0-100"
end
```

### Ascending Order Check

```techlang
set a 1
set b 5
set c 10
if_chain a < b < c do
    print "Values are in ascending order"
end
```

### Mixed Operators

```techlang
set val 50
if_chain 0 <= val <= 100 do
    print "val is in range [0, 100]"
end
```

### Using Literals

```techlang
set x 5
if_chain 1 < x < 10 do
    print "x is between 1 and 10"
end
```

### Equality Chain

```techlang
set a 5
set b 5
set c 5
if_chain a == b == c do
    print "All values are equal"
end
```

## Implementation

- Handler: `techlang/chained_comparisons.py`
- Tests: `tests/test_chained_comparisons.py`
- Example: `examples/chained_comparisons.tl`

## See Also

- [Control Flow](control-flow.md) - Standard if/else conditions
- [Loop Else](loop-else.md) - Loops with else blocks
