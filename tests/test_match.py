from techlang.interpreter import run


def test_match_numeric_guards():
    code = """
    set x 15
    match x
        case < 10
            print "low"
        case >= 15
            print "high"
        case default
            print "mid"
    end
    """
    assert run(code).strip() == "high"


def test_match_string_values():
    code = """
    str_create status "ok"
    match status
        case "error"
            print "bad"
        case == "ok"
            print "good"
        case default
            print "unknown"
    end
    """
    assert run(code).strip() == "good"
