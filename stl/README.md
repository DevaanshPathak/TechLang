# TechLang Standard Template Library (STL)

The TechLang STL provides reusable modules for common programming tasks. All modules follow the export/public API system for clean interfaces.

**Alias:** You can use `stdlib` as an alias for `stl`:
- `package use stdlib/validation` (or `stl/validation`)
- `call stdlib.validation.is_positive` (or `stl.validation.is_positive`)

## Runtime Assumptions (STL Compatibility)

Some STL modules rely on “store into target” forms of core commands (so helpers can avoid printing intermediate values):

- `str_length <string> <targetVar>` stores the length in `<targetVar>`.
- `str_substring <string> <start> <end> <targetString>` stores into `<targetString>`.
- `str_contains <string> <substring> <targetVar>` stores `1/0` into `<targetVar>`.
- `array_get <array> <index> <target>` stores the value into `<target>`.

Arrays used by STL are typically **dynamic arrays** created via:

- `array_create <name>` (no size) creates a dynamic array.
- For dynamic arrays, `array_set` grows as needed.
- For dynamic arrays, out-of-bounds `array_get ... <target>` stores `0` (sentinel) instead of erroring. This is used by `stl/collections` loops.

Control-flow also accepts operator synonyms used in examples:

- `eq/ne/gt/lt/ge/le` map to `==/!=/>/</>=/<=`.

## Available Modules

### strings.tl - String Utilities
Advanced string manipulation functions.

**Functions:**
- `is_empty(s)` - Check if string is empty
- `capitalize(text)` - Capitalize first character
- `title_case(text)` - Convert to title case (capitalize each word)
- `repeat(text, count)` - Repeat string n times
- `pad_left(text, width, pad_char)` - Pad string on left
- `pad_right(text, width, pad_char)` - Pad string on right
- `starts_with(text, prefix)` - Check if string starts with prefix
- `ends_with(text, suffix)` - Check if string ends with suffix
- `count_char(text, char)` - Count occurrences of character

**Example:**
```techlang
package use stl/strings

str_create name "alice"
call stl.strings.capitalize name result
print result  # Output: Alice

str_create text "hello"
call stl.strings.repeat text 3 repeated
print repeated  # Output: hellohellohello

str_create num "42"
call stl.strings.pad_left num 5 "0" padded
print padded  # Output: 00042
```

---

### math.tl - Math Utilities
Mathematical helper functions.

**Functions:**
- `min(a, b)` - Return minimum of two numbers
- `max(a, b)` - Return maximum of two numbers
- `abs(n)` - Return absolute value
- `clamp(value, min_val, max_val)` - Clamp value between min and max
- `sign(n)` - Return -1, 0, or 1
- `is_even(n)` - Check if number is even
- `is_odd(n)` - Check if number is odd
- `sum_range(start, end)` - Sum integers from start to end
- `factorial(n)` - Calculate factorial (n!)
- `gcd(a, b)` - Greatest common divisor
- `lerp(a, b, t)` - Linear interpolation between a and b

**Example:**
```techlang
package use stl/math

set x 5
set y 10
call stl/math.max x y result
print result  # Output: 10

set n -42
call stl/math.abs n result
print result  # Output: 42

set val 15
set min_val 0
set max_val 10
call stl/math.clamp val min_val max_val clamped
print clamped  # Output: 10

set n 5
call stl/math.factorial n result
print result  # Output: 120
```

---

### collections.tl - Collections Utilities
Array and dictionary helper functions.

**Array Functions:**
- `array_sum(arr)` - Sum all elements in array
- `array_product(arr)` - Multiply all elements in array
- `array_min(arr)` - Find minimum value
- `array_max(arr)` - Find maximum value
- `array_contains(arr, target)` - Check if array contains value
- `array_index_of(arr, target)` - Find index of value (-1 if not found)
- `array_count(arr)` - Count elements in array
- `array_reverse(arr)` - Reverse array in place
- `array_fill(arr, value, count)` - Fill array with value

**Dictionary Functions:**
- `dict_has_key(dict, key)` - Check if dictionary contains key
- `dict_count(dict)` - Count keys in dictionary (placeholder)
- `dict_copy(source, dest)` - Copy dictionary (placeholder)

**Example:**
```techlang
package use stl/collections

array_create nums
array_push nums 5
array_push nums 10
array_push nums 15
array_push nums 20

call stl/collections.array_sum nums total
print total  # Output: 50

call stl/collections.array_max nums max_val
print max_val  # Output: 20

set target 15
call stl/collections.array_contains nums target found
print found  # Output: 1

call stl/collections.array_index_of nums target idx
print idx  # Output: 2
```

---

### validation.tl - Validation Utilities
Input validation and type checking functions.

**Numeric Validation:**
- `is_positive(n)` - Check if number is positive
- `is_negative(n)` - Check if number is negative
- `is_zero(n)` - Check if number is zero
- `is_in_range(n, min, max)` - Check if number is in range

**String Validation:**
- `is_numeric_string(s)` - Check if string contains only digits (placeholder)
- `is_alpha_string(s)` - Check if string contains only letters (placeholder)
- `is_alphanumeric_string(s)` - Check if alphanumeric (placeholder)
- `min_length(s, min_len)` - Check minimum string length
- `max_length(s, max_len)` - Check maximum string length
- `length_between(s, min, max)` - Check string length in range

