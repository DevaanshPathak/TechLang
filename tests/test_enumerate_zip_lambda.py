"""
Tests for enumerate, array_zip, and lambda functions
"""
import pytest
from techlang.interpreter import run


class TestEnumerate:
    """Tests for enumerate command (like Python's enumerate())"""

    def test_enumerate_basic(self):
        code = """
array_create items 3
array_set items 0 "apple"
array_set items 1 "banana"
array_set items 2 "cherry"
enumerate items idxs vals
array_get idxs 0
array_get idxs 1
array_get idxs 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "0"
        assert lines[-2] == "1"
        assert lines[-1] == "2"

    def test_enumerate_values(self):
        code = """
array_create items 3
array_set items 0 10
array_set items 1 20
array_set items 2 30
enumerate items idxs vals
array_get vals 0
array_get vals 1
array_get vals 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "10"
        assert lines[-2] == "20"
        assert lines[-1] == "30"

    def test_enumerate_empty_array(self):
        code = """
array_create items
enumerate items idxs vals
print "done"
"""
        assert run(code).strip().split('\n')[-1] == "done"

    def test_enumerate_with_range(self):
        code = """
range 5 nums
enumerate nums idxs vals
array_get idxs 4
array_get vals 4
"""
        lines = run(code).strip().split('\n')
        assert lines[-2] == "4"
        assert lines[-1] == "4"

    def test_enumerate_preserves_original(self):
        code = """
array_create items 3
array_set items 0 100
array_set items 1 200
array_set items 2 300
enumerate items idxs vals
array_get items 0
array_get items 1
array_get items 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "100"
        assert lines[-2] == "200"
        assert lines[-1] == "300"

    def test_enumerate_nonexistent_array(self):
        code = """
enumerate nonexistent idxs vals
"""
        output = run(code).strip()
        assert "Error" in output


class TestArrayZip:
    """Tests for array_zip command (like Python's zip())"""

    def test_zip_basic_pairs(self):
        code = """
array_create names 3
array_set names 0 "Alice"
array_set names 1 "Bob"
array_set names 2 "Charlie"
array_create ages 3
array_set ages 0 25
array_set ages 1 30
array_set ages 2 35
array_zip names ages pairs
array_get pairs 0
"""
        lines = run(code).strip().split('\n')
        # pairs[0] should be ["Alice", 25]
        assert "Alice" in lines[-1] or "25" in lines[-1]

    def test_zip_two_results(self):
        code = """
range 3 nums1
range 10 13 nums2
array_zip nums1 nums2 res1 res2
array_get res1 0
array_get res1 1
array_get res1 2
array_get res2 0
array_get res2 1
array_get res2 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-6] == "0"
        assert lines[-5] == "1"
        assert lines[-4] == "2"
        assert lines[-3] == "10"
        assert lines[-2] == "11"
        assert lines[-1] == "12"

    def test_zip_different_lengths(self):
        code = """
range 5 long_arr
range 3 short_arr
array_zip long_arr short_arr res1 res2
array_get res1 0
array_get res1 1
array_get res1 2
"""
        lines = run(code).strip().split('\n')
        # Should truncate to shorter length (3)
        assert lines[-3] == "0"
        assert lines[-2] == "1"
        assert lines[-1] == "2"

    def test_zip_empty_arrays(self):
        code = """
array_create a
array_create b
array_zip a b result
print "done"
"""
        assert run(code).strip().split('\n')[-1] == "done"

    def test_zip_nonexistent_array(self):
        code = """
range 3 nums
array_zip nums nonexistent result
"""
        output = run(code).strip()
        assert "Error" in output

    def test_zip_with_strings(self):
        code = """
array_create letters 3
array_set letters 0 "a"
array_set letters 1 "b"
array_set letters 2 "c"
array_create numbers 3
array_set numbers 0 1
array_set numbers 1 2
array_set numbers 2 3
array_zip letters numbers l n
array_get l 0
array_get n 0
array_get l 2
array_get n 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-4] == "a"
        assert lines[-3] == "1"
        assert lines[-2] == "c"
        assert lines[-1] == "3"


