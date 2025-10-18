# Control Flow in TechLang

TechLang evaluates commands from left to right. Any construct that introduces a block (`if`, `loop`, `while`, `def`, `match`, `try`, `macro`, …) is terminated with a literal `end` token. Blocks may be nested freely.

## Conditionals

Use `if` with a comparison operator. When the condition is true the nested block runs; otherwise it is skipped.

```techlang
set score 75
if score >= 60
    print "pass"
end

if score < 60
    print "retake"
end
```

Comparisons support `==`, `!=`, `<`, `<=`, `>` and `>=`. The right-hand side accepts integers or existing variables.

## Loops

`loop <count>` repeats its body a fixed number of times. The count can be either a literal integer or a variable that currently holds an integer.

```techlang
set i 0
loop 3
    add i 1
end
print i    # 3
```

For open-ended loops use `while <var> <op> <value>`; the condition is evaluated before every iteration. A safety guard aborts the loop after 1000 iterations to prevent runaway programs.

```techlang
set countdown 3
while countdown > 0
    print countdown
    sub countdown 1
end
```

### Scheduler-friendly pacing

Tight loops can starve other interpreters or threads. Use `sleep <milliseconds>` to add an explicit pause, or `yield` to hand control back to the scheduler without a fixed delay. These commands block the current interpreter, so tests typically mock the timer to avoid slow runs.

```techlang
set ticks 3
loop ticks
    print "tick"
    sleep 50   # wait 50 ms before the next iteration
end

loop ticks
    print "cooperate"
    yield      # no delay, but gives other workers a chance to run
end
```

## Pattern Matching

`match` lets you express guarded branches without chaining several `if` statements. The selector may be a number, string, or variable. Each `case` line can specify an operator, and `case default` handles the fallback.

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

## Functions

`def <name> ... end` stores the raw token list for later reuse. Call a function with `call <name>`. Functions capture the state in which they were defined, so they are safe to invoke from threads and modules.

```techlang
def greet
    print "hello"
end
call greet
```

## Try / Catch

Errors surface as lines starting with `[Error:`. A `try ... catch` block suppresses the first error emitted inside the `try` region and executes the `catch` block instead. Provide one or two identifiers after `catch` to capture the message (without the prefix) and an optional stack snapshot.

```techlang
try
    div numerator denominator
catch errMsg stackDump
    print errMsg
    print stackDump
end
```

If you omit the identifiers the catch block is still executed when an error appears, but nothing is bound.

## Compile-time Macros

Macros expand before the interpreter executes any code. Define a macro with `macro <name> [params...] do ... end` and reference parameters inside the body using `$param`. Invoke the macro with `inline <name> <args...>`; the expanded tokens are spliced into the call site.

```techlang
macro print_twice message do
    print $message
    print $message
end

macro inc target do
    add $target 1
end

set counter 0
inline inc counter
inline print_twice "done"
```

Macros may call other macros; recursion is rejected to prevent infinite expansion loops. Macro bodies can also declare aliases or functions, which are processed after macro expansion just like handwritten code.

---

See the [Examples Index](examples.md) for runnable snippets.