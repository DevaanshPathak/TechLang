"""
Tests for List Methods as Commands
"""

import pytest
from techlang.interpreter import run


class TestArrayInsert:
    """Test array_insert command"""
    
    def test_array_insert(self):
        """Test array_insert at specific index"""
        code = """
        array_create arr
        array_push arr 1
        array_push arr 3
        array_push arr 4
        array_insert arr 1 2
        set n 4
        set idx 0
        loop n
            array_get arr idx val
            print val
            add idx 1
        end
        """
        lines = run(code).strip().splitlines()
        assert lines == ["1", "2", "3", "4"]


class TestArrayExtend:
    """Test array_extend command"""
    
    def test_array_extend(self):
        """Test array_extend to combine arrays"""
        code = """
        array_create arr1
        array_push arr1 1
        array_push arr1 2
        array_create arr2
        array_push arr2 3
        array_push arr2 4
        array_extend arr1 arr2
        array_len arr1 len
        print len
        """
        assert run(code).strip() == "4"


class TestArrayClear:
    """Test array_clear command"""
    
    def test_array_clear(self):
        """Test array_clear removes all elements"""
        code = """
        array_create arr
        array_push arr 1
        array_push arr 2
        array_push arr 3
        array_clear arr
        array_len arr len
        print len
        """
        assert run(code).strip() == "0"


class TestArrayCopy:
    """Test array_copy command"""
    
    def test_array_copy(self):
        """Test array_copy creates shallow copy"""
        code = """
        array_create src
        array_push src 10
        array_push src 20
        array_push src 30
        array_copy src dest
        array_get dest 1 val
        print val
        """
        assert run(code).strip() == "20"


class TestArrayCount:
    """Test array_count command"""
    
    def test_array_count(self):
        """Test array_count occurrences"""
        code = """
        array_create arr
        array_push arr 1
        array_push arr 2
        array_push arr 1
        array_push arr 3
        array_push arr 1
        array_count arr 1 cnt
        print cnt
        """
        assert run(code).strip() == "3"


class TestArrayRemove:
    """Test array_remove command"""
    
    def test_array_remove(self):
        """Test array_remove first occurrence"""
        code = """
        array_create arr
        array_push arr 1
        array_push arr 2
        array_push arr 1
        array_push arr 3
        array_remove arr 1
        array_len arr len
        array_get arr 0 first
        print len
        print first
        """
        lines = run(code).strip().splitlines()
        assert lines == ["3", "2"]


class TestArrayLen:
    """Test array_len command"""
    
    def test_array_len(self):
        """Test array_len returns correct length"""
        code = """
        array_create arr
        array_push arr 1
        array_push arr 2
        array_push arr 3
        array_push arr 4
        array_push arr 5
        array_len arr len
        print len
        """
        assert run(code).strip() == "5"


class TestArrayIndex:
    """Test array_index command"""
    
    def test_array_index(self):
        """Test array_index finds value index"""
        code = """
        array_create arr
        array_push arr 10
        array_push arr 20
        array_push arr 30
        array_push arr 40
        array_index arr 30 idx
        print idx
        """
        assert run(code).strip() == "2"
    
    def test_array_index_not_found(self):
        """Test array_index returns -1 when not found"""
        code = """
        array_create arr
        array_push arr 1
        array_push arr 2
        array_push arr 3
        array_index arr 99 idx
        print idx
        """
        assert run(code).strip() == "-1"
