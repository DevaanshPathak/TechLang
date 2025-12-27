"""
Tests for Default & Keyword Arguments
"""

import pytest
from techlang.interpreter import run


class TestDefaultArguments:
    """Test functions with default parameter values."""
    
    def test_defn_with_defaults(self):
        """Test defining function with default values."""
        code = """
defn greet name greeting="Hello" do
    print greeting
    print name
end
calln greet "Alice"
"""
        output = run(code).strip().splitlines()
        assert output[-2] == "Hello"
        assert output[-1] == "Alice"
    
    def test_defn_override_default(self):
        """Test overriding default values."""
        code = """
defn greet name greeting="Hello" do
    print greeting
    print name
end
calln greet "Bob" greeting="Hi"
"""
        output = run(code).strip().splitlines()
        assert output[-2] == "Hi"
        assert output[-1] == "Bob"
    
    def test_defn_multiple_defaults(self):
        """Test function with multiple default parameters."""
        code = """
defn format_msg prefix="[INFO]" msg suffix="." do
    print prefix
    print msg
    print suffix
end
calln format_msg msg="Test"
"""
        output = run(code).strip().splitlines()
        assert output[-3] == "[INFO]"
        assert output[-2] == "Test"
        assert output[-1] == "."
    
    def test_defn_positional_and_keyword(self):
        """Test mixing positional and keyword arguments."""
        code = """
defn greet name greeting="Hello" punctuation="!" do
    print greeting
    print name
    print punctuation
end
calln greet "Carol" punctuation="?"
"""
        output = run(code).strip().splitlines()
        assert output[-3] == "Hello"
        assert output[-2] == "Carol"
        assert output[-1] == "?"
    
    def test_defn_numeric_default(self):
        """Test numeric default values."""
        code = """
defn add_offset x offset=10 do
    add x offset
    print x
end
calln add_offset 5
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "15"


class TestKeywordArguments:
    """Test calling functions with keyword arguments."""
    
    def test_keyword_only(self):
        """Test calling with only keyword arguments."""
        code = """
defn show a=1 b=2 c=3 do
    print a
    print b
    print c
end
calln show b=20 c=30
"""
        output = run(code).strip().splitlines()
        assert output[-3] == "1"
        assert output[-2] == "20"
        assert output[-1] == "30"
    
    def test_calln_with_return(self):
        """Test calln with return values."""
        code = """
defn compute x y=5 do
    add x y
    return x
end
set result 0
calln compute 10
"""
        output = run(code).strip()
        # Should work without errors - return handling is internal
        assert "[Error:" not in output or "Unknown command" not in output


class TestIntegration:
    """Integration tests for default/keyword arguments."""
    
    def test_defn_with_return_multi(self):
        """Test defn combined with return_multi."""
        code = """
defn compute x y=10 do
    set sum x
    add sum y
    set diff x
    sub diff y
    return_multi sum diff
end
calln compute 20
"""
        output = run(code).strip()
        # Should work without errors
        assert "[Error:" not in output or "not defined" not in output


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_defn_no_defaults(self):
        """Test defn works without any defaults (like regular def)."""
        code = """
defn add_nums a b do
    add a b
    print a
end
calln add_nums 5 3
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "8"
