# System & Processes in TechLang

TechLang provides commands for interacting with the operating system, running processes, and accessing environment information.

## Running System Commands

Execute a shell command and capture its output:

```techlang
let result = system("echo Hello, world!")
print(result)
```

## Working with Processes

Start a process and interact with it:

```techlang
let proc = process("python", ["script.py"])
let output = proc.read()
print(output)
proc.close()
```

## Environment Variables

Get and set environment variables:

```techlang
let path = getenv("PATH")
setenv("MY_VAR", "value")
```

## File System Operations

List files in a directory:

```techlang
let files = listdir(".")
for f in files {
    print(f)
}
```

Get the current working directory:

```techlang
let cwd = getcwd()
print(cwd)
```

---

See the [Examples Index](examples.md)