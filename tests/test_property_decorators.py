"""
Tests for Property Decorators (Getters/Setters)

Note: Property decorators are implemented as part of the OOP system.
This file tests the @property-like functionality via get_field/set_field.
"""

import pytest
from techlang.interpreter import run


class TestPropertyGetters:
    """Tests for property getter functionality."""
    
    def test_get_field_basic(self):
        """Test basic field getter."""
        code = '''
class Point
    field x int 0
    field y int 0
end
new Point p1
set_field p1 x 42
get_field p1 x val
print val
'''
        output = run(code).strip()
        assert output == "42"
    
    def test_get_field_default_value(self):
        """Test getting default field value."""
        code = '''
class Counter
    field count int 0
end
new Counter c
get_field c count val
print val
'''
        output = run(code).strip()
        assert output == "0"


class TestPropertySetters:
    """Tests for property setter functionality."""
    
    def test_set_field_basic(self):
        """Test basic field setter."""
        code = '''
class Box
    field width int 0
    field height int 0
end
new Box b
set_field b width 100
set_field b height 50
get_field b width w
get_field b height h
print w
print h
'''
        output = run(code).strip().splitlines()
        assert output == ["100", "50"]
    
    def test_set_field_update(self):
        """Test updating field value multiple times."""
        code = '''
class Score
    field value int 0
end
new Score s
set_field s value 10
set_field s value 20
set_field s value 30
get_field s value final
print final
'''
        output = run(code).strip()
        assert output == "30"


class TestPropertyWithMethods:
    """Tests combining properties with methods."""
    
    def test_method_modifies_field(self):
        """Test method that modifies object fields."""
        code = '''
class Counter
    field count int 0
    method increment
        add count 1
    end
    method get_value
        return count
    end
end
new Counter ctr
call ctr.increment
call ctr.get_value val
print val
'''
        output = run(code).strip()
        assert "1" in output


class TestPropertyEdgeCases:
    """Edge cases for property access."""
    
    def test_get_nonexistent_field(self):
        """Error when getting nonexistent field."""
        code = '''
class Simple
    field x int 0
end
new Simple s
get_field s nonexistent val
'''
        output = run(code).strip()
        assert "Error" in output
    
    def test_set_nonexistent_field(self):
        """Error when setting nonexistent field."""
        code = '''
class Simple
    field x int 0
end
new Simple s
set_field s nonexistent 42
'''
        output = run(code).strip()
        assert "Error" in output
