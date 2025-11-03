# TechLang Standard Library - Collections Utilities
# Array and dictionary helper functions

package name stl.collections

# ============================================
# Array Functions
# ============================================

def array_sum arr
    # Sum all numeric elements in array
    # Args: arr - array name
    # Returns: sum of all elements
    set total 0
    set i 0
    loop 1000
        array_get arr i val
        if val == 0
            return total
        end
        add total val
        add i 1
    end
    return total
end

def array_product arr
    # Multiply all numeric elements in array
    # Args: arr - array name
    # Returns: product of all elements
    set product 1
    set i 0
    loop 1000
        array_get arr i val
        if val == 0
            return product
        end
        mul product val
        add i 1
    end
    return product
end

def array_min arr
    # Find minimum value in array
    # Args: arr - array name
    # Returns: minimum value (or 0 if empty)
    array_get arr 0 min_val
    if min_val == 0
        return min_val
    end
    set i 1
    loop 1000
        array_get arr i val
        if val == 0
            return min_val
        end
        if val < min_val
            set min_val val
        end
        add i 1
    end
    return min_val
end

def array_max arr
    # Find maximum value in array
    # Args: arr - array name
    # Returns: maximum value (or 0 if empty)
    array_get arr 0 max_val
    if max_val == 0
        return max_val
    end
    set i 1
    loop 1000
        array_get arr i val
        if val == 0
            return max_val
        end
        if val > max_val
            set max_val val
        end
        add i 1
    end
    return max_val
end

def array_contains arr target
    # Check if array contains a value
    # Args: arr - array name, target - value to search for
    # Returns: 1 if found, 0 if not
    set i 0
    loop 1000
        array_get arr i val
        if val == 0
            set result 0
            return result
        end
        if val == target
            set result 1
            return result
        end
        add i 1
    end
    set result 0
    return result
end

def array_index_of arr target
    # Find first index of value in array
    # Args: arr - array name, target - value to search for
    # Returns: index if found, -1 if not found
    set i 0
    loop 1000
        array_get arr i val
        if val == 0
            set result -1
            return result
        end
        if val == target
            return i
        end
        add i 1
    end
    set result -1
    return result
end

def array_count arr
    # Count elements in array (until first 0)
    # Args: arr - array name
    # Returns: number of non-zero elements
    set count 0
    set i 0
    loop 1000
        array_get arr i val
        if val == 0
            return count
        end
        add count 1
        add i 1
    end
    return count
end

def array_reverse arr
    # Reverse array in place
    # Args: arr - array name
    # Returns: 1 on success
    # First count elements
    set count 0
    set i 0
    loop 1000
        array_get arr i val
        if val == 0
            set count i
            return 1
        end
        add i 1
    end
    
    # Reverse by swapping
    set left 0
    sub count 1
    set right count
    
    loop 1000
        if left >= right
            set result 1
            return result
        end
        
        # Swap arr[left] and arr[right]
        array_get arr left left_val
        array_get arr right right_val
        array_set arr left right_val
        array_set arr right left_val
        
        add left 1
        sub right 1
    end
    set result 1
    return result
end

def array_fill arr value count
    # Fill array with a value
    # Args: arr - array name, value - value to fill, count - number of elements
    # Returns: 1 on success
    set i 0
    loop count
        array_set arr i value
        add i 1
    end
    set result 1
    return result
end

# ============================================
# Dictionary Functions
# ============================================

def dict_has_key dict_name key
    # Check if dictionary contains a key
    # Args: dict_name - dictionary name, key - key to check
    # Returns: 1 if exists, 0 if not
    dict_get dict_name key val
    # Note: dict_get returns 0 if key doesn't exist
    # This is a simplification - real check would need error handling
    if val == 0
        set result 0
        return result
    end
    set result 1
    return result
end

def dict_count dict_name
    # Count keys in dictionary
    # Args: dict_name - dictionary name
    # Returns: number of keys
    # Note: TechLang doesn't have dict_keys command yet
    # This is a placeholder that returns 0
    set result 0
    return result
end

def dict_copy source dest
    # Copy dictionary (shallow copy)
    # Args: source - source dictionary name, dest - destination dictionary name
    # Returns: 1 on success
    # Note: TechLang doesn't have dict iteration yet
    # This is a placeholder that returns 0
    set result 0
    return result
end

# ============================================
# Export Public API
# ============================================

export array_sum
export array_product
export array_min
export array_max
export array_contains
export array_index_of
export array_count
export array_reverse
export array_fill
export dict_has_key
export dict_count
export dict_copy


