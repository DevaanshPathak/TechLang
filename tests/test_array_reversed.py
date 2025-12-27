"""
Tests for array_reversed (reversed() iterator)

Tests the array_reversed command which creates a reversed copy of an array.
"""

import pytest
from techlang.interpreter import run


class TestArrayReversed:
    """Test array_reversed command."""
    
    def test_array_reversed_basic(self):
        """Test basic reversed copy"""
        code = """
        array_create nums
        array_push nums 1
        array_push nums 2
        array_push nums 3
        array_reversed nums result
        array_get result 0 v1
        array_get result 1 v2
        array_get result 2 v3
        print v1
        print v2
        print v3
        """
        lines = run(code).strip().splitlines()
        assert lines[-3] == "3"
        assert lines[-2] == "2"
        assert lines[-1] == "1"
    
    def test_array_reversed_original_unchanged(self):
        """Test that original array is not modified"""
        code = """
        array_create nums
        array_push nums 10
        array_push nums 20
        array_push nums 30
        array_reversed nums result
        array_get nums 0 v
        print v
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "10"  # Original unchanged
    
    def test_array_reversed_empty(self):
        """Test reversed of empty array"""
        code = """
        array_create nums
        array_reversed nums result
        array_len result len
        print len
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "0"
    
    def test_array_reversed_single_element(self):
        """Test reversed of single element array"""
        code = """
        array_create nums
        array_push nums 42
        array_reversed nums result
        array_get result 0 v
        print v
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "42"
    
    def test_array_reversed_with_strings(self):
        """Test reversed with string elements"""
        code = """
        array_create words
        array_push words "a"
        array_push words "b"
        array_push words "c"
        array_reversed words result
        array_get result 0 v1
        array_get result 2 v3
        print v1
        print v3
        """
        lines = run(code).strip().splitlines()
        assert lines[-2] == "c"
        assert lines[-1] == "a"
    
    def test_array_reversed_nonexistent_array(self):
        """Test reversed with non-existent array"""
        code = """
        array_reversed nonexistent result
        """
        output = run(code).strip()
        assert "[Error:" in output or "does not exist" in output.lower()
    
    def test_array_reversed_missing_args(self):
        """Test reversed with missing arguments"""
        code = """
        array_reversed
        """
        output = run(code).strip()
        assert "[Error:" in output or "requires" in output.lower()
    
    def test_array_reversed_one_arg(self):
        """Test reversed with only one argument"""
        code = """
        array_create nums
        array_reversed nums
        """
        output = run(code).strip()
        assert "[Error:" in output or "requires" in output.lower()
    
    def test_array_reversed_large_array(self):
        """Test reversed with larger array"""
        code = """
        range 10 nums
        array_reversed nums result
        array_get result 0 first
        array_get result 9 last
        print first
        print last
        """
        lines = run(code).strip().splitlines()
        assert lines[-2] == "9"  # First element of reversed is 9
        assert lines[-1] == "0"  # Last element of reversed is 0
