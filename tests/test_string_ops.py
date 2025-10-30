"""Tests for enhanced string operations in TechLang."""
from techlang.interpreter import run


def test_str_split_basic():
    """Test splitting a string by delimiter."""
    code = """
    str_create text "hello world test"
    str_split text " " parts
    array_get parts 0
    array_get parts 1
    array_get parts 2
    """
    output = run(code).strip().splitlines()
    assert "String split into 3 parts" in output[0]
    assert output[1] == "hello"
    assert output[2] == "world"
    assert output[3] == "test"


def test_str_split_comma_delimiter():
    """Test splitting with comma delimiter."""
    code = """
    str_create csv "apple,banana,cherry"
    str_split csv "," fruits
    array_get fruits 0
    array_get fruits 1
    array_get fruits 2
    """
    output = run(code).strip().splitlines()
    assert "String split into 3 parts" in output[0]
    assert output[1] == "apple"
    assert output[2] == "banana"
    assert output[3] == "cherry"


def test_str_split_nonexistent_string():
    """Test splitting a nonexistent string."""
    code = 'str_split missing " " result'
    output = run(code).strip()
    assert "[Error: String 'missing' does not exist]" in output


def test_str_replace_basic():
    """Test replacing substrings."""
    code = """
    str_create message "hello world"
    str_replace message "world" "universe"
    print message
    """
    assert run(code).strip() == "hello universe"


def test_str_replace_multiple_occurrences():
    """Test replacing all occurrences."""
    code = """
    str_create text "foo bar foo baz foo"
    str_replace text "foo" "qux"
    print text
    """
    assert run(code).strip() == "qux bar qux baz qux"


def test_str_replace_no_match():
    """Test replacing when substring doesn't exist."""
    code = """
    str_create text "hello world"
    str_replace text "xyz" "abc"
    print text
    """
    assert run(code).strip() == "hello world"


def test_str_replace_nonexistent_string():
    """Test replacing in nonexistent string."""
    code = 'str_replace missing "old" "new"'
    output = run(code).strip()
    assert "[Error: String 'missing' does not exist]" in output


def test_str_trim_whitespace():
    """Test trimming whitespace."""
    code = """
    str_create text "  hello world  "
    str_trim text
    print text
    """
    assert run(code).strip() == "hello world"


def test_str_trim_tabs_and_newlines():
    """Test trimming tabs and newlines."""
    # Note: TechLang strings are literals, so \\t is two chars, not a tab
    code = """
    str_create text "   hello   "
    str_trim text
    print text
    """
    assert run(code).strip() == "hello"


def test_str_trim_no_whitespace():
    """Test trimming when no whitespace exists."""
    code = """
    str_create text "hello"
    str_trim text
    print text
    """
    assert run(code).strip() == "hello"


def test_str_trim_nonexistent_string():
    """Test trimming nonexistent string."""
    code = "str_trim missing"
    output = run(code).strip()
    assert "[Error: String 'missing' does not exist]" in output


def test_str_upper_basic():
    """Test converting to uppercase."""
    code = """
    str_create text "hello world"
    str_upper text
    print text
    """
    assert run(code).strip() == "HELLO WORLD"


def test_str_upper_mixed_case():
    """Test uppercase with mixed case input."""
    code = """
    str_create text "HeLLo WoRLd"
    str_upper text
    print text
    """
    assert run(code).strip() == "HELLO WORLD"


def test_str_upper_already_uppercase():
    """Test uppercase on already uppercase text."""
    code = """
    str_create text "HELLO"
    str_upper text
    print text
    """
    assert run(code).strip() == "HELLO"


def test_str_upper_nonexistent_string():
    """Test uppercase on nonexistent string."""
    code = "str_upper missing"
    output = run(code).strip()
    assert "[Error: String 'missing' does not exist]" in output


def test_str_lower_basic():
    """Test converting to lowercase."""
    code = """
    str_create text "HELLO WORLD"
    str_lower text
    print text
    """
    assert run(code).strip() == "hello world"


