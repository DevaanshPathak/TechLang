import pytest


def _can_run_tk() -> bool:
    try:
        import tkinter  # noqa: F401

        return True
    except Exception:
        return False


@pytest.mark.skipif(not _can_run_tk(), reason="tkinter not available")
def test_gui_builds_spec_without_mainloop():
    from techlang.core import InterpreterState
    from techlang.parser import parse
    from techlang.macros import MacroHandler
    from techlang.aliases import AliasHandler
    from techlang.executor import CommandExecutor

    state = InterpreterState()

    code = """
    gui_backend tk
    gui_window win \"Title\" 300 200
    gui_label lbl win \"Hello\"
    gui_entry ent win
    gui_entry_set ent \"abc\"
    gui_button btn win \"OK\"
    """

    tokens = parse(code)
    tokens = MacroHandler.process_macros(tokens, state)
    tokens = AliasHandler.process_aliases(tokens, state)

    executor = CommandExecutor(state, ".")
    executor.execute_block(tokens)

    # No errors expected
    assert "[Error:" not in state.get_output()

    assert state.gui_backend == "tk"
    assert "win" in state.gui_specs
    assert state.gui_specs["win"]["type"] == "window"
    assert state.gui_specs["win"]["title"] == "Title"

    assert state.gui_specs["lbl"]["type"] == "label"
    assert state.gui_specs["lbl"]["parent"] == "win"
    assert state.gui_specs["lbl"]["text"] == "Hello"

    assert state.gui_specs["ent"]["type"] == "entry"
    assert state.gui_specs["ent"].get("value") == "abc"

    assert state.gui_specs["btn"]["type"] == "button"


def test_gui_backend_rejects_invalid_backend():
    from techlang.core import InterpreterState
    from techlang.gui_ops import GuiOpsHandler

    state = InterpreterState()
    consumed = GuiOpsHandler.handle_gui_backend(state, ["gui_backend", "nope"], 0)
    assert consumed == 0
    assert "gui_backend must be" in state.get_output()


def test_gui_window_rejects_non_integer_size():
    from techlang.core import InterpreterState
    from techlang.gui_ops import GuiOpsHandler

    state = InterpreterState()
    consumed = GuiOpsHandler.handle_gui_window(state, ["gui_window", "win", '"T"', "w", "100"], 0)
    assert consumed == 0
    assert "width/height must be integers" in state.get_output()


def test_gui_button_stores_on_click_when_provided():
    from techlang.core import InterpreterState
    from techlang.parser import parse
    from techlang.macros import MacroHandler
    from techlang.aliases import AliasHandler
    from techlang.executor import CommandExecutor

    state = InterpreterState()
    code = """
    def clicked do
        print "ok"
    end
    gui_window win \"Title\" 200 100
    gui_button btn win \"Go\" clicked
    """

    tokens = parse(code)
    tokens = MacroHandler.process_macros(tokens, state)
    tokens = AliasHandler.process_aliases(tokens, state)
    CommandExecutor(state, ".").execute_block(tokens)

    assert state.gui_specs["btn"]["type"] == "button"
    assert state.gui_specs["btn"]["on_click"] == "clicked"


def test_gui_button_omits_on_click_when_missing():
    from techlang.core import InterpreterState
    from techlang.parser import parse
    from techlang.macros import MacroHandler
    from techlang.aliases import AliasHandler
    from techlang.executor import CommandExecutor

    state = InterpreterState()
    code = """
    gui_window win \"Title\" 200 100
    gui_button btn win \"Go\"
    """

    tokens = parse(code)
    tokens = MacroHandler.process_macros(tokens, state)
    tokens = AliasHandler.process_aliases(tokens, state)
    CommandExecutor(state, ".").execute_block(tokens)

    assert state.gui_specs["btn"]["type"] == "button"
    assert state.gui_specs["btn"]["on_click"] is None


def test_gui_entry_get_sets_string_var():
    from techlang.core import InterpreterState
    from techlang.parser import parse
    from techlang.macros import MacroHandler
    from techlang.aliases import AliasHandler
    from techlang.executor import CommandExecutor

    state = InterpreterState()
    code = """
    gui_window win \"Title\" 200 100
    gui_entry ent win
    gui_entry_set ent \"hello\"
    gui_entry_get ent out str
    """

    tokens = parse(code)
    tokens = MacroHandler.process_macros(tokens, state)
    tokens = AliasHandler.process_aliases(tokens, state)
    CommandExecutor(state, ".").execute_block(tokens)

    assert state.strings["out"] == "hello"


