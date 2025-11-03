"""
Tests for the export/public API system in TechLang.
This enables library authors to control which functions are public.
"""

from pathlib import Path
from techlang.interpreter import run


def write_module(base_dir: str, module_name: str, code: str):
    """Helper to write a module file."""
    module_path = Path(base_dir) / f"{module_name}.tl"
    module_path.write_text(code)


def test_export_marks_function_as_public(tmp_path):
    """Test that export command marks a function as exported."""
    code = """
def my_function
    print "hello"
end
export my_function
"""
    output = run(code, base_dir=str(tmp_path))
    assert "[Error:" not in output


def test_export_before_definition_allowed(tmp_path):
    """Test that export can be called before function definition."""
    code = """
export my_function
def my_function
    print "hello"
end
"""
    output = run(code, base_dir=str(tmp_path))
    # Should not produce an error - export before def is allowed
    assert "[Error:" not in output


def test_exported_function_callable_from_module(tmp_path):
    """Test that exported functions can be called from other modules."""
    module_code = """
def greet
    print "Hello from module"
end
export greet
"""
    write_module(str(tmp_path), "mylib", module_code)
    
    program = """
package use mylib
call mylib.greet
"""
    output = run(program, base_dir=str(tmp_path)).strip()
    assert "Hello from module" in output


def test_private_function_not_callable_from_module(tmp_path):
    """Test that non-exported functions cannot be called from outside."""
    module_code = """
def public_func
    print "public"
end

def private_func
    print "private"
end

export public_func
"""
    write_module(str(tmp_path), "mylib", module_code)
    
    program = """
package use mylib
call mylib.private_func
"""
    output = run(program, base_dir=str(tmp_path))
    assert "Function 'private_func' in module 'mylib' is private" in output


def test_exported_function_with_parameters(tmp_path):
    """Test that exported functions work with parameters."""
    module_code = """
def double x
    mul x 2
    return x
end
export double
"""
    write_module(str(tmp_path), "math_utils", module_code)
    
    program = """
package use math_utils
set num 5
call math_utils.double num result
print result
"""
    output = run(program, base_dir=str(tmp_path)).strip()
    assert "10" in output


def test_multiple_exports(tmp_path):
    """Test exporting multiple functions."""
    module_code = """
def add a b
    add a b
    return a
end

def sub a b
    sub a b
    return a
end

def helper
    print "internal helper"
end

export add
export sub
"""
    write_module(str(tmp_path), "calc", module_code)
    
    program = """
package use calc
set x 10
set y 3
call calc.add x y sum
call calc.sub x y diff
print sum
print diff
"""
    output = run(program, base_dir=str(tmp_path)).strip().splitlines()
    assert "13" in output
    assert "7" in output


def test_private_helper_functions(tmp_path):
    """Test that private helper functions work within the module."""
    module_code = """
def private_helper
    set result 42
    return result
end

def public_api
    call private_helper value
    return value
end

export public_api
"""
    write_module(str(tmp_path), "mylib", module_code)
    
    program = """
package use mylib
call mylib.public_api answer
print answer
"""
    output = run(program, base_dir=str(tmp_path)).strip()
    assert "42" in output


def test_calling_private_helper_from_outside_fails(tmp_path):
    """Test that private helpers cannot be called from outside."""
    module_code = """
def private_helper
    print "helper"
end

def public_api
    call private_helper
end

export public_api
"""
    write_module(str(tmp_path), "mylib", module_code)
    
    program = """
package use mylib
call mylib.private_helper
"""
    output = run(program, base_dir=str(tmp_path))
    assert "private" in output.lower()


def test_export_with_string_parameters(tmp_path):
    """Test exported functions with string parameters."""
    module_code = """
def make_greeting name
    str_create msg "Hello, "
    str_concat msg name
    return msg
end
export make_greeting
"""
    write_module(str(tmp_path), "greetings", module_code)
    
    program = """
package use greetings
str_create username "Alice"
call greetings.make_greeting username greeting
print greeting
"""
    output = run(program, base_dir=str(tmp_path)).strip()
    assert "Hello, Alice" in output


def test_export_order_independent(tmp_path):
    """Test that export can come before or after function definition."""
    module_code = """
export func1

def func1
    print "function 1"
end

def func2
    print "function 2"
end

export func2
"""
    write_module(str(tmp_path), "mylib", module_code)
    
    program = """
package use mylib
call mylib.func1
call mylib.func2
"""
    output = run(program, base_dir=str(tmp_path)).strip()
    assert "function 1" in output
    assert "function 2" in output


def test_module_without_exports_all_private(tmp_path):
    """Test that without export, all functions are private."""
    module_code = """
def func1
    print "func1"
end

def func2
    print "func2"
end
"""
    write_module(str(tmp_path), "mylib", module_code)
    
    program = """
package use mylib
call mylib.func1
"""
    output = run(program, base_dir=str(tmp_path))
    assert "private" in output.lower()


def test_export_with_multiple_return_values(tmp_path):
    """Test exported functions with multiple return values."""
    module_code = """
def swap a b
    return b a
end
export swap
"""
    write_module(str(tmp_path), "utils", module_code)
    
    program = """
package use utils
set x 10
set y 20
call utils.swap x y first second
print first
print second
"""
    output = run(program, base_dir=str(tmp_path)).strip().splitlines()
    assert "20" in output
    assert "10" in output


def test_complex_library_with_public_private_api(tmp_path):
    """Test a realistic library with mixed public/private functions."""
    module_code = """
def validate_input x
    if x lt 0
        set x 0
    end
    return x
end

def square x
    call validate_input x cleaned
    mul cleaned cleaned
    return cleaned
end

def cube x
    call validate_input x validated
    mul validated validated
    mul validated x
    return validated
end

export square
export cube
"""
    write_module(str(tmp_path), "geometry", module_code)
    
    program = """
package use geometry
set n 3
call geometry.square n sq
call geometry.cube n cb
print sq
print cb
"""
    output = run(program, base_dir=str(tmp_path)).strip().splitlines()
    assert "9" in output
    assert "27" in output
    
    # Try to call private validate_input
    program2 = """
package use geometry
set n 5
call geometry.validate_input n result
"""
    output2 = run(program2, base_dir=str(tmp_path))
    assert "private" in output2.lower()
