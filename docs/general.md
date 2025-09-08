# General Rules & Syntax

| Topic | Details |
|------|---------|
| Case | Commands are lowercase; variables are case-sensitive |
| Lines | One command per line |
| Strings | Double quotes only: `"text"` |
| Blocks | Begin with a keyword (`loop`, `if`, `def`, `while`, `switch`, `try`) and end with `end` |
| Errors | Printed as `[Error: message]` (non-fatal) |
| Inputs | `input <var>` reads queued inputs (CLI/tests) |

## Quick Examples
```tl
boot ping ping print   # 2
print "Hello"         # Hello
set x 5 add x 3 print x  # 8
```