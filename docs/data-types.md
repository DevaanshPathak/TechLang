# Data Types in TechLang

TechLang provides a variety of built-in data types to support different kinds of data and operations. Understanding these types is essential for writing effective programs.

## Structs (records)

Structs let you bundle named fields with simple typing guarantees. Define the shape with a `struct <Type>` block, then create and mutate instances with `struct` subcommands:

```techlang
struct Person name:string age:int end

struct new Person user
struct set user name "Ada"
struct set user age 37
print user            # Person{name: "Ada", age: 37}
struct get user name  # Ada
```

- Supported field types: `int`, `string` (defaults to `0` / empty string).
- `struct dump <instance>` prints the formatted record without touching `print`.
- The `debug` command now includes a `Structs:` line so you can inspect all live instances.

## Primitive Types

- **Integer (`int`)**: Whole numbers, e.g., `42`, `-7`
- **Float (`float`)**: Decimal numbers, e.g., `3.14`, `-0.001`
- **Boolean (`bool`)**: Logical values, `true` or `false`
- **String (`string`)**: Text data, e.g., `"hello world"`

## Composite Types

- **Array**: Ordered collection of elements of the same type.
  ```techlang
  let numbers = [1, 2, 3, 4]
  ```
- **Tuple**: Fixed-size collection of elements of possibly different types.
  ```techlang
  let point = (3, 4)
  ```
- **Map**: Key-value pairs, similar to dictionaries.
  ```techlang
  let capitals = { "France": "Paris", "Japan": "Tokyo" }
  ```

## Special Types

- **Null (`null`)**: Represents the absence of a value.
- **Any (`any`)**: Can hold a value of any type.

## Type Inference and Annotations

TechLang can infer types, but you can also specify them:

```techlang
let age: int = 30
let name: string = "Alice"
```

## Strings

TechLang provides comprehensive string manipulation commands:

### Creating and Basic Operations

```techlang
str_create message "hello world"
str_length message              # Outputs: 11
str_concat message " again"     # Appends to message
print message                   # hello world again
```

### String Transformation

```techlang
// Case conversion
str_create text "Hello World"
str_upper text                  # HELLO WORLD
str_lower text                  # hello world

// Trimming whitespace
str_create padded "  spaces  "
str_trim padded                 # "spaces"

// Reversing
str_create word "hello"
str_reverse word                # "olleh"
```

### String Manipulation

```techlang
// Replace substrings
str_create message "hello world"
str_replace message "world" "universe"
print message                   # hello universe

// Split into array
str_create csv "apple,banana,cherry"
str_split csv "," fruits
array_get fruits 0              # apple
array_get fruits 1              # banana
```

### String Query

```techlang
// Check if substring exists
str_create text "techlang is awesome"
str_contains text "lang"        # 1 (true)
str_contains text "python"      # 0 (false)

// Get substring
str_substring text 0 8          # "techlang"
```

### String Operations Summary

| Command | Description | Example |
|---------|-------------|---------|
| `str_create` | Create a string | `str_create msg "hello"` |
| `str_concat` | Append to string | `str_concat msg " world"` |
| `str_length` | Get length | `str_length msg` |
| `str_substring` | Extract portion | `str_substring msg 0 5` |
| `str_split` | Split into array | `str_split msg " " words` |
| `str_replace` | Replace substring | `str_replace msg "old" "new"` |
| `str_trim` | Remove whitespace | `str_trim msg` |
| `str_upper` | Convert to uppercase | `str_upper msg` |
| `str_lower` | Convert to lowercase | `str_lower msg` |
| `str_contains` | Check for substring | `str_contains msg "test"` |
| `str_reverse` | Reverse characters | `str_reverse msg` |

## Arrays

Arrays in TechLang are dynamic collections:

```techlang
array_create numbers 5
array_set numbers 0 10
array_get numbers 0      # 10
array_push numbers 20
array_pop numbers
```

### Array Operations

| Command | Description |
|---------|-------------|
| `array_create` | Create array with size |
| `array_set` | Set value at index |
| `array_get` | Get value at index |
| `array_push` | Append value |
| `array_pop` | Remove last value |
| `array_map` | Transform items |
| `array_filter` | Filter items |

## Dictionaries

Dictionaries store key-value pairs:

```techlang
dict_create user
dict_set user "name" "Alice"
dict_set user "age" "30"
dict_get user "name"     # Alice
dict_keys user           # Lists all keys
```

## JSON Operations

TechLang provides comprehensive JSON support for modern application development:

### Parsing JSON

Convert JSON strings to TechLang data structures:

```techlang
# Parse JSON object into dictionary
str_create data '{"name":"Alice","age":30}'
json_parse data user
dict_get user "name"    # Alice

# Parse JSON array
str_create nums "[10,20,30]"
json_parse nums array
array_get array 1       # 20

# Parse primitives
str_create value "42"
json_parse value num    # Creates variable
str_create flag "true"
json_parse flag bool    # true → 1, false → 0
str_create empty "null"
json_parse empty val    # null → 0
```

### Stringifying to JSON

Convert TechLang structures to JSON strings:

```techlang
# Dictionary to JSON
dict_create user
dict_set user "name" "Bob"
dict_set user "age" "25"
json_stringify user json
print json              # {"name":"Bob","age":25}

# Array to JSON
array_create scores 3
array_set scores 0 95
array_set scores 1 87
array_set scores 2 92
json_stringify scores json
print json              # [95,87,92]

# Primitives to JSON
set x 42
json_stringify x json
print json              # 42

str_create text "hello"
json_stringify text json
print json              # "hello"
```

### JSON File Operations

Read and write JSON files:

```techlang
# Write dictionary to JSON file
dict_create config
dict_set config "host" "localhost"
dict_set config "port" "8080"
json_write config "config.json"

# Read JSON from file
json_read "config.json" loaded
dict_get loaded "host"  # localhost

# Works with arrays too
array_create data 3
array_set data 0 100
array_set data 1 200
array_set data 2 300
json_write data "numbers.json"
json_read "numbers.json" nums
array_get nums 1        # 200
```

### JSON Commands Reference

| Command | Description |
|---------|-------------|
| `json_parse <source> <target>` | Parse JSON string into TechLang structure |
| `json_stringify <source> <target>` | Convert structure to JSON string |
| `json_read <path> <target>` | Read and parse JSON from file |
| `json_write <source> <path>` | Write structure to JSON file |

**Type Mapping:**

- JSON objects → TechLang dictionaries
- JSON arrays → TechLang arrays
- JSON strings → TechLang strings
- JSON numbers → TechLang variables
- JSON booleans → 1 (true) or 0 (false)
- JSON null → 0

**Features:**

- ✅ Unicode support (emoji, international characters)
- ✅ Nested structures (objects within objects/arrays)
- ✅ Path security (prevents directory traversal)
- ✅ Roundtrip fidelity (parse → stringify → parse)
- ✅ Pretty-printed output (2-space indentation)

---

See the [Examples Index](examples.md) for