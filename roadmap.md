# TechLang CustomTkinter Roadmap (ctk backend)

**Goal:** Make `gui_backend ctk` a first-class backend using **CustomTkinter** while keeping TechLang’s GUI architecture:

- **Spec-first** (build specs headlessly)
- **Realize-later** (`gui_mainloop` builds runtime objects)
- **Deterministic output** (no `print()` in handlers)
- **CI-safe tests** (spec validation + runtime-required error paths only)

This roadmap focuses on *implementation parity* for the existing TechLang GUI command surface, plus a small set of CTk-specific knobs where it materially improves UX.

---

## Design principles

1. **One command surface, two realizers**
   - Commands like `gui_button`, `gui_set`, `gui_pack`, `gui_bind`, etc. build the same spec regardless of backend.
   - Runtime realization chooses `tkinter` vs `customtkinter` factories based on `gui_backend`.

2. **Backend constraints are explicit**
   - If a command only works in `tk` (e.g., ttk widgets), it should report a clear error when backend is `ctk`.
   - Dialogs still require runtime (called from callbacks) and should keep consistent error wording.

3. **Spec fields stay stable**
   - Avoid backend-specific spec schemas whenever possible.
   - Backend-specific behavior is handled in the realizer via option mapping (e.g., CTk option names).

4. **Option mapping layer**
   - Some Tk options differ from CTk. Implement a small mapping layer in realization:
     - Common aliases (`bg` → `fg_color` / `bg_color` as appropriate)
     - Widget-specific aliases (`textvariable` support vs manual sync)
   - Unknown options should be ignored safely (or error only when clearly invalid).

5. **Test strategy stays headless**
   - Unit tests validate parsing + spec mutation.
   - Runtime-only features are tested as “requires runtime” error paths.
   - Optional integration tests can exist behind an env var, but must not be required in CI.

---

## Current state

- `gui_backend ctk` exists.
- If `customtkinter` is not installed, `gui_mainloop` emits a stable “library not available” error.
- Most command behavior is spec-first and already testable without creating windows.

---

## Roadmap

### Phase CTK-0: Dependency + runtime gating (stability)

**Objective:** Make CTk availability and runtime constraints predictable.

Deliverables:
- Ensure `gui_backend ctk` + `gui_mainloop`:
  - Emits a stable error if `customtkinter` is missing
  - Does not partially mutate runtime maps on failure
- Ensure dialogs (`gui_messagebox`, file dialogs) keep “requires runtime” behavior

Tests:
- Headless tests for missing `customtkinter` path
- Error-message snapshot assertions

Exit criteria:
- `gui_mainloop` behavior is stable when CTk is missing.

---

### Phase CTK-1: Core CTk widget realization parity

**Objective:** Realize the existing Phase 0–2 widget specs with CustomTkinter equivalents.

Target widgets:
- Window
- Frame
- Label
- Button
- Entry
- Checkbutton / Switch (map spec type to closest CTk widget)
- Radiobutton (if supported) or documented fallback

Deliverables:
- Option mapping for the most common options used in docs/examples:
  - text, state, width/height where applicable
  - colors via CTk built-in theming (avoid adding new hard-coded colors)
- Preserve layout behavior (`gui_pack`/`gui_grid`) as much as possible

Tests:
- Spec-first tests (already)
- “Backend constraint” tests (e.g., `ttk` commands rejected under `ctk`)

Exit criteria:
- Existing GUI examples can run under `gui_backend ctk` with minimal changes.

---

### Phase CTK-2: Variables + synchronization semantics

**Objective:** Make `gui_var_*` and entry/value syncing behave consistently.

Deliverables:
- Confirm which CTk widgets support Tk variables directly.
- Implement one consistent rule:
  - Prefer actual variable binding when available
  - Otherwise, store spec values and sync on:
    - widget creation
    - `gui_entry_set`
    - window close (same pattern used for tk Entry)

Tests:
- Headless tests for spec mutations
- Runtime-required paths remain unchanged

Exit criteria:
- `gui_var_new/set/get` work predictably with CTk realization.

---

### Phase CTK-3: Appearance controls (minimal CTk-specific additions)

**Objective:** Add only the CTk knobs that are important and stable.

Candidate commands (keep minimal):
- `gui_ctk_mode "light|dark|system"`
- `gui_ctk_theme "blue|green|dark-blue"` (or allow arbitrary theme name)

Deliverables:
- Store settings spec-first; apply at runtime before widget creation.

Tests:
- Spec storage tests
- If CTk missing: stable error path

Exit criteria:
- Users can switch appearance mode/theme without changing widget code.

---

### Phase CTK-4: CTk equivalents for advanced widgets

**Objective:** Expand beyond core form widgets.

Possible targets (depending on CTk support in your pinned version):
- Tabview as a notebook-like control
- Slider / Progressbar
- OptionMenu / ComboBox
- ScrollableFrame

Deliverables:
- Add new `gui_ctk_*` commands **only** if there is no good mapping from existing generic commands.
- Document any missing parity clearly.

Tests:
- Spec-first tests for new commands

Exit criteria:
- A small “modern UI” demo is feasible with CTk.

---

### Phase CTK-5: Examples + documentation

**Objective:** Make CTk usable and discoverable.

Deliverables:
- Add CTk-specific section to `docs/gui.md`:
  - how to install `customtkinter`
  - what is supported vs tk-only
  - the minimal appearance commands (if added)
- Add examples:
  - `examples/gui_ctk_demo.tl`
  - `examples/gui_ctk_form.tl`

Exit criteria:
- Users can run a CTk demo from `examples/` and understand limitations.

---

## Notes / Known constraints

- CustomTkinter is an external dependency; CI environments may not have it.
- Widget option compatibility is not 1:1 with tkinter; mapping should be conservative.
- Avoid introducing new hard-coded colors/themes in the interpreter; use CTk’s built-in theming instead.
