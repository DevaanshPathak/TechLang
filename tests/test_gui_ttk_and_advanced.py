import pytest

from techlang.interpreter import run


def test_gui_ttk_style_and_theme_spec_storage():
    code = """
    gui_ttk_theme_use \"clam\"
    gui_ttk_style_set TButton \"padding\" 8
    """
    out = run(code).strip()
    assert out == ""  # spec-only


def test_gui_ttk_widgets_and_notebook_tabs_build_specs():
    code = """
    gui_window w \"T\" 200 100
    gui_ttk_notebook nb w
    gui_frame tab1 w
    gui_frame tab2 w
    gui_ttk_notebook_tab nb tab1 \"One\"
    gui_ttk_notebook_tab nb tab2 \"Two\"
    gui_ttk_button b1 tab1 \"OK\"
    gui_ttk_label l1 tab2 \"Hello\"
    """
    out = run(code).strip()
    assert out == ""


def test_gui_text_spec_content_and_get_delete():
    code = """
    gui_window w \"T\" 200 100
    gui_text t w
    gui_text_insert t end \"Hello\"
    gui_text_insert t end \" World\"
    gui_text_get t s str
    gui_text_delete t all
    gui_text_get t s2 str
    print s
    print s2
    print "END"
    """
    lines = run(code).strip().splitlines()
    assert lines[0] == "Hello World"
    assert lines[1] == ""
    assert lines[2] == "END"


def test_gui_text_tag_storage_and_config_parsing():
    code = """
    gui_window w \"T\" 200 100
    gui_text t w
    gui_text_tag_add t tag1 1.0 1.4
    gui_text_tag_config t tag1 \"foreground\" \"red\" \"font\" \"Arial\"
    """
    out = run(code).strip()
    assert out == ""


def test_gui_canvas_line_id_and_coords_and_move_and_delete():
    code = """
    gui_window w \"T\" 200 100
    gui_canvas c w
    gui_canvas_create_line c 0 0 10 20 id var
    gui_canvas_coords c 1 coords str
    gui_canvas_move c 1 5 5
    gui_canvas_coords c 1 coords2 str
    gui_canvas_delete c 1
    print id
    print coords
    print coords2
    """
    lines = run(code).strip().splitlines()
    assert lines[0] == "1"
    assert lines[1] == "0.0 0.0 10.0 20.0"
    assert lines[2] == "5.0 5.0 15.0 25.0"
