from techlang.interpreter import run


def test_switch_matches_case():
    code = """
    set x 1
    switch x
        case 1
            print "one"
        case 2
            print "two"
        default
            print "other"
    end
    """
    assert run(code).strip() == "one"


def test_switch_default():
    code = """
    set x 3
    switch x
        case 1
            print "one"
        case 2
            print "two"
        default
            print "other"
    end
    """
    assert run(code).strip() == "other"


def test_try_catch_handles_error():
    code = """
    set a 10
    set b 0
    try
        div a b
    catch
        print "Division by zero!"
    end
    """
    assert run(code).strip().splitlines()[-1] == "Division by zero!"


def test_try_no_error_skips_catch():
    code = """
    set a 10
    set b 2
    try
        div a b
        print a
    catch
        print "err"
    end
    """
    # div 10 2 = 5, prints 5; catch should not run
    assert run(code).strip().splitlines()[-1] == "5"

