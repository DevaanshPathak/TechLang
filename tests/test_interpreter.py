from techlang.interpreter import run

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
    assert "[unknown command: xyz]" in output

def test_variable_set_and_add():
    code = "set x 5 add x 3 print x debug"
    output = run(code).strip().splitlines()
    assert output[0] == "8"
    assert output[1] == "Stack: []"
    assert output[2] == "Vars: {'x': 8}"

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

def test_input_output():
    result = run("input user print user", inputs=["Alice"])
    assert result.strip() == "Alice"

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
    from techlang.interpreter import run
    output = run(code).strip().splitlines()
    assert output == ["2"]

import os
from techlang.interpreter import run

def test_import_file(tmp_path):
    # Create a temporary utils.tl file
    utils_file = tmp_path / "utils.tl"
    utils_file.write_text("ping\nping\nprint")

    # Create main code that imports it
    code = f"""
    import {utils_file.name}
    ping
    print
    """

    # Change working directory to temp so import works
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        result = run(code).strip().splitlines()
        assert result == ["2", "3"]
    finally:
        os.chdir(old_cwd)

from techlang.interpreter import run

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