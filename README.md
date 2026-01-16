# TechLang

**TechLang** is a hacker-themed, stack-based programming language implemented in Python. It features its own custom interpreter, language parser, and playful syntax (`ping`, `crash`, `upload`, etc.). The project includes a CLI, a GUI, and a web-based playground.

---

## What is TechLang?

TechLang is designed for experimenting with:

- Language design
- Interpreter building
- Syntax parsing
- Fun and engaging programming constructs

---

## Project Structure

```
TechLang/
├── techlang/            # Interpreter & parser logic
│   ├── interpreter.py   # Main interpreter entry point
│   ├── parser.py        # Tokenizer and syntax parser
│   ├── executor.py      # Command execution dispatcher
│   ├── core.py          # InterpreterState and core types
│   ├── basic_commands.py # Core language commands
│   ├── variables.py     # Variable operations
│   ├── stack.py         # Stack operations
│   ├── control_flow.py  # if, loop, while, switch, try/catch
│   ├── data_types.py    # Arrays, strings, dicts, JSON
│   ├── struct_ops.py    # Structured types
│   ├── file_ops.py      # File I/O operations
│   ├── net_ops.py       # HTTP client and server
│   ├── graphics_ops.py  # Graphics rendering (Pillow)
│   ├── database.py      # SQLite3 database operations
│   ├── memory_ops.py    # Memory management
│   ├── math_ops.py      # Math and date/time functions
│   ├── thread_ops.py    # Threading and concurrency
│   ├── system_ops.py    # System and process operations
│   ├── debugger.py      # Debugger with breakpoints
│   ├── class_ops.py     # OOP: classes, inheritance, methods
│   ├── function_ops.py  # First-class functions, closures
│   ├── decorator_ops.py # Python-like decorators
│   ├── context_ops.py   # Context managers (with statement)
│   ├── async_ops.py     # Async/await and event loop
│   ├── help_ops.py      # Help system
│   ├── imports.py       # Module imports
│   ├── aliases.py       # Command aliases
│   ├── macros.py        # Macro expansion
│   ├── blocks.py        # Block depth tracking
│   ├── formatter.py     # Code formatter
│   ├── linter.py        # Code linter
│   └── __init__.py
│
├── tests/               # Pytest-based unit tests (776+ tests)
│   ├── test_interpreter.py
│   ├── test_database.py
│   ├── test_database_advanced.py
│   ├── test_data_types.py
│   ├── test_json.py
│   ├── test_string_ops.py
│   ├── test_comments.py
│   ├── test_debugger.py
│   ├── test_file_ops.py
│   ├── test_graphics.py
│   ├── test_math_ops.py
│   ├── test_memory.py
│   ├── test_network.py
│   ├── test_threads.py
│   ├── test_system.py
│   ├── test_formatter.py
│   └── ...
│
├── docs/                # Comprehensive documentation
│   ├── general.md       # Syntax and rules
│   ├── core.md          # Core commands
│   ├── control-flow.md  # Control structures
│   ├── data-types.md    # Data structures and JSON
│   ├── file-io.md       # File operations
│   ├── network.md       # HTTP and networking
│   ├── graphics.md      # Graphics and visualization
│   ├── database.md      # Database operations
│   ├── math.md          # Math and date/time
│   ├── memory.md        # Memory management
│   ├── concurrency.md   # Threading and async
│   ├── system.md        # System and processes
│   ├── debugging.md     # Debugger guide
│   ├── cookbook.md      # Recipes and patterns
│   ├── examples.md      # Example programs index
│   └── help-cli.md      # CLI and help system
│
├── examples/            # Sample TechLang programs (26 files)
│   ├── hello.tl
│   ├── loop.tl
│   ├── if.tl
│   ├── vars.tl
│   ├── functions.tl
│   ├── arrays.tl
│   ├── strings.tl
│   ├── string_operations.tl
│   ├── dictionaries.tl
│   ├── json_demo.tl
│   ├── database.tl
│   ├── files.tl
│   ├── network.tl
│   ├── graphics.tl
│   ├── memory.tl
│   ├── threads.tl
│   ├── debugger_demo.tl
│   ├── cookbook_multifeature.tl
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
├── .github/             # GitHub Actions CI/CD
│   └── workflows/
│       ├── pytest.yml   # Test suite
│       └── lint.yml     # Code linting
│
├── cli.py               # CLI for running .tl files
├── format_tl.py         # TechLang code formatter
├── run_tests.py         # Test suite runner
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── DOCUMENTATION.md     # Master documentation index
├── DEV.md               # Developer guide
├── AGENTS.md            # AI agent guide
├── PLAYGROUND.MD        # Playground guide
└── .venv/               # Python virtual environment
```

---

## Getting Started

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

## Running TechLang

### Option 1: Interpreter via Python

```python
from techlang.interpreter import run

code = "boot ping ping print"
print(run(code))  # Output: 2
```

### Option 2: Command-Line Interface

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

### Option 3: Web Playground (Flask)

```bash
cd techlang_web
python app.py
```

