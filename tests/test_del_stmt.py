"""
Tests for del Statement

Tests the del, del_array, and del_dict commands for deleting
variables, array elements, and dictionary keys.
"""

import pytest
from techlang.interpreter import run


class TestDelVariable:
    """Test del command for deleting variables."""
    
    def test_del_variable(self):
        """Test deleting a numeric variable"""
        code = """
        set x 42
        del x
        print x
        """
        output = run(code).strip()
        # Should error because x no longer exists
        assert "[Error:" in output or "not defined" in output.lower()
    
    def test_del_string(self):
        """Test deleting a string variable"""
        code = """
        str_create msg "hello"
        del msg
        print msg
        """
        output = run(code).strip()
        # Should error because msg no longer exists
        assert "[Error:" in output or "not defined" in output.lower() or "undefined" in output.lower()
    
    def test_del_array(self):
        """Test deleting an entire array"""
        code = """
        array_create nums
        array_push nums 1
        array_push nums 2
        del nums
        array_get nums 0
        """
        output = run(code).strip()
        # Should error because nums no longer exists
        assert "[Error:" in output or "does not exist" in output.lower()
    
    def test_del_dict(self):
        """Test deleting an entire dictionary"""
        code = """
        dict_create d
        dict_set d "key" "value"
        del d
        dict_get d "key"
        """
        output = run(code).strip()
        # Should error because d no longer exists
        assert "[Error:" in output or "does not exist" in output.lower()
    
    def test_del_nonexistent(self):
        """Test deleting non-existent variable gives error"""
        code = """
        del nonexistent
        """
        output = run(code).strip()
        assert "[Error:" in output


class TestDelArray:
    """Test del_array command for deleting array elements."""
    
    def test_del_array_element(self):
        """Test deleting element from array"""
        code = """
        array_create nums
        array_push nums 10
        array_push nums 20
        array_push nums 30
        del_array nums 1
        array_get nums 1
        """
        lines = run(code).strip().splitlines()
        # After deleting index 1 (20), index 1 should now be 30
        assert lines[-1] == "30"
    
    def test_del_array_first_element(self):
        """Test deleting first element"""
        code = """
        array_create arr
        array_push arr "a"
        array_push arr "b"
        array_push arr "c"
        del_array arr 0
        array_get arr 0
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "b"
    
    def test_del_array_last_element(self):
        """Test deleting last element"""
        code = """
        array_create arr
        array_push arr 1
        array_push arr 2
        array_push arr 3
        del_array arr 2
        array_len arr len
        print len
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "2"
    
    def test_del_array_out_of_bounds(self):
        """Test deleting with out of bounds index"""
        code = """
        array_create arr
        array_push arr 1
        del_array arr 5
        """
        output = run(code).strip()
        assert "[Error:" in output
    
    def test_del_array_nonexistent(self):
        """Test deleting from non-existent array"""
        code = """
        del_array nonexistent 0
        """
        output = run(code).strip()
        assert "[Error:" in output


class TestDelDict:
    """Test del_dict command for deleting dictionary keys."""
    
    def test_del_dict_key(self):
        """Test deleting key from dictionary"""
        code = """
        dict_create d
        dict_set d "name" "Alice"
        dict_set d "age" 30
        del_dict d "age"
        dict_has_key d "age" has_age
        print has_age
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "0"
    
    def test_del_dict_preserves_other_keys(self):
        """Test that deleting one key preserves others"""
        code = """
        dict_create d
        dict_set d "a" 1
        dict_set d "b" 2
        dict_set d "c" 3
        del_dict d "b"
        dict_get d "a"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "1"
    
    def test_del_dict_integer_key(self):
        """Test deleting integer key"""
        code = """
        dict_create d
        dict_set d 1 "one"
        dict_set d 2 "two"
        del_dict d 1
        dict_has_key d 1 has_one
        print has_one
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "0"
    
    def test_del_dict_nonexistent_key(self):
        """Test deleting non-existent key gives error"""
        code = """
        dict_create d
        dict_set d "a" 1
        del_dict d "nonexistent"
        """
        output = run(code).strip()
        assert "[Error:" in output
    
    def test_del_dict_nonexistent_dict(self):
        """Test deleting from non-existent dict"""
        code = """
        del_dict nonexistent "key"
        """
        output = run(code).strip()
        assert "[Error:" in output


class TestDelEdgeCases:
    """Test edge cases for del commands."""
    
    def test_del_error_no_args(self):
        """Test del without arguments gives error"""
        code = """
        del
        """
        output = run(code).strip()
        assert "[Error:" in output
    
    def test_del_array_error_no_index(self):
        """Test del_array without index gives error"""
        code = """
        array_create arr
        del_array arr
        """
        output = run(code).strip()
        assert "[Error:" in output
    
    def test_del_dict_error_no_key(self):
        """Test del_dict without key gives error"""
        code = """
        dict_create d
        del_dict d
        """
        output = run(code).strip()
        assert "[Error:" in output
    
    def test_del_and_recreate(self):
        """Test deleting and recreating variable"""
        code = """
        set x 10
        del x
        set x 20
        print x
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "20"
    
    def test_del_multiple_items(self):
        """Test deleting multiple items in sequence"""
        code = """
        set a 1
        set b 2
        set c 3
        del a
        del b
        print c
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "3"


class TestDelIntegration:
    """Integration tests for del commands."""
    
    def test_del_in_loop(self):
        """Test using del inside loop"""
        code = """
        array_create items
        array_push items 1
        array_push items 2
        array_push items 3
        array_push items 4
        
        del_array items 3
        del_array items 2
        del_array items 1
        del_array items 0
        
        array_len items len
        print len
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "0"
    
    def test_del_in_function(self):
        """Test del inside function"""
        code = """
        set global_var 100
        
        def cleanup do
            global global_var
            del global_var
        end
        
        call cleanup
        print global_var
        """
        output = run(code).strip()
        # Should error because global_var was deleted
        assert "[Error:" in output or "not defined" in output.lower()
    
    def test_cleanup_dict_entries(self):
        """Test cleaning up dictionary entries"""
        code = """
        dict_create cache
        dict_set cache "temp1" 100
        dict_set cache "temp2" 200
        dict_set cache "keep" 999
        
        del_dict cache "temp1"
        del_dict cache "temp2"
        
        dict_len cache len
        print len
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "1"
