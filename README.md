# 🖥️ TechLang

**TechLang** is a hacker-themed, stack-based programming language implemented in Python. It features its own custom interpreter, language parser, and playful syntax (`ping`, `crash`, `upload`, etc.). The project includes a CLI, a GUI, and a web-based playground.

---

## 🧠 What is TechLang?

TechLang is designed for experimenting with:

- Language design
- Interpreter building
- Syntax parsing
- Fun and engaging programming constructs

---

## 📁 Project Structure

```
TechLang/
├── techlang/            # Interpreter & parser logic
│   ├── interpreter.py
│   ├── parser.py
│   ├── database.py      # SQLite3 database operations
│   ├── core.py
│   ├── basic_commands.py
│   ├── variables.py
│   ├── stack.py
│   ├── control_flow.py
│   ├── imports.py
│   ├── aliases.py
│   ├── blocks.py
│   └── __init__.py
│
├── tests/               # Pytest-based unit tests
│   ├── test_interpreter.py
│   └── test_database.py
│
├── examples/            # Sample TechLang programs
│   ├── hello.tl
│   ├── loop.tl
│   ├── if.tl
│   ├── database.tl      # SQLite3 example
│   └── ...
│
├── playground/          # Optional GUI playground (Tkinter)
│   └── gui.py
│
├── techlang_web/        # Flask-based web playground
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   ├── static/
│   └── uploads/
│
├── uploads/             # Uploaded .tl files for testing
│
├── cli.py               # CLI for running .tl files
├── run_tests.py         # Runs all tests
├── requirements.txt     # Dependencies
├── README.md            # This file
├── DEV.md               # Developer guide
├── PLAYGROUND.MD        # Playground guide
└── .venv/               # Python virtual environment
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/devaanshpathak/techlang.git
cd techlang
````

### 2. Set up a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running TechLang

### ✅ Option 1: Interpreter via Python

```python
from techlang.interpreter import run

code = "boot ping ping print"
print(run(code))  # Output: 2
```

### ✅ Option 2: Command-Line Interface

```bash
# Using the bundled script
python cli.py examples/hello.tl

# With console entry (after `pip install -e .` or packaging), use the `tl` command:
tl examples/hello.tl

# Start interactive REPL
tl -i

# Verbose mode
tl -v examples/hello.tl
```

### ✅ Option 3: Web Playground (Flask)

```bash
cd techlang_web
python app.py
```

* Visit: `http://localhost:8080`
* Paste or upload `.tl` code and see output

### ✅ Option 4: GUI (Tkinter)

```bash
python playground/gui.py
```

---

## 🧪 Running Tests

```bash
python run_tests.py
```

* Covers interpreter logic, variables, loops, stack, conditions, functions, input, database operations, and more.

---

## ✨ Language Features (Highlights)

### Core & Variables
`boot`, `ping`, `crash`, `print`, `set`, `add`, `sub`, `mul`, `div`, `input`, `upload`, `download`, `debug`, `import`, `alias`, `hack`

### Comments
Three styles supported: `#` single-line, `//` C-style single-line, `/* */` multi-line blocks

### Control Flow
`loop ... end`, `if ... end`, `while ... end`, `switch/case/default`, `try/catch`, `def ... end`, `call`

### Data Types
- Arrays: `array_create`, `array_set`, `array_get`, `array_push`, `array_pop`, `array_map`, `array_filter`
- Strings: `str_create`, `str_concat`, `str_length`, `str_substring`, `str_split`, `str_replace`, `str_trim`, `str_upper`, `str_lower`, `str_contains`, `str_reverse`
- Dictionaries: `dict_create`, `dict_set`, `dict_get`, `dict_keys`
- **JSON**: `json_parse`, `json_stringify`, `json_read`, `json_write` (full Unicode support)

### File I/O
`file_read`, `file_write`, `file_append`, `file_exists`, `file_delete`, `file_list`

### Network & Web
HTTP: `http_get`, `http_post`, `http_status`
Server stubs: `server_start`, `server_route`, `server_stop`

