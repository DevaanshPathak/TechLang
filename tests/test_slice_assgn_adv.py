"""
Tests for Feature 8: Slice Assignment & Advanced Slicing
- array_slice_step, array_set_slice, str_slice, str_slice_step
"""
import pytest
from techlang.interpreter import run


class TestArraySliceStep:
    """Array slice with step"""

    def test_array_slice_step_basic(self):
        code = """
range 10 nums
array_slice_step nums 0 10 2 evens
array_get evens 0 first
array_get evens 1 second
print first
print second
"""
        output = run(code).strip().splitlines()
        assert output[-2:] == ["0", "2"]

    def test_array_slice_step_odd_indices(self):
        code = """
range 10 nums
array_slice_step nums 1 10 2 odds
array_get odds 0 first
array_get odds 1 second
print first
print second
"""
        output = run(code).strip().splitlines()
        assert output[-2:] == ["1", "3"]

    def test_array_slice_step_large_step(self):
        code = """
range 20 nums
array_slice_step nums 0 20 5 result
array_get result 0 a
array_get result 1 b
print a
print b
"""
        output = run(code).strip().splitlines()
        assert output[-2:] == ["0", "5"]


class TestArraySetSlice:
    """Replace slice with values"""

    def test_array_set_slice_basic(self):
        code = """
range 5 nums
array_create repl 2
array_set repl 0 99
array_set repl 1 88
array_set_slice nums 1 3 repl
array_get nums 1 val1
array_get nums 2 val2
print val1
print val2
"""
        output = run(code).strip().splitlines()
        assert output[-2:] == ["99", "88"]

    def test_array_set_slice_at_start(self):
        code = """
range 5 nums
array_create repl 2
array_set repl 0 100
array_set repl 1 200
array_set_slice nums 0 2 repl
array_get nums 0 val
print val
"""
        assert run(code).strip().splitlines()[-1] == "100"


class TestStrSlice:
    """String slicing"""

    def test_str_slice_basic(self):
        code = """
str_create msg "Hello, World!"
str_slice msg 0 5 result
print result
"""
        assert run(code).strip() == "Hello"

    def test_str_slice_middle(self):
        code = """
str_create msg "Hello, World!"
str_slice msg 7 12 result
print result
"""
        assert run(code).strip() == "World"

    def test_str_slice_negative(self):
        code = """
str_create msg "Hello, World!"
str_slice msg -6 -1 result
print result
"""
        assert run(code).strip() == "World"


class TestStrSliceStep:
    """String slice with step"""

    def test_str_slice_step_basic(self):
        code = """
str_create msg "abcdefgh"
str_slice_step msg 0 8 2 result
print result
"""
        assert run(code).strip() == "aceg"

    def test_str_slice_step_reverse(self):
        code = """
str_create msg "abcdef"
str_slice_step msg 0 6 3 result
print result
"""
        assert run(code).strip() == "ad"


class TestSlicingIntegration:
    """Integration tests for slicing"""

    def test_slice_and_format(self):
        code = """
range 10 nums
array_slice_step nums 0 10 2 evens
array_get evens 2 val
format_num val "03d" result
print result
"""
        assert run(code).strip().splitlines()[-1] == "004"
