# TechLang STL - String Utilities
# Advanced string manipulation functions with clean public API

package name stl.strings

# ============================================
# Private Helper Functions
# ============================================

def _validate_string s
    # Internal: Check if string exists
    # Returns 1 if valid, 0 if not
    # Note: This is a placeholder - real validation would check state
    set result 1
    return result
end

# ============================================
# Public API Functions
# ============================================

def is_empty s
    # Check if a string is empty (length 0)
    # Args: s - string variable name
    # Returns: 1 if empty, 0 if not
    str_length s len
    if len == 0
        set result 1
        return result
    end
    set result 0
    return result
end

def capitalize source_text
    # Capitalize first character and lowercase the rest
    # Args: source_text - string to capitalize
    # Returns: capitalized string
    str_length source_text len
    if len == 0
        str_create result ""
        return result
    end

    str_substring source_text 0 1 first
    str_substring source_text 1 len rest

    str_create first_up ""
    str_concat first_up first
    str_upper first_up

    str_create rest_low ""
    str_concat rest_low rest
    str_lower rest_low

    str_create result ""
    str_concat result first_up
    str_concat result rest_low
    return result
end

def title_case text
    # Convert string to title case (capitalize each word)
    # Args: text - string to convert
    # Returns: title cased string
    str_split text " " words
    str_create result ""
    set i 0
    # Get array length by trying to access until error
    set max 100
    loop max
        array_get words i word
        if word == 0
            return result
        end
        call capitalize word capped
        if i > 0
            str_concat result " "
        end
        str_concat result capped
        add i 1
    end
    return result
end

def repeat text count
    # Repeat a string n times
    # Args: text - string to repeat, count - number of repetitions
    # Returns: repeated string
    str_create result ""
    set i 0
    loop count
        str_concat result text
    end
    return result
end

def pad_left text width pad_char
    # Pad string on left to reach width
    # Args: text - string to pad, width - target width, pad_char - character to pad with
    # Returns: padded string
    str_length text current_len
    sub width current_len
    set pad_count width
    if pad_count < 0
        set pad_count 0
    end
    call repeat pad_char pad_count padding
    str_create result ""
    str_concat result padding
    str_concat result text
    return result
end

def pad_right text width pad_char
    # Pad string on right to reach width
    # Args: text - string to pad, width - target width, pad_char - character to pad with
    # Returns: padded string
    str_length text current_len
    sub width current_len
    set pad_count width
    if pad_count < 0
        set pad_count 0
    end
    call repeat pad_char pad_count padding
    str_create result ""
    str_concat result text
    str_concat result padding
    return result
end

def starts_with text prefix
    # Check if string starts with prefix
    # Args: text - string to check, prefix - prefix to look for
    # Returns: 1 if starts with prefix, 0 otherwise
    str_length prefix prefix_len
    str_substring text 0 prefix_len extracted
    str_create prefix_copy ""
    str_concat prefix_copy prefix
    if extracted == prefix_copy
        set result 1
        return result
    end
    set result 0
    return result
end

def ends_with text suffix
    # Check if string ends with suffix
    # Args: text - string to check, suffix - suffix to look for
    # Returns: 1 if ends with suffix, 0 otherwise
    str_length text text_len
    str_length suffix suffix_len
    sub text_len suffix_len
    set start_pos text_len
    if start_pos < 0
        set result 0
        return result
    end
    str_substring text start_pos suffix_len extracted
    str_create suffix_copy ""
    str_concat suffix_copy suffix
    if extracted == suffix_copy
        set result 1
        return result
    end
    set result 0
    return result
end

def count_char text char
    # Count occurrences of a character in string
    # Args: text - string to search, char - character to count
    # Returns: count of occurrences
    set count 0
    str_length text len
    set i 0
    loop len
        str_substring text i 1 current
        if current == char
            add count 1
        end
        add i 1
    end
    return count
end

# ============================================
# Export Public API
# ============================================

export is_empty
export capitalize
export title_case
export repeat
export pad_left
export pad_right
export starts_with
export ends_with
export count_char

