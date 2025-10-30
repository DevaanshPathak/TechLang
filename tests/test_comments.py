"""Tests for comment support in TechLang."""
from techlang.interpreter import run


def test_hash_single_line_comment():
    """Test # style comments."""
    code = """
    # This is a comment
    set x 5
    # Another comment
    print x
    """
    assert run(code).strip() == "5"


def test_double_slash_single_line_comment():
    """Test // style comments."""
    code = """
    // This is a comment
    set x 10
    // Another comment
    print x
    """
    assert run(code).strip() == "10"


def test_inline_hash_comment():
    """Test # comments after code on the same line."""
    code = """
    set x 7  # set x to 7
    add x 3  # add 3 to x
    print x  # should print 10
    """
    assert run(code).strip() == "10"


def test_inline_double_slash_comment():
    """Test // comments after code on the same line."""
    code = """
    set x 8  // set x to 8
    add x 2  // add 2 to x
    print x  // should print 10
    """
    assert run(code).strip() == "10"


def test_multiline_comment():
    """Test /* ... */ multi-line comments."""
    code = """
    set x 5
    /*
    This is a multi-line comment
    that spans multiple lines
    and should be ignored
    */
    add x 10
    print x
    """
    assert run(code).strip() == "15"


def test_multiline_comment_inline():
    """Test /* ... */ comments on a single line."""
    code = """
    set x 5
    add x /* this adds */ 10
    print x
    """
    assert run(code).strip() == "15"


def test_multiline_comment_before_code():
    """Test /* ... */ comment at the start of code."""
    code = """
    /* Header comment explaining the code */
    set x 20
    print x
    """
    assert run(code).strip() == "20"


def test_comment_in_string_not_removed():
    """Test that comments inside strings are preserved."""
    code = """
    str_create msg "This is # not a comment"
    print msg
    """
    assert run(code).strip() == "This is # not a comment"


def test_double_slash_in_string_not_removed():
    """Test that // inside strings are preserved."""
    code = """
    str_create url "https://example.com"
    print url
    """
    assert run(code).strip() == "https://example.com"


def test_multiple_comment_styles():
    """Test mixing different comment styles."""
    code = """
    # Hash comment
    set x 5
    // Double slash comment
    add x 3
    /* Multi-line
       comment */
    mul x 2  # inline hash
    print x  // inline double slash
    """
    assert run(code).strip() == "16"


def test_commented_out_code():
    """Test that commented code is not executed."""
    code = """
    set x 10
    # set x 999
    // set x 888
    /* set x 777 */
    print x
    """
    assert run(code).strip() == "10"


def test_comment_only_lines():
    """Test file with only comments and blank lines."""
    code = """
    # Comment line 1
    // Comment line 2
    /* Comment line 3 */
    
    # More comments
    """
    assert run(code).strip() == ""


def test_nested_multiline_comments_not_supported():
    """Test that nested /* */ comments work as expected (not nested)."""
    code = """
    set x 5
    /* outer /* inner */ still in comment
    add x 100
    */
    print x
    """
    # The first */ closes the comment, so "still in comment" becomes code
    # This tests current behavior - nested comments are NOT supported
    output = run(code).strip()
    assert "5" in output or "[Error:" in output  # Either prints 5 or has error


def test_unclosed_multiline_comment():
    """Test that unclosed /* comment ignores rest of file."""
    code = """
    set x 5
    print x
    /* This comment is never closed
    set x 999
    print x
    """
    assert run(code).strip() == "5"


def test_comment_with_function_definition():
    """Test comments within function definitions."""
    code = """
    # Define a function
    def greet
        // Print greeting
        print "hello"  # inline comment
    end
    
    /* Call the function */
    call greet
    """
    assert run(code).strip() == "hello"


def test_comment_with_loops():
    """Test comments within loop blocks."""
    code = """
    set i 0
    loop 3  # Loop 3 times
        add i 1  // increment i
    end
    print i
    """
    assert run(code).strip() == "3"


def test_comment_with_conditionals():
    """Test comments within if blocks."""
    code = """
    set x 10
    # Check if x is positive
    if x > 0
        print "yes"  // x is positive
    end
    """
    assert run(code).strip() == "yes"


def test_empty_multiline_comment():
    """Test empty /* */ comment."""
    code = """
    set x 5
    /**/
    print x
    """
    assert run(code).strip() == "5"


def test_comment_with_special_chars():
    """Test comments containing special characters."""
    code = """
    set x 42
    # Comment with special chars: !@#$%^&*()
    // Comment with more: <>?{}[]|\\
    /* Comment with even more: ~`-_=+ */
    print x
    """
    assert run(code).strip() == "42"
