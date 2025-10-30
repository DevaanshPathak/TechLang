"""Tests for debugger operations in TechLang."""
from techlang.interpreter import run


def test_breakpoint_sets_breakpoint():
    """Test that breakpoint command sets a breakpoint."""
    code = '''
    set x 10
    breakpoint
    set x 20
    '''
    output = run(code).strip()
    assert "[Breakpoint set at command" in output


def test_step_enables_stepping():
    """Test that step command enables step mode."""
    code = '''
    step
    set x 5
    '''
    output = run(code).strip()
    assert "[Step mode enabled" in output


def test_continue_from_pause():
    """Test continue command."""
    code = '''
    continue
    '''
    output = run(code).strip()
    assert "[Not currently paused]" in output


def test_inspect_shows_state():
    """Test inspect command shows state details."""
    code = '''
    set x 10
    set y 20
    inspect
    '''
    output = run(code).strip()
    assert "=== Debug Inspection" in output
    assert "Variables" in output


def test_watch_variable():
    """Test watching a variable."""
    code = '''
    watch myvar
    set myvar 42
    '''
    output = run(code).strip()
    assert "[Watching variable 'myvar']" in output


def test_unwatch_variable():
    """Test unwatching a variable."""
    code = '''
    watch x
    unwatch x
    '''
    output = run(code).strip()
    assert "[Stopped watching 'x']" in output


def test_clear_breakpoints():
    """Test clearing all breakpoints."""
    code = '''
    breakpoint
    breakpoint
    clear_breakpoints
    '''
    output = run(code).strip()
    assert "[Cleared" in output
    assert "breakpoint" in output


def test_inspect_with_arrays():
    """Test inspect shows arrays."""
    code = '''
    array_create nums 3
    array_set nums 0 10
    inspect
    '''
    output = run(code).strip()
    assert "Arrays:" in output
    assert "nums" in output


def test_inspect_with_strings():
    """Test inspect shows strings."""
    code = '''
    str_create greeting "hello"
    inspect
    '''
    output = run(code).strip()
    assert "Strings" in output


def test_inspect_with_dictionaries():
    """Test inspect shows dictionaries."""
    code = '''
    dict_create user
    dict_set user "name" "Alice"
    inspect
    '''
    output = run(code).strip()
    assert "Dictionaries:" in output
    assert "user" in output


def test_watch_shows_in_inspect():
    """Test watched variables appear in inspect output."""
    code = '''
    set x 10
    watch x
    inspect
    '''
    output = run(code).strip()
    assert "Watched Variables:" in output
    assert "x = 10" in output


def test_inspect_shows_command_count():
    """Test inspect shows command number."""
    code = '''
    set x 1
    set x 2
    inspect
    '''
    output = run(code).strip()
    assert "Command #" in output


def test_inspect_shows_current_value():
    """Test inspect shows current value."""
    code = '''
    set x 42
    inspect
    '''
    output = run(code).strip()
    assert "Current Value:" in output


def test_inspect_shows_stack():
    """Test inspect shows stack."""
    code = '''
    set x 10
    fork
    fork
    inspect
    '''
    output = run(code).strip()
    assert "Stack" in output


def test_multiple_breakpoints():
    """Test setting multiple breakpoints."""
    code = '''
    breakpoint
    set x 10
    breakpoint
    set x 20
    clear_breakpoints
    '''
    output = run(code).strip()
    lines = output.strip().splitlines()
    breakpoint_lines = [l for l in lines if "Breakpoint set" in l]
    assert len(breakpoint_lines) == 2


def test_watch_nonexistent_variable():
    """Test watching a variable that doesn't exist yet."""
    code = '''
    watch foo
    inspect
    '''
    output = run(code).strip()
    assert "[Watching variable 'foo']" in output
    assert "foo = <not defined>" in output


def test_unwatch_nonexistent():
    """Test unwatching a variable that wasn't watched."""
    code = '''
    unwatch bar
    '''
    output = run(code).strip()
    assert "was not being watched" in output


def test_debugger_with_loops():
    """Test debugger commands work with loops."""
    code = '''
    set count 0
    watch count
    loop 3
        add count 1
    end
    inspect
    '''
    output = run(code).strip()
    assert "Watched Variables:" in output


def test_debugger_with_functions():
    """Test debugger with function definitions."""
    code = '''
    def myfunc
        set result 42
        inspect
    end
    call myfunc
    '''
    output = run(code).strip()
    assert "Debug Inspection" in output


def test_inspect_limits_variable_display():
    """Test that inspect limits variable display when there are many."""
    code = '''
    set a 1
    set b 2
    set c 3
    set d 4
    set e 5
    set f 6
    set g 7
    inspect
    '''
    output = run(code).strip()
    # Should show count and sample
    assert "Variables[" in output


def test_watch_string_variable():
    """Test watching a string variable."""
    code = '''
    str_create msg "hello"
    watch msg
    inspect
    '''
    output = run(code).strip()
    assert 'msg = "hello"' in output


def test_breakpoint_and_step_together():
    """Test using breakpoint and step together."""
    code = '''
    breakpoint
    step
    set x 10
    '''
    output = run(code).strip()
    assert "[Breakpoint set" in output
    assert "[Step mode enabled" in output
