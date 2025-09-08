# Help & CLI in TechLang

TechLang includes a command-line interface (CLI) for running scripts, exploring code interactively, and accessing documentation.

## Running Scripts

Execute a TechLang script file:

```sh
tl path/to/script.tl
```

## Interactive REPL

Start an interactive Read-Eval-Print Loop (REPL) session:

```sh
tl -i
```

Type commands and see results immediately.

## Getting Help

Display built-in help:

```sh
tl --help
```

Show version information:

```sh
tl --version
```

## Command-Line Arguments

Pass arguments to your script:

```sh
tl myscript.tl arg1 arg2
```

Access them in your code:

```techlang
for arg in args {
    print(arg)
}
```

## Script Exit Codes

Set the exit code for your script:

```techlang
exit(0)   // Success
exit(1)   // Error
```

---

See the [Examples Index](examples.md) for more code samples.