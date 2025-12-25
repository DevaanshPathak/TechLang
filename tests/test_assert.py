"""
Tests for the assert command
"""
import pytest
from techlang.interpreter import run


class TestAssertBasic:
    """Basic tests for the assert command"""

    def test_assert_equal_passes(self):
        code = """
set x 10
assert x == 10
print "passed"
"""
        assert run(code).strip() == "passed"

    def test_assert_equal_fails(self):
        code = """
set x 10
assert x == 5 "x should be 5"
print "should not reach"
"""
        output = run(code).strip()
        assert "AssertionError" in output
        assert "x should be 5" in output

    def test_assert_not_equal_passes(self):
        code = """
set x 10
assert x != 5
print "passed"
"""
        assert run(code).strip() == "passed"

    def test_assert_not_equal_fails(self):
        code = """
set x 10
assert x != 10
"""
        output = run(code).strip()
        assert "AssertionError" in output

    def test_assert_greater_than_passes(self):
        code = """
set x 10
assert x > 5
print "passed"
"""
        assert run(code).strip() == "passed"

    def test_assert_greater_than_fails(self):
        code = """
set x 3
assert x > 5 "x must be greater than 5"
"""
        output = run(code).strip()
        assert "AssertionError" in output
        assert "x must be greater than 5" in output

    def test_assert_less_than_passes(self):
        code = """
set x 3
assert x < 10
print "passed"
"""
        assert run(code).strip() == "passed"

    def test_assert_greater_equal_passes(self):
        code = """
set x 10
assert x >= 10
print "passed"
"""
        assert run(code).strip() == "passed"

    def test_assert_less_equal_passes(self):
        code = """
set x 10
assert x <= 10
print "passed"
"""
        assert run(code).strip() == "passed"


class TestAssertOperatorAliases:
    """Tests for operator aliases (eq, ne, gt, lt, ge, le)"""

    def test_assert_eq_alias(self):
        code = """
set x 10
assert x eq 10
print "passed"
"""
        assert run(code).strip() == "passed"

    def test_assert_ne_alias(self):
        code = """
set x 10
assert x ne 5
print "passed"
"""
        assert run(code).strip() == "passed"

    def test_assert_gt_alias(self):
        code = """
set x 10
assert x gt 5
print "passed"
"""
        assert run(code).strip() == "passed"

    def test_assert_lt_alias(self):
        code = """
set x 3
assert x lt 10
print "passed"
"""
        assert run(code).strip() == "passed"

    def test_assert_ge_alias(self):
        code = """
set x 10
assert x ge 10
print "passed"
"""
        assert run(code).strip() == "passed"

    def test_assert_le_alias(self):
        code = """
set x 10
assert x le 10
print "passed"
"""
        assert run(code).strip() == "passed"


class TestAssertStrings:
    """Tests for assert with string values"""

    def test_assert_string_equal(self):
        code = '''
str_create name "hello"
assert name == "hello"
print "passed"
'''
        assert run(code).strip() == "passed"

    def test_assert_string_not_equal(self):
        code = '''
str_create name "hello"
assert name != "world"
print "passed"
'''
        assert run(code).strip() == "passed"

    def test_assert_string_fails(self):
        code = '''
str_create name "hello"
assert name == "world" "name should be world"
'''
        output = run(code).strip()
        assert "AssertionError" in output


class TestAssertVariableComparison:
    """Tests for assert comparing two variables"""

    def test_assert_two_variables_equal(self):
        code = """
set x 10
set y 10
assert x == y
print "passed"
"""
        assert run(code).strip() == "passed"

    def test_assert_two_variables_not_equal(self):
        code = """
set x 10
set y 5
assert x != y
print "passed"
"""
        assert run(code).strip() == "passed"


class TestAssertEdgeCases:
    """Edge case tests for assert"""

    def test_assert_undefined_variable(self):
        code = """
assert undefined == 10
"""
        output = run(code).strip()
        assert "Error" in output

    def test_assert_zero(self):
        code = """
set x 0
assert x == 0
print "passed"
"""
        assert run(code).strip() == "passed"

    def test_assert_negative(self):
        code = """
set x -5
assert x < 0
print "passed"
"""
        assert run(code).strip() == "passed"

    def test_assert_with_string_message_var(self):
        code = '''
set x 5
str_create msg "value must be 10"
assert x == 10 msg
'''
        output = run(code).strip()
        assert "value must be 10" in output


class TestAssertIntegration:
    """Integration tests for assert"""

    def test_multiple_asserts(self):
        code = """
set x 10
set y 20
assert x == 10
assert y == 20
assert x < y
print "all passed"
"""
        assert run(code).strip() == "all passed"

    def test_assert_after_calculation(self):
        code = """
set x 5
mul x 2
assert x == 10
print "passed"
"""
        assert run(code).strip() == "passed"

    def test_assert_in_conditional_flow(self):
        code = """
set x 10
if x > 5
    assert x > 5
    print "condition verified"
end
"""
        assert run(code).strip() == "condition verified"