def test_gui_entry_get_can_store_into_variable():
    from techlang.core import InterpreterState
    from techlang.parser import parse
    from techlang.macros import MacroHandler
    from techlang.aliases import AliasHandler
    from techlang.executor import CommandExecutor

    state = InterpreterState()
    code = """
    gui_window win \"Title\" 200 100
    gui_entry ent win
    gui_entry_set ent \"123\"
    gui_entry_get ent out var
    """

    tokens = parse(code)
    tokens = MacroHandler.process_macros(tokens, state)
    tokens = AliasHandler.process_aliases(tokens, state)
    CommandExecutor(state, ".").execute_block(tokens)

    assert state.variables["out"] == "123"


def test_gui_destroy_removes_child_from_parent():
    from techlang.core import InterpreterState
    from techlang.parser import parse
    from techlang.macros import MacroHandler
    from techlang.aliases import AliasHandler
    from techlang.executor import CommandExecutor

    state = InterpreterState()
    code = """
    gui_window win \"Title\" 200 100
    gui_label lbl win \"Hello\"
    gui_destroy lbl
    """

    tokens = parse(code)
    tokens = MacroHandler.process_macros(tokens, state)
    tokens = AliasHandler.process_aliases(tokens, state)
    CommandExecutor(state, ".").execute_block(tokens)

    assert "lbl" not in state.gui_specs
    assert "lbl" not in state.gui_specs["win"]["children"]


def test_gui_entry_get_errors_for_missing_widget():
    from techlang.core import InterpreterState
    from techlang.gui_ops import GuiOpsHandler

    state = InterpreterState()
    consumed = GuiOpsHandler.handle_gui_entry_get(state, ["gui_entry_get", "nope", "out"], 0)
    assert consumed == 0
    assert "does not exist" in state.get_output()


def test_gui_mainloop_errors_for_missing_window_spec():
    from techlang.core import InterpreterState
    from techlang.gui_ops import GuiOpsHandler

    state = InterpreterState()
    consumed = GuiOpsHandler.handle_gui_mainloop(state, ["gui_mainloop", "win"], 0, ".")
    assert consumed == 0
    assert "does not exist" in state.get_output()


def test_gui_mainloop_missing_ctk_reports_error():
    # Ensure we get a clean error when customtkinter isn't installed.
    pytest.importorskip("tkinter")

    from techlang.core import InterpreterState
    from techlang.executor import CommandExecutor

    state = InterpreterState()

    # Force backend to ctk and define a minimal window spec
    state.gui_backend = "ctk"
    state.gui_specs["win"] = {"type": "window", "title": "x", "width": 100, "height": 80, "children": []}
    state.gui_order.append("win")

    from techlang.gui_ops import GuiOpsHandler

    # If customtkinter exists in this environment, skip (we only want to validate error path)
    import importlib.util

    if importlib.util.find_spec("customtkinter") is not None:
        pytest.skip("customtkinter installed; error-path test not applicable")

    executor = CommandExecutor(state, ".")
    consumed = GuiOpsHandler.handle_gui_mainloop(state, ["gui_mainloop", "win"], 0, executor.base_dir)
    assert consumed == 0
    assert "customtkinter" in state.get_output()


def test_gui_set_and_get_store_in_spec_without_mainloop():
    from techlang.core import InterpreterState
    from techlang.parser import parse
    from techlang.macros import MacroHandler
    from techlang.aliases import AliasHandler
    from techlang.executor import CommandExecutor

    state = InterpreterState()
    code = """
    gui_window win \"Title\" 200 100
    gui_label lbl win \"Hello\"
    gui_set lbl \"text\" \"Updated\"
    gui_get lbl \"text\" out str
    """

    tokens = parse(code)
    tokens = MacroHandler.process_macros(tokens, state)
    tokens = AliasHandler.process_aliases(tokens, state)
    CommandExecutor(state, ".").execute_block(tokens)

    assert state.gui_specs["lbl"]["options"]["text"] == "Updated"
    assert state.strings["out"] == "Updated"


def test_gui_ctk_settings_store_spec_first_without_mainloop():
    from techlang.core import InterpreterState
    from techlang.parser import parse
    from techlang.macros import MacroHandler
    from techlang.aliases import AliasHandler
    from techlang.executor import CommandExecutor

    state = InterpreterState()
    code = """
    gui_backend ctk
    gui_ctk_appearance dark
    gui_ctk_theme "blue"
    gui_ctk_scaling 125
    """

    tokens = parse(code)
    tokens = MacroHandler.process_macros(tokens, state)
    tokens = AliasHandler.process_aliases(tokens, state)
    CommandExecutor(state, ".").execute_block(tokens)

    assert "[Error:" not in state.get_output()
    assert state.gui_backend == "ctk"
    assert state.gui_ctk_appearance == "dark"
    assert state.gui_ctk_theme == "blue"
    assert float(state.gui_ctk_scaling) == 125.0


