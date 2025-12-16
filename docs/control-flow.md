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

Comparisons support `==`, `!=`, `<`, `<=`, `>` and `>=`.

For convenience (and for compatibility with some examples), these operator aliases are also accepted:

- `eq/ne/gt/lt/ge/le` map to `==/!=/>/</>=/<=`.

The right-hand side accepts integers or existing variables. Equality/inequality also works with string operands (for example comparing two string variables).

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

`def <name> [param1 param2 ...] ... end` stores the function body for later reuse. Functions can accept parameters and return multiple values. Call a function with `call <name> [args...] [returnVar1 returnVar2 ...]`.

### Basic Functions

```techlang
def greet
    print "hello"
end
call greet
```

### Functions with Parameters

Parameters are passed by position and create local variables within the function scope:

```techlang
def double x
    mul x 2
    return x
end

set num 5
call double num result
print result  # prints 10
```

Parameters can be numeric or string variables:

```techlang
def make_greeting name
    str_create msg "Hello "
    str_concat msg name
    return msg
end

str_create username "Alice"
call make_greeting username greeting
print greeting  # prints "Hello Alice"
```

### Multiple Return Values

Functions can return multiple values using the `return` keyword:

```techlang
def swap a b
    return b a
end

set x 10
set y 20
call swap x y first second
print first  # prints 20
print second  # prints 10
```

### Local Scope

Parameters are local to the function and don't affect global variables with the same name:

```techlang
set global 100
def modify x
    set x 999
    return x
end
call modify global local
print local  # prints 999
print global  # still prints 100
```

### Literal Arguments

You can pass literal values directly to functions:

```techlang
def square n
    mul n n
    return n
end

call square 7 result
print result  # prints 49
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

## Interactive REPL

The TechLang REPL (`tl -i`) provides an enhanced interactive environment with several productivity features:

### Command History

History is automatically persisted to `~/.techlang_history` and restored on startup. Use the arrow keys to navigate through previous commands (up to 1000 entries). History is saved when you exit the REPL.

```bash
$ tl -i
TechLang REPL. Type 'exit' or Ctrl-D to quit. Type ':help' for meta-commands.
tl> set x 5
tl> print x
5
tl> # Press up arrow to recall "print x"
```

### Auto-indentation

The REPL tracks block depth and automatically indents continuation lines, making multi-line blocks easier to write:

```techlang
tl> def greet
...     set msg "hello"
...     print msg
... end
```

Indentation uses 4 spaces per nesting level. Block keywords include: `def`, `if`, `loop`, `while`, `switch`, `match`, `try`, `macro`, and `struct` (except `struct new/set/get/dump`).

### Meta-commands

Meta-commands start with `:` and provide REPL-specific functionality:

| Command | Description |
|---------|-------------|
| `:load <file.tl>` | Load and execute a TechLang file without exiting the REPL |
| `:help` | Show available meta-commands |
| `:clear` | Clear the current input buffer (useful if you're stuck in a block) |
| `:history` | Display the last 20 commands from history |
| `exit` or `quit` | Exit the REPL (Ctrl-D also works) |

**Example usage:**

```techlang
tl> :load examples/hello.tl
[Loading examples/hello.tl...]
Hello, TechLang!

tl> :clear
[Buffer cleared]

tl> :history
   1  set x 5
   2  print x
   3  def greet
   4  :load examples/hello.tl

tl> :help
TechLang REPL Meta-Commands:
  :load <file.tl>   Load and execute a TechLang file
  :help             Show this help message
  :clear            Clear the current buffer
  :history          Show command history
  exit / quit       Exit the REPL (or Ctrl-D)
```

**Loading files:**

The `:load` command is particularly useful for testing and iterating on `.tl` files:

```techlang
tl> :load mymodule.tl
[Loading mymodule.tl...]
# Module executes, functions/aliases become available

tl> call my_function
# Use functions defined in the loaded file
```

The `.tl` extension is optional—`:load hello` will load `hello.tl` automatically.

### Block Detection

The REPL executes code immediately when the block depth returns to zero. For single-line commands without blocks, execution happens right away. For multi-line blocks, the REPL waits for the matching `end` token:

```techlang
tl> ping print
1
tl> loop 3
...     ping print
... end
1
2
3
```

If you get stuck in a block (forgot an `end`), use `:clear` to reset the buffer.

---

See the [Examples Index](examples.md) for runnable snippets.