# TechLang STL - Random Utilities
# Deterministic randomness via math_seed and math_random store-form.

package name stl.random

def seed n
    math_seed n
    return 1
end

def randint lo hi
    # Return random integer in [lo, hi].
    math_random lo hi _stl_rand_val
    return _stl_rand_val
end

def choice arr
    # Choose a random element from array arr.
    # Returns: value ok
    set _stl_rand_ok 0

    # Count elements until sentinel 0.
    set _stl_rand_done 0
    set _stl_rand_count 0
    set _stl_rand_i 0
    loop 1000
        if _stl_rand_done == 0
            array_get arr _stl_rand_i _stl_rand_val
            if _stl_rand_val == 0
                set _stl_rand_count _stl_rand_i
                set _stl_rand_done 1
            end
            if _stl_rand_val != 0
                add _stl_rand_i 1
            end
        end
    end

    if _stl_rand_count <= 0
        return 0 0
    end

    set _stl_rand_hi _stl_rand_count
    sub _stl_rand_hi 1
    math_random 0 _stl_rand_hi _stl_rand_idx
    array_get arr _stl_rand_idx _stl_rand_choice
    set _stl_rand_ok 1
    return _stl_rand_choice _stl_rand_ok
end

def shuffle arr outArr
    # Fisher–Yates shuffle into outArr (does not modify arr).
    array_create outArr

    # Copy arr -> outArr and compute count.
    set _stl_shuf_done 0
    set _stl_shuf_count 0
    set _stl_shuf_i 0
    loop 1000
        if _stl_shuf_done == 0
            array_get arr _stl_shuf_i _stl_shuf_val
            if _stl_shuf_val == 0
                set _stl_shuf_count _stl_shuf_i
                set _stl_shuf_done 1
            end
            if _stl_shuf_val != 0
                array_set outArr _stl_shuf_i _stl_shuf_val
                add _stl_shuf_i 1
            end
        end
    end

    if _stl_shuf_count <= 1
        return 1
    end

    # Shuffle outArr in place.
    set _stl_shuf_i _stl_shuf_count
    sub _stl_shuf_i 1
    loop 1000
        if _stl_shuf_i <= 0
            return 1
        end
        math_random 0 _stl_shuf_i _stl_shuf_j
        array_get outArr _stl_shuf_i _stl_shuf_a
        array_get outArr _stl_shuf_j _stl_shuf_b
        array_set outArr _stl_shuf_i _stl_shuf_b
        array_set outArr _stl_shuf_j _stl_shuf_a
        sub _stl_shuf_i 1
    end
    return 1
end

export seed
export randint
export choice
export shuffle
