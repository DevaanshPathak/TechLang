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

## Match Blocks

Use `match` to replace deeply nested `if`/`switch` chains with guard-style branches. The TechLang syntax is line-based and terminates with `end`:

```techlang
set temperature 68
match temperature
    case < 32
        print "freezing"
    case >= 80
        print "hot"
    case default
        print "mild"
end
```

Each `case` may specify an operator (`==`, `!=`, `<`, `<=`, `>`, `>=`). If you omit the operator the comparison defaults to equality. Strings can be matched with quoted literals:

```techlang
str_create status "ok"
match status
    case "error"
        print "bad"
    case == "ok"
        print "good"
    case default
        print "unknown"
end
```

## Enhanced try/catch

`try ... catch` still watches for output lines that begin with `[Error:`. You can now capture the error message (without the prefix) and optionally a snapshot of the operand stack:

```techlang
try
    div a b
catch errMsg stackSnapshot
    print errMsg           # e.g. Cannot divide by zero...
    print stackSnapshot    # stringified stack contents
end
```

If no variable names follow `catch`, it behaves as before.

---

See the [Examples Index](examples.md) for runnable