### Graphics
`graphics_init`, `graphics_draw_line`, `graphics_draw_circle`, `graphics_draw_text`, `graphics_show`

### Math & Science
`math_sin`, `math_cos`, `math_sqrt`, `math_pow`, `math_random`, `math_pi`, `math_e`

### Database
CRUD: `db_create`, `db_insert`, `db_select`, `db_update`, `db_delete`, `db_execute`, `db_close`
Advanced: `db_begin`, `db_commit`, `db_rollback`, `db_tables`, `db_schema`, `db_indexes`, `db_connect`, `db_disconnect`

### Memory Management
`mem_alloc`, `mem_free`, `mem_read`, `mem_write`, `mem_dump`

### Concurrency & Async
`thread_create`, `thread_join`, `thread_sleep`, `async_start`, `async_wait`

### System & Processes
System: `sys_exec`, `sys_env`, `sys_time`, `sys_date`, `sys_exit`
Processes: `proc_spawn`, `proc_wait`, `proc_kill`

### Debugger
`breakpoint`, `step`, `continue`, `inspect`, `watch`, `unwatch`, `clear_breakpoints`

### Help
`help` or `help <command>` to see built-in docs.

---

## 📂 Example Programs

All in the `examples/` folder:

```bash
python cli.py examples/loop.tl
python cli.py examples/input.tl
python cli.py examples/database.tl
# Extended feature demos
python cli.py examples/data_types_demo.tl
python cli.py examples/files.tl
python cli.py examples/network.tl
python cli.py examples/graphics.tl
python cli.py examples/memory.tl
python cli.py examples/threads.tl
```

Or try them in the web playground.

---

## 📦 Requirements

* Python 3.10+
* `flask` (for web)
* `pytest` (for tests)
* `tkinter` (optional GUI)
* `sqlite3` (built-in Python module)

Install all with:

```bash
pip install -r requirements.txt
```

---

## 🤖 Future Ideas

* Error highlighting in web playground
* CLI flags for debug mode or stack tracing
* Bytecode version of TechLang
* Language transpiler to Python
* Additional database features (transactions, indexes, foreign keys)
* Database schema introspection

---

## ❤️ Credits

Crafted for hackers, students, and language lovers who want to build something weird, beautiful, and programmable.

---

## ➕ Additional Commands (Quick Reference)

Below are recently added commands grouped by feature area. See `examples/` and tests for usage.

### Data Types
- Arrays: `array_create name size`, `array_set name idx val`, `array_get name idx`, `array_push name val`, `array_pop name`
- Strings: `str_create name "text"`, `str_concat name otherOr"text"`, `str_length name`, `str_substring name start end`
- Dictionaries: `dict_create name`, `dict_set name "key" "val"`, `dict_get name "key"`, `dict_keys name`

### Control Flow
- While loop: `while x > 0 ... end`
- Switch/Case: `switch x ... case 1 ... case 2 ... default ... end`
- Try/Catch: `try ... catch ... end`

### File I/O
- `file_read "path" var`, `file_write "path" "text"`, `file_append "path" "text"`
- `file_exists "path"`, `file_delete "path"`, `file_list "dir"`

### Network & Web
- HTTP client: `http_get "url" resp`, `http_post "url" data`, `http_status resp`
- Server stubs: `server_start port`, `server_route "path" handler`, `server_stop`

### Graphics (Pillow-backed)
- `graphics_init w h`, `graphics_draw_line x1 y1 x2 y2`, `graphics_draw_circle x y r`, `graphics_draw_text x y "txt"`, `graphics_show`

### Math & Science
- Functions: `math_sin a`, `math_cos a`, `math_sqrt n`, `math_pow b e`, `math_random lo hi`
- Constants: `math_pi`, `math_e`

### Database (Advanced)
- Transactions: `db_begin`, `db_commit`, `db_rollback`
- Introspection: `db_tables`, `db_schema table`, `db_indexes table`
- Connections: `db_connect "path"`, `db_disconnect`

### Memory Management (planned)
- `mem_alloc size`, `mem_free address`, `mem_read address`, `mem_write address value`, `mem_dump`
