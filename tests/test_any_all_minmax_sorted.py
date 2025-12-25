"""
Tests for any, all, array_min, array_max, and array_sorted
"""
import pytest
from techlang.interpreter import run


class TestAny:
    """Tests for any command (like Python's any())"""

    def test_any_all_truthy(self):
        code = """
array_create nums 3
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
any nums result
print result
"""
        assert run(code).strip().split('\n')[-1] == "1"

    def test_any_some_truthy(self):
        code = """
array_create nums 3
array_set nums 0 0
array_set nums 1 0
array_set nums 2 5
any nums result
print result
"""
        assert run(code).strip().split('\n')[-1] == "1"

    def test_any_none_truthy(self):
        code = """
array_create nums 3
array_set nums 0 0
array_set nums 1 0
array_set nums 2 0
any nums result
print result
"""
        assert run(code).strip().split('\n')[-1] == "0"

    def test_any_empty_array(self):
        code = """
array_create nums
any nums result
print result
"""
        # Empty array: any([]) returns False in Python
        assert run(code).strip().split('\n')[-1] == "0"

    def test_any_with_range(self):
        code = """
range 5 nums
any nums result
print result
"""
        # range(5) = [0,1,2,3,4], has truthy values
        assert run(code).strip().split('\n')[-1] == "1"

    def test_any_nonexistent_array(self):
        code = """
any nonexistent result
"""
        output = run(code).strip()
        assert "Error" in output


class TestAll:
    """Tests for all command (like Python's all())"""

    def test_all_all_truthy(self):
        code = """
array_create nums 3
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
all nums result
print result
"""
        assert run(code).strip().split('\n')[-1] == "1"

    def test_all_some_falsy(self):
        code = """
array_create nums 3
array_set nums 0 1
array_set nums 1 0
array_set nums 2 3
all nums result
print result
"""
        assert run(code).strip().split('\n')[-1] == "0"

    def test_all_none_truthy(self):
        code = """
array_create nums 3
array_set nums 0 0
array_set nums 1 0
array_set nums 2 0
all nums result
print result
"""
        assert run(code).strip().split('\n')[-1] == "0"

    def test_all_empty_array(self):
        code = """
array_create nums
all nums result
print result
"""
        # Empty array: all([]) returns True in Python
        assert run(code).strip().split('\n')[-1] == "1"

    def test_all_with_range(self):
        code = """
range 1 5 nums
all nums result
print result
"""
        # range(1,5) = [1,2,3,4], all truthy
        assert run(code).strip().split('\n')[-1] == "1"

    def test_all_range_with_zero(self):
        code = """
range 5 nums
all nums result
print result
"""
        # range(5) = [0,1,2,3,4], has 0 which is falsy
        assert run(code).strip().split('\n')[-1] == "0"


class TestArrayMin:
    """Tests for array_min command"""

    def test_min_basic(self):
        code = """
array_create nums 5
array_set nums 0 5
array_set nums 1 2
array_set nums 2 8
array_set nums 3 1
array_set nums 4 9
array_min nums result
print result
"""
        assert run(code).strip().split('\n')[-1] == "1"

    def test_min_negative(self):
        code = """
array_create nums 3
array_set nums 0 5
array_set nums 1 -10
array_set nums 2 3
array_min nums result
print result
"""
        assert run(code).strip().split('\n')[-1] == "-10"

    def test_min_single_element(self):
        code = """
array_create nums 1
array_set nums 0 42
array_min nums result
print result
"""
        assert run(code).strip().split('\n')[-1] == "42"

    def test_min_with_key(self):
        code = """
# Find number with minimum absolute value
lambda absval x "abs(x)"
array_create nums 4
array_set nums 0 -10
array_set nums 1 5
array_set nums 2 -2
array_set nums 3 8
array_min nums absval result
print result
"""
        # -2 has minimum absolute value (2)
        assert run(code).strip().split('\n')[-1] == "-2"

    def test_min_empty_error(self):
        code = """
array_create nums
array_min nums result
"""
        output = run(code).strip()
        assert "Error" in output

    def test_min_with_range(self):
        code = """
range 10 20 nums
array_min nums result
print result
"""
        assert run(code).strip().split('\n')[-1] == "10"


class TestArrayMax:
    """Tests for array_max command"""

    def test_max_basic(self):
        code = """
array_create nums 5
array_set nums 0 5
array_set nums 1 2
array_set nums 2 8
array_set nums 3 1
array_set nums 4 9
array_max nums result
print result
"""
        assert run(code).strip().split('\n')[-1] == "9"

    def test_max_negative(self):
        code = """
array_create nums 3
array_set nums 0 -5
array_set nums 1 -10
array_set nums 2 -3
array_max nums result
print result
"""
        assert run(code).strip().split('\n')[-1] == "-3"

    def test_max_single_element(self):
        code = """
array_create nums 1
array_set nums 0 42
array_max nums result
print result
"""
        assert run(code).strip().split('\n')[-1] == "42"

    def test_max_with_key(self):
        code = """
# Find number with maximum absolute value
lambda absval x "abs(x)"
array_create nums 4
array_set nums 0 -10
array_set nums 1 5
array_set nums 2 -2
array_set nums 3 8
array_max nums absval result
print result
"""
        # -10 has maximum absolute value (10)
        assert run(code).strip().split('\n')[-1] == "-10"

    def test_max_empty_error(self):
        code = """
array_create nums
array_max nums result
"""
        output = run(code).strip()
        assert "Error" in output

    def test_max_with_range(self):
        code = """
range 10 20 nums
array_max nums result
print result
"""
        assert run(code).strip().split('\n')[-1] == "19"


