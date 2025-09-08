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
        assert "key1" in output
        assert "key2" in output
    
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
