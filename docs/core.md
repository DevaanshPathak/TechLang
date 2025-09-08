# Core Commands

| Command | Syntax | Description | Example |
|--------|--------|-------------|---------|
| boot | `boot` | Reset current value to 0 | `boot print  # 0` |
| ping | `ping` | Increment current value by 1 | `boot ping print  # 1` |
| crash | `crash` | Decrement current value by 1 | `boot crash print  # -1` |
| print | `print [arg]` | Print current value, variable, or quoted text | `print "Hello"` → Hello |
| set | `set <var> <int>` | Assign integer to variable | `set x 5` |
| add | `add <var> <int|var>` | Add to variable (integer) | `set x 10 add x 5` |
| sub | `sub <var> <int|var>` | Subtract from variable | `set x 10 sub x 3` |
| mul | `mul <var> <int|var>` | Multiply variable | `set x 4 mul x 6` |
| div | `div <var> <int|var>` | Integer divide (safe error on 0) | `set x 8 div x 2` |
| input | `input <var>` | Read next input into var | `(inputs=[Alice]) input name` |
| upload | `upload` | Push current value to stack |  |
| download | `download` | Pop stack to current value |  |
| debug | `debug` | Print stack/vars/datatypes |  |
| alias | `alias <short> <command>` | Create shorthand | `alias inc ping` |
| import | `import <name>` | Load `name.tl` (once) | `import math_utils` |

## Notes
- `div` uses integer division.
- `print` without argument prints the running `value`.

## Quick Examples
```tl
boot ping ping print   # 2
set score 10 add score 7 print score   # 17
alias inc ping  inc inc print          # 2
```