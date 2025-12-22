# GUI (Tkinter)

TechLang’s GUI support is **spec-first**: GUI commands build a *spec* in `InterpreterState`, and only `gui_mainloop <window>` realizes widgets and starts the event loop.

This design keeps GUI code testable in CI (tests validate parsing/specs without opening windows).

---

## Core concepts

- **Spec objects** live in `state.gui_specs` and are referenced by stable names.
- **Runtime handles** (real `tkinter` objects) are stored separately while the mainloop is running.
- **All output** must go through `state.add_output()` / `add_error()`.

---

## Phase 1 primitives (foundation)

### Universal properties

```techlang
gui_set <widget> "option" <value>
gui_get <widget> "option" <target> [str|var]
```

- `gui_set` stores options into the widget spec and (if the widget exists at runtime) attempts to apply them via `configure`.
- `gui_get` reads from runtime when available (via `cget`), otherwise from the stored spec.

### Layout

```techlang
gui_pack <widget> [key value]...
gui_grid <widget> [key value]...
```

These store layout info on the spec. When the GUI is realized, layout is applied; if no layout is specified, widgets are packed by default.

### Events

```techlang
gui_bind <widget> "<Event>" <fn>
```

Stores a binding in the spec and (if runtime is active) binds it immediately. Callbacks execute `call <fn>`.

---

## Phase 2: Core widget coverage (tk)

### Basic widgets

```techlang
gui_frame <name> <parent>
gui_label <name> <parent> "text"
gui_button <name> <parent> "text" [fn]
gui_entry <name> <parent>
gui_entry_get <entry> <target> [str|var]
gui_entry_set <entry> <"text"|stringVar>
```

### Additional widgets

```techlang
gui_checkbutton <name> <parent> "text" [var]
gui_radiobutton <name> <parent> "text" <var> <value>
gui_text <name> <parent>
gui_listbox <name> <parent>
gui_canvas <name> <parent>
gui_scrollbar <name> <parent> [vertical|horizontal]
```

### Tk variables

```techlang
gui_var_new <name> <string|int|bool|double>
gui_var_set <name> <value>
gui_var_get <name> <target> [str|var]
```

---

## Phase 3: Menus + dialogs

### Menus

```techlang
gui_menubar <name> <window>
gui_menu <name> <parent> "label"
gui_menu_item <name> <menu> "label" [fn]
```

### Dialogs

Dialogs require a running GUI (typically called from event callbacks):

```techlang
gui_messagebox <type> "title" "message" <target> [str|var]
gui_filedialog_open "title" <target> [str|var]
gui_filedialog_save "title" <target> [str|var]
```

---

## Phase 4: ttk widgets + styling (tk backend)

ttk widgets require the `tk` backend (not `ctk`).

### Theme + styles

```techlang
gui_ttk_theme_use "theme"
gui_ttk_style_set <style> "option" <value>
```

Notes:
- Theme/style changes are applied when `gui_mainloop` realizes the window.
- Options are stored spec-first and can be configured before the mainloop.

### ttk widgets

```techlang
gui_ttk_label <name> <parent> "text"
gui_ttk_button <name> <parent> "text" [fn]
gui_ttk_entry <name> <parent>
gui_ttk_combobox <name> <parent>
gui_ttk_treeview <name> <parent>
gui_ttk_progressbar <name> <parent>
gui_ttk_separator <name> <parent>
```

### Notebook tabs

```techlang
gui_ttk_notebook <name> <parent>
gui_ttk_notebook_tab <notebook> <child> "label"
```

---

## Phase 5: Advanced Text + Canvas APIs (spec-first)

These commands are designed to work headlessly by updating the widget spec. When a GUI is running, they also attempt to apply to runtime widgets where possible.

### Text content

```techlang
gui_text_insert <text> <start|0|1.0|end> "text"
gui_text_get <text> <target> [str|var]
gui_text_delete <text> all
```

### Text tags

```techlang
gui_text_tag_add <text> <tag> <start> <end>
gui_text_tag_config <text> <tag> [key value]...
```

### Canvas item helpers

```techlang
gui_canvas_create_line <canvas> x1 y1 x2 y2 [target [str|var]]
gui_canvas_move <canvas> <id> dx dy
gui_canvas_delete <canvas> <id|all>
gui_canvas_coords <canvas> <id> <target> [str|var]
```

---

## Lifecycle

```techlang
gui_backend <tk|ctk>
gui_window <name> "title" <w> <h>
gui_mainloop <window>
gui_destroy <name>
```

Notes:
- `gui_mainloop` is **blocking**.
- Specs are synchronized back after the window closes (e.g. entry text).

---

## GUI examples

Runnable examples:

- `examples/gui_ttk_demo.tl` — ttk widgets + styles + dialog from a click handler
- `examples/gui_text_canvas_demo.tl` — Text insert/tags + Canvas line item
