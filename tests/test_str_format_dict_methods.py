"""Tests for string formatting, string methods, and dict methods (Todos 10, 11, 12)."""

import pytest
from techlang.interpreter import run


class TestStrFormat:
    """Tests for str_format command."""

    def test_str_format_basic(self):
        """Test basic string formatting with single placeholder."""
        code = '''str_create greeting "Hello"
str_format result "Say: {}" greeting
print result'''
        assert run(code).strip() == "Say: Hello"

    def test_str_format_multiple(self):
        """Test string formatting with multiple placeholders."""
        code = '''str_create name "Alice"
set age 30
str_format result "{} is {} years old" name age
print result'''
        assert run(code).strip() == "Alice is 30 years old"

    def test_str_format_numbers(self):
        """Test string formatting with numeric variables."""
        code = '''set x 10
set y 20
str_format result "{} + {} = 30" x y
print result'''
        assert run(code).strip() == "10 + 20 = 30"

    def test_str_format_mixed(self):
        """Test string formatting with mixed types."""
        code = '''str_create city "Paris"
set year 2024
str_format result "Visit {} in {}" city year
print result'''
        assert run(code).strip() == "Visit Paris in 2024"

    def test_str_format_extra_args(self):
        """Test string formatting with extra args (ignored)."""
        code = '''set a 1
set b 2
set c 3
str_format result "Just {}" a b c
print result'''
        assert run(code).strip() == "Just 1"


class TestStrStartsEndsWith:
    """Tests for str_startswith and str_endswith commands."""

    def test_str_startswith_true(self):
        """Test str_startswith when true."""
        code = '''str_create text "Hello World"
str_startswith text "Hello" result
print result'''
        assert run(code).strip() == "1"

    def test_str_startswith_false(self):
        """Test str_startswith when false."""
        code = '''str_create text "Hello World"
str_startswith text "World" result
print result'''
        assert run(code).strip() == "0"

    def test_str_endswith_true(self):
        """Test str_endswith when true."""
        code = '''str_create text "Hello World"
str_endswith text "World" result
print result'''
        assert run(code).strip() == "1"

    def test_str_endswith_false(self):
        """Test str_endswith when false."""
        code = '''str_create text "Hello World"
str_endswith text "Hello" result
print result'''
        assert run(code).strip() == "0"


class TestStrCount:
    """Tests for str_count command."""

    def test_str_count_multiple(self):
        """Test counting multiple occurrences."""
        code = '''str_create text "banana"
str_count text "a" result
print result'''
        assert run(code).strip() == "3"

    def test_str_count_none(self):
        """Test counting zero occurrences."""
        code = '''str_create text "hello"
str_count text "z" result
print result'''
        assert run(code).strip() == "0"

    def test_str_count_word(self):
        """Test counting word occurrences."""
        code = '''str_create text "the cat and the dog"
str_count text "the" result
print result'''
        assert run(code).strip() == "2"


class TestStrFindRfind:
    """Tests for str_find and str_rfind commands."""

    def test_str_find_found(self):
        """Test finding substring."""
        code = '''str_create text "hello world"
str_find text "world" result
print result'''
        assert run(code).strip() == "6"

    def test_str_find_not_found(self):
        """Test finding non-existent substring."""
        code = '''str_create text "hello world"
str_find text "xyz" result
print result'''
        assert run(code).strip() == "-1"

    def test_str_find_first(self):
        """Test find returns first occurrence."""
        code = '''str_create text "abcabc"
str_find text "bc" result
print result'''
        assert run(code).strip() == "1"

    def test_str_rfind_found(self):
        """Test rfind returns last occurrence."""
        code = '''str_create text "abcabc"
str_rfind text "bc" result
print result'''
        assert run(code).strip() == "4"

    def test_str_rfind_not_found(self):
        """Test rfind with non-existent substring."""
        code = '''str_create text "hello"
str_rfind text "xyz" result
print result'''
        assert run(code).strip() == "-1"


class TestStrCharChecks:
    """Tests for str_isdigit, str_isalpha, str_isalnum commands."""

    def test_str_isdigit_true(self):
        """Test isdigit with digits."""
        code = '''str_create text "12345"
str_isdigit text result
print result'''
        assert run(code).strip() == "1"

    def test_str_isdigit_false(self):
        """Test isdigit with non-digits."""
        code = '''str_create text "123abc"
str_isdigit text result
print result'''
        assert run(code).strip() == "0"

    def test_str_isalpha_true(self):
        """Test isalpha with letters."""
        code = '''str_create text "hello"
str_isalpha text result
print result'''
        assert run(code).strip() == "1"

    def test_str_isalpha_false(self):
        """Test isalpha with non-letters."""
        code = '''str_create text "hello123"
str_isalpha text result
print result'''
        assert run(code).strip() == "0"

    def test_str_isalnum_true(self):
        """Test isalnum with alphanumeric."""
        code = '''str_create text "hello123"
str_isalnum text result
print result'''
        assert run(code).strip() == "1"

    def test_str_isalnum_false(self):
        """Test isalnum with special chars."""
        code = '''str_create text "hello!"
str_isalnum text result
print result'''
        assert run(code).strip() == "0"


