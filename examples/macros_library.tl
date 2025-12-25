# TechLang Macro Library - Common Utilities
# This file can be loaded with :loadmacro in REPL or via macro imports

# Debug logging macro (conditional on debug variable)
macro debug_log if debug_enabled msg do
        print "[DEBUG]"
        print $msg
    end

# Repeat a command N times
    macro repeat_cmd n cmd arg do
        loop $n
            $cmd $arg
        end
    end

# Simple assertion macro
    macro assert condition msg do
        if $condition eq 0
            print "[ASSERTION FAILED]"
            print $msg
        end
    end

# Increment variable by N
    macro inc_by var amount do
        add $var $amount
    end

# Decrement variable by N
    macro dec_by var amount do
        sub $var $amount
    end

# Swap two variables
    macro swap a b do
        set temp $a
        set $a $b
        set $b temp
    end

# Print with prefix
    macro log_info msg do
        print "[INFO]"
        print $msg
    end

    macro log_error msg do
        print "[ERROR]"
        print $msg
    end

    macro log_warn msg do
        print "[WARNING]"
        print $msg
    end

# Safe division (check for zero)
    macro safe_div numerator denominator result do
        if $denominator eq 0
            print "[Error: Division by zero]"
            set $result 0
            else
            set $result $numerator
            div $result $denominator
        end
    end

# Clamp value between min and max (using basic commands)
    macro clamp_value val min_v max_v do
        if $val < $min_v
            set $val $min_v
        end
        if $val > $max_v
            set $val $max_v
        end
    end