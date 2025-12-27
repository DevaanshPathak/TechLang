"""
Tests for Dict Methods
- dict_setdefault: Set default value if key doesn't exist
- dict_copy: Create a shallow copy of a dictionary  
- dict_fromkeys: Create dict from array of keys with default value
- dict_merge: Merge two dictionaries into a new one
"""

import pytest
from techlang.interpreter import run


class TestDictSetdefault:
    """Test dict_setdefault command"""
    
    def test_setdefault_new_key(self):
        """Test dict_setdefault adds key when not present"""
        code = """
        dict_create d
        dict_setdefault d "name" "Alice"
        dict_get d "name"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "Alice"
    
    def test_setdefault_existing_key(self):
        """Test dict_setdefault doesn't override existing key"""
        code = """
        dict_create d
        dict_set d "name" "Bob"
        dict_setdefault d "name" "Alice"
        dict_get d "name"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "Bob"
    
    def test_setdefault_numeric_value(self):
        """Test dict_setdefault with numeric default"""
        code = """
        dict_create d
        dict_setdefault d "count" 0
        dict_get d "count"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "0"
    
    def test_setdefault_from_variable(self):
        """Test dict_setdefault with variable as default"""
        code = """
        dict_create d
        set default_val 42
        dict_setdefault d "value" default_val
        dict_get d "value"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "42"


class TestDictCopy:
    """Test dict_copy command"""
    
    def test_copy_basic(self):
        """Test dict_copy creates independent copy"""
        code = """
        dict_create original
        dict_set original "a" 1
        dict_set original "b" 2
        dict_copy original copy
        dict_get copy "a"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "1"
    
    def test_copy_independence(self):
        """Test modifications to copy don't affect original"""
        code = """
        dict_create original
        dict_set original "key" "value1"
        dict_copy original copy
        dict_set copy "key" "value2"
        dict_get original "key"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "value1"
    
    def test_copy_preserves_all_keys(self):
        """Test dict_copy preserves all keys"""
        code = """
        dict_create original
        dict_set original "a" 1
        dict_set original "b" 2
        dict_set original "c" 3
        dict_copy original copy
        dict_len copy len
        print len
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "3"


class TestDictFromkeys:
    """Test dict_fromkeys command"""
    
    def test_fromkeys_basic(self):
        """Test dict_fromkeys creates dict from array keys"""
        code = """
        array_create keys
        array_push keys "a"
        array_push keys "b"
        array_push keys "c"
        dict_fromkeys keys 0 result
        dict_get result "a"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "0"
    
    def test_fromkeys_all_same_value(self):
        """Test dict_fromkeys sets all values to same default"""
        code = """
        array_create keys
        array_push keys "x"
        array_push keys "y"
        dict_fromkeys keys "default" result
        dict_get result "x"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "default"
    
    def test_fromkeys_length(self):
        """Test dict_fromkeys creates correct number of keys"""
        code = """
        array_create keys
        array_push keys "one"
        array_push keys "two"
        array_push keys "three"
        dict_fromkeys keys 0 result
        dict_len result len
        print len
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "3"


class TestDictMerge:
    """Test dict_merge command"""
    
    def test_merge_basic(self):
        """Test dict_merge combines two dicts"""
        code = """
        dict_create d1
        dict_set d1 "a" 1
        dict_create d2
        dict_set d2 "b" 2
        dict_merge d1 d2 result
        dict_len result len
        print len
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "2"
    
    def test_merge_second_wins(self):
        """Test dict_merge gives priority to second dict"""
        code = """
        dict_create d1
        dict_set d1 "key" "from_d1"
        dict_create d2
        dict_set d2 "key" "from_d2"
        dict_merge d1 d2 result
        dict_get result "key"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "from_d2"
    
    def test_merge_preserves_originals(self):
        """Test dict_merge doesn't modify originals"""
        code = """
        dict_create d1
        dict_set d1 "a" 1
        dict_create d2
        dict_set d2 "b" 2
        dict_merge d1 d2 result
        dict_has_key d1 "b" has_b
        print has_b
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "0"
    
    def test_merge_empty_dicts(self):
        """Test dict_merge with empty dicts"""
        code = """
        dict_create d1
        dict_create d2
        dict_merge d1 d2 result
        dict_len result len
        print len
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "0"


class TestDictMethodsIntegration:
    """Integration tests for dict methods"""
    
    def test_setdefault_with_copy(self):
        """Test combining setdefault and copy"""
        code = """
        dict_create config
        dict_setdefault config "host" "localhost"
        dict_setdefault config "port" 8080
        dict_copy config backup
        dict_set config "port" 9000
        dict_get backup "port"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "8080"
    
    def test_fromkeys_then_merge(self):
        """Test creating dict from keys then merging"""
        code = """
        array_create keys
        array_push keys "x"
        array_push keys "y"
        dict_fromkeys keys 0 defaults
        dict_create overrides
        dict_set overrides "x" 100
        dict_merge defaults overrides result
        dict_get result "x"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "100"