def test_gui_ctk_appearance_rejects_invalid_value():
    from techlang.core import InterpreterState
    from techlang.gui_ops import GuiOpsHandler

    state = InterpreterState()
    consumed = GuiOpsHandler.handle_gui_ctk_appearance(state, ["gui_ctk_appearance", "nope"], 0)
    assert consumed == 0
    assert "gui_ctk_appearance must be" in state.get_output()


def test_gui_ctk_scaling_rejects_non_numeric():
    from techlang.core import InterpreterState
    from techlang.gui_ops import GuiOpsHandler

    state = InterpreterState()
    consumed = GuiOpsHandler.handle_gui_ctk_scaling(state, ["gui_ctk_scaling", "abc"], 0)
    assert consumed == 0
    assert "must be numeric" in state.get_output()


def test_gui_ctk_widgets_store_spec_first_without_mainloop():
    from techlang.core import InterpreterState
    from techlang.parser import parse
    from techlang.macros import MacroHandler
    from techlang.aliases import AliasHandler
    from techlang.executor import CommandExecutor

    state = InterpreterState()
    # Provide an array for values-list resolution
    state.arrays["vals"] = ["One", "Two"]

    code = """
    gui_backend ctk
    gui_window win \"Title\" 200 100
    gui_ctk_tabview tabs win
    gui_ctk_tab tab1 tabs \"First\"

    gui_ctk_switch sw tab1 \"Enabled\" v_enabled
    gui_ctk_slider sl tab1 v_amount
    gui_ctk_progressbar pb tab1
    gui_ctk_progress_set pb 0.5

    gui_ctk_optionmenu om tab1 \"A,B,C\" v_choice
    gui_ctk_combobox cb tab1 vals v_choice2
    """

    tokens = parse(code)
    tokens = MacroHandler.process_macros(tokens, state)
    tokens = AliasHandler.process_aliases(tokens, state)
    CommandExecutor(state, ".").execute_block(tokens)

    assert "[Error:" not in state.get_output()
    assert state.gui_specs["tabs"]["type"] == "ctk_tabview"
    assert state.gui_specs["tab1"]["type"] == "ctk_tab"
    assert state.gui_specs["sw"]["type"] == "ctk_switch"
    assert state.gui_specs["sw"]["var"] == "v_enabled"
    assert state.gui_specs["sl"]["type"] == "ctk_slider"
    assert state.gui_specs["sl"]["var"] == "v_amount"
    assert state.gui_specs["pb"]["type"] == "ctk_progressbar"
    assert float(state.gui_specs["pb"]["value"]) == 0.5
    assert state.gui_specs["om"]["values"] == ["A", "B", "C"]
    assert state.gui_specs["cb"]["values"] == ["One", "Two"]


def test_gui_ctk_progress_set_rejects_non_numeric():
    from techlang.core import InterpreterState
    from techlang.gui_ops import GuiOpsHandler

    state = InterpreterState()
    state.gui_specs["pb"] = {"type": "ctk_progressbar", "parent": "win", "options": {}, "bindings": {}}
    state.gui_specs["win"] = {"type": "window", "title": "x", "width": 1, "height": 1}
    state.gui_order.extend(["win", "pb"])

    consumed = GuiOpsHandler.handle_gui_ctk_progress_set(state, ["gui_ctk_progress_set", "pb", "nope"], 0)
    assert consumed == 0
    assert "Progress value must be a number" in state.get_output()


def test_gui_pack_and_grid_store_layout_options():
    from techlang.core import InterpreterState
    from techlang.parser import parse
    from techlang.macros import MacroHandler
    from techlang.aliases import AliasHandler
    from techlang.executor import CommandExecutor

    state = InterpreterState()
    code = """
    gui_window win \"Title\" 200 100
    gui_label a win \"A\"
    gui_label b win \"B\"
    gui_pack a side \"left\" fill \"x\"
    gui_grid b row 0 column 1
    """

    tokens = parse(code)
    tokens = MacroHandler.process_macros(tokens, state)
    tokens = AliasHandler.process_aliases(tokens, state)
    CommandExecutor(state, ".").execute_block(tokens)

    assert state.gui_specs["a"]["layout"]["manager"] == "pack"
    assert state.gui_specs["a"]["layout"]["options"]["side"] == "left"
    assert state.gui_specs["b"]["layout"]["manager"] == "grid"
    assert state.gui_specs["b"]["layout"]["options"]["row"] == 0
    assert state.gui_specs["b"]["layout"]["options"]["column"] == 1


