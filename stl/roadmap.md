# STL Expansion Roadmap (5 New Modules)

This roadmap proposes **five** new Standard Library modules to add under `stl/`.

## Design constraints (so STL stays usable and testable)

- **No unintended output**: STL functions should not emit output unless explicitly designed as `print_*` helpers.
- **Return values > printed values**: Prefer core commands that can store into variables/strings/dicts/arrays.
- **Avoid temp name collisions**: STL functions must namespace internal temporaries (e.g. `_stl_json_*`) because TechLang functions share the interpreter state.
- **CI-safe behavior**: Network and OS-dependent functions should be deterministic and/or have tests that can be skipped with clear markers.

---

## Module 1: `stl/net.tl` (HTTP + convenience)

### Goal
Make HTTP workflows ergonomic and consistent, building on the existing core commands:
- `http_get "url" <respVar>` stores body in `strings[respVar]` and status in `<respVar>_status`.
- `http_post "url" <dataToken>` stores body in `strings[response]` and status in `response_status`.

### Proposed public API
- `net.get url respName` — wraps `http_get` with consistent naming.
- `net.get_status respName outVar` — reads `<respName>_status` into `outVar`.
- `net.get_text url outStr outStatusVar` — one-shot helper: uses an internal response name, returns body + status.
- `net.get_json url outDict outStatusVar` — GET then `json_parse` into `outDict`.
- `net.post_text url dataToken outStr outStatusVar` — POST returning body + status.

### Notes / edge cases
- Error handling should return status `0` and body `""` on failure (consistent, easy to branch on).
- Prefer deterministic tests using a **local stub server** only if it already exists; otherwise keep tests minimal and skip if networking is unavailable.

### Work items
- Implement `stl/net.tl`.
- Add tests:
  - Parsing a known JSON response (skipped if network not available), or
  - Mock-free unit tests focused on internal naming + variable wiring (no actual HTTP).

---

## Module 2: `stl/json.tl` (JSON helpers)

### Goal
Provide small, composable helpers on top of the existing JSON core commands:
- `json_parse <sourceStr> <targetDictOrArray>`
- `json_stringify <sourceDictOrArray> <targetStr>`
- `json_read "path" <targetDictOrArray>`
- `json_write <sourceDictOrArray> "path"`

### Proposed public API
- `json.parse str out` — thin wrapper around `json_parse`.
- `json.stringify obj outStr` — thin wrapper around `json_stringify`.
- `json.read path out` — wrapper around `json_read`.
- `json.write obj path` — wrapper around `json_write`.
- `json.try_parse str out okVar` — sets `okVar` to `1/0`.
- `json.get_str dict key outStr foundVar` — safe key lookup returning `foundVar`.
- `json.get_num dict key outVar foundVar` — numeric lookup.

### Core prerequisites (recommended)
These improve ergonomics and eliminate the need for output-capturing hacks:
- Add **store-into-target** forms for dictionary reads:
  - `dict_get <name> "key" <target> [str|var]` (instead of printing).

### Work items
- Implement `stl/json.tl` wrappers that work today (parse/stringify/read/write/try_parse).
- If `dict_get` is enhanced, implement `json.get_*` helpers.
- Add tests for parse/stringify roundtrips and `try_parse`.

---

## Module 3: `stl/datetime.tl` (Date/time utilities)

### Goal
Make date/time operations usable in programs without requiring external processes.

### Proposed public API
- `datetime.now_iso outStr` — current UTC ISO string.
- `datetime.unix_now outVar` — unix timestamp (seconds).
- `datetime.format_unix ts fmt outStr` — formatted UTC string.
- `datetime.is_iso8601 str outVar` — basic validation (shape + key characters).
- `datetime.parse_iso_parts iso outYear outMonth outDay outHour outMin outSec okVar` — basic ISO parsing (UTC only).

### Core prerequisites (recommended)
Right now `now` and `format_date` only print. To keep STL “no unintended output”, add optional targets:
- `now <targetStr>`
- `format_date <seconds> ["fmt"] <targetStr>`
- `sys_time <targetVar>` (or reuse an existing numeric time command with target)

### Work items
- Implement `stl/datetime.tl` once store-forms exist.
- Add tests that freeze format expectations (UTC only).

---

## Module 4: `stl/random.tl` (Randomness)

### Goal
Expose random utilities that are usable inside functions (without printing) and suitable for testing.

### Proposed public API
- `random.randint lo hi outVar`
- `random.choice arr outVar okVar` — choose an element.
- `random.shuffle arr outArr` — Fisher–Yates shuffle.
- `random.seed n` — deterministic runs.

### Core prerequisites (recommended)
- Extend core to support **store output instead of printing**:
  - `math_random <lo> <hi> <targetVar>`
- Add seeding support:
  - `math_seed <n>` (or `random_seed <n>`)

### Work items
- Implement `stl/random.tl` after the above core additions.
- Add deterministic tests using `random.seed`.

---

## Module 5: `stl/io.tl` (File/text utilities) + `stl/path.tl` (Path helpers)

### Goal
Make file operations ergonomic while preserving sandbox rules (relative to `base_dir`) and avoiding output-only APIs.

### Proposed public API (I/O)
- `io.read_text path outStr okVar` — wraps `file_read` with error-to-flag.
- `io.write_text path text okVar` — wraps `file_write`.
- `io.append_text path text okVar` — wraps `file_append`.
- `io.delete path okVar` — wraps `file_delete`.
- `io.exists path outVar` — returns `1/0`.
- `io.listdir path outArr okVar` — returns entries array.

### Proposed public API (paths)
- `path.join a b outStr` — minimal join.
- `path.basename p outStr`
- `path.dirname p outStr`
- `path.extname p outStr`

### Core prerequisites (recommended)
Some current file commands print results; STL needs store-forms:
- `file_exists "path" <targetVar>`
- `file_list "dir" <targetArr>`

### Work items
- Add the core store-forms.
- Implement `stl/io.tl` and `stl/path.tl`.
- Add tests using `tmp_path` with `base_dir` to avoid touching real FS.

---

## Suggested implementation order
1) `stl/net.tl` and basic `stl/json.tl` wrappers (already supported well by core).
2) Add store-into-target core forms (`now`, `format_date`, `math_random`, `file_exists`, `file_list`, `dict_get`).
3) Implement `stl/datetime.tl`, `stl/random.tl`, `stl/io.tl` + `stl/path.tl`.

## Definition of done (per module)
- Module exists under `stl/` with exported functions.
- Tests exist in `tests/` for core behavior.
- Module documented in `stl/README.md` and `docs/` where appropriate.
