# tests/test_interpreter.py

from techlang.interpreter import run
import os
from typing import List

# ---------------------------
# Basic Commands
# ---------------------------
def test_print_value():
    code = "boot ping ping print"
    assert run(code).strip() == "2"

def test_stack_usage():
    code = "boot ping upload ping print download print debug"
    output = run(code).strip().splitlines()
    assert output == ["2", "1", "Stack: []", "Vars: {}"]

def test_hack_command():
    code = "boot ping ping hack print"
    assert run(code).strip() == "4"

def test_unknown_command():
    code = "boot xyz print"
    output = run(code).strip().splitlines()
    assert "[Error: Unknown command 'xyz']" in output

# ---------------------------
# Variable Operations
# ---------------------------
def test_variable_set_and_add():
    code = "set x 5 add x 3 print x debug"
    output = run(code).strip().splitlines()
    assert output[0] == "8"
    assert output[1] == "Stack: []"
    assert output[2] == "Vars: {'x': 8}"

def test_math_commands():
    code = '''
    set x 10
    add x 5
    mul x 2
    sub x 3
    div x 4
    print x
    '''
    assert run(code).strip() == "6"

# ---------------------------
# Flow Control
# ---------------------------
def test_looping():
    code = "set x 3 loop x ping print end"
    output = run(code).strip().splitlines()
    assert output == ["1", "2", "3"]

def test_if_condition():
    code = "set x 2 if x > 1 ping print end"
    output = run(code).strip().splitlines()
    assert output == ["1"]

def test_function_call():
    code = """
    def hello
        ping ping print
    end

    call hello
    """
    output = run(code).strip().splitlines()
    assert output == ["2"]

# ---------------------------
# Input / Output
# ---------------------------
def test_input_output():
    result = run("input user print user", inputs=["Alice"])
    assert result.strip() == "Alice"

# ---------------------------
# Aliases
# ---------------------------
def test_alias():
    code = """
    alias start boot
    alias inc ping
    start
    inc inc print
    """
    assert run(code).strip().splitlines() == ["2"]

def test_alias_expansion():
    code = """
    alias start boot
    alias inc ping
    start
    inc inc print
    """
    output = run(code).strip().splitlines()
    assert output == ["2"]

# ---------------------------
# Edge Cases / Advanced Tests
# ---------------------------
def test_large_input():
    # 10,000 pings
    code = "ping " * 10000 + "print"
    output = run(code).strip()
    assert output == "10000"

def test_nested_loops_and_conditions():
    code = """
    set x 2
    loop x
        if x > 0
            ping
        end
    end
    print
    """
    output = run(code).strip().splitlines()
    assert output[-1] == "2"

def test_div_by_zero():
    code = "set x 5 div x 0 print"
    output = run(code).strip().splitlines()
    assert any("Division by zero" in line or "Error" in line for line in output)
