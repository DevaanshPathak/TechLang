# 🧠 TechLang

**TechLang** is a fun and weird esolang inspired by tech terminology like `boot`, `ping`, and `hack`.  
It’s designed for experimentation, learning, and making programming feel like a system admin RPG.

---

## 📦 Features

- Stack-based memory
- Arithmetic & debug commands
- CLI and GUI support
- Interpreted in Python
- Easy to extend

---

## 🚀 Quick Start

```bash
# Run from CLI
python cli.py examples/hello.tl

# Or launch the GUI
python -m playground.gui
````

---

## 💻 TechLang Commands

| Command    | Action                        |
| ---------- | ----------------------------- |
| `boot`     | Resets the value to 0         |
| `ping`     | Increments the value          |
| `crash`    | Decrements the value          |
| `hack`     | Doubles the value             |
| `print`    | Prints the current value      |
| `upload`   | Pushes value to stack         |
| `download` | Pops value from stack         |
| `reboot`   | Alias for `boot`              |
| `debug`    | Prints current stack          |
| `lag`      | Sleeps for 1 second           |
| `fork`     | Clones current value to stack |

---

## 📁 Project Structure

```
TechLang/
├── techlang/           # Parser & interpreter
│   ├── parser.py
│   └── interpreter.py
├── playground/         # GUI playground
│   └── gui.py
├── examples/           # .tl sample programs
├── tests/              # Unit tests
├── cli.py              # Command-line interface
├── run_tests.py        # Test runner
└── README.md
```

---

## 🧪 Tests

```bash
python run_tests.py
```

---

## ✨ Made for Twist by DevaanshPathak

TechLang was built as part of the Hack Club's Twist YSWS. Feel free to fork and make it weirder!