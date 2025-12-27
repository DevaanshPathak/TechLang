"""
Tests for Dataclasses / Named Tuples
"""

import pytest
from techlang.interpreter import run


class TestDataclassDefinition:
    """Tests for dataclass definition."""
    
    def test_dataclass_simple(self):
        """Define a simple dataclass."""
        code = '''
dataclass Point
    field x int 0
    field y int 0
end
print "defined"
'''
        output = run(code).strip()
        assert output == "defined"
    
    def test_dataclass_with_defaults(self):
        """Define a dataclass with default values."""
        code = '''
dataclass Person
    field name string ""
    field age int 0
    field active bool 1
end
print "ok"
'''
        output = run(code).strip()
        assert output == "ok"


class TestDataclassNew:
    """Tests for dataclass instantiation."""
    
    def test_dataclass_new_basic(self):
        """Create a dataclass instance with defaults."""
        code = '''
dataclass Point
    field x int 0
    field y int 0
end
dataclass_new Point p1
dataclass_get p1 x val
print val
'''
        output = run(code).strip()
        assert output == "0"
    
    def test_dataclass_new_with_values(self):
        """Create a dataclass instance with field values."""
        code = '''
dataclass Point
    field x int 0
    field y int 0
end
dataclass_new Point p1 x=10 y=20
dataclass_get p1 x xval
dataclass_get p1 y yval
print xval
print yval
'''
        output = run(code).strip().splitlines()
        assert output == ["10", "20"]
    
    def test_dataclass_new_partial_values(self):
        """Create a dataclass with some values overridden."""
        code = '''
dataclass Person
    field name string "Unknown"
    field age int 0
end
dataclass_new Person p1 name="Alice"
dataclass_get p1 name n
dataclass_get p1 age a
print n
print a
'''
        output = run(code).strip().splitlines()
        assert output == ["Alice", "0"]


class TestDataclassOperations:
    """Tests for dataclass operations."""
    
    def test_dataclass_set(self):
        """Set a field value in a dataclass."""
        code = '''
dataclass Point
    field x int 0
    field y int 0
end
dataclass_new Point p1
dataclass_set p1 x 42
dataclass_get p1 x val
print val
'''
        output = run(code).strip()
        assert output == "42"
    
    def test_dataclass_eq_equal(self):
        """Compare two equal dataclass instances."""
        code = '''
dataclass Point
    field x int 0
    field y int 0
end
dataclass_new Point p1 x=10 y=20
dataclass_new Point p2 x=10 y=20
dataclass_eq p1 p2 result
print result
'''
        output = run(code).strip()
        assert output == "1"
    
    def test_dataclass_eq_not_equal(self):
        """Compare two different dataclass instances."""
        code = '''
dataclass Point
    field x int 0
    field y int 0
end
dataclass_new Point p1 x=10 y=20
dataclass_new Point p2 x=5 y=15
dataclass_eq p1 p2 result
print result
'''
        output = run(code).strip()
        assert output == "0"
    
    def test_dataclass_str(self):
        """Get string representation of a dataclass."""
        code = '''
dataclass Point
    field x int 0
    field y int 0
end
dataclass_new Point p1 x=10 y=20
dataclass_str p1 s
print s
'''
        output = run(code).strip()
        assert "Point" in output
        assert "10" in output
        assert "20" in output
    
    def test_dataclass_to_dict(self):
        """Convert dataclass to dictionary."""
        code = '''
dataclass Point
    field x int 0
    field y int 0
end
dataclass_new Point p1 x=10 y=20
dataclass_to_dict p1 d
dict_get d "x"
'''
        lines = run(code).strip().splitlines()
        assert lines[-1] == "10"


class TestEdgeCases:
    """Edge case tests for dataclasses."""
    
    def test_dataclass_undefined_error(self):
        """Error when using undefined dataclass."""
        code = '''
dataclass_new UndefinedType x
'''
        output = run(code).strip()
        assert "Error" in output
    
    def test_dataclass_field_not_exist(self):
        """Error when accessing nonexistent field."""
        code = '''
dataclass Point
    field x int 0
end
dataclass_new Point p1
dataclass_get p1 z val
'''
        output = run(code).strip()
        assert "Error" in output
