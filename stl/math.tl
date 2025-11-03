# TechLang Standard Library - Math Utilities
# Mathematical helper functions

package name stl.math

# ============================================
# Public API Functions
# ============================================

def min a b
    # Return minimum of two numbers
    # Args: a, b - numbers to compare
    # Returns: smaller number
    if a < b
        return a
    end
    return b
end

def max a b
    # Return maximum of two numbers
    # Args: a, b - numbers to compare
    # Returns: larger number
    if a > b
        return a
    end
    return b
end

def abs n
    # Return absolute value
    # Args: n - number
    # Returns: absolute value
    if n < 0
        mul n -1
        return n
    end
    return n
end

def clamp value min_val max_val
    # Clamp value between min and max
    # Args: value - number to clamp, min_val - minimum, max_val - maximum
    # Returns: clamped value
    if value < min_val
        return min_val
    end
    if value > max_val
        return max_val
    end
    return value
end

def sign n
    # Return sign of number (-1, 0, or 1)
    # Args: n - number
    # Returns: -1 if negative, 0 if zero, 1 if positive
    if n < 0
        set result -1
        return result
    end
    if n > 0
        set result 1
        return result
    end
    set result 0
    return result
end

def is_even n
    # Check if number is even
    # Args: n - number to check
    # Returns: 1 if even, 0 if odd
    math_mod n 2
    if n == 0
        set result 1
        return result
    end
    set result 0
    return result
end

def is_odd n
    # Check if number is odd
    # Args: n - number to check
    # Returns: 1 if odd, 0 if even
    math_mod n 2
    if n == 1
        set result 1
        return result
    end
    set result 0
    return result
end

def sum_range start end
    # Sum integers from start to end (inclusive)
    # Args: start - first number, end - last number
    # Returns: sum of range
    set total 0
    set i start
    loop 1000
        if i > end
            return total
        end
        add total i
        add i 1
    end
    return total
end

def factorial n
    # Calculate factorial (n!)
    # Args: n - number (must be >= 0)
    # Returns: factorial of n
    if n < 0
        set result 0
        return result
    end
    if n == 0
        set result 1
        return result
    end
    set result 1
    set i 1
    loop n
        if i > n
            return result
        end
        mul result i
        add i 1
    end
    return result
end

def gcd a b
    # Calculate greatest common divisor (Euclidean algorithm)
    # Args: a, b - two numbers
    # Returns: GCD of a and b
    # Make both positive
    if a < 0
        mul a -1
    end
    if b < 0
        mul b -1
    end
    
    # Euclidean algorithm
    loop 1000
        if b == 0
            return a
        end
        set temp b
        math_mod a b
        set b a
        set a temp
    end
    return a
end

def lerp a b t
    # Linear interpolation between a and b
    # Args: a - start value, b - end value, t - interpolation factor (0-1)
    # Returns: interpolated value
    # result = a + (b - a) * t
    sub b a
    set diff b
    mul diff t
    add a diff
    return a
end

# ============================================
# Export Public API
# ============================================

export min
export max
export abs
export clamp
export sign
export is_even
export is_odd
export sum_range
export factorial
export gcd
export lerp


