"""
Tests for Pythonic Features:
- Feature 1: Dataclasses / Named Tuples
- Feature 2: Property Decorators (Getters/Setters)
- Feature 3: in / not in Operators
"""

import pytest
from techlang.interpreter import run


# ============================================================================
# Feature 1: Dataclasses / Named Tuples
# ============================================================================

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


# ============================================================================
# Feature 3: in / not in Operators
# ============================================================================

class TestInOperator:
    """Tests for 'in' operator."""
    
    def test_in_array_found(self):
        """Check if value exists in array."""
        code = '''
array_create nums 3
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
in 20 nums result
print result
'''
        lines = run(code).strip().splitlines()
        assert lines[-1] == "1"
    
    def test_in_array_not_found(self):
        """Check if value doesn't exist in array."""
        code = '''
array_create nums 3
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
in 99 nums result
print result
'''
        lines = run(code).strip().splitlines()
        assert lines[-1] == "0"
    
    def test_in_dict_key_found(self):
        """Check if key exists in dictionary."""
        code = '''
dict_create d
dict_set d "name" "Alice"
dict_set d "age" 30
in "name" d result
print result
'''
        lines = run(code).strip().splitlines()
        assert lines[-1] == "1"
    
    def test_in_dict_key_not_found(self):
        """Check if key doesn't exist in dictionary."""
        code = '''
dict_create d
dict_set d "name" "Alice"
in "email" d result
print result
'''
        lines = run(code).strip().splitlines()
        assert lines[-1] == "0"
    
    def test_in_string_substring_found(self):
        """Check if substring exists in string."""
        code = '''
str_create greeting "Hello World"
in "World" greeting result
print result
'''
        output = run(code).strip()
        assert output == "1"
    
    def test_in_string_substring_not_found(self):
        """Check if substring doesn't exist in string."""
        code = '''
str_create greeting "Hello World"
in "xyz" greeting result
print result
'''
        output = run(code).strip()
        assert output == "0"
    
    def test_in_set_found(self):
        """Check if value exists in set."""
        code = '''
set_create s
set_add s 10
set_add s 20
set_add s 30
in 20 s result
print result
'''
        lines = run(code).strip().splitlines()
        assert lines[-1] == "1"
    
    def test_in_set_not_found(self):
        """Check if value doesn't exist in set."""
        code = '''
set_create s
set_add s 10
set_add s 20
in 99 s result
print result
'''
        lines = run(code).strip().splitlines()
        assert lines[-1] == "0"


class TestNotInOperator:
    """Tests for 'not_in' operator."""
    
    def test_not_in_array_true(self):
        """not_in returns 1 when value not in array."""
        code = '''
array_create nums 3
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
not_in 99 nums result
print result
'''
        lines = run(code).strip().splitlines()
        assert lines[-1] == "1"
    
    def test_not_in_array_false(self):
        """not_in returns 0 when value is in array."""
        code = '''
array_create nums 3
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
not_in 20 nums result
print result
'''
        lines = run(code).strip().splitlines()
        assert lines[-1] == "0"
    
    def test_not_in_dict(self):
        """not_in with dictionary."""
        code = '''
dict_create d
dict_set d "name" "Alice"
not_in "email" d result
print result
'''
        lines = run(code).strip().splitlines()
        assert lines[-1] == "1"
    
    def test_not_in_string(self):
        """not_in with string."""
        code = '''
str_create greeting "Hello World"
not_in "xyz" greeting result
print result
'''
        lines = run(code).strip().splitlines()
        assert lines[-1] == "1"


class TestContainsOperator:
    """Tests for 'contains' operator (alternative syntax)."""
    
    def test_contains_array(self):
        """contains checks if array contains value."""
        code = '''
array_create nums 3
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
contains nums 20 result
print result
'''
        lines = run(code).strip().splitlines()
        assert lines[-1] == "1"
    
    def test_contains_dict(self):
        """contains checks if dict contains key."""
        code = '''
dict_create d
dict_set d "name" "Alice"
contains d "name" result
print result
'''
        lines = run(code).strip().splitlines()
        assert lines[-1] == "1"


class TestInWithVariables:
    """Test in/not_in with variable references."""
    
    def test_in_with_variable_value(self):
        """Check if variable value is in array."""
        code = '''
array_create nums 3
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
set target 20
in target nums result
print result
'''
        lines = run(code).strip().splitlines()
        assert lines[-1] == "1"
    
    def test_in_with_string_variable(self):
        """Check if string variable is in another string."""
        code = '''
str_create haystack "Hello World"
str_create needle "World"
in needle haystack result
print result
'''
        lines = run(code).strip().splitlines()
        assert lines[-1] == "1"


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests combining multiple features."""
    
    def test_dataclass_with_in_operator(self):
        """Use dataclass and in operator together."""
        code = '''
dataclass Item
    field name string ""
    field price int 0
end
dataclass_new Item i1 name="Apple" price=100
dataclass_to_dict i1 d
in "name" d hasName
in "price" d hasPrice
print hasName
print hasPrice
'''
        output = run(code).strip().splitlines()
        assert output == ["1", "1"]
    
    def test_in_operator_in_loop(self):
        """Use in operator within a loop."""
        code = '''
array_create allowed 3
array_set allowed 0 1
array_set allowed 1 3
array_set allowed 2 5
set count 0
loop 5
    set i count
    add i 1
    in i allowed found
    if found == 1
        print i
    end
    add count 1
end
'''
        lines = run(code).strip().splitlines()
        # Filter to get only the numeric outputs
        nums = [l for l in lines if l.isdigit()]
        assert nums == ["1", "3", "5"]


class TestEdgeCases:
    """Edge case tests."""
    
    def test_in_empty_array(self):
        """Check membership in empty array."""
        code = '''
array_create empty
in 5 empty result
print result
'''
        output = run(code).strip()
        assert output == "0"
    
    def test_in_empty_dict(self):
        """Check membership in empty dictionary."""
        code = '''
dict_create empty
in "key" empty result
print result
'''
        lines = run(code).strip().splitlines()
        assert lines[-1] == "0"
    
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
    
    def test_in_nonexistent_container(self):
        """Error when checking membership in nonexistent container."""
        code = '''
in 5 nonexistent result
'''
        output = run(code).strip()
        assert "Error" in output
