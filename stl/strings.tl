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
    str_length s _ss_is_empty_len
    if _ss_is_empty_len == 0
        set _ss_is_empty_result 1
        return _ss_is_empty_result
    end
    set _ss_is_empty_result 0
    return _ss_is_empty_result
end

def capitalize source_text
    # Capitalize first character and lowercase the rest
    # Args: source_text - string to capitalize
    # Returns: capitalized string
    str_length source_text _ss_cap_len
    if _ss_cap_len == 0
        str_create _ss_cap_result ""
        return _ss_cap_result
    end

    str_substring source_text 0 1 _ss_cap_first
    str_substring source_text 1 _ss_cap_len _ss_cap_rest

    str_create _ss_cap_first_up ""
    str_concat _ss_cap_first_up _ss_cap_first
    str_upper _ss_cap_first_up

    str_create _ss_cap_rest_low ""
    str_concat _ss_cap_rest_low _ss_cap_rest
    str_lower _ss_cap_rest_low

    str_create _ss_cap_result ""
    str_concat _ss_cap_result _ss_cap_first_up
    str_concat _ss_cap_result _ss_cap_rest_low
    return _ss_cap_result
end

def title_case text
    # Convert string to title case (capitalize each word)
    # Args: text - string to convert
    # Returns: title cased string
    # Note: Avoids str_split since it emits output lines.

    str_create _ss_tc_result ""
    str_create _ss_tc_word ""
    set _ss_tc_has_any 0

    str_length text _ss_tc_len
    set _ss_tc_i 0
    loop _ss_tc_len
        set _ss_tc_end_pos _ss_tc_i
        add _ss_tc_end_pos 1
        str_substring text _ss_tc_i _ss_tc_end_pos _ss_tc_ch

        if _ss_tc_ch == " "
            str_length _ss_tc_word _ss_tc_wlen
            if _ss_tc_wlen > 0
                call capitalize _ss_tc_word _ss_tc_capped
                if _ss_tc_has_any == 1
                    str_concat _ss_tc_result " "
                end
                str_concat _ss_tc_result _ss_tc_capped
                set _ss_tc_has_any 1
                str_create _ss_tc_word ""
            end
        end

        if _ss_tc_ch != " "
            str_concat _ss_tc_word _ss_tc_ch
        end

        add _ss_tc_i 1
    end

    str_length _ss_tc_word _ss_tc_wlen
    if _ss_tc_wlen > 0
        call capitalize _ss_tc_word _ss_tc_capped
        if _ss_tc_has_any == 1
            str_concat _ss_tc_result " "
        end
        str_concat _ss_tc_result _ss_tc_capped
    end

    return _ss_tc_result
end

def repeat text count
    # Repeat a string n times
    # Args: text - string to repeat, count - number of repetitions
    # Returns: repeated string
    str_create _ss_rep_result ""
    set _ss_rep_i 0
    loop count
        str_concat _ss_rep_result text
    end
    return _ss_rep_result
end

def pad_left text width pad_char
    # Pad string on left to reach width
    # Args: text - string to pad, width - target width, pad_char - character to pad with
    # Returns: padded string
    str_length text _ss_pl_current_len
    sub width _ss_pl_current_len
    set _ss_pl_pad_count width
    if _ss_pl_pad_count < 0
        set _ss_pl_pad_count 0
    end
    call repeat pad_char _ss_pl_pad_count _ss_pl_padding
    str_create _ss_pl_result ""
    str_concat _ss_pl_result _ss_pl_padding
    str_concat _ss_pl_result text
    return _ss_pl_result
end

def pad_right text width pad_char
    # Pad string on right to reach width
    # Args: text - string to pad, width - target width, pad_char - character to pad with
    # Returns: padded string
    str_length text _ss_pr_current_len
    sub width _ss_pr_current_len
    set _ss_pr_pad_count width
    if _ss_pr_pad_count < 0
        set _ss_pr_pad_count 0
    end
    call repeat pad_char _ss_pr_pad_count _ss_pr_padding
    str_create _ss_pr_result ""
    str_concat _ss_pr_result text
    str_concat _ss_pr_result _ss_pr_padding
    return _ss_pr_result
end

def starts_with text prefix
    # Check if string starts with prefix
    # Args: text - string to check, prefix - prefix to look for
    # Returns: 1 if starts with prefix, 0 otherwise
    str_length prefix _ss_sw_prefix_len
    str_substring text 0 _ss_sw_prefix_len _ss_sw_extracted
    str_create _ss_sw_prefix_copy ""
    str_concat _ss_sw_prefix_copy prefix
    if _ss_sw_extracted == _ss_sw_prefix_copy
        set _ss_sw_result 1
        return _ss_sw_result
    end
    set _ss_sw_result 0
    return _ss_sw_result
end

def ends_with text suffix
    # Check if string ends with suffix
    # Args: text - string to check, suffix - suffix to look for
    # Returns: 1 if ends with suffix, 0 otherwise
    str_length text _ss_ew_text_len
    str_length suffix _ss_ew_suffix_len
    sub _ss_ew_text_len _ss_ew_suffix_len
    set _ss_ew_start_pos _ss_ew_text_len
    if _ss_ew_start_pos < 0
        set _ss_ew_result 0
        return _ss_ew_result
    end
    set _ss_ew_end_pos _ss_ew_start_pos
    add _ss_ew_end_pos _ss_ew_suffix_len
    str_substring text _ss_ew_start_pos _ss_ew_end_pos _ss_ew_extracted
    str_create _ss_ew_suffix_copy ""
    str_concat _ss_ew_suffix_copy suffix
    if _ss_ew_extracted == _ss_ew_suffix_copy
        set _ss_ew_result 1
        return _ss_ew_result
    end
    set _ss_ew_result 0
    return _ss_ew_result
end

def count_char text char
    # Count occurrences of a character in string
    # Args: text - string to search, char - character to count
    # Returns: count of occurrences
    set _ss_cc_count 0
    str_length text _ss_cc_len
    set _ss_cc_i 0
    loop _ss_cc_len
        set _ss_cc_end_pos _ss_cc_i
        add _ss_cc_end_pos 1
        str_substring text _ss_cc_i _ss_cc_end_pos _ss_cc_current
        if _ss_cc_current == char
            add _ss_cc_count 1
        end
        add _ss_cc_i 1
    end
    return _ss_cc_count
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

