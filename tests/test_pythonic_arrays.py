"""
Tests for Python-like array operations: array_slice, range, array_comprehend
"""
import pytest
from techlang.interpreter import run


class TestArraySlice:
    """Tests for array_slice command (like Python's list[start:end])"""

    def test_slice_basic(self):
        code = """
array_create nums 5
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
array_set nums 3 40
array_set nums 4 50
array_slice nums 1 4 result
array_get result 0
"""
        assert run(code).strip().split('\n')[-1] == "20"

    def test_slice_length(self):
        code = """
array_create nums 5
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
array_set nums 3 40
array_set nums 4 50
array_slice nums 1 4 result
array_get result 0
array_get result 1
array_get result 2
"""
        lines = run(code).strip().split('\n')
        # result should contain [20, 30, 40]
        assert lines[-3] == "20"
        assert lines[-2] == "30"
        assert lines[-1] == "40"

    def test_slice_from_start(self):
        code = """
array_create nums 5
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
array_set nums 3 4
array_set nums 4 5
array_slice nums 0 3 result
array_get result 0
array_get result 1
array_get result 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "1"
        assert lines[-2] == "2"
        assert lines[-1] == "3"

    def test_slice_to_end(self):
        code = """
array_create nums 5
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
array_set nums 3 4
array_set nums 4 5
array_slice nums 3 5 result
array_get result 0
array_get result 1
"""
        lines = run(code).strip().split('\n')
        assert lines[-2] == "4"
        assert lines[-1] == "5"

    def test_slice_negative_start(self):
        code = """
array_create nums 5
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
array_set nums 3 40
array_set nums 4 50
array_slice nums -2 5 result
array_get result 0
array_get result 1
"""
        lines = run(code).strip().split('\n')
        # -2 means start from index 3 (length 5, so 5-2=3)
        assert lines[-2] == "40"
        assert lines[-1] == "50"

    def test_slice_negative_end(self):
        code = """
array_create nums 5
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
array_set nums 3 40
array_set nums 4 50
array_slice nums 0 -2 result
array_get result 0
array_get result 1
array_get result 2
"""
        lines = run(code).strip().split('\n')
        # -2 means end at index 3 (length 5, so 5-2=3)
        assert lines[-3] == "10"
        assert lines[-2] == "20"
        assert lines[-1] == "30"

    def test_slice_empty_result(self):
        code = """
array_create nums 5
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
array_slice nums 2 2 result
print "done"
"""
        # slice from 2 to 2 should be empty
        assert run(code).strip().split('\n')[-1] == "done"

    def test_slice_with_variables(self):
        code = """
