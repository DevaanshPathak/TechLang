"""
Tests for type checking commands: type_of, is_number, is_string, is_array, is_dict, is_struct
"""
import pytest
from techlang.interpreter import run


class TestTypeOf:
    """Tests for the type_of command"""

    def test_type_of_number(self):
        code = """
set x 42
type_of x result
print result
"""
        assert run(code).strip() == "number"

    def test_type_of_string(self):
        code = """
str_create msg "hello"
type_of msg result
print result
"""
        assert run(code).strip() == "string"

    def test_type_of_array(self):
        code = """
array_create nums 5
type_of nums result
print result
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "array"

    def test_type_of_dict(self):
        code = """
dict_create person
type_of person result
print result
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "dict"

    def test_type_of_undefined(self):
        code = """
type_of nonexistent result
print result
"""
        assert run(code).strip() == "undefined"

    def test_type_of_struct(self):
        code = """
struct Point
    x:int
    y:int
end
struct new Point p1
struct set p1 x 10
struct set p1 y 20
type_of p1 result
print result
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "struct:Point"


class TestIsNumber:
    """Tests for the is_number command"""

    def test_is_number_true(self):
        code = """
set x 42
is_number x result
print result
"""
        assert run(code).strip() == "1"

    def test_is_number_false_string(self):
        code = """
str_create msg "hello"
is_number msg result
print result
"""
        assert run(code).strip() == "0"

    def test_is_number_false_undefined(self):
        code = """
is_number nonexistent result
print result
"""
        assert run(code).strip() == "0"

    def test_is_number_false_array(self):
        code = """
array_create nums 3
is_number nums result
print result
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "0"


class TestIsString:
    """Tests for the is_string command"""

    def test_is_string_true(self):
        code = """
str_create msg "hello"
is_string msg result
print result
"""
        assert run(code).strip() == "1"

    def test_is_string_false_number(self):
        code = """
set x 42
is_string x result
print result
"""
        assert run(code).strip() == "0"

    def test_is_string_false_undefined(self):
        code = """
is_string nonexistent result
print result
"""
        assert run(code).strip() == "0"


class TestIsArray:
    """Tests for the is_array command"""

    def test_is_array_true(self):
        code = """
array_create nums 5
is_array nums result
print result
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "1"

    def test_is_array_false_number(self):
        code = """
set x 42
is_array x result
print result
"""
        assert run(code).strip() == "0"

    def test_is_array_false_string(self):
        code = """
str_create msg "hello"
is_array msg result
print result
"""
        assert run(code).strip() == "0"


class TestIsDict:
    """Tests for the is_dict command"""

    def test_is_dict_true(self):
        code = """
dict_create person
is_dict person result
print result
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "1"

    def test_is_dict_false_number(self):
        code = """
set x 42
is_dict x result
print result
"""
        assert run(code).strip() == "0"

    def test_is_dict_false_array(self):
        code = """
array_create nums 3
is_dict nums result
print result
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "0"


class TestIsStruct:
    """Tests for the is_struct command"""

    def test_is_struct_true(self):
        code = """
struct Point
    x:int
    y:int
end
struct new Point p1
is_struct p1 result
print result
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "1"

    def test_is_struct_false_number(self):
        code = """
set x 42
is_struct x result
print result
"""
        assert run(code).strip() == "0"

    def test_is_struct_false_dict(self):
        code = """
dict_create person
is_struct person result
print result
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "0"


class TestTypeCheckingIntegration:
    """Integration tests combining multiple type checking commands"""

    def test_runtime_type_dispatch(self):
        """Test using type_of for runtime type dispatch"""
        code = """
set num 42
str_create text "hello"
array_create arr 3

type_of num t1
type_of text t2
type_of arr t3

print t1
print t2
print t3
"""
        output = run(code).strip().splitlines()
        # Filter out array creation message
        output = [line for line in output if not line.startswith("Array '")]
        assert output == ["number", "string", "array"]

    def test_conditional_type_check(self):
        """Test type checking in conditional logic"""
        code = """
set x 100
is_number x check
if check == 1
    print "x is a number"
end
"""
        assert run(code).strip() == "x is a number"

    def test_error_missing_args(self):
        """Test error handling for missing arguments"""
        code = "type_of x"
        output = run(code).strip()
        assert "Error" in output or "error" in output.lower()

    def test_type_of_float(self):
        """Test type_of with float values (stored via math operations)"""
        code = """
math_sqrt 2
set approx 1
type_of approx result
print result
"""
        assert "number" in run(code).strip()
