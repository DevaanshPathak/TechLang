from techlang.interpreter import run


def test_macro_expands_inline_body():
    code = """
    macro greet name do
        print "Hello"
        print $name
    end
    inline greet "World"
    """
    output = run(code)
    lines = output.splitlines()
    assert lines == ["Hello", "World"]


def test_macro_parameter_substitution_with_variables():
    code = """
    macro inc var do
        add $var 1
    end
    set counter 1
    inline inc counter
    print counter
    """
    output = run(code)
    assert output.strip() == "2"


def test_recursive_macro_reports_error():
    code = """
    macro loopback do
        inline loopback
    end
    inline loopback
    """
    output = run(code)
    assert "Recursive macro expansion detected" in output
    assert "loopback" in output


def test_conditional_macro_expansion():
    """Test that conditional macros work with state from REPL-style execution."""
    # Note: Conditional macros check state when process_macros() is called
    # In regular file execution, this happens before any code runs
    # So conditional macros are most useful in REPL or when using persistent state
    
    # Test 1: Variable set before macro processing (simulating REPL)
    from techlang.core import InterpreterState
    from techlang.parser import parse
    from techlang.macros import MacroHandler
    from techlang.aliases import AliasHandler
    from techlang.executor import CommandExecutor
    
    state = InterpreterState()
    state.set_variable("debug", 1)
    
    code = """
    macro log if debug msg do
        print "DEBUG:"
        print $msg
    end
    inline log "test message"
    """
    
    tokens = parse(code)
    tokens = MacroHandler.process_macros(tokens, state)
    tokens = AliasHandler.process_aliases(tokens, state)
    executor = CommandExecutor(state, ".")
    executor.execute_block(tokens)
    
    output = state.get_output()
    assert "DEBUG:" in output
    assert "test message" in output


def test_nested_macro_expansion():
    """Test that macros can expand other macros."""
    code = """
    macro inner x do
        print $x
    end
    macro outer y do
        inline inner $y
    end
    inline outer "nested"
    """
    output = run(code)
    assert output.strip() == "nested"


def test_macro_with_multiple_parameters():
    """Test macros with multiple parameters."""
    code = """
    macro add_and_print a b do
        add $a $b
        print $a
    end
    set x 5
    set y 10
    inline add_and_print x y
    """
    output = run(code)
    assert output.strip() == "15"