array_create nums 5
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
array_set nums 3 40
array_set nums 4 50
set start 1
set end 3
array_slice nums start end result
array_get result 0
array_get result 1
"""
        lines = run(code).strip().split('\n')
        assert lines[-2] == "20"
        assert lines[-1] == "30"


class TestRange:
    """Tests for range command (like Python's range())"""

    def test_range_single_arg(self):
        code = """
range 5 nums
array_get nums 0
array_get nums 1
array_get nums 2
array_get nums 3
array_get nums 4
"""
        lines = run(code).strip().split('\n')
        assert lines[-5] == "0"
        assert lines[-4] == "1"
        assert lines[-3] == "2"
        assert lines[-2] == "3"
        assert lines[-1] == "4"

    def test_range_two_args(self):
        code = """
range 1 5 nums
array_get nums 0
array_get nums 1
array_get nums 2
array_get nums 3
"""
        lines = run(code).strip().split('\n')
        assert lines[-4] == "1"
        assert lines[-3] == "2"
        assert lines[-2] == "3"
        assert lines[-1] == "4"

    def test_range_three_args_step(self):
        code = """
range 0 10 2 nums
array_get nums 0
array_get nums 1
array_get nums 2
array_get nums 3
array_get nums 4
"""
        lines = run(code).strip().split('\n')
        assert lines[-5] == "0"
        assert lines[-4] == "2"
        assert lines[-3] == "4"
        assert lines[-2] == "6"
        assert lines[-1] == "8"

    def test_range_negative_step(self):
        code = """
range 10 0 -2 nums
array_get nums 0
array_get nums 1
array_get nums 2
array_get nums 3
array_get nums 4
"""
        lines = run(code).strip().split('\n')
        assert lines[-5] == "10"
        assert lines[-4] == "8"
        assert lines[-3] == "6"
        assert lines[-2] == "4"
        assert lines[-1] == "2"

    def test_range_empty(self):
        code = """
range 5 0 nums
print "done"
"""
        # range(5, 0) with default step 1 should be empty
        assert run(code).strip().split('\n')[-1] == "done"

    def test_range_with_variables(self):
        code = """
set start 2
set end 7
range start end nums
array_get nums 0
array_get nums 4
"""
        lines = run(code).strip().split('\n')
        assert lines[-2] == "2"
        assert lines[-1] == "6"

    def test_range_zero_step_error(self):
        code = """
range 0 10 0 nums
"""
        output = run(code).strip()
        assert "Error" in output
        assert "zero" in output.lower()

    def test_range_large(self):
        code = """
range 100 nums
array_get nums 99
"""
        assert run(code).strip().split('\n')[-1] == "99"


class TestArrayComprehend:
    """Tests for array_comprehend command (like Python list comprehension)"""

    def test_comprehend_multiply(self):
        code = """
array_create nums 3
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
array_comprehend nums result "x * 2"
array_get result 0
array_get result 1
array_get result 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "2"
        assert lines[-2] == "4"
        assert lines[-1] == "6"

    def test_comprehend_add(self):
        code = """
array_create nums 3
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
array_comprehend nums result "x + 5"
array_get result 0
array_get result 1
array_get result 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "15"
        assert lines[-2] == "25"
        assert lines[-1] == "35"

    def test_comprehend_subtract(self):
        code = """
array_create nums 3
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
array_comprehend nums result "x - 3"
array_get result 0
array_get result 1
array_get result 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "7"
        assert lines[-2] == "17"
        assert lines[-1] == "27"

    def test_comprehend_divide(self):
        code = """
array_create nums 3
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
array_comprehend nums result "x / 2"
array_get result 0
array_get result 1
array_get result 2
"""
        lines = run(code).strip().split('\n')
        assert float(lines[-3]) == 5.0
        assert float(lines[-2]) == 10.0
        assert float(lines[-1]) == 15.0

    def test_comprehend_floor_divide(self):
        code = """
array_create nums 3
array_set nums 0 10
array_set nums 1 21
array_set nums 2 35
array_comprehend nums result "x // 3"
array_get result 0
array_get result 1
array_get result 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "3"
        assert lines[-2] == "7"
        assert lines[-1] == "11"

    def test_comprehend_modulo(self):
        code = """
array_create nums 3
array_set nums 0 10
array_set nums 1 21
array_set nums 2 35
array_comprehend nums result "x % 3"
array_get result 0
array_get result 1
array_get result 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "1"
        assert lines[-2] == "0"
        assert lines[-1] == "2"

    def test_comprehend_power(self):
        code = """
array_create nums 3
array_set nums 0 2
array_set nums 1 3
array_set nums 2 4
array_comprehend nums result "x ** 2"
array_get result 0
array_get result 1
array_get result 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "4"
        assert lines[-2] == "9"
        assert lines[-1] == "16"

    def test_comprehend_negate(self):
        code = """
array_create nums 3
array_set nums 0 5
array_set nums 1 -3
array_set nums 2 10
array_comprehend nums result "-x"
array_get result 0
array_get result 1
array_get result 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "-5"
        assert lines[-2] == "3"
        assert lines[-1] == "-10"

    def test_comprehend_abs(self):
        code = """
array_create nums 3
array_set nums 0 -5
array_set nums 1 3
array_set nums 2 -10
array_comprehend nums result "abs(x)"
array_get result 0
array_get result 1
array_get result 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "5"
        assert lines[-2] == "3"
        assert lines[-1] == "10"

    def test_comprehend_identity(self):
        code = """
array_create nums 3
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
array_comprehend nums result "x"
array_get result 0
array_get result 1
array_get result 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "1"
        assert lines[-2] == "2"
        assert lines[-1] == "3"

    def test_comprehend_reverse_operation(self):
        code = """
array_create nums 3
array_set nums 0 2
array_set nums 1 3
array_set nums 2 4
array_comprehend nums result "10 - x"
array_get result 0
array_get result 1
array_get result 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "8"
        assert lines[-2] == "7"
        assert lines[-1] == "6"

    def test_comprehend_with_range(self):
        code = """
range 1 6 nums
array_comprehend nums squares "x ** 2"
array_get squares 0
array_get squares 1
array_get squares 2
array_get squares 3
array_get squares 4
"""
        lines = run(code).strip().split('\n')
        assert lines[-5] == "1"
        assert lines[-4] == "4"
        assert lines[-3] == "9"
        assert lines[-2] == "16"
        assert lines[-1] == "25"

    def test_comprehend_invalid_expression(self):
        code = """
array_create nums 3
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
array_comprehend nums result "invalid expr"
"""
        output = run(code).strip()
        assert "Error" in output or "Unsupported" in output


class TestIntegration:
    """Integration tests combining multiple Python-like features"""

    def test_slice_and_comprehend(self):
        code = """
range 10 nums
array_slice nums 2 7 middle
array_comprehend middle doubled "x * 2"
array_get doubled 0
array_get doubled 1
array_get doubled 2
"""
        lines = run(code).strip().split('\n')
        # nums = [0,1,2,3,4,5,6,7,8,9]
        # middle = [2,3,4,5,6]
        # doubled = [4,6,8,10,12]
        assert lines[-3] == "4"
        assert lines[-2] == "6"
        assert lines[-1] == "8"

    def test_range_and_loop(self):
        code = """
range 1 4 nums
set total 0
loop 3
    array_get nums total idx
    add total 1
end
print total
"""
        assert run(code).strip().split('\n')[-1] == "3"

    def test_comprehend_preserves_source(self):
        code = """
array_create nums 3
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
array_comprehend nums result "x * 10"
array_get nums 0
array_get nums 1
array_get nums 2
"""
        lines = run(code).strip().split('\n')
        # Original should be unchanged
        assert lines[-3] == "1"
        assert lines[-2] == "2"
        assert lines[-1] == "3"
