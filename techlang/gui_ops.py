from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from .core import InterpreterState
from .data_types import DataTypesHandler


class GuiOpsHandler:
    @staticmethod
    def _strip_quotes(token: str) -> str:
        if token.startswith('"') and token.endswith('"') and len(token) >= 2:
            return token[1:-1]
        return token

    @staticmethod
    def _resolve_value_token(state: InterpreterState, token: str) -> object:
        # Value resolution rules (best-effort, Tk-friendly):
        # - quoted string => string
        # - string var => string
        # - numeric var => number
        # - int/float literals => number
        # - otherwise => raw token string
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        if token in state.strings:
            return state.strings[token]
        if token in state.arrays:
            return list(state.arrays[token])
        if state.has_variable(token):
            return state.get_variable(token)
        try:
            if "." in token:
                return float(token)
            return int(token)
        except Exception:
            return token

    @staticmethod
    def _store_value(state: InterpreterState, target: str, mode: str, value: object) -> None:
        text = "" if value is None else str(value)
        if mode == "var":
            state.variables[target] = text
        else:
            state.strings[target] = text

    @staticmethod
    def _parse_kv_options(state: InterpreterState, tokens: List[str], start: int) -> tuple[Dict[str, object], int]:
        # Parse key/value pairs until a new command/block token is encountered.
        # Returns: (options_dict, tokens_consumed_after_start)
        options: Dict[str, object] = {}
        consumed = 0
        j = start
        from .basic_commands import BasicCommandHandler

        while j + 1 < len(tokens):
            key_token = tokens[j]
            if key_token in {"end", "case", "default", "catch"}:
                break
            if key_token in BasicCommandHandler.KNOWN_COMMANDS:
                break
            val_token = tokens[j + 1]
            if val_token in BasicCommandHandler.KNOWN_COMMANDS and val_token not in {"end", "case", "default", "catch"}:
                # Likely a missing value; stop parsing options.
                break
            options[str(key_token)] = GuiOpsHandler._resolve_value_token(state, val_token)
            j += 2
            consumed += 2

        return options, consumed

    @staticmethod
    def _get_spec(state: InterpreterState, name: str) -> Optional[Dict[str, object]]:
        return state.gui_specs.get(name)

    @staticmethod
    def _require_spec(state: InterpreterState, name: str, kind: Optional[str] = None) -> Optional[Dict[str, object]]:
        spec = GuiOpsHandler._get_spec(state, name)
        if spec is None:
            state.add_error(f"GUI object '{name}' does not exist")
            return None
        if kind is not None and spec.get("type") != kind:
            state.add_error(f"GUI object '{name}' is not a {kind}")
            return None
        return spec

    @staticmethod
    def handle_gui_backend(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("gui_backend requires backend name: tk or ctk")
            return 0
        backend = tokens[index + 1].lower()
        if backend not in {"tk", "ctk"}:
            state.add_error("gui_backend must be 'tk' or 'ctk'")
            return 0
        state.gui_backend = backend
        return 1

    @staticmethod
    def handle_gui_ctk_appearance(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ctk_appearance <light|dark|system>
        if index + 1 >= len(tokens):
            state.add_error("gui_ctk_appearance requires: gui_ctk_appearance <light|dark|system>")
            return 0
        mode = tokens[index + 1].lower()
        if mode not in {"light", "dark", "system"}:
            state.add_error("gui_ctk_appearance must be light, dark, or system")
            return 0
        state.gui_ctk_appearance = mode
        return 1

    @staticmethod
    def handle_gui_ctk_theme(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ctk_theme <"name"|nameStrVar>
        if index + 1 >= len(tokens):
            state.add_error('gui_ctk_theme requires: gui_ctk_theme "name_or_path"')
            return 0
        theme = DataTypesHandler._resolve_string_token(state, tokens[index + 1], "CTk theme")
        if theme is None:
            return 0
        state.gui_ctk_theme = theme
        return 1

    @staticmethod
    def handle_gui_ctk_scaling(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ctk_scaling <percent>
        if index + 1 >= len(tokens):
            state.add_error("gui_ctk_scaling requires: gui_ctk_scaling <percent>")
            return 0
        raw = GuiOpsHandler._resolve_value_token(state, tokens[index + 1])
        try:
            val = float(raw)
        except Exception:
            state.add_error("gui_ctk_scaling percent must be numeric")
            return 0

        # Roadmap syntax is percent. If user supplies a ratio (<= 10), convert.
        if 0 < val <= 10:
            val = val * 100.0
        if val <= 0:
            state.add_error("gui_ctk_scaling percent must be positive")
            return 0

        state.gui_ctk_scaling = val
        return 1

    # -----------------
    # CTK-4: CTk-first widgets (spec-first)
    # -----------------

    @staticmethod
    def _resolve_values_list(state: InterpreterState, token: str) -> Optional[List[str]]:
        # Accept an array name (from state.arrays) or a quoted CSV string.
        if token in state.arrays and isinstance(state.arrays.get(token), list):
            return [str(v) for v in state.arrays.get(token, [])]
        values = DataTypesHandler._resolve_string_token(state, token, "Values")
        if values is None:
            return None
        raw = str(values)
        if not raw:
            return []
        return [part.strip() for part in raw.split(",") if part.strip()]

    @staticmethod
    def handle_gui_ctk_switch(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ctk_switch <name> <parent> "text" [var]
        if index + 3 >= len(tokens):
            state.add_error('gui_ctk_switch requires: gui_ctk_switch <name> <parent> "text" [var]')
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        text = DataTypesHandler._resolve_string_token(state, tokens[index + 3], "Switch text")
        if text is None:
            return 0

        var_name: Optional[str] = None
        consumed = 3
        if index + 4 < len(tokens):
            candidate = tokens[index + 4]
            from .basic_commands import BasicCommandHandler

            if (
                candidate not in {"end", "case", "default", "catch"}
                and candidate not in BasicCommandHandler.KNOWN_COMMANDS
                and not (candidate.startswith('"') and candidate.endswith('"'))
            ):
                var_name = candidate
                consumed = 4

        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {
            "type": "ctk_switch",
            "parent": parent,
            "text": text,
            "var": var_name,
            "options": {},
            "bindings": {},
        }
        state.gui_order.append(name)
        GuiOpsHandler._add_child(state, parent, name)
        return consumed

    @staticmethod
    def handle_gui_ctk_slider(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ctk_slider <name> <parent> [var]
        if index + 2 >= len(tokens):
            state.add_error("gui_ctk_slider requires: gui_ctk_slider <name> <parent> [var]")
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]

        var_name: Optional[str] = None
        consumed = 2
        if index + 3 < len(tokens):
            candidate = tokens[index + 3]
            from .basic_commands import BasicCommandHandler

            if (
                candidate not in {"end", "case", "default", "catch"}
                and candidate not in BasicCommandHandler.KNOWN_COMMANDS
                and not (candidate.startswith('"') and candidate.endswith('"'))
            ):
                var_name = candidate
                consumed = 3

        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {"type": "ctk_slider", "parent": parent, "var": var_name, "options": {}, "bindings": {}}
        state.gui_order.append(name)
        GuiOpsHandler._add_child(state, parent, name)
        return consumed

    @staticmethod
    def handle_gui_ctk_progressbar(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ctk_progressbar <name> <parent> [var]
        if index + 2 >= len(tokens):
            state.add_error("gui_ctk_progressbar requires: gui_ctk_progressbar <name> <parent> [var]")
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]

        var_name: Optional[str] = None
        consumed = 2
        if index + 3 < len(tokens):
            candidate = tokens[index + 3]
            from .basic_commands import BasicCommandHandler

            if (
                candidate not in {"end", "case", "default", "catch"}
                and candidate not in BasicCommandHandler.KNOWN_COMMANDS
                and not (candidate.startswith('"') and candidate.endswith('"'))
            ):
                var_name = candidate
                consumed = 3

        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {
            "type": "ctk_progressbar",
            "parent": parent,
            "var": var_name,
            "value": 0,
            "options": {},
            "bindings": {},
        }
        state.gui_order.append(name)
        GuiOpsHandler._add_child(state, parent, name)
        return consumed

    @staticmethod
    def handle_gui_ctk_progress_set(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ctk_progress_set <progressbar> <value>
        if index + 2 >= len(tokens):
            state.add_error("gui_ctk_progress_set requires: gui_ctk_progress_set <progressbar> <value>")
            return 0
        name = tokens[index + 1]
        value_token = tokens[index + 2]
        spec = GuiOpsHandler._require_spec(state, name, kind="ctk_progressbar")
        if spec is None:
            return 0

        value_obj = GuiOpsHandler._resolve_value_token(state, value_token)
        try:
            value = float(value_obj)
        except Exception:
            state.add_error("Progress value must be a number")
            return 0

        spec["value"] = value
        widget = state.gui_runtime_widgets.get(name)
        if widget is not None and hasattr(widget, "set"):
            try:
                widget.set(value)
            except Exception:
                pass
        return 2

    @staticmethod
    def handle_gui_ctk_optionmenu(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ctk_optionmenu <name> <parent> <values> [var]
        if index + 3 >= len(tokens):
            state.add_error("gui_ctk_optionmenu requires: gui_ctk_optionmenu <name> <parent> <values> [var]")
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        values_token = tokens[index + 3]
        values = GuiOpsHandler._resolve_values_list(state, values_token)
        if values is None:
            return 0

        var_name: Optional[str] = None
        consumed = 3
        if index + 4 < len(tokens):
            candidate = tokens[index + 4]
            from .basic_commands import BasicCommandHandler

            if (
                candidate not in {"end", "case", "default", "catch"}
                and candidate not in BasicCommandHandler.KNOWN_COMMANDS
                and not (candidate.startswith('"') and candidate.endswith('"'))
            ):
                var_name = candidate
                consumed = 4

        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {
            "type": "ctk_optionmenu",
            "parent": parent,
            "values": values,
            "var": var_name,
            "options": {},
            "bindings": {},
        }
        state.gui_order.append(name)
        GuiOpsHandler._add_child(state, parent, name)
        return consumed

    @staticmethod
    def handle_gui_ctk_combobox(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ctk_combobox <name> <parent> <values> [var]
        if index + 3 >= len(tokens):
            state.add_error("gui_ctk_combobox requires: gui_ctk_combobox <name> <parent> <values> [var]")
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        values_token = tokens[index + 3]
        values = GuiOpsHandler._resolve_values_list(state, values_token)
        if values is None:
            return 0

        var_name: Optional[str] = None
        consumed = 3
        if index + 4 < len(tokens):
            candidate = tokens[index + 4]
            from .basic_commands import BasicCommandHandler

            if (
                candidate not in {"end", "case", "default", "catch"}
                and candidate not in BasicCommandHandler.KNOWN_COMMANDS
                and not (candidate.startswith('"') and candidate.endswith('"'))
            ):
                var_name = candidate
                consumed = 4

        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {
            "type": "ctk_combobox",
            "parent": parent,
            "values": values,
            "var": var_name,
            "options": {},
            "bindings": {},
        }
        state.gui_order.append(name)
        GuiOpsHandler._add_child(state, parent, name)
        return consumed

    @staticmethod
    def handle_gui_ctk_tabview(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ctk_tabview <name> <parent>
        if index + 2 >= len(tokens):
            state.add_error("gui_ctk_tabview requires: gui_ctk_tabview <name> <parent>")
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {"type": "ctk_tabview", "parent": parent, "options": {}, "bindings": {}, "children": []}
        state.gui_order.append(name)
        GuiOpsHandler._add_child(state, parent, name)
        return 2

    @staticmethod
    def handle_gui_ctk_tab(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ctk_tab <name> <tabview> "label"
        if index + 3 >= len(tokens):
            state.add_error('gui_ctk_tab requires: gui_ctk_tab <name> <tabview> "label"')
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        label = DataTypesHandler._resolve_string_token(state, tokens[index + 3], "Tab label")
        if label is None:
            return 0

        parent_spec = GuiOpsHandler._require_spec(state, parent, kind="ctk_tabview")
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {"type": "ctk_tab", "parent": parent, "label": label, "options": {}, "bindings": {}, "children": []}
        state.gui_order.append(name)
        GuiOpsHandler._add_child(state, parent, name)
        return 3

    @staticmethod
    def handle_gui_window(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_window <name> "title" <width> <height>
        if index + 4 >= len(tokens):
            state.add_error('gui_window requires: gui_window <name> "title" <width> <height>')
            return 0

        name = tokens[index + 1]
        title_token = tokens[index + 2]
        width_token = tokens[index + 3]
        height_token = tokens[index + 4]

        title = DataTypesHandler._resolve_string_token(state, title_token, "Window title")
        if title is None:
            return 0

        try:
            width = int(width_token)
            height = int(height_token)
        except ValueError:
            state.add_error("Window width/height must be integers")
            return 0

        state.gui_specs[name] = {
            "type": "window",
            "title": title,
            "width": width,
            "height": height,
            "children": [],
        }
        state.gui_order.append(name)
        return 4

    @staticmethod
    def handle_gui_label(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_label <name> <parent> "text"
        if index + 3 >= len(tokens):
            state.add_error('gui_label requires: gui_label <name> <parent> "text"')
            return 0

        name = tokens[index + 1]
        parent = tokens[index + 2]
        text_token = tokens[index + 3]

        text = DataTypesHandler._resolve_string_token(state, text_token, "Label text")
        if text is None:
            return 0

        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0

        state.gui_specs[name] = {
            "type": "label",
            "parent": parent,
            "text": text,
            "options": {},
            "bindings": {},
        }
        state.gui_order.append(name)
        if isinstance(parent_spec.get("children"), list):
            parent_spec["children"].append(name)
        return 3

    @staticmethod
    def handle_gui_entry(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_entry <name> <parent>
        if index + 2 >= len(tokens):
            state.add_error("gui_entry requires: gui_entry <name> <parent>")
            return 0

        name = tokens[index + 1]
        parent = tokens[index + 2]

        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0

        state.gui_specs[name] = {
            "type": "entry",
            "parent": parent,
            "options": {},
            "bindings": {},
        }
        state.gui_order.append(name)
        if isinstance(parent_spec.get("children"), list):
            parent_spec["children"].append(name)
        return 2

    @staticmethod
    def handle_gui_button(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_button <name> <parent> "text" [on_click_fn]
        if index + 3 >= len(tokens):
            state.add_error('gui_button requires: gui_button <name> <parent> "text" [on_click_fn]')
            return 0

        name = tokens[index + 1]
        parent = tokens[index + 2]
        text_token = tokens[index + 3]

        text = DataTypesHandler._resolve_string_token(state, text_token, "Button text")
        if text is None:
            return 0

        on_click: Optional[str] = None
        consumed = 3
        if index + 4 < len(tokens):
            candidate = tokens[index + 4]
            # If the next token looks like a new command, treat callback as omitted.
            # This mirrors other handlers that allow optional args.
            from .basic_commands import BasicCommandHandler

            if (
                candidate not in {"end", "case", "default", "catch"}
                and candidate not in BasicCommandHandler.KNOWN_COMMANDS
                and not (candidate.startswith('"') and candidate.endswith('"'))
            ):
                on_click = candidate
                consumed = 4

        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0

        state.gui_specs[name] = {
            "type": "button",
            "parent": parent,
            "text": text,
            "on_click": on_click,
            "options": {},
            "bindings": {},
        }
        state.gui_order.append(name)
        if isinstance(parent_spec.get("children"), list):
            parent_spec["children"].append(name)
        return consumed

    @staticmethod
    def handle_gui_entry_get(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_entry_get <entry> <target> [str|var]
        # Default: store into a TechLang string (backward compatible)
        if index + 2 >= len(tokens):
            state.add_error("gui_entry_get requires: gui_entry_get <entry> <target> [str|var]")
            return 0
        entry_name = tokens[index + 1]
        target = tokens[index + 2]

        mode = "str"
        if index + 3 < len(tokens):
            candidate = tokens[index + 3].lower()
            if candidate in {"str", "var"}:
                mode = candidate

        spec = GuiOpsHandler._require_spec(state, entry_name, kind="entry")
        if spec is None:
            return 0

        value = spec.get("value", "")
        widget = state.gui_runtime_widgets.get(entry_name)
        if widget is not None and hasattr(widget, "get"):
            try:
                value = widget.get()
            except Exception:
                pass
        if mode == "var":
            # Store into variables; keep as string so numeric parsing can happen later if needed.
            state.variables[target] = str(value)
            return 3 if index + 3 < len(tokens) and tokens[index + 3].lower() in {"str", "var"} else 2

        state.strings[target] = str(value)
        return 3 if index + 3 < len(tokens) and tokens[index + 3].lower() in {"str", "var"} else 2

    @staticmethod
    def handle_gui_entry_set(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_entry_set <entry> <"text"|stringVar>
        if index + 2 >= len(tokens):
            state.add_error('gui_entry_set requires: gui_entry_set <entry> <"text"|stringVar>')
            return 0
        entry_name = tokens[index + 1]
        value_token = tokens[index + 2]

        spec = GuiOpsHandler._require_spec(state, entry_name, kind="entry")
        if spec is None:
            return 0

        value = DataTypesHandler._resolve_string_token(state, value_token, "Entry value")
        if value is None:
            return 0

        spec["value"] = value

        widget = state.gui_runtime_widgets.get(entry_name)
        if widget is not None:
            try:
                if hasattr(widget, "delete"):
                    widget.delete(0, "end")
                if hasattr(widget, "insert"):
                    widget.insert(0, str(value))
            except Exception:
                pass
        return 2

    # Phase 1: universal property API
    @staticmethod
    def handle_gui_set(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_set <widget> "option" <value>
        if index + 3 >= len(tokens):
            state.add_error('gui_set requires: gui_set <widget> "option" <value>')
            return 0
        name = tokens[index + 1]
        option_token = tokens[index + 2]
        value_token = tokens[index + 3]

        spec = GuiOpsHandler._require_spec(state, name)
        if spec is None:
            return 0

        option = DataTypesHandler._resolve_string_token(state, option_token, "GUI option")
        if option is None:
            return 0

        value = GuiOpsHandler._resolve_value_token(state, value_token)
        options = spec.get("options")
        if not isinstance(options, dict):
            options = {}
            spec["options"] = options
        options[str(option)] = value

        widget = state.gui_runtime_widgets.get(name)
        if widget is not None and hasattr(widget, "configure"):
            try:
                widget.configure(**{str(option): value})
            except Exception:
                # Ignore runtime configure errors; spec still updated.
                pass
        return 3

    @staticmethod
    def handle_gui_get(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_get <widget> "option" <target> [str|var]
        if index + 3 >= len(tokens):
            state.add_error('gui_get requires: gui_get <widget> "option" <target> [str|var]')
            return 0

        name = tokens[index + 1]
        option_token = tokens[index + 2]
        target = tokens[index + 3]

        mode = "str"
        if index + 4 < len(tokens):
            candidate = tokens[index + 4].lower()
            if candidate in {"str", "var"}:
                mode = candidate

        spec = GuiOpsHandler._require_spec(state, name)
        if spec is None:
            return 0

        option = DataTypesHandler._resolve_string_token(state, option_token, "GUI option")
        if option is None:
            return 0

        value: object = ""
        widget = state.gui_runtime_widgets.get(name)
        if widget is not None and hasattr(widget, "cget"):
            try:
                value = widget.cget(str(option))
            except Exception:
                value = ""
        else:
            options = spec.get("options")
            if isinstance(options, dict):
                value = options.get(str(option), "")
        GuiOpsHandler._store_value(state, target, mode, value)

        return 4 if index + 4 < len(tokens) and tokens[index + 4].lower() in {"str", "var"} else 3

    # Phase 1: layout managers (minimum)
    @staticmethod
    def handle_gui_pack(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_pack <widget> [key value]...
        if index + 1 >= len(tokens):
            state.add_error("gui_pack requires: gui_pack <widget> [key value]...")
            return 0
        name = tokens[index + 1]
        spec = GuiOpsHandler._require_spec(state, name)
        if spec is None:
            return 0

        opts, consumed_opts = GuiOpsHandler._parse_kv_options(state, tokens, index + 2)
        spec["layout"] = {"manager": "pack", "options": opts}

        widget = state.gui_runtime_widgets.get(name)
        if widget is not None and hasattr(widget, "pack"):
            try:
                widget.pack(**{str(k): v for k, v in opts.items()})
            except Exception:
                pass

        return 1 + consumed_opts

    @staticmethod
    def handle_gui_grid(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_grid <widget> [key value]...
        if index + 1 >= len(tokens):
            state.add_error("gui_grid requires: gui_grid <widget> [key value]...")
            return 0
        name = tokens[index + 1]
        spec = GuiOpsHandler._require_spec(state, name)
        if spec is None:
            return 0

        opts, consumed_opts = GuiOpsHandler._parse_kv_options(state, tokens, index + 2)
        spec["layout"] = {"manager": "grid", "options": opts}

        widget = state.gui_runtime_widgets.get(name)
        if widget is not None and hasattr(widget, "grid"):
            try:
                widget.grid(**{str(k): v for k, v in opts.items()})
            except Exception:
                pass

        return 1 + consumed_opts

    # Phase 1: event binding
    @staticmethod
    def handle_gui_bind(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_bind <widget> "<Event>" <fn>
        if index + 3 >= len(tokens):
            state.add_error('gui_bind requires: gui_bind <widget> "<Event>" <fn>')
            return 0
        name = tokens[index + 1]
        event_token = tokens[index + 2]
        fn = tokens[index + 3]

        spec = GuiOpsHandler._require_spec(state, name)
        if spec is None:
            return 0
        event = DataTypesHandler._resolve_string_token(state, event_token, "GUI event")
        if event is None:
            return 0

        bindings = spec.get("bindings")
        if not isinstance(bindings, dict):
            bindings = {}
            spec["bindings"] = bindings
        bindings[str(event)] = fn

        widget = state.gui_runtime_widgets.get(name)
        if widget is not None and hasattr(widget, "bind"):
            try:
                from .executor import CommandExecutor  # local import

                def _callback(_evt=None):
                    executor = CommandExecutor(state, getattr(state, "gui_runtime_base_dir", "."))
                    executor.execute_block(["call", fn])

                widget.bind(str(event), _callback)
            except Exception:
                pass

        return 3

    # Phase 2: widgets
    @staticmethod
    def handle_gui_frame(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_frame <name> <parent>
        if index + 2 >= len(tokens):
            state.add_error("gui_frame requires: gui_frame <name> <parent>")
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]

        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0

        state.gui_specs[name] = {
            "type": "frame",
            "parent": parent,
            "children": [],
            "options": {},
            "bindings": {},
        }
        state.gui_order.append(name)
        if isinstance(parent_spec.get("children"), list):
            parent_spec["children"].append(name)
        return 2

    @staticmethod
    def handle_gui_checkbutton(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_checkbutton <name> <parent> "text" [var]
        if index + 3 >= len(tokens):
            state.add_error('gui_checkbutton requires: gui_checkbutton <name> <parent> "text" [var]')
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        text_token = tokens[index + 3]

        text = DataTypesHandler._resolve_string_token(state, text_token, "Checkbutton text")
        if text is None:
            return 0

        var_name: Optional[str] = None
        consumed = 3
        if index + 4 < len(tokens):
            candidate = tokens[index + 4]
            from .basic_commands import BasicCommandHandler

            if (
                candidate not in {"end", "case", "default", "catch"}
                and candidate not in BasicCommandHandler.KNOWN_COMMANDS
                and not (candidate.startswith('"') and candidate.endswith('"'))
            ):
                var_name = candidate
                consumed = 4

        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0

        state.gui_specs[name] = {
            "type": "checkbutton",
            "parent": parent,
            "text": text,
            "var": var_name,
            "options": {},
            "bindings": {},
        }
        state.gui_order.append(name)
        if isinstance(parent_spec.get("children"), list):
            parent_spec["children"].append(name)
        return consumed

    @staticmethod
    def handle_gui_radiobutton(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_radiobutton <name> <parent> "text" <var> <value>
        if index + 5 >= len(tokens):
            state.add_error('gui_radiobutton requires: gui_radiobutton <name> <parent> "text" <var> <value>')
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        text_token = tokens[index + 3]
        var_name = tokens[index + 4]
        value_token = tokens[index + 5]

        text = DataTypesHandler._resolve_string_token(state, text_token, "Radiobutton text")
        if text is None:
            return 0

        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0

        state.gui_specs[name] = {
            "type": "radiobutton",
            "parent": parent,
            "text": text,
            "var": var_name,
            "value": GuiOpsHandler._resolve_value_token(state, value_token),
            "options": {},
            "bindings": {},
        }
        state.gui_order.append(name)
        if isinstance(parent_spec.get("children"), list):
            parent_spec["children"].append(name)
        return 5

    @staticmethod
    def handle_gui_text(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_text <name> <parent>
        if index + 2 >= len(tokens):
            state.add_error("gui_text requires: gui_text <name> <parent>")
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {"type": "text", "parent": parent, "options": {}, "bindings": {}}
        state.gui_order.append(name)
        if isinstance(parent_spec.get("children"), list):
            parent_spec["children"].append(name)
        return 2

    @staticmethod
    def handle_gui_listbox(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_listbox <name> <parent>
        if index + 2 >= len(tokens):
            state.add_error("gui_listbox requires: gui_listbox <name> <parent>")
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {"type": "listbox", "parent": parent, "options": {}, "bindings": {}}
        state.gui_order.append(name)
        if isinstance(parent_spec.get("children"), list):
            parent_spec["children"].append(name)
        return 2

    @staticmethod
    def handle_gui_canvas(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_canvas <name> <parent>
        if index + 2 >= len(tokens):
            state.add_error("gui_canvas requires: gui_canvas <name> <parent>")
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {"type": "canvas", "parent": parent, "options": {}, "bindings": {}, "items": []}
        state.gui_order.append(name)
        if isinstance(parent_spec.get("children"), list):
            parent_spec["children"].append(name)
        return 2

    @staticmethod
    def handle_gui_scrollbar(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_scrollbar <name> <parent> [orient]
        if index + 2 >= len(tokens):
            state.add_error("gui_scrollbar requires: gui_scrollbar <name> <parent> [orient]")
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        orient = "vertical"
        consumed = 2
        if index + 3 < len(tokens):
            candidate = tokens[index + 3].lower()
            if candidate in {"vertical", "horizontal"}:
                orient = candidate
                consumed = 3

        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {"type": "scrollbar", "parent": parent, "orient": orient, "options": {}, "bindings": {}}
        state.gui_order.append(name)
        if isinstance(parent_spec.get("children"), list):
            parent_spec["children"].append(name)
        return consumed

    # Phase 2: canvas basic item creation
    @staticmethod
    def handle_gui_canvas_create_line(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_canvas_create_line <canvas> x1 y1 x2 y2
        if index + 5 >= len(tokens):
            state.add_error("gui_canvas_create_line requires: gui_canvas_create_line <canvas> x1 y1 x2 y2")
            return 0
        canvas_name = tokens[index + 1]
        spec = GuiOpsHandler._require_spec(state, canvas_name, kind="canvas")
        if spec is None:
            return 0
        try:
            x1 = float(tokens[index + 2])
            y1 = float(tokens[index + 3])
            x2 = float(tokens[index + 4])
            y2 = float(tokens[index + 5])
        except ValueError:
            state.add_error("Canvas coordinates must be numbers")
            return 0
        items = spec.get("items")
        if not isinstance(items, list):
            items = []
            spec["items"] = items
        items.append({"kind": "line", "x1": x1, "y1": y1, "x2": x2, "y2": y2})
        return 5

    # Phase 2: Tk variables
    @staticmethod
    def handle_gui_var_new(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_var_new <name> <type>
        if index + 2 >= len(tokens):
            state.add_error("gui_var_new requires: gui_var_new <name> <type>")
            return 0
        name = tokens[index + 1]
        vtype = tokens[index + 2].lower()
        if vtype not in {"string", "int", "bool", "double"}:
            state.add_error("gui_var_new type must be one of: string, int, bool, double")
            return 0
        state.gui_vars[name] = {"type": vtype, "value": "" if vtype == "string" else 0}
        return 2

    @staticmethod
    def handle_gui_var_set(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_var_set <name> <value>
        if index + 2 >= len(tokens):
            state.add_error("gui_var_set requires: gui_var_set <name> <value>")
            return 0
        name = tokens[index + 1]
        value_token = tokens[index + 2]
        spec = state.gui_vars.get(name)
        if spec is None:
            state.add_error(f"GUI var '{name}' does not exist")
            return 0
        spec["value"] = GuiOpsHandler._resolve_value_token(state, value_token)

        runtime_var = state.gui_runtime_vars.get(name)
        if runtime_var is not None and hasattr(runtime_var, "set"):
            try:
                runtime_var.set(spec["value"])
            except Exception:
                pass
        return 2

    @staticmethod
    def handle_gui_var_get(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_var_get <name> <target> [str|var]
        if index + 2 >= len(tokens):
            state.add_error("gui_var_get requires: gui_var_get <name> <target> [str|var]")
            return 0
        name = tokens[index + 1]
        target = tokens[index + 2]
        mode = "str"
        if index + 3 < len(tokens):
            candidate = tokens[index + 3].lower()
            if candidate in {"str", "var"}:
                mode = candidate

        spec = state.gui_vars.get(name)
        if spec is None:
            state.add_error(f"GUI var '{name}' does not exist")
            return 0
        value = spec.get("value", "")
        runtime_var = state.gui_runtime_vars.get(name)
        if runtime_var is not None and hasattr(runtime_var, "get"):
            try:
                value = runtime_var.get()
            except Exception:
                pass
        GuiOpsHandler._store_value(state, target, mode, value)
        return 3 if index + 3 < len(tokens) and tokens[index + 3].lower() in {"str", "var"} else 2

    # Phase 3: menus
    @staticmethod
    def handle_gui_menubar(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_menubar <name> <window>
        if index + 2 >= len(tokens):
            state.add_error("gui_menubar requires: gui_menubar <name> <window>")
            return 0
        name = tokens[index + 1]
        window = tokens[index + 2]
        window_spec = GuiOpsHandler._require_spec(state, window, kind="window")
        if window_spec is None:
            return 0
        state.gui_specs[name] = {"type": "menubar", "parent": window, "children": []}
        window_spec["menubar"] = name
        state.gui_order.append(name)
        return 2

    @staticmethod
    def handle_gui_menu(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_menu <name> <parent_menu_or_menubar> "label"
        if index + 3 >= len(tokens):
            state.add_error('gui_menu requires: gui_menu <name> <parent> "label"')
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        label_token = tokens[index + 3]
        label = DataTypesHandler._resolve_string_token(state, label_token, "Menu label")
        if label is None:
            return 0

        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        if parent_spec.get("type") not in {"menubar", "menu"}:
            state.add_error(f"GUI object '{parent}' is not a menubar or menu")
            return 0

        state.gui_specs[name] = {"type": "menu", "parent": parent, "label": label, "children": []}
        if isinstance(parent_spec.get("children"), list):
            parent_spec["children"].append(name)
        state.gui_order.append(name)
        return 3

    @staticmethod
    def handle_gui_menu_item(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_menu_item <name> <menu> "label" [fn]
        if index + 3 >= len(tokens):
            state.add_error('gui_menu_item requires: gui_menu_item <name> <menu> "label" [fn]')
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        label_token = tokens[index + 3]

        label = DataTypesHandler._resolve_string_token(state, label_token, "Menu item label")
        if label is None:
            return 0

        fn: Optional[str] = None
        consumed = 3
        if index + 4 < len(tokens):
            candidate = tokens[index + 4]
            from .basic_commands import BasicCommandHandler

            if (
                candidate not in {"end", "case", "default", "catch"}
                and candidate not in BasicCommandHandler.KNOWN_COMMANDS
                and not (candidate.startswith('"') and candidate.endswith('"'))
            ):
                fn = candidate
                consumed = 4

        parent_spec = GuiOpsHandler._require_spec(state, parent, kind="menu")
        if parent_spec is None:
            return 0

        state.gui_specs[name] = {"type": "menu_item", "parent": parent, "label": label, "fn": fn}
        if isinstance(parent_spec.get("children"), list):
            parent_spec["children"].append(name)
        state.gui_order.append(name)
        return consumed

    # Phase 3: dialogs
    @staticmethod
    def handle_gui_messagebox(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_messagebox <type> "title" "message" <target> [str|var]
        if index + 4 >= len(tokens):
            state.add_error('gui_messagebox requires: gui_messagebox <type> "title" "message" <target> [str|var]')
            return 0
        mtype = tokens[index + 1].lower()
        title_token = tokens[index + 2]
        message_token = tokens[index + 3]
        target = tokens[index + 4]

        mode = "str"
        if index + 5 < len(tokens):
            candidate = tokens[index + 5].lower()
            if candidate in {"str", "var"}:
                mode = candidate

        title = DataTypesHandler._resolve_string_token(state, title_token, "Messagebox title")
        if title is None:
            return 0
        message = DataTypesHandler._resolve_string_token(state, message_token, "Messagebox message")
        if message is None:
            return 0

        # Require a running GUI (typically called from callbacks while gui_mainloop is active)
        if not state.gui_runtime_widgets:
            state.add_error("GUI dialogs require a running GUI (call gui_mainloop first)")
            return 0

        try:
            import tkinter.messagebox as messagebox
        except Exception:
            state.add_error("tkinter messagebox not available")
            return 0

        result: object = ""
        try:
            if mtype in {"info", "showinfo"}:
                messagebox.showinfo(title, message)
                result = "ok"
            elif mtype in {"warning", "showwarning"}:
                messagebox.showwarning(title, message)
                result = "ok"
            elif mtype in {"error", "showerror"}:
                messagebox.showerror(title, message)
                result = "ok"
            elif mtype in {"yesno", "askyesno"}:
                result = 1 if messagebox.askyesno(title, message) else 0
            elif mtype in {"okcancel", "askokcancel"}:
                result = 1 if messagebox.askokcancel(title, message) else 0
            else:
                state.add_error("gui_messagebox type must be one of: info, warning, error, yesno, okcancel")
                return 0
        except Exception as e:
            state.add_error(f"GUI dialog error: {e}")
            return 0

        GuiOpsHandler._store_value(state, target, mode, result)
        return 5 if index + 5 < len(tokens) and tokens[index + 5].lower() in {"str", "var"} else 4

    @staticmethod
    def handle_gui_filedialog_open(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_filedialog_open "title" <target> [str|var]
        if index + 2 >= len(tokens):
            state.add_error('gui_filedialog_open requires: gui_filedialog_open "title" <target> [str|var]')
            return 0
        title_token = tokens[index + 1]
        target = tokens[index + 2]
        mode = "str"
        if index + 3 < len(tokens):
            candidate = tokens[index + 3].lower()
            if candidate in {"str", "var"}:
                mode = candidate

        title = DataTypesHandler._resolve_string_token(state, title_token, "File dialog title")
        if title is None:
            return 0

        if not state.gui_runtime_widgets:
            state.add_error("GUI dialogs require a running GUI (call gui_mainloop first)")
            return 0

        try:
            import tkinter.filedialog as filedialog
        except Exception:
            state.add_error("tkinter filedialog not available")
            return 0

        try:
            path = filedialog.askopenfilename(title=title)
        except Exception as e:
            state.add_error(f"GUI dialog error: {e}")
            return 0

        GuiOpsHandler._store_value(state, target, mode, path)
        return 3 if index + 3 < len(tokens) and tokens[index + 3].lower() in {"str", "var"} else 2

    @staticmethod
    def handle_gui_filedialog_save(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_filedialog_save "title" <target> [str|var]
        if index + 2 >= len(tokens):
            state.add_error('gui_filedialog_save requires: gui_filedialog_save "title" <target> [str|var]')
            return 0
        title_token = tokens[index + 1]
        target = tokens[index + 2]
        mode = "str"
        if index + 3 < len(tokens):
            candidate = tokens[index + 3].lower()
            if candidate in {"str", "var"}:
                mode = candidate

        title = DataTypesHandler._resolve_string_token(state, title_token, "File dialog title")
        if title is None:
            return 0

        if not state.gui_runtime_widgets:
            state.add_error("GUI dialogs require a running GUI (call gui_mainloop first)")
            return 0

        try:
            import tkinter.filedialog as filedialog
        except Exception:
            state.add_error("tkinter filedialog not available")
            return 0

        try:
            path = filedialog.asksaveasfilename(title=title)
        except Exception as e:
            state.add_error(f"GUI dialog error: {e}")
            return 0

        GuiOpsHandler._store_value(state, target, mode, path)
        return 3 if index + 3 < len(tokens) and tokens[index + 3].lower() in {"str", "var"} else 2

    @staticmethod
    def handle_gui_destroy(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_destroy <name>
        if index + 1 >= len(tokens):
            state.add_error("gui_destroy requires: gui_destroy <name>")
            return 0
        name = tokens[index + 1]
        spec = GuiOpsHandler._get_spec(state, name)
        if spec is None:
            state.add_error(f"GUI object '{name}' does not exist")
            return 0

        parent = spec.get("parent")
        if isinstance(parent, str):
            parent_spec = state.gui_specs.get(parent)
            if parent_spec and isinstance(parent_spec.get("children"), list):
                parent_spec["children"] = [c for c in parent_spec["children"] if c != name]

        state.gui_specs.pop(name, None)
        state.gui_order = [n for n in state.gui_order if n != name]
        return 1

    @staticmethod
    def handle_gui_mainloop(state: InterpreterState, tokens: List[str], index: int, base_dir: str) -> int:
        # gui_mainloop <window>
        if index + 1 >= len(tokens):
            state.add_error("gui_mainloop requires: gui_mainloop <window>")
            return 0

        window_name = tokens[index + 1]
        window_spec = GuiOpsHandler._require_spec(state, window_name, kind="window")
        if window_spec is None:
            return 0

        backend = state.gui_backend

        try:
            if backend == "ctk":
                try:
                    import customtkinter as ctk  # type: ignore
                except Exception:
                    state.add_error("'customtkinter' library not available")
                    return 0

                # Apply CTk settings before creating any widgets.
                try:
                    if isinstance(state.gui_ctk_appearance, str) and state.gui_ctk_appearance:
                        ctk.set_appearance_mode(state.gui_ctk_appearance)
                except Exception:
                    pass
                try:
                    if isinstance(state.gui_ctk_theme, str) and state.gui_ctk_theme:
                        theme_value = state.gui_ctk_theme
                        if theme_value.lower().endswith(".json") or ("/" in theme_value) or ("\\" in theme_value):
                            theme_path = Path(theme_value)
                            if not theme_path.is_absolute():
                                theme_path = Path(base_dir) / theme_path
                            ctk.set_default_color_theme(str(theme_path))
                        else:
                            ctk.set_default_color_theme(theme_value)
                except Exception:
                    pass
                try:
                    if isinstance(state.gui_ctk_scaling, (int, float)) and state.gui_ctk_scaling:
                        ctk.set_widget_scaling(float(state.gui_ctk_scaling) / 100.0)
                except Exception:
                    pass

                ui = ctk
                root_factory = ctk.CTk
                toplevel_factory = ctk.CTkToplevel
                label_factory = ctk.CTkLabel
                button_factory = ctk.CTkButton
                entry_factory = ctk.CTkEntry
                frame_factory = ctk.CTkFrame
            else:
                import tkinter as tk

                ui = tk
                root_factory = tk.Tk
                toplevel_factory = tk.Toplevel
                label_factory = tk.Label
                button_factory = tk.Button
                entry_factory = tk.Entry
                frame_factory = tk.Frame
        except Exception as e:
            state.add_error(f"GUI backend import failed: {e}")
            return 0

        # Realize windows first in creation order
        realized: Dict[str, object] = {}
        root = None

        runtime_vars: Dict[str, object] = {}

        def _make_window(name: str, spec: Dict[str, object]):
            nonlocal root
            title = str(spec.get("title", ""))
            width = int(spec.get("width", 400))
            height = int(spec.get("height", 300))

            if root is None:
                w = root_factory()
                root = w
            else:
                w = toplevel_factory(root)

            if hasattr(w, "title"):
                w.title(title)
            if hasattr(w, "geometry"):
                w.geometry(f"{width}x{height}")
            return w

        try:
            for name in state.gui_order:
                spec = state.gui_specs.get(name)
                if not spec or spec.get("type") != "window":
                    continue
                realized[name] = _make_window(name, spec)

            if window_name not in realized:
                realized[window_name] = _make_window(window_name, window_spec)

            # Now that root exists, create Tk variables (works for both tk and ctk).
            try:
                if tk_mod is not None:
                    for var_name, var_spec in state.gui_vars.items():
                        vtype = str(var_spec.get("type", "string")).lower()
                        if vtype == "int":
                            runtime_vars[var_name] = tk_mod.IntVar(master=root)
                        elif vtype == "bool":
                            runtime_vars[var_name] = tk_mod.BooleanVar(master=root)
                        elif vtype == "double":
                            runtime_vars[var_name] = tk_mod.DoubleVar(master=root)
                        else:
                            runtime_vars[var_name] = tk_mod.StringVar(master=root)
                        try:
                            runtime_vars[var_name].set(var_spec.get("value", ""))
                        except Exception:
                            pass
            except Exception:
                runtime_vars = {}

            # Create non-window widgets in order
            from .executor import CommandExecutor  # local import to avoid cycles at module import time

            def _make_on_click(fn_name: str):
                def _callback():
                    executor = CommandExecutor(state, base_dir)
                    executor.execute_block(["call", fn_name])

                return _callback

            def _apply_layout(widget_obj: object, widget_spec: Dict[str, object]) -> None:
                layout = widget_spec.get("layout")
                if isinstance(layout, dict):
                    mgr = layout.get("manager")
                    opts = layout.get("options")
                    if isinstance(opts, dict):
                        call_opts = {str(k): v for k, v in opts.items()}
                    else:
                        call_opts = {}
                    try:
                        if mgr == "grid" and hasattr(widget_obj, "grid"):
                            widget_obj.grid(**call_opts)
                            return
                        if mgr == "pack" and hasattr(widget_obj, "pack"):
                            widget_obj.pack(**call_opts)
                            return
                    except Exception:
                        pass
                # Default layout
                if hasattr(widget_obj, "pack"):
                    try:
                        widget_obj.pack()
                    except Exception:
                        pass

            def _resolve_runtime_option_value(val: object) -> object:
                # Allow special references like gui_var names and widget.method references.
                if isinstance(val, str) and val in runtime_vars:
                    return runtime_vars[val]
                if isinstance(val, str) and "." in val:
                    wname, meth = val.split(".", 1)
                    wobj = realized.get(wname)
                    if wobj is not None and hasattr(wobj, meth):
                        try:
                            return getattr(wobj, meth)
                        except Exception:
                            return val
                return val

            # Expose runtime handles separately from spec while the GUI runs.
            state.gui_runtime_widgets = realized
            state.gui_runtime_vars = runtime_vars
            state.gui_runtime_base_dir = base_dir

            # ttk style/theme (tk only)
            ttk = None
            ttk_style = None
            if backend != "ctk":
                try:
                    import tkinter.ttk as ttk  # type: ignore

                    ttk_style = ttk.Style(master=root)
                    if isinstance(state.gui_ttk_theme, str) and state.gui_ttk_theme:
                        try:
                            ttk_style.theme_use(state.gui_ttk_theme)
                        except Exception:
                            pass
                    if isinstance(state.gui_ttk_styles, dict):
                        for style_name, opts in state.gui_ttk_styles.items():
                            if not isinstance(opts, dict):
                                continue
                            resolved = {str(k): _resolve_runtime_option_value(v) for k, v in opts.items()}
                            try:
                                ttk_style.configure(style_name, **resolved)
                            except Exception:
                                pass
                except Exception:
                    ttk = None
                    ttk_style = None

            for name in state.gui_order:
                spec = state.gui_specs.get(name)
                if not spec:
                    continue
                kind = spec.get("type")
                if kind in {"window", "menubar", "menu", "menu_item"}:
                    continue

                parent_name = spec.get("parent")
                if not isinstance(parent_name, str) or parent_name not in realized:
                    state.add_error(f"GUI object '{name}' has invalid parent '{parent_name}'")
                    return 0

                parent_obj = realized[parent_name]

                options = spec.get("options")
                if not isinstance(options, dict):
                    options = {}

                runtime_options: Dict[str, object] = {}
                for k, v in options.items():
                    runtime_options[str(k)] = _resolve_runtime_option_value(v)

                if kind == "label":
                    w = label_factory(parent_obj, text=str(spec.get("text", "")), **runtime_options)
                elif kind == "button":
                    cmd = None
                    fn = spec.get("on_click")
                    if isinstance(fn, str) and fn:
                        cmd = _make_on_click(fn)
                    # Prevent user-specified command from overriding TechLang callback
                    runtime_options.pop("command", None)
                    w = button_factory(parent_obj, text=str(spec.get("text", "")), command=cmd, **runtime_options)
                elif kind == "entry":
                    w = entry_factory(parent_obj, **runtime_options)
                    if "value" in spec and hasattr(w, "insert"):
                        w.insert(0, str(spec.get("value", "")))
                elif kind == "frame":
                    w = frame_factory(parent_obj, **runtime_options)
                elif kind == "ttk_button":
                    if ttk is None:
                        state.add_error("ttk widgets require tk backend")
                        return 0
                    cmd = None
                    fn = spec.get("on_click")
                    if isinstance(fn, str) and fn:
                        cmd = _make_on_click(fn)
                    runtime_options.pop("command", None)
                    w = ttk.Button(parent_obj, text=str(spec.get("text", "")), command=cmd, **runtime_options)
                elif kind == "ttk_label":
                    if ttk is None:
                        state.add_error("ttk widgets require tk backend")
                        return 0
                    w = ttk.Label(parent_obj, text=str(spec.get("text", "")), **runtime_options)
                elif kind == "ttk_entry":
                    if ttk is None:
                        state.add_error("ttk widgets require tk backend")
                        return 0
                    w = ttk.Entry(parent_obj, **runtime_options)
                    if "value" in spec and hasattr(w, "insert"):
                        w.insert(0, str(spec.get("value", "")))
                elif kind == "ttk_combobox":
                    if ttk is None:
                        state.add_error("ttk widgets require tk backend")
                        return 0
                    w = ttk.Combobox(parent_obj, **runtime_options)
                elif kind == "ttk_treeview":
                    if ttk is None:
                        state.add_error("ttk widgets require tk backend")
                        return 0
                    w = ttk.Treeview(parent_obj, **runtime_options)
                elif kind == "ttk_notebook":
                    if ttk is None:
                        state.add_error("ttk widgets require tk backend")
                        return 0
                    w = ttk.Notebook(parent_obj, **runtime_options)
                elif kind == "ttk_progressbar":
                    if ttk is None:
                        state.add_error("ttk widgets require tk backend")
                        return 0
                    w = ttk.Progressbar(parent_obj, **runtime_options)
                elif kind == "ttk_separator":
                    if ttk is None:
                        state.add_error("ttk widgets require tk backend")
                        return 0
                    w = ttk.Separator(parent_obj, **runtime_options)
                elif kind == "checkbutton":
                    var_name = spec.get("var")
                    var_obj = runtime_vars.get(var_name) if isinstance(var_name, str) else None
                    if var_obj is not None:
                        runtime_options.setdefault("variable", var_obj)
                    if backend == "ctk" and ctk_mod is not None and hasattr(ctk_mod, "CTkCheckBox"):
                        w = ctk_mod.CTkCheckBox(parent_obj, text=str(spec.get("text", "")), **runtime_options)
                    else:
                        w = tk_mod.Checkbutton(parent_obj, text=str(spec.get("text", "")), **runtime_options)
                elif kind == "radiobutton":
                    var_name = spec.get("var")
                    var_obj = runtime_vars.get(var_name) if isinstance(var_name, str) else None
                    if var_obj is not None:
                        runtime_options.setdefault("variable", var_obj)
                    runtime_options.setdefault("value", spec.get("value"))
                    if backend == "ctk" and ctk_mod is not None and hasattr(ctk_mod, "CTkRadioButton"):
                        w = ctk_mod.CTkRadioButton(parent_obj, text=str(spec.get("text", "")), **runtime_options)
                    else:
                        w = tk_mod.Radiobutton(parent_obj, text=str(spec.get("text", "")), **runtime_options)
                elif kind == "text":
                    if backend == "ctk" and ctk_mod is not None and hasattr(ctk_mod, "CTkTextbox"):
                        w = ctk_mod.CTkTextbox(parent_obj, **runtime_options)
                    else:
                        w = tk_mod.Text(parent_obj, **runtime_options)
                    # Apply spec-first content, if any
                    content = spec.get("content")
                    if isinstance(content, str) and hasattr(w, "insert"):
                        try:
                            w.insert("end", content)
                        except Exception:
                            pass
                    tags = spec.get("tags")
                    if isinstance(tags, dict) and hasattr(w, "tag_config"):
                        for tag_name, tag_spec in tags.items():
                            if not isinstance(tag_spec, dict):
                                continue
                            opts = tag_spec.get("options")
                            if isinstance(opts, dict):
                                try:
                                    w.tag_config(tag_name, **{str(k): v for k, v in opts.items()})
                                except Exception:
                                    pass
                elif kind == "listbox":
                    w = tk_mod.Listbox(parent_obj, **runtime_options)
                elif kind == "canvas":
                    w = tk_mod.Canvas(parent_obj, **runtime_options)
                    items = spec.get("items")
                    if isinstance(items, list):
                        for item in items:
                            if not isinstance(item, dict):
                                continue
                            ik = item.get("kind")
                            try:
                                if ik == "line" and hasattr(w, "create_line"):
                                    w.create_line(item.get("x1"), item.get("y1"), item.get("x2"), item.get("y2"))
                            except Exception:
                                pass
                elif kind == "scrollbar":
                    orient = str(spec.get("orient", "vertical")).lower()
                    if backend == "ctk" and ctk_mod is not None and hasattr(ctk_mod, "CTkScrollbar"):
                        # CTkScrollbar uses `orientation` (string) rather than tk's `orient` constants.
                        runtime_options.pop("orient", None)
                        runtime_options.setdefault("orientation", "horizontal" if orient == "horizontal" else "vertical")
                        try:
                            w = ctk_mod.CTkScrollbar(parent_obj, **runtime_options)
                        except Exception:
                            # Fallback to tk.Scrollbar
                            runtime_options.pop("orientation", None)
                            if orient == "horizontal":
                                runtime_options.setdefault("orient", tk_mod.HORIZONTAL)
                            else:
                                runtime_options.setdefault("orient", tk_mod.VERTICAL)
                            w = tk_mod.Scrollbar(parent_obj, **runtime_options)
                    else:
                        if orient == "horizontal":
                            runtime_options.setdefault("orient", tk_mod.HORIZONTAL)
                        else:
                            runtime_options.setdefault("orient", tk_mod.VERTICAL)
                        w = tk_mod.Scrollbar(parent_obj, **runtime_options)

                # --- CTk-first widgets (CTK-4) ---
                elif kind == "ctk_switch":
                    if backend != "ctk" or ctk_mod is None:
                        state.add_error("ctk widgets require ctk backend")
                        return 0
                    var_name = spec.get("var")
                    var_obj = runtime_vars.get(var_name) if isinstance(var_name, str) else None
                    if var_obj is not None:
                        runtime_options.setdefault("variable", var_obj)
                    w = ctk_mod.CTkSwitch(parent_obj, text=str(spec.get("text", "")), **runtime_options)

                elif kind == "ctk_slider":
                    if backend != "ctk" or ctk_mod is None:
                        state.add_error("ctk widgets require ctk backend")
                        return 0
                    var_name = spec.get("var")
                    var_obj = runtime_vars.get(var_name) if isinstance(var_name, str) else None
                    if var_obj is not None:
                        runtime_options.setdefault("variable", var_obj)
                    w = ctk_mod.CTkSlider(parent_obj, **runtime_options)

                elif kind == "ctk_progressbar":
                    if backend != "ctk" or ctk_mod is None:
                        state.add_error("ctk widgets require ctk backend")
                        return 0
                    var_name = spec.get("var")
                    var_obj = runtime_vars.get(var_name) if isinstance(var_name, str) else None
                    if var_obj is not None:
                        runtime_options.setdefault("variable", var_obj)
                    w = ctk_mod.CTkProgressBar(parent_obj, **runtime_options)
                    if "value" in spec and hasattr(w, "set"):
                        try:
                            w.set(float(spec.get("value", 0)))
                        except Exception:
                            pass

                elif kind == "ctk_optionmenu":
                    if backend != "ctk" or ctk_mod is None:
                        state.add_error("ctk widgets require ctk backend")
                        return 0
                    values = spec.get("values")
                    if not isinstance(values, list):
                        values = []
                    var_name = spec.get("var")
                    var_obj = runtime_vars.get(var_name) if isinstance(var_name, str) else None
                    if var_obj is not None:
                        runtime_options.setdefault("variable", var_obj)
                    w = ctk_mod.CTkOptionMenu(parent_obj, values=[str(v) for v in values], **runtime_options)

                elif kind == "ctk_combobox":
                    if backend != "ctk" or ctk_mod is None:
                        state.add_error("ctk widgets require ctk backend")
                        return 0
                    values = spec.get("values")
                    if not isinstance(values, list):
                        values = []
                    var_name = spec.get("var")
                    var_obj = runtime_vars.get(var_name) if isinstance(var_name, str) else None
                    if var_obj is not None:
                        runtime_options.setdefault("variable", var_obj)
                    w = ctk_mod.CTkComboBox(parent_obj, values=[str(v) for v in values], **runtime_options)

                elif kind == "ctk_tabview":
                    if backend != "ctk" or ctk_mod is None:
                        state.add_error("ctk widgets require ctk backend")
                        return 0
                    w = ctk_mod.CTkTabview(parent_obj, **runtime_options)

                elif kind == "ctk_tab":
                    if backend != "ctk" or ctk_mod is None:
                        state.add_error("ctk widgets require ctk backend")
                        return 0
                    label = str(spec.get("label", ""))
                    if not hasattr(parent_obj, "add"):
                        state.add_error("ctk_tab parent must be a ctk_tabview")
                        return 0
                    try:
                        w = parent_obj.add(label)
                    except Exception:
                        if hasattr(parent_obj, "tab"):
                            try:
                                w = parent_obj.tab(label)
                            except Exception:
                                state.add_error("Failed to create ctk tab")
                                return 0
                        else:
                            state.add_error("Failed to create ctk tab")
                            return 0
                else:
                    state.add_error(f"Unsupported GUI widget type '{kind}'")
                    return 0

                realized[name] = w

                # Apply bindings registered in the spec
                bindings = spec.get("bindings")
                if isinstance(bindings, dict) and hasattr(w, "bind"):
                    for ev, fn_name in bindings.items():
                        if not isinstance(ev, str) or not isinstance(fn_name, str) or not fn_name:
                            continue
                        try:
                            def _mk(fn: str):
                                def _cb(_evt=None):
                                    executor = CommandExecutor(state, base_dir)
                                    executor.execute_block(["call", fn])

                                return _cb

                            w.bind(ev, _mk(fn_name))
                        except Exception:
                            pass

                if kind != "ctk_tab":
                    _apply_layout(w, spec)

            # Notebook tab attachments (ttk)
            if backend != "ctk" and ttk is not None:
                for name in state.gui_order:
                    spec = state.gui_specs.get(name)
                    if not spec or spec.get("type") != "ttk_notebook":
                        continue
                    nb = realized.get(name)
                    if nb is None or not hasattr(nb, "add"):
                        continue
                    tabs = spec.get("tabs")
                    if not isinstance(tabs, list):
                        continue
                    for tab in tabs:
                        if not isinstance(tab, dict):
                            continue
                        child_name = tab.get("child")
                        label = tab.get("label")
                        if not isinstance(child_name, str) or child_name not in realized:
                            continue
                        child_obj = realized[child_name]
                        try:
                            nb.add(child_obj, text=str(label) if label is not None else "")
                        except Exception:
                            pass

            # Menus (tk only)
            if backend != "ctk":
                for win_name, win_obj in realized.items():
                    win_spec = state.gui_specs.get(win_name)
                    if not win_spec or win_spec.get("type") != "window":
                        continue
                    menubar_name = win_spec.get("menubar")
                    if not isinstance(menubar_name, str):
                        continue
                    menubar_spec = state.gui_specs.get(menubar_name)
                    if not menubar_spec or menubar_spec.get("type") != "menubar":
                        continue
                    try:
                        bar = ui.Menu(win_obj)
                    except Exception:
                        continue
                    realized[menubar_name] = bar
                    try:
                        win_obj.config(menu=bar)
                    except Exception:
                        pass

                    def _build_menu(menu_name: str, parent_menu_obj: object) -> None:
                        menu_spec = state.gui_specs.get(menu_name)
                        if not menu_spec or menu_spec.get("type") != "menu":
                            return
                        try:
                            m = ui.Menu(parent_menu_obj, tearoff=0)
                        except Exception:
                            return
                        realized[menu_name] = m
                        label = str(menu_spec.get("label", ""))
                        try:
                            parent_menu_obj.add_cascade(label=label, menu=m)
                        except Exception:
                            pass
                        children = menu_spec.get("children")
                        if not isinstance(children, list):
                            return
                        for child_name in children:
                            child_spec = state.gui_specs.get(child_name)
                            if not child_spec:
                                continue
                            ctype = child_spec.get("type")
                            if ctype == "menu":
                                _build_menu(child_name, m)
                            elif ctype == "menu_item":
                                item_label = str(child_spec.get("label", ""))
                                fn_name = child_spec.get("fn")
                                cmd = None
                                if isinstance(fn_name, str) and fn_name:
                                    cmd = _make_on_click(fn_name)
                                try:
                                    m.add_command(label=item_label, command=cmd)
                                except Exception:
                                    pass

                    children = menubar_spec.get("children")
                    if isinstance(children, list):
                        for menu_name in children:
                            _build_menu(menu_name, bar)

            # Keep entry specs updated when window closes by reading final values
            if root is None:
                state.add_error("GUI could not start (no root window)")
                return 0

            # Optional integration-test helper: schedule an auto-close.
            # Only active when TECHLANG_GUI_AUTOCLOSE_MS is set.
            try:
                import os

                ms_raw = os.environ.get("TECHLANG_GUI_AUTOCLOSE_MS", "").strip()
                if ms_raw:
                    ms = int(ms_raw)
                    if ms > 0 and hasattr(root, "after") and hasattr(root, "destroy"):
                        root.after(ms, root.destroy)
            except Exception:
                pass

            root.mainloop()

            # After GUI closes, sync entry values back into specs
            for name, spec in list(state.gui_specs.items()):
                if spec.get("type") != "entry":
                    continue
                widget = realized.get(name)
                if widget is not None and hasattr(widget, "get"):
                    try:
                        spec["value"] = widget.get()
                    except Exception:
                        pass

            # Sync ttk entry values back
            for name, spec in list(state.gui_specs.items()):
                if spec.get("type") != "ttk_entry":
                    continue
                widget = realized.get(name)
                if widget is not None and hasattr(widget, "get"):
                    try:
                        spec["value"] = widget.get()
                    except Exception:
                        pass

        except Exception as e:
            # Typical headless error: _tkinter.TclError: no display name and no $DISPLAY environment variable
            state.add_error(f"GUI runtime error: {e}")
            return 0

        # Clear runtime handles when mainloop ends.
        state.gui_runtime_widgets = {}
        state.gui_runtime_vars = {}
        state.gui_runtime_base_dir = "."

        return 1

    # -----------------
    # Phase 4: ttk
    # -----------------

    @staticmethod
    def _add_child(state: InterpreterState, parent: str, child: str) -> None:
        parent_spec = state.gui_specs.get(parent)
        if parent_spec and isinstance(parent_spec.get("children"), list):
            parent_spec["children"].append(child)

    @staticmethod
    def handle_gui_ttk_style_set(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ttk_style_set <style> "option" <value>
        if index + 3 >= len(tokens):
            state.add_error('gui_ttk_style_set requires: gui_ttk_style_set <style> "option" <value>')
            return 0
        style_name = tokens[index + 1]
        opt_token = tokens[index + 2]
        val_token = tokens[index + 3]

        opt = DataTypesHandler._resolve_string_token(state, opt_token, "ttk option")
        if opt is None:
            return 0
        val = GuiOpsHandler._resolve_value_token(state, val_token)
        if style_name not in state.gui_ttk_styles or not isinstance(state.gui_ttk_styles.get(style_name), dict):
            state.gui_ttk_styles[style_name] = {}
        state.gui_ttk_styles[style_name][str(opt)] = val
        return 3

    @staticmethod
    def handle_gui_ttk_theme_use(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ttk_theme_use "theme"
        if index + 1 >= len(tokens):
            state.add_error('gui_ttk_theme_use requires: gui_ttk_theme_use "theme"')
            return 0
        theme = DataTypesHandler._resolve_string_token(state, tokens[index + 1], "ttk theme")
        if theme is None:
            return 0
        state.gui_ttk_theme = theme
        return 1

    @staticmethod
    def handle_gui_ttk_button(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ttk_button <name> <parent> "text" [fn]
        if index + 3 >= len(tokens):
            state.add_error('gui_ttk_button requires: gui_ttk_button <name> <parent> "text" [fn]')
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        text = DataTypesHandler._resolve_string_token(state, tokens[index + 3], "Button text")
        if text is None:
            return 0

        from .basic_commands import BasicCommandHandler

        on_click: Optional[str] = None
        consumed = 3
        if index + 4 < len(tokens):
            candidate = tokens[index + 4]
            if (
                candidate not in {"end", "case", "default", "catch"}
                and candidate not in BasicCommandHandler.KNOWN_COMMANDS
                and not (candidate.startswith('"') and candidate.endswith('"'))
            ):
                on_click = candidate
                consumed = 4

        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {
            "type": "ttk_button",
            "parent": parent,
            "text": text,
            "on_click": on_click,
            "options": {},
            "bindings": {},
        }
        state.gui_order.append(name)
        GuiOpsHandler._add_child(state, parent, name)
        return consumed

    @staticmethod
    def handle_gui_ttk_label(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ttk_label <name> <parent> "text"
        if index + 3 >= len(tokens):
            state.add_error('gui_ttk_label requires: gui_ttk_label <name> <parent> "text"')
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        text = DataTypesHandler._resolve_string_token(state, tokens[index + 3], "Label text")
        if text is None:
            return 0
        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {"type": "ttk_label", "parent": parent, "text": text, "options": {}, "bindings": {}}
        state.gui_order.append(name)
        GuiOpsHandler._add_child(state, parent, name)
        return 3

    @staticmethod
    def handle_gui_ttk_entry(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ttk_entry <name> <parent>
        if index + 2 >= len(tokens):
            state.add_error("gui_ttk_entry requires: gui_ttk_entry <name> <parent>")
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {"type": "ttk_entry", "parent": parent, "options": {}, "bindings": {}}
        state.gui_order.append(name)
        GuiOpsHandler._add_child(state, parent, name)
        return 2

    @staticmethod
    def handle_gui_ttk_combobox(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ttk_combobox <name> <parent>
        if index + 2 >= len(tokens):
            state.add_error("gui_ttk_combobox requires: gui_ttk_combobox <name> <parent>")
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {"type": "ttk_combobox", "parent": parent, "options": {}, "bindings": {}}
        state.gui_order.append(name)
        GuiOpsHandler._add_child(state, parent, name)
        return 2

    @staticmethod
    def handle_gui_ttk_treeview(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ttk_treeview <name> <parent>
        if index + 2 >= len(tokens):
            state.add_error("gui_ttk_treeview requires: gui_ttk_treeview <name> <parent>")
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {"type": "ttk_treeview", "parent": parent, "options": {}, "bindings": {}}
        state.gui_order.append(name)
        GuiOpsHandler._add_child(state, parent, name)
        return 2

    @staticmethod
    def handle_gui_ttk_notebook(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ttk_notebook <name> <parent>
        if index + 2 >= len(tokens):
            state.add_error("gui_ttk_notebook requires: gui_ttk_notebook <name> <parent>")
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {"type": "ttk_notebook", "parent": parent, "options": {}, "bindings": {}, "tabs": []}
        state.gui_order.append(name)
        GuiOpsHandler._add_child(state, parent, name)
        return 2

    @staticmethod
    def handle_gui_ttk_notebook_tab(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ttk_notebook_tab <notebook> <child> "label"
        if index + 3 >= len(tokens):
            state.add_error('gui_ttk_notebook_tab requires: gui_ttk_notebook_tab <notebook> <child> "label"')
            return 0
        nb_name = tokens[index + 1]
        child = tokens[index + 2]
        label = DataTypesHandler._resolve_string_token(state, tokens[index + 3], "Tab label")
        if label is None:
            return 0
        nb_spec = GuiOpsHandler._require_spec(state, nb_name, kind="ttk_notebook")
        if nb_spec is None:
            return 0
        child_spec = GuiOpsHandler._require_spec(state, child)
        if child_spec is None:
            return 0
        tabs = nb_spec.get("tabs")
        if not isinstance(tabs, list):
            tabs = []
            nb_spec["tabs"] = tabs
        tabs.append({"child": child, "label": label})
        return 3

    @staticmethod
    def handle_gui_ttk_progressbar(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ttk_progressbar <name> <parent>
        if index + 2 >= len(tokens):
            state.add_error("gui_ttk_progressbar requires: gui_ttk_progressbar <name> <parent>")
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {"type": "ttk_progressbar", "parent": parent, "options": {}, "bindings": {}}
        state.gui_order.append(name)
        GuiOpsHandler._add_child(state, parent, name)
        return 2

    @staticmethod
    def handle_gui_ttk_separator(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_ttk_separator <name> <parent>
        if index + 2 >= len(tokens):
            state.add_error("gui_ttk_separator requires: gui_ttk_separator <name> <parent>")
            return 0
        name = tokens[index + 1]
        parent = tokens[index + 2]
        parent_spec = GuiOpsHandler._require_spec(state, parent)
        if parent_spec is None:
            return 0
        state.gui_specs[name] = {"type": "ttk_separator", "parent": parent, "options": {}, "bindings": {}}
        state.gui_order.append(name)
        GuiOpsHandler._add_child(state, parent, name)
        return 2

    # -----------------
    # Phase 5: advanced text/canvas
    # -----------------

    @staticmethod
    def handle_gui_text_insert(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_text_insert <text> <pos> "text"
        if index + 3 >= len(tokens):
            state.add_error('gui_text_insert requires: gui_text_insert <text> <pos> "text"')
            return 0
        name = tokens[index + 1]
        pos = tokens[index + 2]
        text = DataTypesHandler._resolve_string_token(state, tokens[index + 3], "Text to insert")
        if text is None:
            return 0
        spec = GuiOpsHandler._require_spec(state, name, kind="text")
        if spec is None:
            return 0
        content = spec.get("content")
        if not isinstance(content, str):
            content = ""
        if pos == "end":
            content = content + text
        elif pos in {"0", "start", "1.0"}:
            content = text + content
        else:
            state.add_error("gui_text_insert only supports pos: start|0|1.0|end")
            return 0
        spec["content"] = content
        widget = state.gui_runtime_widgets.get(name)
        if widget is not None and hasattr(widget, "insert"):
            try:
                widget.insert(pos, text)
            except Exception:
                try:
                    widget.insert("end", text)
                except Exception:
                    pass
        return 3

    @staticmethod
    def handle_gui_text_get(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_text_get <text> <target> [str|var]
        if index + 2 >= len(tokens):
            state.add_error("gui_text_get requires: gui_text_get <text> <target> [str|var]")
            return 0
        name = tokens[index + 1]
        target = tokens[index + 2]
        mode = "str"
        if index + 3 < len(tokens):
            candidate = tokens[index + 3].lower()
            if candidate in {"str", "var"}:
                mode = candidate

        spec = GuiOpsHandler._require_spec(state, name, kind="text")
        if spec is None:
            return 0

        value: object = spec.get("content", "")
        widget = state.gui_runtime_widgets.get(name)
        if widget is not None and hasattr(widget, "get"):
            try:
                value = widget.get("1.0", "end")
            except Exception:
                pass
        GuiOpsHandler._store_value(state, target, mode, value)
        return 3 if index + 3 < len(tokens) and tokens[index + 3].lower() in {"str", "var"} else 2

    @staticmethod
    def handle_gui_text_delete(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_text_delete <text> all
        if index + 2 >= len(tokens):
            state.add_error("gui_text_delete requires: gui_text_delete <text> all")
            return 0
        name = tokens[index + 1]
        scope = tokens[index + 2]
        spec = GuiOpsHandler._require_spec(state, name, kind="text")
        if spec is None:
            return 0
        if scope != "all":
            state.add_error("gui_text_delete only supports: all")
            return 0
        spec["content"] = ""
        widget = state.gui_runtime_widgets.get(name)
        if widget is not None and hasattr(widget, "delete"):
            try:
                widget.delete("1.0", "end")
            except Exception:
                pass
        return 2

    @staticmethod
    def handle_gui_text_tag_add(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_text_tag_add <text> <tag> <start> <end>
        if index + 4 >= len(tokens):
            state.add_error("gui_text_tag_add requires: gui_text_tag_add <text> <tag> <start> <end>")
            return 0
        name = tokens[index + 1]
        tag = tokens[index + 2]
        start = tokens[index + 3]
        end = tokens[index + 4]
        spec = GuiOpsHandler._require_spec(state, name, kind="text")
        if spec is None:
            return 0
        tags = spec.get("tags")
        if not isinstance(tags, dict):
            tags = {}
            spec["tags"] = tags
        if tag not in tags or not isinstance(tags.get(tag), dict):
            tags[tag] = {"ranges": [], "options": {}}
        ranges = tags[tag].get("ranges")
        if not isinstance(ranges, list):
            ranges = []
            tags[tag]["ranges"] = ranges
        ranges.append({"start": start, "end": end})

        widget = state.gui_runtime_widgets.get(name)
        if widget is not None and hasattr(widget, "tag_add"):
            try:
                widget.tag_add(tag, start, end)
            except Exception:
                pass
        return 4

    @staticmethod
    def handle_gui_text_tag_config(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_text_tag_config <text> <tag> [key value]...
        if index + 2 >= len(tokens):
            state.add_error("gui_text_tag_config requires: gui_text_tag_config <text> <tag> [key value]...")
            return 0
        name = tokens[index + 1]
        tag = tokens[index + 2]
        spec = GuiOpsHandler._require_spec(state, name, kind="text")
        if spec is None:
            return 0

        opts, consumed_opts = GuiOpsHandler._parse_kv_options(state, tokens, index + 3)
        tags = spec.get("tags")
        if not isinstance(tags, dict):
            tags = {}
            spec["tags"] = tags
        if tag not in tags or not isinstance(tags.get(tag), dict):
            tags[tag] = {"ranges": [], "options": {}}
        if not isinstance(tags[tag].get("options"), dict):
            tags[tag]["options"] = {}
        tags[tag]["options"].update(opts)

        widget = state.gui_runtime_widgets.get(name)
        if widget is not None and hasattr(widget, "tag_config"):
            try:
                widget.tag_config(tag, **{str(k): v for k, v in opts.items()})
            except Exception:
                pass
        return 2 + consumed_opts

    @staticmethod
    def handle_gui_canvas_create_line(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_canvas_create_line <canvas> x1 y1 x2 y2 [target [str|var]]
        if index + 5 >= len(tokens):
            state.add_error("gui_canvas_create_line requires: gui_canvas_create_line <canvas> x1 y1 x2 y2")
            return 0
        canvas_name = tokens[index + 1]
        spec = GuiOpsHandler._require_spec(state, canvas_name, kind="canvas")
        if spec is None:
            return 0
        try:
            x1 = float(tokens[index + 2])
            y1 = float(tokens[index + 3])
            x2 = float(tokens[index + 4])
            y2 = float(tokens[index + 5])
        except ValueError:
            state.add_error("Canvas coordinates must be numbers")
            return 0
        items = spec.get("items")
        if not isinstance(items, list):
            items = []
            spec["items"] = items

        item_id = len(items) + 1
        items.append({"id": item_id, "kind": "line", "x1": x1, "y1": y1, "x2": x2, "y2": y2})

        consumed = 5
        if index + 6 < len(tokens):
            target = tokens[index + 6]
            mode = "str"
            if index + 7 < len(tokens) and tokens[index + 7].lower() in {"str", "var"}:
                mode = tokens[index + 7].lower()
                consumed = 7
            else:
                consumed = 6
            GuiOpsHandler._store_value(state, target, mode, item_id)

        return consumed

    @staticmethod
    def handle_gui_canvas_move(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_canvas_move <canvas> <id> dx dy
        if index + 4 >= len(tokens):
            state.add_error("gui_canvas_move requires: gui_canvas_move <canvas> <id> dx dy")
            return 0
        canvas_name = tokens[index + 1]
        spec = GuiOpsHandler._require_spec(state, canvas_name, kind="canvas")
        if spec is None:
            return 0
        try:
            item_id = int(tokens[index + 2])
            dx = float(tokens[index + 3])
            dy = float(tokens[index + 4])
        except ValueError:
            state.add_error("Canvas move requires numeric id, dx, dy")
            return 0
        items = spec.get("items")
        if not isinstance(items, list):
            state.add_error("Canvas has no items")
            return 0
        for item in items:
            if isinstance(item, dict) and item.get("id") == item_id:
                for k in ("x1", "x2"):
                    if isinstance(item.get(k), (int, float)):
                        item[k] = float(item[k]) + dx
                for k in ("y1", "y2"):
                    if isinstance(item.get(k), (int, float)):
                        item[k] = float(item[k]) + dy
                break
        return 4

    @staticmethod
    def handle_gui_canvas_delete(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_canvas_delete <canvas> <id|all>
        if index + 2 >= len(tokens):
            state.add_error("gui_canvas_delete requires: gui_canvas_delete <canvas> <id|all>")
            return 0
        canvas_name = tokens[index + 1]
        target = tokens[index + 2]
        spec = GuiOpsHandler._require_spec(state, canvas_name, kind="canvas")
        if spec is None:
            return 0
        items = spec.get("items")
        if not isinstance(items, list):
            items = []
        if target == "all":
            spec["items"] = []
            return 2
        try:
            item_id = int(target)
        except ValueError:
            state.add_error("Canvas delete target must be an id or 'all'")
            return 0
        spec["items"] = [i for i in items if not (isinstance(i, dict) and i.get("id") == item_id)]
        return 2

    @staticmethod
    def handle_gui_canvas_coords(state: InterpreterState, tokens: List[str], index: int) -> int:
        # gui_canvas_coords <canvas> <id> <target> [str|var]
        if index + 3 >= len(tokens):
            state.add_error("gui_canvas_coords requires: gui_canvas_coords <canvas> <id> <target> [str|var]")
            return 0
        canvas_name = tokens[index + 1]
        try:
            item_id = int(tokens[index + 2])
        except ValueError:
            state.add_error("Canvas coords id must be an integer")
            return 0
        target = tokens[index + 3]
        mode = "str"
        if index + 4 < len(tokens) and tokens[index + 4].lower() in {"str", "var"}:
            mode = tokens[index + 4].lower()

        spec = GuiOpsHandler._require_spec(state, canvas_name, kind="canvas")
        if spec is None:
            return 0
        items = spec.get("items")
        if not isinstance(items, list):
            state.add_error("Canvas has no items")
            return 0
        coords = ""
        for item in items:
            if isinstance(item, dict) and item.get("id") == item_id:
                coords = f"{item.get('x1')} {item.get('y1')} {item.get('x2')} {item.get('y2')}"
                break
        GuiOpsHandler._store_value(state, target, mode, coords)
        return 4 if index + 4 < len(tokens) and tokens[index + 4].lower() in {"str", "var"} else 3
