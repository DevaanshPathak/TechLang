"""
Tests for F-Strings / Format Specifiers
- fstring, format_num, format_align, str_pad_left, str_pad_right
"""
import pytest
from techlang.interpreter import run


class TestFString:
    """F-string interpolation"""

    def test_fstring_simple(self):
        code = """
str_create name "Alice"
set age 30
fstring msg "Name: {name}, Age: {age}"
print msg
"""
        assert run(code).strip() == "Name: Alice, Age: 30"

    def test_fstring_numbers(self):
        code = """
set pi 314
fstring msg "Pi is {pi}"
print msg
"""
        assert run(code).strip() == "Pi is 314"

    def test_fstring_alignment(self):
        code = """
str_create name "Bob"
fstring msg "Name: {name:>10}"
print msg
"""
        assert run(code).strip() == "Name:        Bob"

    def test_fstring_multiple_vars(self):
        code = """
str_create first "John"
str_create last "Doe"
set id 123
fstring msg "{first} {last} (ID: {id})"
print msg
"""
        assert run(code).strip() == "John Doe (ID: 123)"


class TestFormatNum:
    """Number formatting"""

    def test_format_num_zero_pad(self):
        code = """
set val 314
format_num val "05d" result
print result
"""
        assert run(code).strip() == "00314"

    def test_format_num_thousands(self):
        code = """
set val 1234567
format_num val "," result
print result
"""
        assert run(code).strip() == "1,234,567"

    def test_format_num_decimal(self):
        code = """
set val 75
format_num val "d" result
print result
"""
        assert run(code).strip() == "75"

    def test_format_num_hex(self):
        code = """
set val 255
format_num val "x" result
print result
"""
        assert run(code).strip() == "ff"


class TestFormatAlign:
    """Text alignment formatting"""

    def test_format_align_center(self):
        code = """
str_create name "Bob"
format_align name 10 center "*" result
print result
"""
        output = run(code).strip()
        assert output == "***Bob****"

    def test_format_align_left(self):
        code = """
str_create name "Hi"
format_align name 5 left "-" result
print result
"""
        assert run(code).strip() == "Hi---"

    def test_format_align_right(self):
        code = """
str_create name "Hi"
format_align name 5 right "-" result
print result
"""
        assert run(code).strip() == "---Hi"


class TestStrPadLeft:
    """Left padding"""

    def test_str_pad_left_number(self):
        code = """
set num 42
str_pad_left num 5 "0" result
print result
"""
        assert run(code).strip() == "00042"

    def test_str_pad_left_string(self):
        code = """
str_create s "abc"
str_pad_left s 6 "X" result
print result
"""
        assert run(code).strip() == "XXXabc"


class TestStrPadRight:
    """Right padding"""

    def test_str_pad_right_basic(self):
        code = """
str_create name "Hi"
str_pad_right name 5 "." result
print result
"""
        assert run(code).strip() == "Hi..."

    def test_str_pad_right_number(self):
        code = """
set n 7
str_pad_right n 3 "0" result
print result
"""
        assert run(code).strip() == "700"


class TestFormatIntegration:
    """Integration tests for formatting"""

    def test_dict_comprehend_and_format(self):
        code = """
array_create prices 3
array_set prices 0 100
array_set prices 1 200
array_set prices 2 300
dict_comprehend prices tax_map "x" "x * 10"
dict_get tax_map 100
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "1000"

    def test_combined_formatting(self):
        code = """
str_create name "Test"
set value 42
fstring msg "Result: {name} = {value}"
print msg
"""
        assert run(code).strip() == "Result: Test = 42"
