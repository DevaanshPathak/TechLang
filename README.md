# 🖥️ TechLang

**TechLang** is a hacker-themed, stack-based toy programming language implemented in Python. It features its own custom interpreter, language parser, and playful syntax (`ping`, `crash`, `upload`, etc.). The project includes a CLI, a GUI, and a web-based playground.

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
python cli.py examples/hello.tl
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

## ✨ Language Features

| Command     | Description                         |
| ----------- | ----------------------------------- |
| `boot`      | Resets value to 0                   |
| `ping`      | Increments current value            |
| `crash`     | Decrements current value            |
| `print`     | Prints current value or variable    |
| `set x 5`   | Sets variable `x` to 5              |
| `add x 2`   | Adds 2 to variable `x`              |
| `input x`   | Assigns input to variable `x`       |
| `loop 3`    | Loops a block of code 3 times       |
| `if x > 5`  | Executes block if condition is true |
| `def f`     | Defines a function                  |
| `call f`    | Calls a defined function            |
| `upload`    | Pushes value to stack               |
| `download`  | Pops value from stack               |
| `debug`     | Prints internal state               |
| `import x`  | Imports a `.tl` file (e.g., `x.tl`) |
| `alias a b` | Creates a shorthand (a → b)         |
| `hack`      | Doubles current value               |
| `db_create table "cols"` | Creates a SQLite table with columns |
| `db_insert table "vals"` | Inserts data into a table |
| `db_select "query"` | Executes a SELECT query |
| `db_update "query"` | Executes an UPDATE query |
| `db_delete "query"` | Executes a DELETE query |
| `db_execute "sql"` | Executes any SQL statement |
| `db_close` | Closes database connections |

---

## 📂 Example Programs

All in the `examples/` folder:

```bash
python cli.py examples/loop.tl
python cli.py examples/input.tl
python cli.py examples/database.tl
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