def test_str_lower_mixed_case():
    """Test lowercase with mixed case input."""
    code = """
    str_create text "HeLLo WoRLd"
    str_lower text
    print text
    """
    assert run(code).strip() == "hello world"


def test_str_lower_already_lowercase():
    """Test lowercase on already lowercase text."""
    code = """
    str_create text "hello"
    str_lower text
    print text
    """
    assert run(code).strip() == "hello"


def test_str_lower_nonexistent_string():
    """Test lowercase on nonexistent string."""
    code = "str_lower missing"
    output = run(code).strip()
    assert "[Error: String 'missing' does not exist]" in output


def test_str_contains_found():
    """Test checking if substring exists (found)."""
    code = """
    str_create text "hello world"
    str_contains text "world"
    """
    assert run(code).strip() == "1"


def test_str_contains_not_found():
    """Test checking if substring exists (not found)."""
    code = """
    str_create text "hello world"
    str_contains text "universe"
    """
    assert run(code).strip() == "0"


def test_str_contains_partial_match():
    """Test substring matching with partial word."""
    code = """
    str_create text "testing"
    str_contains text "test"
    """
    assert run(code).strip() == "1"


def test_str_contains_case_sensitive():
    """Test that contains is case-sensitive."""
    code = """
    str_create text "Hello World"
    str_contains text "hello"
    """
    assert run(code).strip() == "0"


def test_str_contains_nonexistent_string():
    """Test contains on nonexistent string."""
    code = 'str_contains missing "test"'
    output = run(code).strip()
    assert "[Error: String 'missing' does not exist]" in output


def test_str_reverse_basic():
    """Test reversing a string."""
    code = """
    str_create text "hello"
    str_reverse text
    print text
    """
    assert run(code).strip() == "olleh"


def test_str_reverse_palindrome():
    """Test reversing a palindrome."""
    code = """
    str_create text "racecar"
    str_reverse text
    print text
    """
    assert run(code).strip() == "racecar"


def test_str_reverse_with_spaces():
    """Test reversing string with spaces."""
    code = """
    str_create text "hello world"
    str_reverse text
    print text
    """
    assert run(code).strip() == "dlrow olleh"


def test_str_reverse_nonexistent_string():
    """Test reversing nonexistent string."""
    code = "str_reverse missing"
    output = run(code).strip()
    assert "[Error: String 'missing' does not exist]" in output


def test_string_operations_chaining():
    """Test chaining multiple string operations."""
    code = """
    str_create text "  HELLO WORLD  "
    str_trim text
    str_lower text
    str_replace text "world" "universe"
    print text
    """
    assert run(code).strip() == "hello universe"


def test_str_split_then_process():
    """Test splitting and processing results."""
    code = """
    str_create data "apple,BANANA,Cherry"
    str_split data "," items
    array_get items 1
    """
    output = run(code).strip().splitlines()
    assert output[-1] == "BANANA"


def test_case_conversion_preserves_non_letters():
    """Test that case conversion preserves numbers and symbols."""
    code = """
    str_create text "Hello123!@#"
    str_upper text
    print text
    """
    assert run(code).strip() == "HELLO123!@#"


def test_empty_string_operations():
    """Test operations on empty strings."""
    code = """
    str_create empty ""
    str_upper empty
    str_reverse empty
    str_trim empty
    str_length empty
    """
    assert run(code).strip() == "0"


def test_str_replace_with_empty_string():
    """Test replacing with empty string (deletion)."""
    code = """
    str_create text "hello world"
    str_replace text " " ""
    print text
    """
    assert run(code).strip() == "helloworld"


def test_str_contains_empty_substring():
    """Test contains with empty substring."""
    code = """
    str_create text "hello"
    str_contains text ""
    """
    assert run(code).strip() == "1"  # Empty string is always contained


def test_str_split_single_char_delimiter():
    """Test splitting by single character delimiter."""
    code = """
    str_create text "a:b:c"
    str_split text ":" chars
    array_get chars 0
    array_get chars 1
    array_get chars 2
    """
    output = run(code).strip().splitlines()
    assert "String split into 3 parts" in output[0]
    assert output[1] == "a"
    assert output[2] == "b"
    assert output[3] == "c"
