import os
from techlang.interpreter import run


def test_graphics_saves_file(tmp_path, monkeypatch):
    # Ensure Pillow may not be present; if absent, expect error
    code = """
    graphics_init 100 80
    graphics_draw_line 0 0 99 79
    graphics_show
    """
    out = run(code, base_dir=str(tmp_path)).strip().splitlines()
    if any("not installed" in line for line in out):
        assert True  # Pillow missing is acceptable
    else:
        assert any("Canvas saved" in line for line in out)

