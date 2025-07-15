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
