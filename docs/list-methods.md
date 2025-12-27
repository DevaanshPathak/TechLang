# List Methods

Additional array/list methods that mirror Python's list operations.

## Commands

| Command | Description |
|---------|-------------|
| `array_insert <arr> <idx> <val>` | Insert value at index |
| `array_extend <arr> <source>` | Extend with another array |
| `array_clear <arr>` | Remove all elements |
| `array_copy <src> <dst>` | Create shallow copy |
| `array_count <arr> <val> <result>` | Count occurrences |
| `array_remove <arr> <val>` | Remove first occurrence |
| `array_len <arr> <result>` | Get array length |
| `array_index <arr> <val> <result>` | Find index (-1 if not found) |

## Examples

### Insert at Index

```techlang
array_create nums
array_push nums 1
array_push nums 2
array_push nums 4
array_insert nums 2 3    # Insert 3 at index 2
# nums is now [1, 2, 3, 4]
```

### Extend Array

```techlang
array_create a
array_push a 1
array_push a 2

array_create b
array_push b 3
array_push b 4

array_extend a b
# a is now [1, 2, 3, 4]
```

### Count Occurrences

```techlang
array_create nums
array_push nums 1
array_push nums 2
array_push nums 2
array_push nums 3
array_count nums 2 count
print count    # Outputs: 2
```

### Find Index

```techlang
array_create arr
array_push arr 10
array_push arr 20
array_push arr 30

array_index arr 20 idx
print idx    # Outputs: 1

array_index arr 99 idx
print idx    # Outputs: -1 (not found)
```

### Copy Array

```techlang
array_create original
array_push original 1
array_push original 2

array_copy original copy
# copy is now [1, 2], independent of original
```

### Clear Array

```techlang
array_create data
array_push data 1
array_push data 2
array_push data 3
array_clear data
array_len data len
print len    # Outputs: 0
```

### Remove Element

```techlang
array_create nums
array_push nums 1
array_push nums 2
array_push nums 3
array_push nums 2
array_remove nums 2    # Removes first occurrence of 2
# nums is now [1, 3, 2]
```

## Implementation

- Handler: `techlang/list_methods.py`
- Tests: `tests/test_list_methods.py`
- Example: `examples/list_methods.tl`

## See Also

- [Data Types](data-types.md) - Core array operations
- [String Methods](str-methods.md) - String manipulation
