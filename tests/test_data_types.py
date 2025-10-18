import pytest
from techlang.interpreter import run


class TestArrayOperations:
    """Test array creation, manipulation, and access operations"""
    
    def test_array_create(self):
        """Test array creation with valid size"""
        code = "array_create mylist 5"
        output = run(code)
        assert "Array 'mylist' created with size 5" in output
    
    def test_array_create_invalid_size(self):
        """Test array creation with negative size"""
        code = "array_create mylist -1"
        output = run(code)
        assert "Array size must be non-negative" in output
    
    def test_array_set_and_get(self):
        """Test setting and getting array values"""
        code = """
        array_create mylist 3
        array_set mylist 0 42
        array_set mylist 1 84
        array_set mylist 2 126
        array_get mylist 0
        array_get mylist 1
        array_get mylist 2
        """
        output = run(code)
        assert "42" in output
        assert "84" in output
        assert "126" in output
    
    def test_array_set_out_of_bounds(self):
        """Test setting array value out of bounds"""
        code = """
        array_create mylist 2
        array_set mylist 5 42
        """
        output = run(code)
        assert "Array index 5 out of bounds" in output
    
    def test_array_push_and_pop(self):
        """Test pushing and popping array values"""
        code = """
        array_create mylist 2
        array_set mylist 0 10
        array_set mylist 1 20
        array_push mylist 30
        array_pop mylist
        array_pop mylist
        """
        output = run(code)
        assert "30" in output
        assert "20" in output
    
    def test_array_pop_empty(self):
        """Test popping from empty array"""
        code = """
        array_create mylist 0
        array_push mylist 42
        array_pop mylist
        array_pop mylist
        """
        output = run(code)
        assert "Array 'mylist' is empty" in output

    def test_array_map_add(self):
        """Test array_map with add operation"""
        code = """
        array_create items 3
        array_set items 0 1
        array_set items 1 2
        array_set items 2 3
        array_map items plus add 5
        array_get plus 0
        array_get plus 1
        array_get plus 2
        """
        output = run(code)
        assert "Mapped array 'items' into 'plus' with op add 5 (items: 3)" in output
        assert "6" in output
        assert "7" in output
        assert "8" in output

    def test_array_filter_gt(self):
        """Test array_filter with greater-than predicate"""
        code = """
        array_create items 4
        array_set items 0 2
        array_set items 1 4
        array_set items 2 6
        array_set items 3 8
        array_filter items big gt 5
        array_get big 0
        array_get big 1
        """
        output = run(code)
        assert "Filtered array 'items' into 'big' with predicate gt 5 (kept 2/4)" in output
        assert "6" in output
        assert "8" in output


class TestStringOperations:
    """Test string creation, manipulation, and access operations"""
    
    def test_str_create(self):
        """Test string creation"""
        code = 'str_create mystring "hello"'
        output = run(code)
        # String creation doesn't output anything, just verify no errors
        assert "[Error:" not in output
    
    def test_str_concat(self):
        """Test string concatenation"""
        code = """
        str_create mystring "hello"
        str_concat mystring " world"
        print mystring
        """
        output = run(code)
        assert "hello world" in output
    
    def test_str_length(self):
        """Test string length calculation"""
        code = """
        str_create mystring "hello"
        str_length mystring
        """
        output = run(code)
        assert "5" in output
    
    def test_str_substring(self):
        """Test substring extraction"""
        code = """
        str_create mystring "hello world"
        str_substring mystring 0 5
        str_substring mystring 6 11
        """
        output = run(code)
        assert "hello" in output
        assert "world" in output
    
    def test_str_substring_invalid_range(self):
        """Test substring with invalid range"""
        code = """
        str_create mystring "hello"
        str_substring mystring 10 15
        """
        output = run(code)
        assert "Invalid substring range" in output

    def test_string_interpolate_success(self):
        """Test string interpolation fills placeholders"""
        code = """
        str_create name "Ada"
        set year 2024
        string_interpolate message "Hello {name}, welcome to {year}!"
        print message
        """
        output = run(code)
        assert "Hello Ada, welcome to 2024!" in output

    def test_string_interpolate_missing_placeholder(self):
        """Test interpolation reports missing placeholder"""
        code = """
        string_interpolate message "Hi {unknown}"
        """
        output = run(code)
        assert "Placeholder 'unknown' is not defined" in output

    def test_string_match_true_false(self):
        """Test regex matching returning 1 or 0"""
        code = """
        str_create sentence "The quick brown fox jumps over the lazy dog"
    string_match "fox" sentence hasfox
    print hasfox
    string_match "cat" sentence hascat
    print hascat
        """
        output = run(code)
        lines = [line.strip() for line in output.strip().splitlines()]
        assert "1" in lines
        assert "0" in lines

    def test_string_match_invalid_pattern(self):
        """Test regex errors surface as interpreter errors"""
        code = """
        str_create text "abc"
        string_match "(" text has_match
        """
        output = run(code)
        assert "Invalid regular expression" in output


class TestDictionaryOperations:
    """Test dictionary creation, manipulation, and access operations"""
    
    def test_dict_create(self):
        """Test dictionary creation"""
        code = "dict_create mydict"
        output = run(code)
        assert "Dictionary 'mydict' created" in output
    
    def test_dict_set_and_get(self):
        """Test setting and getting dictionary values"""
        code = """
        dict_create mydict
        dict_set mydict "name" "Alice"
        dict_set mydict "age" "25"
        dict_get mydict "name"
        dict_get mydict "age"
        """
        output = run(code)
        assert "Alice" in output
        assert "25" in output
    
    def test_dict_keys(self):
        """Test getting dictionary keys"""
        code = """
        dict_create mydict
        dict_set mydict "key1" "value1"
        dict_set mydict "key2" "value2"
        dict_keys mydict
        """
        output = run(code)
        assert "Keys[2]: key1, key2" in output

    def test_dict_keys_empty(self):
        """Test dictionary keys output when empty"""
        code = """
        dict_create empty
        dict_keys empty
        """
        output = run(code)
        assert "Keys[0]: (empty)" in output
    
    def test_dict_get_nonexistent_key(self):
        """Test getting value for nonexistent key"""
        code = """
        dict_create mydict
        dict_get mydict "nonexistent"
        """
        output = run(code)
        assert "Key 'nonexistent' not found" in output


class TestDataTypesIntegration:
    """Test integration between different data types"""
    
    def test_arrays_and_strings(self):
        """Test arrays and strings working together"""
        code = """
        array_create words 2
        array_set words 0 "hello"
        array_set words 1 "world"
        str_create sentence ""
        str_concat sentence "hello"
        str_concat sentence " world"
        print sentence
        """
        output = run(code)
        assert "hello world" in output
    
    def test_debug_shows_all_data_types(self):
        """Test that debug command shows all data types"""
        code = """
        array_create mylist 1
        str_create mystring "test"
        dict_create mydict
        debug
        """
        output = run(code)
        assert "Arrays:" in output
        assert "Strings:" in output
        assert "Dictionaries:" in output
        assert "mylist" in output
        assert "mystring" in output
        assert "mydict" in output
