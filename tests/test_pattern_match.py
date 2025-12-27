"""
Tests for Full Pattern Matching

Tests the match_full command with enhanced pattern matching.
"""

import pytest
from techlang.interpreter import run


class TestPatternMatchOr:
    """Test OR patterns in match."""
    
    def test_or_pattern_match_first(self):
        """Test OR pattern matches first value"""
        code = """
        set x 1
        match_full x
            case_or 1 2 3 do
                print "small"
            end
            case _ do
                print "other"
            end
        end
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "small"
    
    def test_or_pattern_match_middle(self):
        """Test OR pattern matches middle value"""
        code = """
        set x 2
        match_full x
            case_or 1 2 3 do
                print "small"
            end
            case _ do
                print "other"
            end
        end
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "small"
    
    def test_or_pattern_no_match(self):
        """Test OR pattern falls through to default"""
        code = """
        set x 10
        match_full x
            case_or 1 2 3 do
                print "small"
            end
            case _ do
                print "other"
            end
        end
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "other"


class TestPatternMatchList:
    """Test list destructuring patterns."""
    
    def test_list_pattern_exact(self):
        """Test list pattern with exact match"""
        code = """
        array_create arr
        array_push arr 10
        array_push arr 20
        match_full arr
            case_list x y do
                print x
                print y
            end
            case _ do
                print "no match"
            end
        end
        """
        lines = run(code).strip().splitlines()
        assert lines[-2] == "10"
        assert lines[-1] == "20"
    
    def test_list_pattern_wrong_length(self):
        """Test list pattern with wrong length"""
        code = """
        array_create arr
        array_push arr 1
        array_push arr 2
        array_push arr 3
        match_full arr
            case_list x y do
                print "two"
            end
            case _ do
                print "default"
            end
        end
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "default"
    
    def test_list_pattern_with_rest(self):
        """Test list pattern with *rest syntax"""
        code = """
        array_create arr
        array_push arr 1
        array_push arr 2
        array_push arr 3
        array_push arr 4
        match_full arr
            case_list first *rest do
                print first
                array_len rest len
                print len
            end
        end
        """
        lines = run(code).strip().splitlines()
        assert lines[-2] == "1"
        assert lines[-1] == "3"  # rest has [2,3,4] = 3 elements


class TestPatternMatchDict:
    """Test dict destructuring patterns."""
    
    def test_dict_pattern_match(self):
        """Test dict pattern matches and extracts"""
        code = """
        dict_create d
        dict_set d "name" "Alice"
        dict_set d "age" 30
        match_full d
            case_dict name:n age:a do
                print n
                print a
            end
            case _ do
                print "no match"
            end
        end
        """
        lines = run(code).strip().splitlines()
        # dict_create outputs a message, so check last 2 lines
        assert "Alice" in lines[-2]
        assert "30" in lines[-1]
    
    def test_dict_pattern_missing_key(self):
        """Test dict pattern with missing key"""
        code = """
        dict_create d
        dict_set d "name" "Bob"
        match_full d
            case_dict name:n age:a do
                print "matched"
            end
            case _ do
                print "default"
            end
        end
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "default"


class TestPatternMatchSimple:
    """Test simple value patterns."""
    
    def test_simple_value_match(self):
        """Test simple value matching"""
        code = """
        set x 42
        match_full x
            case 42 do
                print "found 42"
            end
            case _ do
                print "not found"
            end
        end
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "found 42"
    
    def test_wildcard_match(self):
        """Test wildcard pattern"""
        code = """
        set x 999
        match_full x
            case 1 do
                print "one"
            end
            case _ do
                print "wildcard"
            end
        end
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "wildcard"
    
    def test_default_keyword(self):
        """Test default keyword as wildcard"""
        code = """
        set x 0
        match_full x
            case 1 do
                print "one"
            end
            case default do
                print "default case"
            end
        end
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "default case"


class TestPatternMatchErrors:
    """Test error handling in pattern matching."""
    
    def test_match_full_missing_value(self):
        """Test match_full with missing value"""
        code = """
        match_full
            case 1 do
                print "one"
            end
        end
        """
        output = run(code).strip()
        assert "[Error:" in output or "requires" in output.lower()
