"""
Tests for array sort/reverse/find/unique/join commands
"""
import pytest
from techlang.interpreter import run


class TestArraySort:
    """Tests for the array_sort command"""

    def test_sort_ascending_default(self):
        code = """
array_create nums 5
array_set nums 0 5
array_set nums 1 2
array_set nums 2 8
array_set nums 3 1
array_set nums 4 9
array_sort nums
array_get nums 0
array_get nums 1
array_get nums 2
"""
        output = run(code).strip().splitlines()
        # Filter for just the numbers
        nums = [line for line in output if line.isdigit()]
        assert nums == ["1", "2", "5"]

    def test_sort_ascending_explicit(self):
        code = """
array_create nums 3
array_set nums 0 30
array_set nums 1 10
array_set nums 2 20
array_sort nums asc
array_get nums 0
array_get nums 1
array_get nums 2
"""
        output = run(code).strip().splitlines()
        nums = [line for line in output if line.isdigit()]
        assert nums == ["10", "20", "30"]

    def test_sort_descending(self):
        code = """
array_create nums 3
array_set nums 0 10
array_set nums 1 30
array_set nums 2 20
array_sort nums desc
array_get nums 0
array_get nums 1
array_get nums 2
"""
        output = run(code).strip().splitlines()
        nums = [line for line in output if line.isdigit()]
        assert nums == ["30", "20", "10"]

    def test_sort_strings(self):
        code = """
array_create words 3
array_set words 0 "cherry"
array_set words 1 "apple"
array_set words 2 "banana"
array_sort words
array_get words 0
array_get words 1
array_get words 2
"""
        output = run(code).strip().splitlines()
        words = [line for line in output if line in ("apple", "banana", "cherry")]
        assert words == ["apple", "banana", "cherry"]

    def test_sort_nonexistent_array(self):
        code = "array_sort nonexistent"
        output = run(code).strip()
        assert "Error" in output


class TestArrayReverse:
    """Tests for the array_reverse command"""

    def test_reverse_numbers(self):
        code = """
array_create nums 3
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
array_reverse nums
array_get nums 0
array_get nums 1
array_get nums 2
"""
        output = run(code).strip().splitlines()
        nums = [line for line in output if line.isdigit()]
        assert nums == ["3", "2", "1"]

    def test_reverse_single_element(self):
        code = """
array_create nums 1
array_set nums 0 42
array_reverse nums
array_get nums 0
"""
        output = run(code).strip().splitlines()
        nums = [line for line in output if line.isdigit()]
        assert nums == ["42"]

    def test_reverse_nonexistent_array(self):
        code = "array_reverse nonexistent"
        output = run(code).strip()
        assert "Error" in output


class TestArrayFind:
    """Tests for the array_find command"""

    def test_find_existing_value(self):
        code = """
array_create nums 4
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
array_set nums 3 40
array_find nums 30 idx
print idx
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "2"

    def test_find_first_element(self):
        code = """
array_create nums 3
array_set nums 0 100
array_set nums 1 200
array_set nums 2 300
array_find nums 100 idx
print idx
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "0"

    def test_find_not_found(self):
        code = """
array_create nums 3
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
array_find nums 99 idx
print idx
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "-1"

    def test_find_string_in_array(self):
        code = """
array_create words 3
array_set words 0 "hello"
array_set words 1 "world"
array_set words 2 "test"
array_find words "world" idx
print idx
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "1"


class TestArrayUnique:
    """Tests for the array_unique command"""

    def test_unique_with_duplicates(self):
        code = """
array_create nums 6
array_set nums 0 1
array_set nums 1 2
array_set nums 2 2
array_set nums 3 3
array_set nums 4 1
array_set nums 5 3
array_unique nums
array_get nums 0
array_get nums 1
array_get nums 2
"""
        output = run(code).strip().splitlines()
        nums = [line for line in output if line.isdigit() and int(line) < 10]
        assert nums == ["1", "2", "3"]

    def test_unique_no_duplicates(self):
        code = """
array_create nums 3
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
array_unique nums
array_get nums 0
array_get nums 1
array_get nums 2
"""
        output = run(code).strip().splitlines()
        nums = [line for line in output if line.isdigit() and int(line) < 10]
        assert nums == ["1", "2", "3"]

    def test_unique_preserves_order(self):
        code = """
array_create nums 5
array_set nums 0 5
array_set nums 1 3
array_set nums 2 5
array_set nums 3 1
array_set nums 4 3
array_unique nums
array_get nums 0
array_get nums 1
array_get nums 2
"""
        output = run(code).strip().splitlines()
        nums = [line for line in output if line.isdigit() and int(line) < 10]
        assert nums == ["5", "3", "1"]


class TestArrayJoin:
    """Tests for the array_join command"""

    def test_join_with_comma(self):
        code = """
array_create nums 3
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
array_join nums "," result
print result
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "1,2,3"

    def test_join_with_space(self):
        code = """
array_create words 3
array_set words 0 "hello"
array_set words 1 "world"
array_set words 2 "test"
array_join words " " result
print result
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "hello world test"

    def test_join_empty_delimiter(self):
        code = """
array_create chars 3
array_set chars 0 "a"
array_set chars 1 "b"
array_set chars 2 "c"
array_join chars "" result
print result
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "abc"

    def test_join_single_element(self):
        code = """
array_create nums 1
array_set nums 0 42
array_join nums "," result
print result
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "42"


class TestArraySortIntegration:
    """Integration tests for array sorting and related commands"""

    def test_sort_then_reverse(self):
        code = """
array_create nums 4
array_set nums 0 3
array_set nums 1 1
array_set nums 2 4
array_set nums 3 2
array_sort nums
array_reverse nums
array_get nums 0
array_get nums 1
array_get nums 2
array_get nums 3
"""
        output = run(code).strip().splitlines()
        nums = [line for line in output if line.isdigit() and int(line) < 10]
        assert nums == ["4", "3", "2", "1"]

    def test_unique_then_sort(self):
        code = """
array_create nums 6
array_set nums 0 3
array_set nums 1 1
array_set nums 2 3
array_set nums 3 2
array_set nums 4 1
array_set nums 5 2
array_unique nums
array_sort nums
array_join nums "," result
print result
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "1,2,3"

    def test_find_after_sort(self):
        code = """
array_create nums 4
array_set nums 0 30
array_set nums 1 10
array_set nums 2 40
array_set nums 3 20
array_sort nums
array_find nums 30 idx
print idx
"""
        output = run(code).strip().splitlines()
        # After sorting: [10, 20, 30, 40], so 30 is at index 2
        assert output[-1] == "2"
