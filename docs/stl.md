# TechLang STL (Standard Template Library)

The TechLang STL is a set of reusable TechLang modules located in the `stl/` folder.

## Loading & calling

Load a module with:

```techlang
package use stl/<module>
```

Then call exported functions with either `.` or `::`:

```techlang
call stl.<module>.<function> ...
call stl::<module>::<function> ...
```

### `stdlib` alias

`stdlib` is an alias for `stl`, so you can also load/call like:

```techlang
package use stdlib/validation
call stdlib.validation.is_positive n result
```

## Notes & conventions

- STL functions are **exported explicitly** via `export`.
- Many STL helpers use internal variables/strings prefixed with `_stl_` to avoid collisions.
- Some core commands print informational output (notably `json_parse` / `json_stringify`). STL wrappers do not suppress those lines.

---

## Module: `stl/strings` (String utilities)

### Purpose
Higher-level string helpers built on TechLang `str_*` commands.

### Load
```techlang
package use stl/strings
```

### Public API
- `is_empty(s) -> 1|0`
- `capitalize(source_text) -> string`
- `title_case(text) -> string`
- `repeat(text, count) -> string`
- `pad_left(text, width, pad_char) -> string`
- `pad_right(text, width, pad_char) -> string`
- `starts_with(text, prefix) -> 1|0`
- `ends_with(text, suffix) -> 1|0`
- `count_char(text, char) -> number`

### Underlying core commands
Uses `str_length`, `str_substring`, `str_concat`, `str_upper`, `str_lower`, and `str_contains`.

### Example
```techlang
package use stl/strings

str_create name "alice"
call stl.strings.capitalize name capped
print capped

call stl.strings.pad_left capped 8 "_" padded
print padded
```

---

## Module: `stl/math` (Math utilities)

### Purpose
Common numeric helpers implemented in TechLang.

### Load
```techlang
package use stl/math
```

### Public API
- `min(a, b) -> number`
- `max(a, b) -> number`
- `abs(n) -> number`
- `clamp(value, min_val, max_val) -> number`
- `sign(n) -> -1|0|1`
- `is_even(n) -> 1|0`
- `is_odd(n) -> 1|0`
- `sum_range(start, end) -> number`
- `factorial(n) -> number`
- `gcd(a, b) -> number`
- `lerp(a, b, t) -> number`

### Underlying core commands
Uses arithmetic commands (`add`, `sub`, `mul`, `div`) and `math_mod`.

### Example
```techlang
package use stl/math

set a 12
set b 18
call stl.math.gcd a b g
print g

set x -7
call stl.math.abs x ax
print ax
```

---

## Module: `stl/collections` (Array & dictionary utilities)

### Purpose
Helpers for arrays/dictionaries, designed to work with TechLang’s dynamic arrays.

### Load
```techlang
package use stl/collections
```

### Public API (arrays)
- `array_sum(arr) -> number`
- `array_product(arr) -> number`
- `array_min(arr) -> number`
- `array_max(arr) -> number`
- `array_contains(arr, target) -> 1|0`
- `array_index_of(arr, target) -> index|-1`
- `array_count(arr) -> number`
- `array_reverse(arr) -> 1`
- `array_fill(arr, value, count) -> 1`

### Public API (dictionaries)
- `dict_has_key(dict_name, key) -> 1|0` (simplified)
- `dict_count(dict_name) -> number` (placeholder)
- `dict_copy(source, dest) -> number` (placeholder)

### Underlying core commands
Uses `array_create`, `array_set`, `array_get`, `array_push`, and `dict_get`.

### Example
```techlang
package use stl/collections

array_create nums
array_push nums 5
array_push nums 10
array_push nums 15

call stl.collections.array_sum nums total
print total

set target 10
call stl.collections.array_index_of nums target idx
print idx
```

---

## Module: `stl/validation` (Validation utilities)

### Purpose
Numeric/string validation helpers.

### Load
```techlang
package use stl/validation
```

### Public API
**Numeric:**
- `is_positive(n) -> 1|0`
- `is_negative(n) -> 1|0`
- `is_zero(n) -> 1|0`
- `is_in_range(n, min_val, max_val) -> 1|0`

**Strings:**
- `is_numeric_string(s) -> 1|0`
- `is_alpha_string(s) -> 1|0`
- `is_alphanumeric_string(s) -> 1|0`
- `min_length(s, min_len) -> 1|0`
- `max_length(s, max_len) -> 1|0`
- `length_between(s, min_len, max_len) -> 1|0`

**Formats:**
- `is_email(s) -> 1|0`
- `is_url(s) -> 1|0`

**Logical:**
- `require_all(c1, c2) -> 1|0`
- `require_any(c1, c2) -> 1|0`

### Underlying core commands
Uses `str_length`, `str_substring`, and `str_contains`.

### Example
```techlang
package use stl/validation

str_create email "user@example.com"
call stl.validation.is_email email ok
print ok

str_create s "12345"
call stl.validation.is_numeric_string s ok
print ok
```

---

## Module: `stl/json` (JSON utilities)

### Purpose
Thin wrappers around the core JSON commands.

### Load
```techlang
package use stl/json
```

### Public API
- `parse(source, target)`
  - Wraps: `json_parse <source> <target>`
  - Notes: `source` can be a string variable containing JSON or a quoted JSON literal.
- `stringify(source, target_str)`
  - Wraps: `json_stringify <source> <target_str>`
- `read(path, target)`
  - Wraps: `json_read "path" <target>`
- `write(source, path)`
  - Wraps: `json_write <source> "path"`
- `try_parse(source, target) -> 1|0`
  - Wraps `json_parse` in `try/catch`.

### Underlying core commands
`json_parse`, `json_stringify`, `json_read`, `json_write`.

### Example
```techlang
package use stl/json

str_create payload "{\"x\": 1}"
call stl.json.parse payload obj

call stl.json.stringify obj out
print out

str_create bad "not-json"
call stl.json.try_parse bad tmp ok
print ok
```

---

## Module: `stl/net` (Network utilities)

### Purpose
Convenience wrappers around core HTTP commands.

### Dependency
Core `http_get` / `http_post` require the Python `requests` library. If it’s missing, TechLang reports:

- `[Error: 'requests' library not available]`

### Load
```techlang
package use stl/net
```

### Public API
- `get(url, resp_name)`
  - Wraps: `http_get <url> <resp_name>`
  - Side-effects: stores response body into string `<resp_name>` and status into numeric `<resp_name>_status`.

- `get_text(url) -> (body, status)`
  - Wraps `http_get`, returning both response body and HTTP status.

- `get_json(url, target_dict) -> status`
  - Wraps `http_get` then `json_parse` into `target_dict`.

- `post_text(url, data_token) -> (body, status)`
  - Wraps `http_post`, returning both response body and HTTP status.

### Underlying core commands
`http_get`, `http_post`, `json_parse`.

### Example
```techlang
package use stl/net

str_create url "http://localhost:8000/json"
call stl.net.get_text url body status
print status

call stl.net.get_json url obj status
print status
```
