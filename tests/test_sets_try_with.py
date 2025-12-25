"""Tests for set operations, try/catch/else/finally, and with statement (Todos 13, 14, 15)."""

import pytest
from techlang.interpreter import run


class TestSetCreate:
    """Tests for set_create command."""

    def test_set_create_basic(self):
        """Test creating an empty set."""
        code = "set_create s"
        output = run(code).strip()
        assert "Set 's' created" in output

    def test_set_create_multiple(self):
        """Test creating multiple sets."""
        code = '''set_create a
set_create b'''
        output = run(code).strip()
        assert "Set 'a' created" in output
        assert "Set 'b' created" in output


class TestSetAddRemove:
    """Tests for set_add and set_remove commands."""

    def test_set_add_number(self):
        """Test adding numbers to set."""
        code = '''set_create s
set_add s 1
set_add s 2
set_add s 3
set_len s len
print len'''
        output = run(code).strip().splitlines()
        assert output[-1] == "3"

    def test_set_add_string(self):
        """Test adding strings to set."""
        code = '''set_create s
str_create hello "hello"
set_add s hello
set_len s len
print len'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"

    def test_set_add_duplicate(self):
        """Test adding duplicates (should be ignored)."""
        code = '''set_create s
set_add s 1
set_add s 1
set_add s 1
set_len s len
print len'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"

    def test_set_remove(self):
        """Test removing from set."""
        code = '''set_create s
set_add s 1
set_add s 2
set_remove s 1
set_len s len
print len'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"


class TestSetContains:
    """Tests for set_contains command."""

    def test_set_contains_true(self):
        """Test contains when value present."""
        code = '''set_create s
set_add s 42
set_contains s 42 result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"

    def test_set_contains_false(self):
        """Test contains when value absent."""
        code = '''set_create s
set_add s 42
set_contains s 100 result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "0"


class TestSetOperations:
    """Tests for set operations (union, intersection, difference)."""

    def test_set_union(self):
        """Test union of two sets."""
        code = '''set_create a
set_create b
set_add a 1
set_add a 2
set_add b 2
set_add b 3
set_union a b result
set_len result len
print len'''
        output = run(code).strip().splitlines()
        assert output[-1] == "3"

    def test_set_intersection(self):
        """Test intersection of two sets."""
        code = '''set_create a
set_create b
set_add a 1
set_add a 2
set_add b 2
set_add b 3
set_intersection a b result
set_len result len
print len'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"

    def test_set_difference(self):
        """Test difference of two sets."""
        code = '''set_create a
set_create b
set_add a 1
set_add a 2
set_add a 3
set_add b 2
set_difference a b result
set_len result len
print len'''
        output = run(code).strip().splitlines()
        assert output[-1] == "2"

    def test_set_symmetric_difference(self):
        """Test symmetric difference of two sets."""
        code = '''set_create a
set_create b
set_add a 1
set_add a 2
set_add b 2
set_add b 3
set_symmetric_difference a b result
set_len result len
print len'''
        output = run(code).strip().splitlines()
        assert output[-1] == "2"


class TestSetSubsetSuperset:
    """Tests for subset/superset checks."""

    def test_set_issubset_true(self):
        """Test issubset when true."""
        code = '''set_create small
set_create big
set_add small 1
set_add big 1
set_add big 2
set_issubset small big result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"

    def test_set_issubset_false(self):
        """Test issubset when false."""
        code = '''set_create a
set_create b
set_add a 1
set_add a 3
set_add b 1
set_add b 2
set_issubset a b result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "0"

    def test_set_issuperset_true(self):
        """Test issuperset when true."""
        code = '''set_create big
set_create small
set_add big 1
set_add big 2
set_add small 1
set_issuperset big small result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"


class TestSetConversion:
    """Tests for set-array conversion."""

    def test_set_to_array(self):
        """Test converting set to array."""
        code = '''set_create s
