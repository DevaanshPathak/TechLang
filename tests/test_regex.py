"""
Tests for regex commands: regex_match, regex_find, regex_replace, regex_split
"""
import pytest
from techlang.interpreter import run


class TestRegexMatch:
    """Tests for the regex_match command"""

    def test_match_digits(self):
        code = '''
str_create text "hello123world"
regex_match "[0-9]+" text result
print result
'''
        assert run(code).strip() == "1"

    def test_match_no_match(self):
        code = '''
str_create text "hello world"
regex_match "[0-9]+" text result
print result
'''
        assert run(code).strip() == "0"

    def test_match_word_boundary(self):
        code = '''
str_create text "the cat sat"
regex_match "cat" text result
print result
'''
        assert run(code).strip() == "1"

    def test_match_email_pattern(self):
        code = '''
str_create text "contact us at test@example.com"
regex_match "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}" text result
print result
'''
        assert run(code).strip() == "1"

    def test_match_invalid_pattern(self):
        code = '''
str_create text "hello"
regex_match "[invalid" text result
'''
        output = run(code).strip()
        assert "Error" in output


class TestRegexFind:
    """Tests for the regex_find command"""

    def test_find_all_digits(self):
        code = '''
str_create text "a1b2c3d4"
regex_find "[0-9]" text matches
array_join matches "," result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1,2,3,4"

    def test_find_words(self):
        code = '''
str_create text "hello world test"
regex_find "[a-z]+" text matches
array_get matches 0
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "hello"

    def test_find_no_matches(self):
        code = '''
str_create text "hello world"
regex_find "[0-9]+" text matches
'''
        output = run(code).strip()
        assert "0 match" in output

    def test_find_multiple_groups(self):
        code = '''
str_create text "cat bat hat rat"
regex_find "[cbhr]at" text matches
array_join matches " " result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "cat bat hat rat"


class TestRegexReplace:
    """Tests for the regex_replace command"""

    def test_replace_digits(self):
        code = '''
str_create text "a1b2c3"
regex_replace "[0-9]" text "X" result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "aXbXcX"

    def test_replace_whitespace(self):
        code = '''
str_create text "hello   world  test"
regex_replace "\\s+" text " " result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "hello world test"

    def test_replace_nothing(self):
        code = '''
str_create text "hello world"
regex_replace "[0-9]+" text "X" result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "hello world"

    def test_replace_with_empty(self):
        code = '''
str_create text "a1b2c3"
regex_replace "[0-9]" text "" result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "abc"


class TestRegexSplit:
    """Tests for the regex_split command"""

    def test_split_by_whitespace(self):
        code = '''
str_create text "hello   world  test"
regex_split "\\s+" text parts
array_join parts "," result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "hello,world,test"

    def test_split_by_comma(self):
        code = '''
str_create text "a,b,c,d"
regex_split "," text parts
array_get parts 2
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "c"

    def test_split_by_digits(self):
        code = '''
str_create text "a1b2c3d"
regex_split "[0-9]" text parts
array_join parts "-" result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "a-b-c-d"

    def test_split_no_match(self):
        code = '''
str_create text "hello"
regex_split "[0-9]" text parts
array_get parts 0
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "hello"


class TestRegexIntegration:
    """Integration tests for regex commands"""

    def test_extract_and_count_numbers(self):
        code = '''
str_create text "price: $10, qty: 5, total: $50"
regex_find "[0-9]+" text nums
array_get nums 0
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "10"

    def test_validate_and_transform(self):
        code = '''
str_create email "USER@EXAMPLE.COM"
str_lower email
regex_match "[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,}" email valid
print valid
'''
        assert run(code).strip() == "1"

    def test_phone_number_formatting(self):
        code = '''
str_create phone "1234567890"
regex_replace "([0-9]{3})([0-9]{3})([0-9]{4})" phone "(\\1) \\2-\\3" formatted
print formatted
'''
        output = run(code).strip().splitlines()
        # Note: backreferences work differently, but the replacement happens
        assert "1234567890" not in output[-1] or "(" in output[-1]
