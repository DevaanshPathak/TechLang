# TechLang Development Guide

## 🚀 Overview

TechLang is a minimalistic, stack-based programming language designed for learning and experimenting with command-based interpreters.
This guide is for contributors who want to understand the codebase, follow code style, add new features, or run tests.

---

## 📂 Repository Structure

```
TechLang/
├─ cli.py                 # CLI interface for TechLang
├─ run_tests.py           # Script to run all tests
├─ requirements.txt       # Python dependencies
├─ README.md              # Project overview
├─ DEV.md                 # This developer guide
├─ PLAYGROUND.MD          # Playground guide
├─ techlang/              # Core interpreter and parser
│   ├─ __init__.py
│   ├─ interpreter.py
│   ├─ parser.py
│   ├─ database.py        # SQLite3 database operations
│   ├─ core.py
│   ├─ basic_commands.py
│   ├─ variables.py
│   ├─ stack.py
│   ├─ control_flow.py
│   ├─ imports.py
│   ├─ aliases.py
│   └─ blocks.py
├─ techlang_web/          # Flask playground site
│   ├─ app.py
│   ├─ templates/
│   │   └─ index.html
│   ├─ static/
│   └─ uploads/
├─ tests/                 # Unit tests
│   ├─ test_interpreter.py
│   └─ test_database.py
├─ examples/              # Sample TechLang programs
│   ├─ hello.tl
│   ├─ loop.tl
│   ├─ if.tl
│   ├─ database.tl        # SQLite3 example
│   └─ ...
└─ playground/            # GUI-based local playground
```

---

## 📐 Code Architecture

### Interpreter

* **Stack-based:** Operations manipulate a stack.
* **Variables:** `set`, `add`, `sub`, etc. store values in a variable table.
* **Commands:** Core commands include `boot`, `ping`, `print`, `upload`, `download`, `hack`, `debug`, etc.
* **Loops:** `loop ... end` blocks are executed multiple times.
* **Functions:** Defined with `def ... end` and called using `call`.
* **Aliases:** `alias` allows shorthand commands.
* **Database:** SQLite3 integration with `db_create`, `db_insert`, `db_select`, `db_update`, `db_delete`, `db_execute`, and `db_close` commands.

### Command Execution Flow

```
               ┌──────────────┐
               │   Start      │
               │(Interpreter) │
               └─────┬────────┘
                     │
                     ▼
             ┌───────────────┐
             │ Read Code Line│
             └─────┬─────────┘
                   │
      ┌────────────┴─────────────┐
      ▼                          ▼
  Is it a command?           Is it a variable/alias?
      │                          │
      ▼                          ▼
Parse & Validate             Resolve alias/var
      │                          │
      ▼                          ▼
  Execute Command             Push/Update stack/vars
      │
      ▼
 ┌─────────────┐
 │ Increment PC│
 └─────┬───────┘
       │
       ▼
  ┌─────────────┐
  │ Is it a loop│
  │ block?      │
  └────┬────────┘
       │ Yes
       ▼
 ┌─────────────┐
 │ Evaluate    │
 │ Loop count  │
 └─────┬───────┘
       │
       ▼
 ┌─────────────┐
 │ Execute     │
 │ Inside Loop │
 └─────┬───────┘
       │
       ▼
 ┌─────────────┐
 │ End loop →  │
 │ Check exit  │
 └─────┬───────┘
       │
       ▼
 ┌─────────────┐
 │ Function Def│
 └─────┬───────┘
       │
       ▼
 ┌─────────────┐
 │ Store func  │
 │ in table    │
 └─────┬───────┘
       │
       ▼
 ┌─────────────┐
 │ Function    │
 │ Call        │
 └─────┬───────┘
       │
       ▼
 ┌─────────────┐
 │ Execute     │
 │ Function    │
 │ body        │
 └─────┬───────┘
       │
       ▼
 ┌─────────────┐
 │ Print / IO  │
 │ Commands    │
 └─────┬───────┘
       │
       ▼
 ┌─────────────┐
 │ Debug/Stack │
 │ Display     │
 └─────┬───────┘
       │
       ▼
 ┌─────────────┐
 │ End of Code │
 └─────────────┘
       │
       ▼
      ┌──────────┐
      │ Return   │
      │ Output   │
      └──────────┘
```