* Visit: `http://localhost:8080`
* Paste or upload `.tl` code and see output

### Option 4: GUI (Tkinter)

```bash
python playground/gui.py
```

### GUI docs & examples

- Docs: `docs/gui.md`
- Examples:
	- `examples/gui_ttk_demo.tl`
	- `examples/gui_text_canvas_demo.tl`

---

## Running Tests

```bash
python run_tests.py
```

* Covers interpreter logic, variables, loops, stack, conditions, functions, input, database operations, and more.

---

## Language Features (Highlights)

### Core & Variables
`boot`, `ping`, `crash`, `print`, `set`, `add`, `sub`, `mul`, `div`, `input`, `upload`, `download`, `debug`, `import`, `alias`, `hack`

### Comments
Three styles supported: `#` single-line, `//` C-style single-line, `/* */` multi-line blocks

### Control Flow
`loop ... end`, `if ... end`, `while ... end`, `switch/case/default`, `try/catch`, `def ... end`, `call`

### Macro System (NEW)
- **Conditional Macros**: `macro name if condition param do ... end` - Expand only when condition is true
- **Nested Macros**: Macros can invoke other macros with full parameter substitution
- **Macro Libraries**: Load reusable macro collections from external files
- **REPL Integration**: `:loadmacro` command for interactive macro loading
- See [Advanced Macro Guide](docs/macros-advanced.md) for details

### Enhanced REPL (NEW)
- **Persistent State**: Variables, functions, and macros persist across commands
- **Introspection**: `:state` shows all variables, `:macros` lists macros
- **State Management**: `:reset` clears state without restarting
- **Macro Loading**: `:loadmacro file` loads macro libraries interactively
- **Command History**: Full readline support with persistent history
- See [REPL Guide](docs/repl-guide.md) for complete reference

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

### Object-Oriented Programming (NEW)
- **Classes**: `class Name ... end` with fields, methods, and constructors
- **Inheritance**: `class Child extends Parent` with method overriding
- **Instance Methods**: `method name params ... end` with `self` reference
- **Static Methods**: `static name params ... end` (no instance needed)
- **Field Access**: `get_field`, `set_field` for instance data
- **Type Checking**: `instanceof` for runtime type checks
- See [OOP Guide](docs/oop.md) for complete reference

### First-Class Functions & Closures (NEW)
- **Function Values**: `fn name params do ... end` creates callable values
- **Closures**: Functions capture outer scope variables
- **Function References**: `fn_ref funcName var` gets reference to existing function
- **Higher-Order Functions**: `map_fn`, `filter_fn`, `reduce_fn` for functional programming
- **Partial Application**: `partial func newFunc arg=val` binds arguments
- **Function Composition**: `compose f g composed` creates pipelines
- **Lambda Expressions**: `lambda name param "expr"` for simple transforms
- See [Functions Guide](docs/functions.md) for complete reference

### Decorators (NEW)
- **Decorator Definition**: `decorator name mode do ... end` (mode: before/after/both)
- **Apply Decorator**: `decorate func decorator` wraps function with decorator
- **Built-in Decorators**: `@log` and `@time` for common use cases
- See [Decorators Guide](docs/decorators.md) for complete reference

### Context Managers (NEW)
- **Built-in Contexts**: `with timer do ... end`, `with suppress do ... end`
- **File Context**: `with file "path" do ... end` for automatic file handling
- **Lock Context**: `with lock mutex do ... end` for thread safety
- **Transaction**: `with transaction do ... end` for database rollback
- **Custom Contexts**: `context name enter exit do ... end`
- See [Context Managers Guide](docs/context-managers.md) for complete reference

### Async/Await (NEW)
- **Async Functions**: `async def name do ... end` for coroutines
- **Await**: `await coroutine -> result` for async results
- **Task Spawning**: `spawn coroutine -> task_id` for background tasks
- **Gathering**: `gather t1 t2 t3 -> results` for parallel execution
- **Task Management**: `task_status`, `task_cancel` for control
- See [Async/Await Guide](docs/async-await.md) for complete reference

### Exception Handling
- **throw/raise**: `throw "message" [ErrorType]` to raise exceptions
- **try/catch**: Catch and handle thrown exceptions
- Exception type available for conditional handling

### Help
`help` or `help <command>` to see built-in docs.

---

## Example Programs

All in the `examples/` folder:

```bash
# Basic Examples
python cli.py examples/hello.tl
python cli.py examples/loop.tl
python cli.py examples/if.tl
python cli.py examples/vars.tl
python cli.py examples/functions.tl
python cli.py examples/input.tl

# Data Structures
python cli.py examples/arrays.tl
python cli.py examples/strings.tl
python cli.py examples/string_operations.tl
python cli.py examples/dictionaries.tl
python cli.py examples/data_types_demo.tl

# Advanced Features
python cli.py examples/json_demo.tl
python cli.py examples/comments.tl
python cli.py examples/alias.tl
python cli.py examples/switch_try.tl
python cli.py examples/while_loops.tl

# System Integration
python cli.py examples/database.tl
python cli.py examples/files.tl
python cli.py examples/network.tl
python cli.py examples/graphics.tl
python cli.py examples/memory.tl
python cli.py examples/threads.tl

# Debugging & Recipes
python cli.py examples/debugger_demo.tl
python cli.py examples/cookbook_multifeature.tl

# OOP & Functional Programming
python cli.py examples/oop_demo.tl
```

