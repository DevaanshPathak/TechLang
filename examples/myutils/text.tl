# myutils/text.tl - Text utilities submodule

def greet input_name
    print "Hello,"
    print input_name
end
export greet

def shout input_text
    str_upper input_text
    print input_text
end
export shout

def whisper input_text
    str_lower input_text
    print input_text
end
export whisper
