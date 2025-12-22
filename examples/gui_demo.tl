# Minimal GUI demo (tkinter)

# Define a function that runs when the button is clicked

def on_click do
    print "Button clicked!"
end

# Build GUI spec

gui_backend tk

gui_window win "TechLang GUI" 420 200

gui_label title win "Hello from TechLang"

gui_entry input win

gui_entry_set input "Type here..."

gui_button btn win "Click me" on_click

# Start UI (blocking)

gui_mainloop win

# After window closes, you can read the final entry value

gui_entry_get input final_text
print final_text