class TestLambda:
    """Tests for lambda, array_apply, and lambda_call commands"""

    def test_lambda_define(self):
        code = """
lambda double x "x * 2"
print "defined"
"""
        assert run(code).strip() == "defined"

    def test_lambda_array_apply_multiply(self):
        code = """
lambda double x "x * 2"
range 1 6 nums
array_apply nums double result
array_get result 0
array_get result 1
array_get result 2
array_get result 3
array_get result 4
"""
        lines = run(code).strip().split('\n')
        assert lines[-5] == "2"
        assert lines[-4] == "4"
        assert lines[-3] == "6"
        assert lines[-2] == "8"
        assert lines[-1] == "10"

    def test_lambda_array_apply_square(self):
        code = """
lambda square x "x ** 2"
range 1 5 nums
array_apply nums square result
array_get result 0
array_get result 1
array_get result 2
array_get result 3
"""
        lines = run(code).strip().split('\n')
        assert lines[-4] == "1"
        assert lines[-3] == "4"
        assert lines[-2] == "9"
        assert lines[-1] == "16"

    def test_lambda_array_apply_add(self):
        code = """
lambda add_ten x "x + 10"
range 5 nums
array_apply nums add_ten result
array_get result 0
array_get result 4
"""
        lines = run(code).strip().split('\n')
        assert lines[-2] == "10"
        assert lines[-1] == "14"

    def test_lambda_call_basic(self):
        code = """
lambda double x "x * 2"
lambda_call double 5 result
print result
"""
        assert run(code).strip().split('\n')[-1] == "10"

    def test_lambda_call_with_variable(self):
        code = """
lambda square x "x ** 2"
set val 7
lambda_call square val result
print result
"""
        assert run(code).strip().split('\n')[-1] == "49"

    def test_lambda_negate(self):
        code = """
lambda neg x "-x"
range 1 4 nums
array_apply nums neg result
array_get result 0
array_get result 1
array_get result 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "-1"
        assert lines[-2] == "-2"
        assert lines[-1] == "-3"

    def test_lambda_abs(self):
        code = """
lambda absolute x "abs(x)"
array_create nums 3
array_set nums 0 -5
array_set nums 1 3
array_set nums 2 -10
array_apply nums absolute result
array_get result 0
array_get result 1
array_get result 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "5"
        assert lines[-2] == "3"
        assert lines[-1] == "10"

    def test_lambda_nonexistent(self):
        code = """
range 3 nums
array_apply nums nonexistent result
"""
        output = run(code).strip()
        assert "Error" in output

    def test_lambda_call_nonexistent(self):
        code = """
lambda_call nonexistent 5 result
"""
        output = run(code).strip()
        assert "Error" in output

    def test_multiple_lambdas(self):
        code = """
lambda double x "x * 2"
lambda square x "x ** 2"
lambda add_one x "x + 1"
range 1 4 nums
array_apply nums double doubled
array_apply doubled square squared
array_apply squared add_one final
array_get final 0
array_get final 1
array_get final 2
"""
        lines = run(code).strip().split('\n')
        # 1*2=2, 2^2=4, 4+1=5
        # 2*2=4, 4^2=16, 16+1=17
        # 3*2=6, 6^2=36, 36+1=37
        assert lines[-3] == "5"
        assert lines[-2] == "17"
        assert lines[-1] == "37"


class TestIntegration:
    """Integration tests combining enumerate, zip, and lambda"""

    def test_enumerate_and_lambda(self):
        code = """
range 1 5 nums
enumerate nums idxs vals
lambda triple x "x * 3"
array_apply vals triple tripled
array_get tripled 0
array_get tripled 1
array_get tripled 2
"""
        lines = run(code).strip().split('\n')
        assert lines[-3] == "3"
        assert lines[-2] == "6"
        assert lines[-1] == "9"

    def test_zip_and_lambda(self):
        code = """
range 1 4 a
range 10 40 10 b
array_zip a b res_a res_b
lambda double x "x * 2"
array_apply res_b double doubled
array_get doubled 0
array_get doubled 1
array_get doubled 2
"""
        lines = run(code).strip().split('\n')
        # b = [10, 20, 30], doubled = [20, 40, 60]
        assert lines[-3] == "20"
        assert lines[-2] == "40"
        assert lines[-1] == "60"

    def test_full_pipeline(self):
        code = """
# Create data
range 1 6 data

# Square each number
lambda square x "x ** 2"
array_apply data square squared

# Enumerate to get indices
enumerate squared idxs vals

# Get specific values
array_get vals 0
array_get vals 2
array_get vals 4
"""
        lines = run(code).strip().split('\n')
        # data = [1,2,3,4,5], squared = [1,4,9,16,25]
        assert lines[-3] == "1"
        assert lines[-2] == "9"
        assert lines[-1] == "25"

    def test_chained_lambdas(self):
        code = """
lambda inc x "x + 1"
lambda dbl x "x * 2"
set val 5
lambda_call inc val step1
lambda_call dbl step1 step2
print step2
"""
        # 5 + 1 = 6, 6 * 2 = 12
        assert run(code).strip().split('\n')[-1] == "12"
