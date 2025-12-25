"""
Tests for bitwise operations
"""
import pytest
from techlang.interpreter import run


class TestBitAnd:
    """Tests for bit_and operation"""

    def test_bit_and_basic(self):
        code = """
set a 12
bit_and a 10 result
print result
"""
        # 12 = 1100, 10 = 1010, AND = 1000 = 8
        assert run(code).strip() == "8"

    def test_bit_and_zeros(self):
        code = """
set a 15
bit_and a 0 result
print result
"""
        assert run(code).strip() == "0"

    def test_bit_and_same_value(self):
        code = """
set a 7
bit_and a 7 result
print result
"""
        assert run(code).strip() == "7"

    def test_bit_and_all_ones(self):
        code = """
set a 255
bit_and a 15 result
print result
"""
        # 255 = 11111111, 15 = 00001111, AND = 00001111 = 15
        assert run(code).strip() == "15"


class TestBitOr:
    """Tests for bit_or operation"""

    def test_bit_or_basic(self):
        code = """
set a 12
bit_or a 10 result
print result
"""
        # 12 = 1100, 10 = 1010, OR = 1110 = 14
        assert run(code).strip() == "14"

    def test_bit_or_with_zero(self):
        code = """
set a 15
bit_or a 0 result
print result
"""
        assert run(code).strip() == "15"

    def test_bit_or_same_value(self):
        code = """
set a 7
bit_or a 7 result
print result
"""
        assert run(code).strip() == "7"


class TestBitXor:
    """Tests for bit_xor operation"""

    def test_bit_xor_basic(self):
        code = """
set a 12
bit_xor a 10 result
print result
"""
        # 12 = 1100, 10 = 1010, XOR = 0110 = 6
        assert run(code).strip() == "6"

    def test_bit_xor_same_value(self):
        code = """
set a 7
bit_xor a 7 result
print result
"""
        # XOR of same value = 0
        assert run(code).strip() == "0"

    def test_bit_xor_with_zero(self):
        code = """
set a 15
bit_xor a 0 result
print result
"""
        assert run(code).strip() == "15"

    def test_bit_xor_swap_pattern(self):
        code = """
set a 5
set b 9
bit_xor a b a
bit_xor b a b
bit_xor a b a
print a
print b
"""
        # XOR swap: a=5, b=9 -> a=9, b=5
        lines = run(code).strip().split('\n')
        assert lines[-2] == "9"
        assert lines[-1] == "5"


class TestBitNot:
    """Tests for bit_not operation"""

    def test_bit_not_basic(self):
        code = """
set a 0
bit_not a result
print result
"""
        # NOT 0 = -1 (two's complement)
        assert run(code).strip() == "-1"

    def test_bit_not_one(self):
        code = """
set a 1
bit_not a result
print result
"""
        # NOT 1 = -2 (two's complement)
        assert run(code).strip() == "-2"

    def test_bit_not_double(self):
        code = """
set a 42
bit_not a temp
bit_not temp result
print result
"""
        # NOT(NOT(x)) = x
        assert run(code).strip() == "42"


class TestBitShiftLeft:
    """Tests for bit_shift_left operation"""

    def test_shift_left_basic(self):
        code = """
set a 1
bit_shift_left a 4 result
print result
"""
        # 1 << 4 = 16
        assert run(code).strip() == "16"

    def test_shift_left_zero_places(self):
        code = """
set a 7
bit_shift_left a 0 result
print result
"""
        assert run(code).strip() == "7"

    def test_shift_left_multiply(self):
        code = """
set a 5
bit_shift_left a 3 result
print result
"""
        # 5 << 3 = 5 * 8 = 40
        assert run(code).strip() == "40"


class TestBitShiftRight:
    """Tests for bit_shift_right operation"""

    def test_shift_right_basic(self):
        code = """
set a 16
bit_shift_right a 4 result
print result
"""
        # 16 >> 4 = 1
        assert run(code).strip() == "1"

    def test_shift_right_zero_places(self):
        code = """
set a 7
bit_shift_right a 0 result
print result
"""
        assert run(code).strip() == "7"

    def test_shift_right_divide(self):
        code = """
set a 40
bit_shift_right a 3 result
print result
"""
        # 40 >> 3 = 40 / 8 = 5
        assert run(code).strip() == "5"


class TestBitOperationsVariables:
    """Tests using variables for second operand"""

    def test_bit_and_two_vars(self):
        code = """
set a 12
set b 10
bit_and a b result
print result
"""
        assert run(code).strip() == "8"

    def test_bit_or_two_vars(self):
        code = """
set a 12
set b 10
bit_or a b result
print result
"""
        assert run(code).strip() == "14"

    def test_bit_xor_two_vars(self):
        code = """
set a 12
set b 10
bit_xor a b result
print result
"""
        assert run(code).strip() == "6"

    def test_shift_with_var(self):
        code = """
set a 8
set n 2
bit_shift_right a n result
print result
"""
        # 8 >> 2 = 2
        assert run(code).strip() == "2"


class TestBitOperationsEdgeCases:
    """Edge case tests"""

    def test_bit_and_undefined_var(self):
        code = """
bit_and undefined 5 result
"""
        output = run(code).strip()
        assert "Error" in output

    def test_bit_shift_negative(self):
        code = """
set a 16
set n -1
bit_shift_right a n result
"""
        # Negative shifts should error or behave predictably
        output = run(code).strip()
        # Could be error or unexpected result, just verify it runs

    def test_large_numbers(self):
        code = """
set a 65535
bit_and a 255 result
print result
"""
        # 65535 & 255 = 255
        assert run(code).strip() == "255"


class TestBitOperationsIntegration:
    """Integration tests"""

    def test_bit_flag_operations(self):
        code = """
set flags 0
bit_or flags 1 flags
bit_or flags 4 flags
print flags
"""
        # Set bits 0 and 2: 0 | 1 | 4 = 5
        assert run(code).strip() == "5"

    def test_check_bit_set(self):
        code = """
set flags 5
bit_and flags 4 result
if result > 0
    print "bit is set"
end
"""
        # 5 & 4 = 4 (non-zero), bit is set
        assert run(code).strip() == "bit is set"

    def test_clear_bit(self):
        code = """
set flags 7
bit_not 2 mask
bit_and flags mask flags
print flags
"""
        # 7 = 111, clear bit 1: NOT 2 = -3, 7 & -3 = 5
        assert run(code).strip() == "5"

    def test_combined_operations(self):
        code = """
set a 12
set b 10
bit_and a b temp1
bit_or a b temp2
bit_xor temp1 temp2 result
print result
"""
        # a=12, b=10
        # temp1 = 12 & 10 = 8
        # temp2 = 12 | 10 = 14
        # result = 8 ^ 14 = 6
        assert run(code).strip() == "6"