---

## 🖊 Code Style

* **Python**:

  * Use **PEP8** formatting.
  * Keep functions ≤ 50 lines if possible.
  * Docstrings required for public functions.
  * Type hints preferred.
* **TechLang (.tl)**:

  * Commands are lowercase.
  * One command per line.
  * Indent `loop`, `if`, `def` blocks consistently (2 spaces).

---

## 🧩 Contributing

1. Fork the repository.
2. Create a feature branch:

   ```bash
   git checkout -b feature/<your-feature>
   ```
3. Install dependencies in a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\Activate.ps1 # Windows PowerShell
   pip install -r requirements.txt
   ```
4. Run tests to ensure nothing breaks:

   ```bash
   python run_tests.py
   ```
5. Commit changes with meaningful messages.
6. Open a pull request.

---

## 🧪 Testing

* All tests reside in `tests/`.
* Use `pytest` or `python run_tests.py`.
* Make sure to add tests for any new commands or features.
* Database tests include cleanup functions to prevent conflicts.
* Example:

  ```python
  from techlang.interpreter import run

  def test_example():
      assert run("boot ping print").strip() == "1"
  
  def test_database():
      code = """
      db_create users "id INTEGER, name TEXT"
      db_insert users "1, Alice"
      db_select "SELECT * FROM users"
      """
      output = run(code)
      assert "Table 'users' created successfully" in output
  ```

---

## 🛠 Debugging

* `debug` command prints the current stack and variable states.
* Use verbose prints during development:

  ```python
  print("DEBUG:", stack, vars)
  ```

## 🗄️ Database Operations

TechLang now includes SQLite3 database support with the following commands:

* `db_create table "columns"` - Creates a new table with specified columns
* `db_insert table "values"` - Inserts data into a table
* `db_select "query"` - Executes SELECT queries and displays results
* `db_update "query"` - Executes UPDATE queries
* `db_delete "query"` - Executes DELETE queries
* `db_execute "sql"` - Executes any SQL statement
* `db_close` - Closes all database connections

### Database Features

* **Connection Management**: Singleton pattern ensures proper connection handling
* **Error Handling**: Graceful error messages for SQL syntax and constraint violations
* **Quote Handling**: Automatic removal of quotes from SQL strings
* **Column Parsing**: Supports complex column definitions like `"id INTEGER PRIMARY KEY"`
* **Data Types**: Full SQLite3 data type support (INTEGER, TEXT, REAL, BLOB, etc.)
* **File Management**: Database files created as `techlang.db` in current directory

### Example Usage

```bash
# Create a table
db_create users "id INTEGER PRIMARY KEY, name TEXT, age INTEGER, email TEXT"

# Insert data
db_insert users "1, Alice, 25, alice@example.com"

# Query data
db_select "SELECT * FROM users WHERE age > 20"

# Update data
db_update "UPDATE users SET age = 26 WHERE name = 'Alice'"

# Delete data
db_delete "DELETE FROM users WHERE name = 'Charlie'"

# Close connections
db_close
```

---

## 🌐 Web Playground

* TechLang includes a Flask-based playground in `techlang_web/`.
* Features:

  * Input `.tl` code in browser.
  * Upload `.tl` files.
  * Interactive output display.
* Run locally:

  ```bash
  cd techlang_web
  python app.py
  ```
* Navigate to `http://127.0.0.1:8080`.

---

## ⚡ Notes

* Always run tests before merging.
* Document any new commands or syntax changes.
* Follow the ASCII flow diagram when implementing new features.