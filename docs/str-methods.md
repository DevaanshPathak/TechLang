# String Methods

Additional string manipulation methods that mirror Python's str operations.

## Commands

| Command | Description |
|---------|-------------|
| `str_join <arr> <sep> <result>` | Join array elements with separator |
| `str_zfill <str> <width> <result>` | Zero-pad to width |
| `str_center <str> <width> <result>` | Center in width |
| `str_ljust <str> <width> <result>` | Left-justify in width |
| `str_rjust <str> <width> <result>` | Right-justify in width |
| `str_title <str> <result>` | Convert to Title Case |
| `str_capitalize <str> <result>` | Capitalize first char |
| `str_swapcase <str> <result>` | Swap upper/lower case |
| `str_isupper <str> <result>` | Check if all uppercase (1/0) |
| `str_islower <str> <result>` | Check if all lowercase (1/0) |
| `str_isspace <str> <result>` | Check if all whitespace (1/0) |
| `str_lstrip <str> <result>` | Strip leading whitespace |
| `str_rstrip <str> <result>` | Strip trailing whitespace |
| `str_strip_chars <str> <chars> <result>` | Strip specific chars |

## Examples

### Join Array

```techlang
array_create words
array_push words "hello"
array_push words "world"
str_join words "-" result
print result    # Outputs: hello-world
```

### Zero Fill

```techlang
str_create num "42"
str_zfill num 5 padded
print padded    # Outputs: 00042
```

### Text Alignment

```techlang
str_create text "hi"
str_center text 10 centered   # "    hi    "
str_ljust text 10 left        # "hi        "
str_rjust text 10 right       # "        hi"
```

### Case Conversion

```techlang
str_create phrase "hello world"
str_title phrase titled
print titled    # Outputs: Hello World

str_capitalize phrase cap
print cap       # Outputs: Hello world

str_create mixed "HeLLo WoRLd"
str_swapcase mixed swapped
print swapped   # Outputs: hEllO wOrlD
```

### Case Checking

```techlang
str_create upper "HELLO"
str_create lower "hello"
str_create spaces "   "

str_isupper upper is_up
print is_up    # Outputs: 1

str_islower lower is_low
print is_low   # Outputs: 1

str_isspace spaces is_sp
print is_sp    # Outputs: 1
```

### String Stripping

```techlang
str_create padded "   hello   "
str_lstrip padded left
print left     # Outputs: "hello   "

str_rstrip padded right
print right    # Outputs: "   hello"

str_create chars_str "xxhelloxx"
str_strip_chars chars_str "x" stripped
print stripped # Outputs: hello
```

### String Processing Pipeline

```techlang
array_create names
array_push names "alice"
array_push names "bob"
array_push names "charlie"

str_create sep ", "
str_join names sep joined
str_title joined titled
print titled    # Outputs: Alice, Bob, Charlie
```

## Implementation

- Handler: `techlang/str_methods.py`
- Tests: `tests/test_str_methods.py`
- Example: `examples/str_methods.tl`

## See Also

- [Data Types](data-types.md) - Core string operations
- [List Methods](list-methods.md) - Array manipulation
