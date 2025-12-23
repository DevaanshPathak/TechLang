# TechLang CustomTkinter demo
# Requires: pip install customtkinter

# Pick CustomTkinter backend + theme settings

gui_backend ctk

gui_ctk_appearance dark
# Built-in themes usually include: blue, green, dark-blue
# Or pass a path to a theme json file.
gui_ctk_theme "blue"

gui_ctk_scaling 110

# Variables used for widget bindings

gui_var_new v_enabled bool

gui_var_new v_amount double

gui_var_new v_choice string

gui_var_new v_choice2 string

# Window + tabview

gui_window win "CTk Demo" 520 360

gui_ctk_tabview tabs win

gui_ctk_tab tab_main tabs "Main"

gui_ctk_tab tab_settings tabs "Settings"

# Main tab widgets

gui_label title tab_main "CTk-first widgets (TechLang)"

gui_pack title pady 10

gui_ctk_switch sw tab_main "Enabled" v_enabled

gui_pack sw pady 6

gui_label lbl_slider tab_main "Amount (slider)"

gui_pack lbl_slider pady 4

gui_ctk_slider sl tab_main v_amount

gui_pack sl fill "x" padx 20

gui_ctk_progressbar pb tab_main

gui_pack pb pady 10 fill "x" padx 20

# Update progress and print values on click

def on_apply do
    gui_ctk_progress_set pb 0.75
    gui_var_get v_enabled enabled str
    gui_var_get v_amount amount str
    gui_var_get v_choice choice str
    gui_var_get v_choice2 choice2 str
    print "Enabled:"
    print enabled
    print "Amount:"
    print amount
    print "Choice:"
    print choice
    print "Choice2:"
    print choice2
end

gui_button btn_apply tab_main "Apply" on_apply

gui_pack btn_apply pady 10

# Settings tab widgets

gui_label choose tab_settings "Pick values"

gui_pack choose pady 8

gui_ctk_optionmenu om tab_settings "Alpha,Beta,Gamma" v_choice

gui_pack om pady 6

gui_ctk_combobox cb tab_settings "One,Two,Three" v_choice2

gui_pack cb pady 6

# Run GUI

gui_mainloop win
