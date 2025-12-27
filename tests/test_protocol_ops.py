"""
Tests for Protocols and Abstract Base Classes

Tests protocol definitions, abstract classes, and runtime checking.
"""

import pytest
from techlang.interpreter import run


class TestProtocols:
    """Test protocol definitions and checking."""
    
    def test_protocol_definition(self):
        """Test defining a protocol"""
        code = """
        protocol Drawable
            abstract_method draw
            abstract_method resize width height
        end
        """
        output = run(code).strip()
        assert "Protocol 'Drawable' defined" in output
        assert "2 required methods" in output
    
    def test_implements_success(self):
        """Test class successfully implements protocol"""
        code = """
        protocol Drawable
            abstract_method draw
        end
        
        class Rectangle
            method draw do
                print "drawing"
            end
        end
        
        implements Rectangle Drawable
        """
        output = run(code).strip()
        assert "Class 'Rectangle' implements protocol 'Drawable'" in output
    
    def test_implements_missing_method(self):
        """Test class missing required method"""
        code = """
        protocol Drawable
            abstract_method draw
            abstract_method resize
        end
        
        class Rectangle
            method draw do
                print "drawing"
            end
        end
        
        implements Rectangle Drawable
        """
        output = run(code).strip()
        assert "[Error:" in output
        assert "does not implement required methods" in output
        assert "resize" in output
    
    def test_protocol_check_success(self):
        """Test protocol_check with implementing class"""
        code = """
        protocol Drawable
            abstract_method draw
        end
        
        class Rectangle
            method draw do
                print "drawing"
            end
        end
        
        implements Rectangle Drawable
        
        new Rectangle rect
        protocol_check rect Drawable result
        print result
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "1"
    
    def test_protocol_check_failure(self):
        """Test protocol_check with non-implementing class"""
        code = """
        protocol Drawable
            abstract_method draw
        end
        
        class Rectangle
            method area do
                print "100"
            end
        end
        
        new Rectangle rect
        protocol_check rect Drawable result
        print result
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "0"


class TestAbstractClasses:
    """Test abstract class definitions."""
    
    def test_abstract_class_definition(self):
        """Test defining an abstract class"""
        code = """
        abstract_class Shape
            abstract_method area
            abstract_method perimeter
        end
        """
        output = run(code).strip()
        assert "Abstract class 'Shape' defined" in output
        assert "2 abstract methods" in output
    
    def test_multiple_protocols(self):
        """Test object implementing multiple protocols"""
        code = """
        protocol Drawable
            abstract_method draw
        end
        
        protocol Resizable
            abstract_method resize
        end
        
        class Rectangle
            method draw do
                print "drawing"
            end
            method resize do
                print "resizing"
            end
        end
        
        implements Rectangle Drawable
        implements Rectangle Resizable
        """
        output = run(code).strip()
        assert "implements protocol 'Drawable'" in output
        assert "implements protocol 'Resizable'" in output


class TestStructuralTyping:
    """Test duck typing / structural conformance."""
    
    def test_structural_conformance(self):
        """Test protocol check with structural typing (no explicit implements)"""
        code = """
        protocol Drawable
            abstract_method draw
        end
        
        class Rectangle
            method draw do
                print "drawing"
            end
        end
        
        new Rectangle rect
        protocol_check rect Drawable result
        print result
        """
        lines = run(code).strip().splitlines()
        # Should pass because Rectangle has draw method (structural typing)
        assert lines[-1] == "1"
    
    def test_structural_non_conformance(self):
        """Test protocol check fails with missing method"""
        code = """
        protocol Drawable
            abstract_method draw
            abstract_method resize
        end
        
        class Rectangle
            method draw do
                print "drawing"
            end
        end
        
        new Rectangle rect
        protocol_check rect Drawable result
        print result
        """
        lines = run(code).strip().splitlines()
        # Should fail because Rectangle is missing resize method
        assert lines[-1] == "0"


class TestProtocolErrors:
    """Test error conditions for protocols."""
    
    def test_implements_undefined_class(self):
        """Test implements with undefined class"""
        code = """
        protocol Drawable
            abstract_method draw
        end
        
        implements NonExistent Drawable
        """
        output = run(code).strip()
        assert "[Error:" in output
        assert "not defined" in output
    
    def test_implements_undefined_protocol(self):
        """Test implements with undefined protocol"""
        code = """
        class Rectangle
            method draw do
                print "drawing"
            end
        end
        
        implements Rectangle NonExistent
        """
        output = run(code).strip()
        assert "[Error:" in output
        assert "not defined" in output
    
    def test_protocol_check_nonexistent_object(self):
        """Test protocol_check with nonexistent object"""
        code = """
        protocol Drawable
            abstract_method draw
        end
        
        protocol_check nonexistent Drawable result
        print result
        """
        lines = run(code).strip().splitlines()
        # Should set result to 0 if object doesn't exist
        assert lines[-1] == "0"
