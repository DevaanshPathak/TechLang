"""
Tests for pass Statement

Tests the pass command which does nothing (no-operation placeholder).
"""

import pytest
from techlang.interpreter import run


class TestPassBasic:
    """Test basic pass statement functionality."""
    
    def test_pass_does_nothing(self):
        """Test that pass is a valid statement that does nothing"""
        code = """
        pass
        print "done"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "done"
    
    def test_pass_in_function(self):
        """Test pass as function body placeholder"""
        code = """
        def empty_func do
            pass
        end
        
        call empty_func
        print "after"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "after"
    
    def test_pass_in_if_block(self):
        """Test pass in if block"""
        code = """
        set x 5
        if x > 0 do
            pass
        end
        print "executed"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "executed"
    
    def test_pass_in_loop(self):
        """Test pass in loop body"""
        code = """
        loop 3 do
            pass
        end
        print "loop done"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "loop done"
    
    def test_pass_multiple(self):
        """Test multiple pass statements"""
        code = """
        pass
        pass
        pass
        print "still works"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "still works"


class TestPassUseCases:
    """Test common use cases for pass."""
    
    def test_pass_placeholder_function(self):
        """Test pass as placeholder for not-yet-implemented function"""
        code = """
        def todo_func do
            pass
        end
        
        def implemented_func do
            print "working"
        end
        
        call todo_func
        call implemented_func
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "working"
    
    def test_pass_in_else_branch(self):
        """Test pass in else branch"""
        code = """
        set x 5
        if x > 10 do
            print "big"
        else
            pass
        end
        print "done"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "done"
    
    def test_pass_with_other_statements(self):
        """Test pass mixed with other statements"""
        code = """
        set x 1
        pass
        add x 1
        pass
        add x 1
        pass
        print x
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "3"
    
    def test_pass_preserves_state(self):
        """Test that pass doesn't modify any state"""
        code = """
        set a 10
        str_create s "hello"
        array_create arr
        array_push arr 1
        
        pass
        
        print a
        print s
        array_get arr 0
        """
        lines = run(code).strip().splitlines()
        assert lines[-3] == "10"
        assert lines[-2] == "hello"
        assert lines[-1] == "1"


class TestPassEdgeCases:
    """Test edge cases for pass statement."""
    
    def test_pass_at_start(self):
        """Test pass at start of program"""
        code = """
        pass
        set x 42
        print x
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "42"
    
    def test_pass_at_end(self):
        """Test pass at end of program"""
        code = """
        print "before"
        pass
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "before"
    
    def test_pass_only_program(self):
        """Test program with only pass"""
        code = """
        pass
        """
        output = run(code).strip()
        assert output == ""
    
    def test_pass_in_nested_blocks(self):
        """Test pass in deeply nested blocks"""
        code = """
        def outer do
            if 1 > 0 do
                loop 1 do
                    pass
                end
            end
        end
        
        call outer
        print "nested done"
        """
        lines = run(code).strip().splitlines()
        assert lines[-1] == "nested done"
