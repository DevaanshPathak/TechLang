"""
Tests for Feature 9: Unpacking & Destructuring
- unpack, unpack_rest, dict_unpack, swap
"""
import pytest
from techlang.interpreter import run


class TestUnpack:
    """Unpack array to variables"""

    def test_unpack_simple(self):
        code = """
array_create coords 3
array_set coords 0 10
array_set coords 1 20
array_set coords 2 30
unpack coords x y z
print x
print y
print z
"""
        output = run(code).strip().splitlines()
        assert output[-3:] == ["10", "20", "30"]

    def test_unpack_two_values(self):
        code = """
array_create pair 2
array_set pair 0 100
array_set pair 1 200
unpack pair a b
print a
print b
"""
        output = run(code).strip().splitlines()
        assert output[-2:] == ["100", "200"]


class TestUnpackRest:
    """Unpack with rest operator"""

    def test_unpack_rest_basic(self):
        code = """
range 5 nums
unpack_rest nums first *middle last
print first
print last
array_get middle 0 m0
print m0
"""
        output = run(code).strip().splitlines()
        assert output == ["0", "4", "1"]

    def test_unpack_rest_first_only(self):
        code = """
range 3 nums
unpack_rest nums head *tail
print head
"""
        assert run(code).strip().splitlines()[-1] == "0"


class TestDictUnpack:
    """Unpack dictionary to variables"""

    def test_dict_unpack_basic(self):
        code = """
dict_create person
dict_set person "name" "Alice"
dict_set person "age" 30
dict_unpack person "name" name "age" age
print name
print age
"""
        output = run(code).strip().splitlines()
        assert output[-2:] == ["Alice", "30"]

    def test_dict_unpack_single_key(self):
        code = """
dict_create data
dict_set data "value" 42
dict_unpack data "value" v
print v
"""
        assert run(code).strip().splitlines()[-1] == "42"


class TestSwap:
    """Swap two variables"""

    def test_swap_numbers(self):
        code = """
set a 10
set b 20
swap a b
print a
print b
"""
        output = run(code).strip().splitlines()
        assert output == ["20", "10"]

    def test_swap_strings(self):
        code = """
str_create a "hello"
str_create b "world"
swap a b
print a
print b
"""
        output = run(code).strip().splitlines()
        assert output == ["world", "hello"]

    def test_swap_same_value(self):
        code = """
set a 5
set b 5
swap a b
print a
print b
"""
        output = run(code).strip().splitlines()
        assert output == ["5", "5"]


class TestUnpackingIntegration:
    """Integration tests for unpacking"""

    def test_comprehend_and_unpack(self):
        code = """
range 3 nums
array_comprehend nums squared "x * x"
unpack squared a b c
print a
print b
print c
"""
        output = run(code).strip().splitlines()
        assert output[-3:] == ["0", "1", "4"]