def test_gui_bind_registers_in_spec():
    from techlang.core import InterpreterState
    from techlang.parser import parse
    from techlang.macros import MacroHandler
    from techlang.aliases import AliasHandler
    from techlang.executor import CommandExecutor

    state = InterpreterState()
    code = """
    def on_click do
        print \"clicked\"
    end
    gui_window win \"Title\" 200 100
    gui_button btn win \"Go\" on_click
    gui_bind btn \"<Button-1>\" on_click
    """

    tokens = parse(code)
    tokens = MacroHandler.process_macros(tokens, state)
    tokens = AliasHandler.process_aliases(tokens, state)
    CommandExecutor(state, ".").execute_block(tokens)

    assert state.gui_specs["btn"]["bindings"]["<Button-1>"] == "on_click"


def test_phase2_widgets_build_specs():
    from techlang.core import InterpreterState
    from techlang.parser import parse
    from techlang.macros import MacroHandler
    from techlang.aliases import AliasHandler
    from techlang.executor import CommandExecutor

    state = InterpreterState()
    code = """
    gui_window win \"Title\" 200 100
    gui_frame frm win
    gui_checkbutton chk frm \"Check\"
    gui_radiobutton r1 frm \"One\" choice 1
    gui_text t frm
    gui_listbox lb frm
    gui_canvas c frm
    gui_scrollbar sb frm vertical
    gui_canvas_create_line c 0 0 10 10
    """

    tokens = parse(code)
    tokens = MacroHandler.process_macros(tokens, state)
    tokens = AliasHandler.process_aliases(tokens, state)
    CommandExecutor(state, ".").execute_block(tokens)

    assert state.gui_specs["frm"]["type"] == "frame"
    assert state.gui_specs["chk"]["type"] == "checkbutton"
    assert state.gui_specs["r1"]["type"] == "radiobutton"
    assert state.gui_specs["t"]["type"] == "text"
    assert state.gui_specs["lb"]["type"] == "listbox"
    assert state.gui_specs["c"]["type"] == "canvas"
    assert state.gui_specs["sb"]["type"] == "scrollbar"
    assert state.gui_specs["c"]["items"][0]["kind"] == "line"


def test_gui_var_new_set_get_are_spec_first():
    from techlang.core import InterpreterState
    from techlang.parser import parse
    from techlang.macros import MacroHandler
    from techlang.aliases import AliasHandler
    from techlang.executor import CommandExecutor

    state = InterpreterState()
    code = """
    gui_var_new flag bool
    gui_var_set flag 1
    gui_var_get flag out var
    """

    tokens = parse(code)
    tokens = MacroHandler.process_macros(tokens, state)
    tokens = AliasHandler.process_aliases(tokens, state)
    CommandExecutor(state, ".").execute_block(tokens)

    assert state.gui_vars["flag"]["type"] == "bool"
    assert state.variables["out"] == "1"


def test_phase3_menus_build_specs():
    from techlang.core import InterpreterState
    from techlang.parser import parse
    from techlang.macros import MacroHandler
    from techlang.aliases import AliasHandler
    from techlang.executor import CommandExecutor

    state = InterpreterState()
    code = """
    def on_open do
        print \"open\"
    end
    gui_window win \"Title\" 200 100
    gui_menubar bar win
    gui_menu file bar \"File\"
    gui_menu_item open file \"Open\" on_open
    """

    tokens = parse(code)
    tokens = MacroHandler.process_macros(tokens, state)
    tokens = AliasHandler.process_aliases(tokens, state)
    CommandExecutor(state, ".").execute_block(tokens)

    assert state.gui_specs["bar"]["type"] == "menubar"
    assert state.gui_specs["win"]["menubar"] == "bar"
    assert "file" in state.gui_specs["bar"]["children"]
    assert state.gui_specs["file"]["type"] == "menu"
    assert "open" in state.gui_specs["file"]["children"]
    assert state.gui_specs["open"]["type"] == "menu_item"
    assert state.gui_specs["open"]["fn"] == "on_open"


def test_gui_messagebox_requires_runtime():
    from techlang.core import InterpreterState
    from techlang.gui_ops import GuiOpsHandler

    state = InterpreterState()
    consumed = GuiOpsHandler.handle_gui_messagebox(
        state,
        ["gui_messagebox", "info", '"T"', '"M"', "out", "str"],
        0,
    )
    assert consumed == 0
    assert "require a running GUI" in state.get_output()


def test_gui_filedialog_requires_runtime():
    from techlang.core import InterpreterState
    from techlang.gui_ops import GuiOpsHandler

    state = InterpreterState()
    consumed = GuiOpsHandler.handle_gui_filedialog_open(state, ["gui_filedialog_open", '"Open"', "out"], 0)
    assert consumed == 0
    assert "require a running GUI" in state.get_output()
