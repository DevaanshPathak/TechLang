"""
Tests for Static Typing / Type Hints

Tests the typed_def, typecheck, and type_assert commands.
"""

import pytest
from techlang.interpreter import run


class TestTypedDef:
    """Test typed_def command."""
    
    def test_typed_def_basic(self):
        """Test basic typed function definition"""
        code = """
        typed_def add a:int b:int -> int do
            set result a
            add result b
            return result
        end
        call add 3 5
        print result
        """
        # Should define and potentially call the function
        lines = run(code).strip().splitlines()
        # Function should be defined without error
        assert not any("[Error:" in line for line in lines)
    
    def test_typed_def_string_param(self):
        """Test typed function with string parameter"""
        code = """
        typed_def greet name:str -> str do
            str_create greeting "Hello, "
            str_concat greeting name greeting
            return greeting
        end
        """
        output = run(code).strip()
        assert "[Error:" not in output
    
    def test_typed_def_no_return_type(self):
        """Test typed function without explicit return type"""
        code = """
        typed_def print_num n:int -> none do
            print n
        end
        """
        output = run(code).strip()
        assert "[Error:" not in output


class TestTypecheck:
    """Test typecheck command."""
    
    def test_typecheck_on(self):
        """Test enabling type checking"""
        code = """
        typecheck on
        """
        output = run(code).strip()
        assert "enabled" in output.lower() or "[Error:" not in output
    
    def test_typecheck_off(self):
        """Test disabling type checking"""
        code = """
        typecheck off
        """
        output = run(code).strip()
        assert "disabled" in output.lower() or "[Error:" not in output
    
    def test_typecheck_invalid_mode(self):
        """Test typecheck with invalid mode"""
        code = """
        typecheck maybe
        """
        output = run(code).strip()
        assert "[Error:" in output
    
    def test_typecheck_missing_args(self):
        """Test typecheck with missing arguments"""
        code = """
        typecheck
        """
        output = run(code).strip()
        assert "[Error:" in output or "requires" in output.lower()


class TestTypeAssert:
    """Test type_assert command."""
    
    def test_type_assert_int_pass(self):
        """Test type_assert passes for correct int type"""
        code = """
        set x 42
        type_assert x int
        print "passed"
        """
        output = run(code).strip()
        assert "passed" in output
    
    def test_type_assert_str_pass(self):
        """Test type_assert passes for correct str type"""
        code = """
        str_create msg "hello"
        type_assert msg str
        print "passed"
        """
        output = run(code).strip()
        assert "passed" in output
    
    def test_type_assert_array_pass(self):
        """Test type_assert passes for correct array type"""
        code = """
        array_create nums
        type_assert nums array
        print "passed"
        """
        output = run(code).strip()
        assert "passed" in output
    
    def test_type_assert_int_fail(self):
        """Test type_assert fails for wrong type"""
        code = """
        str_create msg "hello"
        type_assert msg int
        print "should not reach"
        """
        output = run(code).strip()
        assert "[Error:" in output or "failed" in output.lower()
    
    def test_type_assert_any_always_passes(self):
        """Test type_assert with 'any' type always passes"""
        code = """
        set x 42
        type_assert x any
        str_create msg "hello"
        type_assert msg any
        array_create arr
        type_assert arr any
        print "all passed"
        """
        output = run(code).strip()
        assert "all passed" in output
    
    def test_type_assert_missing_args(self):
        """Test type_assert with missing arguments"""
        code = """
        type_assert x
        """
        output = run(code).strip()
        assert "[Error:" in output or "requires" in output.lower()


class TestTypeOf:
    """Test type_of command (enhanced)."""
    
    def test_type_of_int(self):
        """Test type_of for integer"""
        code = """
        set x 42
        type_of x t
        print t
        """
        lines = run(code).strip().splitlines()
        # The existing type_of uses "number" for int
        assert lines[-1] in ("int", "number")
    
    def test_type_of_string(self):
        """Test type_of for string"""
        code = """
        str_create msg "hello"
        type_of msg t
        print t
        """
        lines = run(code).strip().splitlines()
        # The existing type_of uses "string" for str
        assert lines[-1] in ("str", "string")
    
    def test_type_of_array(self):
        """Test type_of for array"""
        code = """
        array_create nums
        type_of nums t
        print t
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "array"
    
    def test_type_of_dict(self):
        """Test type_of for dictionary"""
        code = """
        dict_create d
        type_of d t
        print t
        """
        lines = run(code).strip().splitlines()
        # Output may include dict_create message
        assert "dict" in lines[-1].lower()
