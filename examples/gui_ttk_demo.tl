# TechLang GUI + ttk demo
# Run: tl examples/gui_ttk_demo.tl

gui_backend tk

gui_window win "TechLang ttk Demo" 420 260

# Optional: pick a theme (depends on platform)
gui_ttk_theme_use "clam"

# Style example: give buttons padding
gui_ttk_style_set TButton "padding" 8

# Notebook with two tabs
gui_ttk_notebook nb win

gui_frame tab_one win

gui_frame tab_two win

gui_ttk_notebook_tab nb tab_one "One"

gui_ttk_notebook_tab nb tab_two "Two"

# Content

gui_ttk_label title tab_one "Hello from ttk"

gui_ttk_button ok tab_one "OK" on_ok

gui_ttk_label info tab_two "Second tab"

# Layout

gui_pack nb "fill" "both" "expand" 1

gui_pack title "padx" 10 "pady" 10

gui_pack ok "padx" 10 "pady" 10

gui_pack info "padx" 10 "pady" 10

# Click handler

def on_ok do
# Dialogs require runtime (this is called from a click)
    gui_messagebox "info" "Clicked" "You clicked OK" _ignored str
end

gui_mainloop win