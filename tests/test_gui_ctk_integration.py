import os

import pytest


def _has_display() -> bool:
    try:
        import tkinter as tk

        root = tk.Tk()
        try:
            root.withdraw()
        finally:
            root.destroy()
        return True
    except Exception:
        return False


@pytest.mark.skipif(os.environ.get("TECHLANG_GUI_INTEGRATION") != "1", reason="GUI integration test disabled")
def test_ctk_mainloop_autoclose_smoke():
    """Optional smoke test.

    Enable with:
      TECHLANG_GUI_INTEGRATION=1

    This test opens a CTk window and auto-closes it quickly. It is intentionally
    skipped by default because many CI environments are headless.
    """

    if not _has_display():
        pytest.skip("No GUI display available")

    try:
        import customtkinter  # type: ignore[import-not-found]  # noqa: F401
    except Exception:
        pytest.skip("customtkinter not installed")

    from techlang.interpreter import run

    os.environ["TECHLANG_GUI_AUTOCLOSE_MS"] = "150"

    code = """
    gui_backend ctk
    gui_ctk_appearance dark
    gui_window win \"Smoke\" 220 120
    gui_label lbl win \"hello\"
    gui_mainloop win
    """

    out = run(code)
    assert "[Error:" not in out
