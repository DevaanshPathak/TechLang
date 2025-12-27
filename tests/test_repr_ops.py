"""
Tests for __str__ / __repr__ Equivalents

Tests the obj_str, obj_repr, and obj_display commands.
"""

import pytest
from techlang.interpreter import run


class TestObjStr:
    """Test obj_str command."""
    
    def test_obj_str_dataclass(self):
        """Test obj_str with dataclass instance"""
        code = """
        dataclass Point
            field x int 0
            field y int 0
        end
        dataclass_new Point p x=10 y=20
        obj_str p result
        print result
        """
        lines = run(code).strip().splitlines()
        assert "Point" in lines[-1]
        assert "10" in lines[-1] or "x" in lines[-1]
    
    def test_obj_str_class_instance(self):
        """Test obj_str with class instance"""
        code = """
        class Point
            field x int 0
            field y int 0
        end
        new Point p
        set_field p x 10
        set_field p y 20
        obj_str p result
        print result
        """
        lines = run(code).strip().splitlines()
        assert "Point" in lines[-1]
    
    def test_obj_str_nonexistent(self):
        """Test obj_str with non-existent instance"""
        code = """
        obj_str nonexistent result
        """
        output = run(code).strip()
        assert "[Error:" in output or "not a class" in output.lower()
    
    def test_obj_str_missing_args(self):
        """Test obj_str with missing arguments"""
        code = """
        obj_str
        """
        output = run(code).strip()
        assert "[Error:" in output or "requires" in output.lower()


class TestObjRepr:
    """Test obj_repr command."""
    
    def test_obj_repr_dataclass(self):
        """Test obj_repr with dataclass instance"""
        code = """
        dataclass Point
            field x int 0
            field y int 0
        end
        dataclass_new Point p x=10 y=20
        obj_repr p result
        print result
        """
        lines = run(code).strip().splitlines()
        assert "Point" in lines[-1]
    
    def test_obj_repr_class_instance(self):
        """Test obj_repr with class instance"""
        code = """
        class Vector
            field x int 0
            field y int 0
            field z int 0
        end
        new Vector v
        set_field v x 1
        set_field v y 2
        set_field v z 3
        obj_repr v result
        print result
        """
        lines = run(code).strip().splitlines()
        assert "Vector" in lines[-1]
    
    def test_obj_repr_missing_args(self):
        """Test obj_repr with missing arguments"""
        code = """
        obj_repr
        """
        output = run(code).strip()
        assert "[Error:" in output or "requires" in output.lower()


class TestObjDisplay:
    """Test obj_display command."""
    
    def test_obj_display_dataclass(self):
        """Test obj_display with dataclass instance"""
        code = """
        dataclass Person
            field name str "unknown"
            field age int 0
        end
        dataclass_new Person bob name="Bob" age=30
        obj_display bob
        """
        lines = run(code).strip().splitlines()
        output = lines[-1]
        assert "Person" in output
    
    def test_obj_display_class_instance(self):
        """Test obj_display with class instance"""
        code = """
        class Circle
            field radius int 0
        end
        new Circle c
        set_field c radius 5
        obj_display c
        """
        lines = run(code).strip().splitlines()
        assert "Circle" in lines[-1]
    
    def test_obj_display_nonexistent(self):
        """Test obj_display with non-existent instance"""
        code = """
        obj_display nonexistent
        """
        output = run(code).strip()
        assert "[Error:" in output or "not a class" in output.lower()
    
    def test_obj_display_missing_args(self):
        """Test obj_display with missing arguments"""
        code = """
        obj_display
        """
        output = run(code).strip()
        assert "[Error:" in output or "requires" in output.lower()