set_add s 1
set_add s 2
set_add s 3
set_to_array s arr
array_get arr 0'''
        output = run(code).strip()
        # Value could be 1, 2, or 3 (set order not guaranteed)
        assert any(str(i) in output for i in [1, 2, 3])

    def test_array_to_set(self):
        """Test converting array to set (removes duplicates)."""
        code = '''array_create nums 5
array_set nums 0 1
array_set nums 1 2
array_set nums 2 2
array_set nums 3 3
array_set nums 4 3
array_to_set nums s
set_len s len
print len'''
        output = run(code).strip().splitlines()
        assert output[-1] == "3"


class TestTryCatchElseFinally:
    """Tests for enhanced try/catch with else/finally."""

    def test_try_catch_basic(self):
        """Test basic try/catch still works."""
        code = '''try
    print undefined_var
catch
    print "caught"
end'''
        output = run(code).strip()
        assert "caught" in output

    def test_try_else_no_error(self):
        """Test else runs when no error."""
        code = '''set x 10
try
    print x
else
    print "no error"
end'''
        output = run(code).strip()
        assert "no error" in output

    def test_try_else_with_error(self):
        """Test else doesn't run when error occurs."""
        code = '''try
    print undefined_var
catch
    print "caught"
else
    print "no error"
end'''
        output = run(code).strip()
        assert "caught" in output
        assert "no error" not in output

    def test_try_finally_always_runs(self):
        """Test finally always runs."""
        code = '''try
    print "try"
finally
    print "finally"
end'''
        output = run(code).strip()
        assert "try" in output
        assert "finally" in output

    def test_try_catch_finally(self):
        """Test finally runs after catch."""
        code = '''try
    print undefined_var
catch
    print "caught"
finally
    print "cleanup"
end'''
        output = run(code).strip()
        assert "caught" in output
        assert "cleanup" in output

    def test_try_else_finally(self):
        """Test full try/else/finally flow."""
        code = '''set x 5
try
    print x
else
    print "success"
finally
    print "done"
end'''
        output = run(code).strip()
        assert "5" in output
        assert "success" in output
        assert "done" in output

    def test_try_full_structure(self):
        """Test try/catch/else/finally all together."""
        code = '''set x 10
try
    print x
catch err
    print err
else
    print "no error"
finally
    print "cleanup"
end'''
        output = run(code).strip().splitlines()
        assert "10" in output
        assert "no error" in output
        assert "cleanup" in output


class TestWithStatement:
    """Tests for with statement (context managers)."""

    def test_with_timer(self):
        """Test with timer records elapsed time."""
        code = '''with timer as t do
    sleep 10
end
print t'''
        output = run(code).strip().splitlines()
        elapsed = int(output[-1])
        assert elapsed >= 10  # At least 10ms

    def test_with_suppress(self):
        """Test with suppress hides errors."""
        code = '''with suppress do
    print undefined_var
end
print "after"'''
        output = run(code).strip()
        assert "[Error:" not in output
        assert "after" in output

    def test_with_suppress_multiple_errors(self):
        """Test with suppress hides multiple errors."""
        code = '''with suppress do
    print undefined1
    print undefined2
end
print "ok"'''
        output = run(code).strip()
        assert "[Error:" not in output
        assert "ok" in output


class TestIntegration:
    """Integration tests combining multiple features."""

    def test_set_with_try_catch(self):
        """Test set operations with error handling."""
        code = '''set_create s
try
    set_add s 1
    set_add s 2
    set_len s len
    print len
else
    print "success"
finally
    set_clear s
    set_len s final_len
    print final_len
end'''
        output = run(code).strip().splitlines()
        assert "2" in output
        assert "success" in output
        assert output[-1] == "0"

    def test_remove_duplicates_pipeline(self):
        """Test using sets to remove duplicates from array."""
        code = '''array_create nums 7
array_set nums 0 1
array_set nums 1 2
array_set nums 2 2
array_set nums 3 3
array_set nums 4 3
array_set nums 5 3
array_set nums 6 4
array_to_set nums unique
set_len unique len
print len'''
        output = run(code).strip().splitlines()
        assert output[-1] == "4"
