"""
Tests for Walrus Operator := (Assignment Expressions)
"""

import pytest
from techlang.interpreter import run


class TestAssignExpr:
    """Test standalone assignment expressions."""
    
    def test_assign_expr_basic(self):
        """Test basic assignment expression."""
        code = """
assign_expr x := 42
print x
"""
        output = run(code).strip().splitlines()
        assert "42" in output  # Output includes the assignment value
    
    def test_assign_expr_from_variable(self):
        """Test assignment expression from existing variable."""
        code = """
set y 100
assign_expr x := y
print x
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "100"


class TestIfAssign:
    """Test walrus operator in if conditions."""
    
    def test_if_assign_true_condition(self):
        """Test if_assign when condition is true."""
        code = """
str_create mystring "Hello World"
if_assign n := str_length mystring > 5 do
    print "Long string"
    print n
end
"""
        output = run(code).strip().splitlines()
        assert "Long string" in output
        assert "11" in output
    
    def test_if_assign_false_condition(self):
        """Test if_assign when condition is false."""
        code = """
str_create mystring "Hi"
if_assign n := str_length mystring > 5 do
    print "Should not print"
end
print "Done"
"""
        output = run(code).strip().splitlines()
        assert "Should not print" not in output
        assert output[-1] == "Done"
    
    def test_if_assign_variable_available(self):
        """Test that assigned variable is available after if."""
        code = """
str_create mystring "Test"
if_assign n := str_length mystring > 2 do
    print "Condition met"
end
print n
"""
        output = run(code).strip().splitlines()
        assert output[-1] == "4"


class TestWhileAssign:
    """Test walrus operator in while loops."""
    
    def test_while_assign_basic(self):
        """Test while_assign with array iteration."""
        code = """
array_create nums 3
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
set idx 0
while idx < 3 do
    array_get nums idx
    add idx 1
end
"""
        output = run(code).strip().splitlines()
        # Should print 10, 20, 30
        assert "10" in output
        assert "20" in output
        assert "30" in output