**Format Validation:**
- `is_email(s)` - Basic email validation (contains @ and .)
- `is_url(s)` - Basic URL validation (starts with http:// or https://)

**Logical Validators:**
- `require_all(c1, c2)` - AND operation (both must be true)
- `require_any(c1, c2)` - OR operation (at least one must be true)

**Example:**
```techlang
package use stl/validation

set x 42
call stl/validation.is_positive x result
print result  # Output: 1

set y -10
call stl/validation.is_negative y result
print result  # Output: 1

set age 25
set min_age 18
set max_age 100
call stl/validation.is_in_range age min_age max_age valid
print valid  # Output: 1

str_create email "user@example.com"
call stl/validation.is_email email valid_email
print valid_email  # Output: 1

str_create password "secret123"
set min_len 8
call stl/validation.min_length password min_len meets_min
print meets_min  # Output: 1
```

---

### json.tl - JSON Utilities
Thin wrappers over core `json_*` commands.

**Functions:**
- `parse(source, target)` - Wrapper for `json_parse`
- `stringify(source, target_str)` - Wrapper for `json_stringify`
- `read(path, target)` - Wrapper for `json_read`
- `write(source, path)` - Wrapper for `json_write`
- `try_parse(source, target)` - Returns `1` on success, else `0`

**Example:**
```techlang
package use stl/json

str_create payload "[1, 2, 3]"
call stl.json.parse payload arr

call stl.json.stringify arr out
print out

str_create bad "not-json"
call stl.json.try_parse bad tmp ok
print ok  # Output: 0
```

---

### net.tl - Network Utilities
Convenience wrappers over core `http_*` commands.

**Functions:**
- `get(url, resp_name)` - Wrapper for `http_get`
- `get_text(url)` - Returns `(body, status)`
- `get_json(url, target_dict)` - Parses JSON into `target_dict`, returns `status`
- `post_text(url, data_token)` - Returns `(body, status)`

**Example:**
```techlang
package use stl/net

str_create url "https://example.com"
call stl.net.get_text url body status
print status

# When the response body is JSON:
call stl.net.get_json url obj status
print status
```

## Usage Patterns

### Loading Multiple Modules
```techlang
package use stl/strings
package use stl/math
package use stl/validation

# Use functions from any loaded module
str_create text "hello world"
call stl/strings.title_case text result
print result

set x 5
set y 10
call stl/math.max x y max_val
print max_val
```

### Combining Functions
```techlang
package use stl/math
package use stl/validation

# Validate input is in range, then clamp
set user_input 150
set min_val 0
set max_val 100

call stl/validation.is_in_range user_input min_val max_val valid
if valid eq 0
    print "Input out of range, clamping..."
    call stl/math.clamp user_input min_val max_val clamped
    set user_input clamped
end
print user_input
```

---

## Design Philosophy

### Private by Default
All helper functions (prefixed with `_`) are private and not exported. Only documented public API functions are accessible.

### Parameter Passing
All stl functions use the function parameter system for clean, predictable interfaces.

### Return Values
Functions return values explicitly using the `return` statement. Side effects are minimized.

### Naming Conventions
- Functions use `snake_case` (e.g., `title_case`, `array_sum`)
- Private helpers prefixed with `_` (e.g., `_validate_string`)
- Module namespaces use dot notation (e.g., `stl/strings.capitalize`)

---

## Extending the Standard Library

### Adding a New Module

1. **Create the module file**: `stl/mymodule.tl`

2. **Declare package name**:
```techlang
package name stl/mymodule
```

3. **Define functions with parameters**:
```techlang
def my_function arg1 arg2
    # Implementation
    return result
end
```

4. **Export public API**:
```techlang
export my_function
export another_function
```

5. **Document in this README**:
Add module description, function list, and examples.

6. **Create tests**:
Add tests in `tests/test_stl/py` to verify functionality.

---

## Testing

To test stl modules, create a test file that loads and exercises each function:

```techlang
package use stl/strings

# Test capitalize
str_create input "hello"
call stl/strings.capitalize input result
print result  # Should output: Hello

# Test repeat
str_create text "x"
call stl/strings.repeat text 5 repeated
print repeated  # Should output: xxxxx
```

Run comprehensive tests:
```bash
python run_tests.py
```

---

## Notes

### Placeholder Functions
Some functions (like `dict_count`, `is_numeric_string`) are placeholders waiting for core TechLang features:
- Dictionary iteration
- Character/ASCII comparison
- Enhanced type checking

These will be fully implemented when the core language supports the required primitives.

### Performance Considerations
- Array functions use loops with max iterations (typically 1000)
- String functions create intermediate strings
- For large datasets, consider implementing specialized versions

---

## Future Enhancements

- **stl/io.tl** - Advanced file I/O helpers
- **stl/json.tl** - JSON parsing/manipulation utilities
- **stl/date.tl** - Date/time formatting and calculations
- **stl/crypto.tl** - Basic hashing and encoding
- **stl/text.tl** - Advanced text processing (regex-like patterns)
- **stl/graph.tl** - Graph algorithms (BFS, DFS, shortest path)
- **stl/sort.tl** - Sorting algorithms
- **stl/random.tl** - Random number generation and selection

---

**Last Updated:** 2025-01-XX  
**TechLang Version:** 1.0  
**Total Modules:** 4

