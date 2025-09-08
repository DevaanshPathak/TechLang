# Control Flow in TechLang

Control flow statements determine the order in which instructions are executed in a TechLang program. TechLang supports several control flow constructs, including conditional statements, loops, and branching.

## Conditional Statements

Use `if`, `else if`, and `else` to execute code based on conditions:

```techlang
if x > 0 {
    print("Positive")
} else if x == 0 {
    print("Zero")
} else {
    print("Negative")
}
```

## Loops

### While Loop

Repeat a block of code while a condition is true:

```techlang
while count < 10 {
    print(count)
    count = count + 1
}
```

### For Loop

Iterate over a range or collection:

```techlang
for i in 1..5 {
    print(i)
}
```

## Branching

Use `break` to exit a loop early, and `continue` to skip to the next iteration:

```techlang
for i in 1..10 {
    if i == 5 {
        break
    }
    if i % 2 == 0 {
        continue
    }
    print(i)
}
```

## Match Statement

Pattern matching for concise branching:

```techlang
match value {
    1 => print("One"),
    2 => print("Two"),
    _ => print("Other")
}
```

---

See the [Examples Index](examples.md) for runnable