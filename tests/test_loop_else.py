"""
Tests for Loop Else (loop_else, while_else, break, continue)
"""

import pytest
from techlang.interpreter import run


class TestBreak:
    """Test break command in loops"""
    
    def test_break_basic(self):
        """Test basic break command"""
        code = """
        set counter 0
        loop_else 10 do
            add counter 1
            if counter > 3
                break
            end
        else
            print "completed"
        end
        print counter
        """
        assert run(code).strip() == "4"


class TestLoopElse:
    """Loop else (loop_else, while_else, break)"""
    
    def test_loop_else_completes(self):
        """Test loop_else runs else when loop completes"""
        code = """
        loop_else 3 do
            print i
        else
            print "done"
        end
        """
        lines = run(code).strip().splitlines()
        assert lines == ["0", "1", "2", "done"]
    
    def test_loop_else_with_break(self):
        """Test loop_else doesn't run else when break is called"""
        code = """
        loop_else 10 do
            if i == 2
                break
            end
            print i
        else
            print "else"
        end
        print "after"
        """
        lines = run(code).strip().splitlines()
        assert lines == ["0", "1", "after"]
    
    def test_loop_else_search_found(self):
        """Test search pattern: found item with break"""
        code = """
        array_create nums
        array_push nums 10
        array_push nums 20
        array_push nums 30
        array_push nums 40
        array_push nums 50
        set target 30
        loop_else 5 do
            array_get nums i val
            if val == target
                print "found"
                break
            end
        else
            print "not found"
        end
        """
        assert run(code).strip() == "found"
    
    def test_loop_else_search_not_found(self):
        """Test search pattern: item not found"""
        code = """
        array_create nums
        array_push nums 10
        array_push nums 20
        array_push nums 30
        set target 99
        loop_else 3 do
            array_get nums i val
            if val == target
                print "found"
                break
            end
        else
            print "not found"
        end
        """
        assert run(code).strip() == "not found"


class TestWhileElse:
    """Test while_else construct"""
    
    def test_while_else_completes(self):
        """Test while_else runs else when condition becomes false"""
        code = """
        set x 0
        while_else x < 3 do
            print x
            add x 1
        else
            print "done"
        end
        """
        lines = run(code).strip().splitlines()
        assert lines == ["0", "1", "2", "done"]
    
    def test_while_else_with_break(self):
        """Test while_else doesn't run else when break is called"""
        code = """
        set x 0
        while_else x < 10 do
            if x == 2
                break
            end
            print x
            add x 1
        else
            print "else"
        end
        print "after"
        """
        lines = run(code).strip().splitlines()
        assert lines == ["0", "1", "after"]