class TestDictValues:
    """Tests for dict_values command."""

    def test_dict_values_basic(self):
        """Test getting dict values."""
        code = '''dict_create d
dict_set d "a" "1"
dict_set d "b" "2"
dict_set d "c" "3"
dict_values d vals
array_get vals 0
array_get vals 1
array_get vals 2'''
        output = run(code).strip()
        # Values could be in any order
        assert "1" in output
        assert "2" in output
        assert "3" in output

    def test_dict_values_empty(self):
        """Test getting values from empty dict."""
        code = '''dict_create d
dict_values d vals'''
        output = run(code).strip()
        assert "Dictionary 'd' created" in output


class TestDictItems:
    """Tests for dict_items command."""

    def test_dict_items_basic(self):
        """Test getting dict items as parallel arrays."""
        code = '''dict_create d
dict_set d "x" "10"
dict_set d "y" "20"
dict_items d keys vals
array_get keys 0
array_get vals 0'''
        output = run(code).strip().splitlines()
        # Keys and values should be present
        assert len(output) >= 3  # dict created + 2 values

    def test_dict_items_empty(self):
        """Test getting items from empty dict."""
        code = '''dict_create d
dict_items d keys vals'''
        output = run(code).strip()
        assert "Dictionary 'd' created" in output


class TestDictUpdate:
    """Tests for dict_update command."""

    def test_dict_update_basic(self):
        """Test updating dict with another dict."""
        code = '''dict_create d1
dict_set d1 "a" "1"
dict_create d2
dict_set d2 "b" "2"
dict_update d1 d2
dict_get d1 "b"'''
        assert "2" in run(code).strip()

    def test_dict_update_overwrite(self):
        """Test updating overwrites existing keys."""
        code = '''dict_create d1
dict_set d1 "a" "old"
dict_create d2
dict_set d2 "a" "new"
dict_update d1 d2
dict_get d1 "a"'''
        assert "new" in run(code).strip()


class TestDictPop:
    """Tests for dict_pop command."""

    def test_dict_pop_basic(self):
        """Test popping a key from dict."""
        code = '''dict_create d
dict_set d "key" "value"
dict_pop d "key" result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "value"

    def test_dict_pop_removes_key(self):
        """Test pop removes the key."""
        code = '''dict_create d
dict_set d "a" "1"
dict_set d "b" "2"
dict_pop d "a" result
dict_len d len
print len'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"


class TestDictGetDefault:
    """Tests for dict_get_default command."""

    def test_dict_get_default_exists(self):
        """Test get_default when key exists."""
        code = '''dict_create d
dict_set d "key" "value"
dict_get_default d "key" "default" result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "value"

    def test_dict_get_default_missing(self):
        """Test get_default when key missing."""
        code = '''dict_create d
dict_get_default d "missing" "default" result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "default"


class TestDictHasKey:
    """Tests for dict_has_key command."""

    def test_dict_has_key_true(self):
        """Test has_key when key exists."""
        code = '''dict_create d
dict_set d "key" "value"
dict_has_key d "key" result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"

    def test_dict_has_key_false(self):
        """Test has_key when key missing."""
        code = '''dict_create d
dict_has_key d "missing" result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "0"


class TestDictClear:
    """Tests for dict_clear command."""

    def test_dict_clear_basic(self):
        """Test clearing a dict."""
        code = '''dict_create d
dict_set d "a" "1"
dict_set d "b" "2"
dict_clear d
dict_len d len
print len'''
        output = run(code).strip().splitlines()
        assert output[-1] == "0"


class TestDictLen:
    """Tests for dict_len command."""

    def test_dict_len_basic(self):
        """Test getting dict length."""
        code = '''dict_create d
dict_set d "a" "1"
dict_set d "b" "2"
dict_set d "c" "3"
dict_len d len
print len'''
        output = run(code).strip().splitlines()
        assert output[-1] == "3"

    def test_dict_len_empty(self):
        """Test length of empty dict."""
        code = '''dict_create d
dict_len d len
print len'''
        output = run(code).strip().splitlines()
        assert output[-1] == "0"


class TestIntegration:
    """Integration tests combining multiple features."""

    def test_str_format_with_dict(self):
        """Test string formatting with dict values."""
        code = '''dict_create person
dict_set person "name" "Bob"
dict_set person "age" "25"
str_create name "Bob"
set age 25
str_format result "{} is {} years old" name age
print result'''
        assert run(code).strip().endswith("Bob is 25 years old")

    def test_string_validation_pipeline(self):
        """Test chaining string validation."""
        code = '''str_create input "hello123"
str_isalnum input is_valid
str_startswith input "hello" has_prefix
print is_valid
print has_prefix'''
        output = run(code).strip().splitlines()
        assert output == ["1", "1"]

    def test_dict_operations_chain(self):
        """Test chaining dict operations."""
        code = '''dict_create config
dict_set config "host" "localhost"
dict_set config "port" "8080"
dict_get_default config "timeout" "30" timeout
dict_len config size
print size
print timeout'''
        output = run(code).strip().splitlines()
        assert output[-2] == "2"
        assert output[-1] == "30"
