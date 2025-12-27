"""
Tests for *args/**kwargs (Variadic Functions)
"""

import pytest
from techlang.interpreter import run


class TestVariadicArgs:
    """Test variadic functions with *args."""
    
    def test_defv_args_basic(self):
        """Test basic *args function."""
        code = """
defv sum_all *nums do
    set total 0
    loop 3 do
        array_get nums 0 val
        add total val
    end
    print total
end
callv sum_all 10 20 30
"""
        # Note: This is simplified since we don't have foreach yet
        output = run(code).strip().splitlines()
        assert output[-1] == "30"  # Only adds first value 3 times
    
    def test_defv_args_with_regular_param(self):
        """Test *args with regular parameters."""
        code = """
defv greet_all greeting *names do
    print greeting
end
callv greet_all "Hello" "Alice" "Bob" "Carol"
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "Hello"
    
    def test_defv_kwargs_basic(self):
        """Test basic **kwargs function."""
        code = """
defv config **settings do
    dict_has_key settings "host" has_host
    print has_host
end
callv config host="localhost" port=8080
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "1"


class TestVariadicKwargs:
    """Test variadic functions with **kwargs."""
    
    def test_defv_kwargs_only(self):
        """Test function with only **kwargs."""
        code = """
defv print_config **opts do
    dict_has_key opts "debug" has_debug
    print has_debug
end
callv print_config debug=1 verbose=0
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "1"
    
    def test_defv_args_and_kwargs(self):
        """Test function with both *args and **kwargs."""
        code = """
defv mixed first *rest **options do
    print first
    dict_has_key options "flag" has_flag
    print has_flag
end
callv mixed 1 2 3 flag=1
"""
        output = run(code).strip().splitlines()
        assert output[-2] == "1"
        assert output[-1] == "1"


class TestEdgeCases:
    """Test edge cases for variadic functions."""
    
    def test_empty_args(self):
        """Test variadic function with no extra args."""
        code = """
defv maybe_sum *nums do
    print "Called"
end
callv maybe_sum
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "Called"