Or try them in the web playground.

---

## Requirements

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

## Future Ideas

* Database transactions and schema introspection (Completed)
* Debugger with breakpoints and stepping (Completed)
* JSON support for modern data interchange (Completed)
* String manipulation operations (Completed)
* Multi-line comments (Completed)
* Error highlighting in web playground
* Bytecode version of TechLang
* Language transpiler to Python
* Foreign key support in database
* Time-travel debugging (step backwards)
* Conditional breakpoints

---

## Credits

Crafted for hackers, students, and language lovers who want to build something weird, beautiful, and programmable.

---

## Quick Command Reference

Comprehensive command reference grouped by category. For detailed documentation, see [DOCUMENTATION.md](DOCUMENTATION.md).

### Core Commands
`boot`, `ping`, `crash`, `print`, `upload`, `download`, `debug`, `hack`, `lag`, `sleep`, `yield`

### Variables & Math
`set`, `add`, `sub`, `mul`, `div`, `input`

### Control Flow
- **Conditionals**: `if x > 5 ... end`
- **Loops**: `loop 10 ... end`, `while x < 100 ... end`
- **Switch/Case**: `switch x ... case 1 ... case 2 ... default ... end`
- **Pattern Matching**: `match expr ... case > 10 ... case == 5 ... end`
- **Error Handling**: `try ... catch [errVar [stackVar]] ... end`
- **Functions**: `def name ... end`, `call name`

### Data Structures
- **Arrays**: `array_create`, `array_set`, `array_get`, `array_push`, `array_pop`, `array_map`, `array_filter`
- **Strings**: `str_create`, `str_concat`, `str_length`, `str_substring`, `str_split`, `str_replace`, `str_trim`, `str_upper`, `str_lower`, `str_contains`, `str_reverse`, `string_interpolate`, `string_match`
- **Dictionaries**: `dict_create`, `dict_set`, `dict_get`, `dict_keys`
- **Structs**: `struct Type field1 field2 ... end`, `struct new`, `struct set`, `struct get`, `struct dump`

### JSON Operations
`json_parse`, `json_stringify`, `json_read`, `json_write` - Full Unicode support for modern data interchange

### File I/O
`file_read`, `file_write`, `file_append`, `file_exists`, `file_delete`, `file_list`

### Network & HTTP
- **Client**: `http_get`, `http_post`, `http_status`
- **Server** (stubs): `server_start`, `server_route`, `server_stop`

### Graphics (Pillow)
`graphics_init`, `graphics_draw_line`, `graphics_draw_circle`, `graphics_draw_text`, `graphics_show`

### Math & Date/Time
- **Trigonometry**: `math_sin`, `math_cos`, `math_tan`, `math_asin`, `math_acos`, `math_atan`
- **Arithmetic**: `math_sqrt`, `math_pow`, `math_random`, `math_round`, `math_floor`, `math_ceil`
- **Conversion**: `math_deg2rad`, `math_rad2deg`
- **Constants**: `math_pi`, `math_e`
- **Date/Time**: `now`, `format_date`, `sys_time`, `sys_date`

### Database (SQLite3)
- **CRUD**: `db_create`, `db_insert`, `db_select`, `db_update`, `db_delete`, `db_execute`, `db_close`
- **Transactions**: `db_begin`, `db_commit`, `db_rollback`
- **Introspection**: `db_tables`, `db_schema`, `db_indexes`
- **Connections**: `db_connect`, `db_disconnect`

### Memory Management
`mem_alloc`, `mem_free`, `mem_read`, `mem_write`, `mem_dump`

### Concurrency & Threading
- **Threads**: `thread_create`, `thread_join`, `thread_sleep`, `thread_status`, `thread_result`, `thread_list`, `thread_wait_all`
- **Async**: `async_start`, `async_wait`
- **Synchronization**: `mutex_create`, `mutex_lock`, `mutex_unlock`
- **Queues**: `queue_push`, `queue_pop`

### System & Processes
- **System**: `sys_exec`, `sys_env`, `sys_time`, `sys_date`, `sys_sleep`, `sys_cwd`, `sys_exit`
- **Processes**: `proc_spawn`, `proc_kill`, `proc_wait`, `proc_status`

### Debugging & Inspection
`breakpoint`, `step`, `continue`, `inspect`, `watch`, `unwatch`, `clear_breakpoints`

### Modules & Macros
- **Modules**: `package use module`, `call module.function`
- **Macros**: `macro name params do ... end`, `inline name args`
- **Aliases**: `alias short command`
- **Imports**: `import name`

### Comments
- Single-line: `# comment` or `// comment`
- Multi-line: `/* comment */`

### Help System
`help` - List all commands  
`help <command>` - Show specific command help