class TestArraySorted:
    """Tests for array_sorted command (non-mutating sort)"""

    def test_sorted_basic(self):
        code = """
array_create nums 5
array_set nums 0 5
array_set nums 1 2
array_set nums 2 8
array_set nums 3 1
array_set nums 4 9
array_sorted nums result
array_get result 0
array_get result 1
array_get result 2
array_get result 3
array_get result 4
"""
        lines = run(code).strip().split('\n')
        assert lines[-5] == "1"
        assert lines[-4] == "2"
        assert lines[-3] == "5"
        assert lines[-2] == "8"
        assert lines[-1] == "9"

    def test_sorted_desc(self):
        code = """
array_create nums 5
array_set nums 0 5
array_set nums 1 2
array_set nums 2 8
array_set nums 3 1
array_set nums 4 9
array_sorted nums result desc
array_get result 0
array_get result 1
array_get result 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "9"
        assert lines[-2] == "8"
        assert lines[-1] == "5"

    def test_sorted_preserves_original(self):
        code = """
array_create nums 3
array_set nums 0 3
array_set nums 1 1
array_set nums 2 2
array_sorted nums result
array_get nums 0
array_get nums 1
array_get nums 2
"""
        lines = run(code).strip().split('\n')
        # Original should be unchanged
        assert lines[-3] == "3"
        assert lines[-2] == "1"
        assert lines[-1] == "2"

    def test_sorted_with_key(self):
        code = """
# Sort by absolute value
lambda absval x "abs(x)"
array_create nums 4
array_set nums 0 -10
array_set nums 1 5
array_set nums 2 -2
array_set nums 3 8
array_sorted nums absval result
array_get result 0
array_get result 1
array_get result 2
array_get result 3
"""
        lines = run(code).strip().split('\n')
        # Sorted by abs: -2(2), 5(5), 8(8), -10(10)
        assert lines[-4] == "-2"
        assert lines[-3] == "5"
        assert lines[-2] == "8"
        assert lines[-1] == "-10"

    def test_sorted_with_key_desc(self):
        code = """
lambda absval x "abs(x)"
array_create nums 4
array_set nums 0 -10
array_set nums 1 5
array_set nums 2 -2
array_set nums 3 8
array_sorted nums absval result desc
array_get result 0
array_get result 1
array_get result 2
array_get result 3
"""
        lines = run(code).strip().split('\n')
        # Sorted by abs descending: -10(10), 8(8), 5(5), -2(2)
        assert lines[-4] == "-10"
        assert lines[-3] == "8"
        assert lines[-2] == "5"
        assert lines[-1] == "-2"

    def test_sorted_empty(self):
        code = """
array_create nums
array_sorted nums result
print "done"
"""
        assert run(code).strip().split('\n')[-1] == "done"

    def test_sorted_single_element(self):
        code = """
array_create nums 1
array_set nums 0 42
array_sorted nums result
array_get result 0
"""
        assert run(code).strip().split('\n')[-1] == "42"


class TestIntegration:
    """Integration tests combining any/all, min/max, and sorted"""

    def test_any_all_combination(self):
        code = """
array_create nums 3
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
any nums has_any
all nums has_all
print has_any
print has_all
"""
        lines = run(code).strip().split('\n')
        assert lines[-2] == "1"
        assert lines[-1] == "1"

    def test_min_max_sorted(self):
        code = """
range 1 10 nums
array_min nums minimum
array_max nums maximum
array_sorted nums sorted_nums desc
array_get sorted_nums 0
print minimum
print maximum
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "9"  # First element of desc sorted
        assert lines[-2] == "1"  # minimum
        assert lines[-1] == "9"  # maximum

    def test_sorted_then_min_max(self):
        code = """
array_create nums 5
array_set nums 0 30
array_set nums 1 10
array_set nums 2 50
array_set nums 3 20
array_set nums 4 40
array_sorted nums sorted_nums
array_min sorted_nums min_val
array_max sorted_nums max_val
array_get sorted_nums 0
array_get sorted_nums 4
print min_val
print max_val
"""
        lines = run(code).strip().split('\n')
        assert lines[-4] == "10"  # First of sorted
        assert lines[-3] == "50"  # Last of sorted
        assert lines[-2] == "10"  # min_val
        assert lines[-1] == "50"  # max_val

    def test_filter_with_any_all(self):
        code = """
# Create array with some zeros
array_create data 5
array_set data 0 1
array_set data 1 0
array_set data 2 3
array_set data 3 0
array_set data 4 5

# Check any and all
any data has_truthy
all data all_truthy
print has_truthy
print all_truthy
"""
        lines = run(code).strip().split('\n')
        assert lines[-2] == "1"  # has_truthy (some non-zero)
        assert lines[-1] == "0"  # all_truthy (has zeros)

    def test_lambda_with_min_max(self):
        code = """
# Find smallest square
lambda square x "x ** 2"
array_create nums 5
array_set nums 0 -3
array_set nums 1 5
array_set nums 2 -1
array_set nums 3 4
array_set nums 4 -2
array_min nums square smallest_square
print smallest_square
"""
        # -1 has smallest square (1)
        assert run(code).strip().split('\n')[-1] == "-1"
