# TechLang GUI demo: Text + Canvas (spec-first)
# Run: tl examples/gui_text_canvas_demo.tl

gui_backend tk

gui_window win "Text + Canvas" 520 320

# Text widget with spec-first content

gui_text t win

gui_text_insert t end "Hello from Text\n"

gui_text_insert t end "This was built spec-first.\n"

# Tag a range and style it
gui_text_tag_add t highlight 1.0 1.5

gui_text_tag_config t highlight "foreground" "red"

# Canvas with a line item

gui_canvas c win

gui_canvas_create_line c 10 10 180 120 line_id var

# Show the id in output (spec-first; prints before mainloop)
print line_id

# Layout

gui_pack t "fill" "x" "padx" 10 "pady" 10

gui_pack c "fill" "both" "expand" 1 "padx" 10 "pady" 10

gui_mainloop win
