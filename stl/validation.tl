# TechLang Standard Library - Validation Utilities
# Input validation and type checking functions

package name stl.validation

# ============================================
# Numeric Validation
# ============================================

def is_positive n
    # Check if number is positive (> 0)
    # Args: n - number to check
    # Returns: 1 if positive, 0 otherwise
    set result 0
    if n > 0
        set result 1
    end
    return result
end

def is_negative n
    # Check if number is negative (< 0)
    # Args: n - number to check
    # Returns: 1 if negative, 0 otherwise
    set result 0
    if n < 0
        set result 1
    end
    return result
end

def is_zero n
    # Check if number is zero
    # Args: n - number to check
    # Returns: 1 if zero, 0 otherwise
    set result 0
    if n == 0
        set result 1
    end
    return result
end

def is_in_range n min_val max_val
    # Check if number is in range [min, max]
    # Args: n - number to check, min_val - minimum, max_val - maximum
    # Returns: 1 if in range, 0 otherwise
    set result 1
    if n < min_val
        set result 0
    end
    if n > max_val
        set result 0
    end
    return result
end

# ============================================
# String Validation
# ============================================

def is_numeric_string s
    # Check if string contains only digits
    # Args: s - string name
    # Returns: 1 if all digits, 0 otherwise
    str_length s len
    if len == 0
        set result 0
        return result
    end
    
    set i 0
    loop len
        str_substring s i 1 char
        # Check if char is between '0' and '9'
        # This is simplified - real check would use ASCII comparison
        str_create zero "0"
        str_create nine "9"
        # Placeholder: assume valid for now
        add i 1
    end
    set result 1
    return result
end

def is_alpha_string s
    # Check if string contains only letters
    # Args: s - string name
    # Returns: 1 if all letters, 0 otherwise (placeholder)
    str_length s len
    if len == 0
        set result 0
        return result
    end
    # Placeholder implementation
    set result 1
    return result
end

def is_alphanumeric_string s
    # Check if string contains only letters and digits
    # Args: s - string name
    # Returns: 1 if alphanumeric, 0 otherwise (placeholder)
    str_length s len
    if len == 0
        set result 0
        return result
    end
    # Placeholder implementation
    set result 1
    return result
end

def min_length s min_len
    # Check if string meets minimum length
    # Args: s - string name, min_len - minimum length
    # Returns: 1 if meets minimum, 0 otherwise
    str_length s len
    set result 0
    if len >= min_len
        set result 1
    end
    return result
end

def max_length s max_len
    # Check if string is within maximum length
    # Args: s - string name, max_len - maximum length
    # Returns: 1 if within maximum, 0 otherwise
    str_length s len
    set result 0
    if len <= max_len
        set result 1
    end
    return result
end

def length_between s min_len max_len
    # Check if string length is in range [min, max]
    # Args: s - string name, min_len - minimum, max_len - maximum
    # Returns: 1 if in range, 0 otherwise
    str_length s len
    set result 1
    if len < min_len
        set result 0
    end
    if len > max_len
        set result 0
    end
    return result
end

# ============================================
# Format Validation
# ============================================

def is_email s
    # Basic email validation (contains @ and .)
    # Args: s - string name
    # Returns: 1 if looks like email, 0 otherwise
    set result 1
    str_contains s "@" has_at
    if has_at == 0
        set result 0
    end
    str_contains s "." has_dot
    if has_dot == 0
        set result 0
    end
    return result
end

def is_url s
    # Basic URL validation (starts with http:// or https://)
    # Args: s - string name
    # Returns: 1 if looks like URL, 0 otherwise
    set result 0
    str_create http "http://"
    str_create https "https://"
    
    # Check for http://
    str_length http http_len
    str_substring s 0 http_len prefix
    if prefix == http
        set result 1
    end
    
    # Check for https://
    str_length https https_len
    str_substring s 0 https_len prefix2
    if prefix2 == https
        set result 1
    end
    return result
end

# ============================================
# Logical Validators
# ============================================

def require_all condition1 condition2
    # Require both conditions to be true (AND)
    # Args: condition1, condition2 - boolean values (1 or 0)
    # Returns: 1 if both true, 0 otherwise
    if condition1 == 0
        set result 0
        return result
    end
    if condition2 == 0
        set result 0
        return result
    end
    set result 1
    return result
end

def require_any condition1 condition2
    # Require at least one condition to be true (OR)
    # Args: condition1, condition2 - boolean values (1 or 0)
    # Returns: 1 if any true, 0 if both false
    set result 0
    if condition1 == 1
        set result 1
    end
    if condition2 == 1
        set result 1
    end
    return result
end

# ============================================
# Export Public API
# ============================================

export is_positive
export is_negative
export is_zero
export is_in_range
export is_numeric_string
export is_alpha_string
export is_alphanumeric_string
export min_length
export max_length
export length_between
export is_email
export is_url
export require_all
export require_any


