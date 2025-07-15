from techlang.interpreter import run

def test_print_value():
    code = "boot ping ping print"
    assert run(code).strip() == "2"

def test_stack_usage():
    code = "boot ping upload ping print download print debug"
    output = run(code).strip().splitlines()
    assert output == ["2", "1", "Stack: [1]"]

def test_hack_command():
    code = "boot ping ping hack print"
    assert run(code).strip() == "4"

def test_unknown_command():
    code = "boot xyz print"
    output = run(code).strip().splitlines()
    assert "[unknown command: xyz]" in output
