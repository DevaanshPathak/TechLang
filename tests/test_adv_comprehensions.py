"""
Tests for Advanced Comprehensions
- dict_comprehend, set_comprehend, generator_expr, comprehend_if
"""
import pytest
from techlang.interpreter import run


class TestDictComprehend:
    """Dict comprehension from array"""

    def test_dict_comprehend_basic(self):
        code = """
array_create nums 5
array_set nums 0 0
array_set nums 1 1
array_set nums 2 2
array_set nums 3 3
array_set nums 4 4
dict_comprehend nums result "x" "x * x"
dict_get result 2
"""
        assert run(code).strip().splitlines()[-1] == "4"

    def test_dict_comprehend_with_expression(self):
        code = """
range 3 nums
dict_comprehend nums result "x" "x * 10"
dict_get result 1
"""
        assert run(code).strip().splitlines()[-1] == "10"


class TestSetComprehend:
    """Set comprehension from array"""

    def test_set_comprehend_removes_duplicates(self):
        code = """
array_create nums 6
array_set nums 0 1
array_set nums 1 2
array_set nums 2 2
array_set nums 3 3
array_set nums 4 3
array_set nums 5 3
set_comprehend nums unique "x"
set_len unique count
print count
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "3"

    def test_set_comprehend_with_transform(self):
        code = """
range 5 nums
set_comprehend nums squares "x * x"
set_len squares count
print count
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "5"


class TestComprehendIf:
    """Conditional comprehension"""

    def test_comprehend_if_even_numbers(self):
        code = """
range 10 nums
comprehend_if nums evens "x" "x % 2 == 0"
array_get evens 0 first
array_get evens 1 second
print first
print second
"""
        output = run(code).strip().splitlines()
        assert output[-2:] == ["0", "2"]

    def test_comprehend_if_greater_than(self):
        code = """
range 10 nums
comprehend_if nums big "x" "x > 5"
array_get big 0 first
print first
"""
        assert run(code).strip().splitlines()[-1] == "6"


class TestGeneratorExpr:
    """Generator expression from array"""

    def test_generator_expr_basic(self):
        code = """
range 5 nums
generator_expr nums gen "x * 2"
generator_next gen val done
print val
"""
        assert run(code).strip() == "0"

    def test_generator_expr_iterate(self):
        code = """
range 3 nums
generator_expr nums gen "x + 1"
generator_next gen v1 d1
generator_next gen v2 d2
print v1
print v2
"""
        output = run(code).strip().splitlines()
        assert output == ["1", "2"]
