"""
Tests for function parameters and return values in TechLang.
These features allow functions to accept inputs and return outputs,
making TechLang capable of building real libraries.
"""

from techlang.interpreter import run


def test_function_with_single_parameter():
    """Test basic function with one parameter."""
    code = """
def double x
    mul x 2
    return x
end

set num 5
call double num result
print result
"""
    output = run(code).strip()
    assert output == "10"


def test_function_with_multiple_parameters():
    """Test function with multiple parameters."""
    code = """
def add_three a b c
    add a b
    add a c
    return a
end

set x 1
set y 2
set z 3
call add_three x y z sum
print sum
"""
    output = run(code).strip()
    assert output == "6"


def test_function_with_no_parameters():
    """Test function with no parameters (backward compatibility)."""
    code = """
def get_magic
    set magic 42
    return magic
end

call get_magic result
print result
"""
    output = run(code).strip()
    assert output == "42"


def test_function_returns_multiple_values():
    """Test function returning multiple values."""
    code = """
def divide_with_remainder a b
    div a b
    return a b
end

set x 10
set y 3
call divide_with_remainder x y q r
print q
print r
"""
    output = run(code).strip().splitlines()
    assert output == ["3", "3"]


def test_function_returns_string():
    """Test function returning string value."""
    code = """
def greet name
    str_create msg "Hello"
    return msg
end

str_create username "Alice"
call greet username greeting
print greeting
"""
    output = run(code).strip()
    assert output == "Hello"


def test_function_with_string_parameter():
    """Test passing string as parameter."""
    code = """
def process_string text
    str_upper text
    return text
end

str_create mytext "hello"
call process_string mytext output
print output
"""
    output = run(code).strip()
    assert output == "HELLO"


def test_function_parameters_are_local():
    """Test that function parameters don't leak outside."""
    code = """
set x 100

def modify_local x
    set x 50
    return x
end

set y 10
call modify_local y result
print result
print x
"""
    output = run(code).strip().splitlines()
    assert output == ["50", "100"]


def test_function_with_literal_arguments():
    """Test passing literal values as arguments."""
    code = """
def add a b
    add a b
    return a
end

call add 5 10 result
print result
"""
    output = run(code).strip()
    assert output == "15"


def test_function_return_without_value():
    """Test return with no values."""
    code = """
def do_nothing
    set x 5
    return
end

call do_nothing
print "done"
"""
    output = run(code).strip()
    assert output == "done"


def test_nested_function_calls_with_params():
    """Test calling functions from within functions."""
    code = """
def inner x
    mul x 2
    return x
end

def outer y
    call inner y temp
    add temp 1
    return temp
end

set num 5
call outer num result
print result
"""
    output = run(code).strip()
    assert output == "11"


def test_function_modifies_and_returns_parameter():
    """Test modifying parameter and returning it."""
    code = """
def increment x
    add x 1
    return x
end

set value 10
call increment value result
print result
print value
"""
    output = run(code).strip().splitlines()
    # Result should be 11, original value should be unchanged (10)
    assert output == ["11", "10"]


def test_function_with_too_few_arguments():
    """Test error handling when not enough arguments provided."""
    code = """
def needs_two a b
    add a b
    return a
end

set x 5
call needs_two x
"""
    output = run(code).strip()
    assert "[Error:" in output and "expects 2 arguments" in output


def test_function_return_multiple_capture_partial():
    """Test capturing only some of multiple return values."""
    code = """
def get_pair
    return 10 20
end

call get_pair first
print first
"""
    output = run(code).strip()
    assert output == "10"


def test_function_chain_return_values():
    """Test using return value as argument to another function."""
    code = """
def double x
    mul x 2
    return x
end

def triple x
    mul x 3
    return x
end

set n 5
call double n temp
call triple temp result
print result
"""
    output = run(code).strip()
    assert output == "30"


def test_backward_compatibility_old_function_format():
    """Test that old functions without parameters still work."""
    code = """
def old_style
    set x 100
    print x
end

call old_style
"""
    output = run(code).strip()
    assert output == "100"


def test_function_parameter_shadows_global():
    """Test that parameters shadow global variables during execution."""
    code = """
set x 999

def use_param x
    print x
    return x
end

call use_param 42 result
print x
print result
"""
    output = run(code).strip().splitlines()
    assert output == ["42", "999", "42"]


def test_function_with_arithmetic_in_body():
    """Test complex arithmetic operations with parameters."""
    code = """
def calculate a b c
    mul a 2
    add a b
    sub a c
    return a
end

call calculate 5 3 2 result
print result
"""
    output = run(code).strip()
    # (5 * 2) + 3 - 2 = 10 + 3 - 2 = 11
    assert output == "11"


def test_return_with_mixed_types():
    """Test returning both numbers and strings."""
    code = """
def get_pair
    return 42 "answer"
end

call get_pair num label
print num
print label
"""
    output = run(code).strip().splitlines()
    assert output == ["42", "answer"]


def test_function_empty_return_values():
    """Test accessing return variables when function returns nothing."""
    code = """
def returns_nothing
    set x 5
end

call returns_nothing result
print result
"""
    output = run(code).strip()
    assert output == "0"  # Should default to 0
