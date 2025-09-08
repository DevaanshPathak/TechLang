from techlang.interpreter import run


def test_help_general_lists_commands():
    out = run("help").strip().splitlines()
    assert any(line.startswith("- ping") for line in out)
    assert any("Use: help <command>" in line for line in out)


def test_help_specific():
    out = run("help print").strip()
    assert "print:" in out

