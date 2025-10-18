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
