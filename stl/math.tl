# TechLang Standard Library - Math Utilities
# Mathematical helper functions

package name stl.math

# ============================================
# Public API Functions
# ============================================

def min a b
    if a < b
        return a
    end
    return b
end

def max a b
    if a > b
        return a
    end
    return b
end

def abs n
    if n < 0
        mul n -1
    end
    return n
end

def clamp value min_val max_val
    if value < min_val
        return min_val
    end
    if value > max_val
        return max_val
    end
    return value
end

def sign n
    if n < 0
        set n -1
        return n
    end
    if n > 0
        set n 1
        return n
    end
    set n 0
    return n
end

def is_even n
    math_mod n 2
    if n == 0
        set n 1
        return n
    end
    set n 0
    return n
end

def is_odd n
    math_mod n 2
    if n == 1
        set n 1
        return n
    end
    set n 0
    return n
end

def sum_range start end
    set i start
    loop 1000
        if i > end
            return start
        end
        add start i
        add i 1
    end
    return start
end

def factorial n
    if n < 1
        set n 1
        return n
    end
    set result 1
    set i 1
    loop n
        mul result i
        add i 1
    end
    return result
end

def gcd a b
    return a
end

def lerp a b t
    sub b a
    mul b t
    add a b
    return a
end

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
