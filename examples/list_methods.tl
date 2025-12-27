# TechLang List Methods as Commands
# ==============================================
# Python-like list methods for array manipulation

print "=== List Methods Demo ==="
print ""

# Setup test array
array_create arr
array_push arr 1
array_push arr 2
array_push arr 3
array_push arr 4
array_push arr 5

# array_len - get length
print "1. array_len - Get Array Length"
array_len arr len
print "   Array length:"
print len
print ""

# array_insert - insert at specific index
print "2. array_insert - Insert at Index"
print "   Before: [1, 2, 3, 4, 5]"
array_insert arr 2 99
print "   After array_insert arr 2 99:"
print "   Index 0:"
array_get arr 0 v
print v
print "   Index 1:"
array_get arr 1 v
print v
print "   Index 2:"
array_get arr 2 v
print v
print "   Index 3:"
array_get arr 3 v
print v
# Result: [1, 2, 99, 3, 4, 5]
print ""

# array_remove - remove first occurrence
print "3. array_remove - Remove First Occurrence"
array_remove arr 99
array_len arr new_len
print "   After removing 99, length:"
print new_len
# Back to [1, 2, 3, 4, 5]
print ""

# array_extend - extend with another array
print "4. array_extend - Combine Arrays"
array_create more
array_push more 6
array_push more 7
array_push more 8
array_extend arr more
array_len arr extended_len
print "   After extending with [6, 7, 8], length:"
print extended_len
# Now: [1, 2, 3, 4, 5, 6, 7, 8]
print ""

# array_copy - shallow copy
print "5. array_copy - Create Shallow Copy"
array_copy arr arr_copy
array_len arr_copy copy_len
print "   Created copy with length:"
print copy_len
print ""

# array_count - count occurrences
print "6. array_count - Count Occurrences"
array_create counts
array_push counts 1
array_push counts 2
array_push counts 2
array_push counts 3
array_push counts 2
array_push counts 4
array_count counts 2 cnt
print "   In [1,2,2,3,2,4], count of 2:"
print cnt
print ""

# array_index - find index of value
print "7. array_index - Find Index"
array_index arr 5 idx
print "   Index of 5 in arr:"
print idx

array_index arr 99 idx_not_found
print "   Index of 99 (not found):"
print idx_not_found
print ""

# array_clear - clear all elements
print "8. array_clear - Remove All Elements"
array_clear counts
array_len counts cleared_len
print "   After array_clear, length:"
print cleared_len
print ""

# Practical example: Building a queue
print "9. Practical Example: Simple Queue"
array_create queue
print "   Enqueue: 10, 20, 30"
array_push queue 10
array_push queue 20
array_push queue 30
print "   Queue:"
array_get queue 0 q0
array_get queue 1 q1
array_get queue 2 q2
print q0
print q1
print q2

# Dequeue (remove from front by shifting)
print "   Dequeue front element:"
array_get queue 0 front
print "   Removed:"
print front

# Shift remaining elements
array_create new_queue
array_get queue 1 v1
array_get queue 2 v2
array_push new_queue v1
array_push new_queue v2
array_copy new_queue queue
print "   Queue after dequeue:"
array_get queue 0 nq0
array_get queue 1 nq1
print nq0
print nq1
print ""

# Using array methods for sorting (manual bubble sort)
print "10. Practical Example: Manual Sorting"
array_create to_sort
array_push to_sort 5
array_push to_sort 2
array_push to_sort 8
array_push to_sort 1
array_push to_sort 9
print "    Before sort: [5, 2, 8, 1, 9]"

# Simple bubble sort using array methods
array_len to_sort n
set passes 0
loop n
    set swapped 0
    set j 0
    set limit n
    sub limit 1
    sub limit passes

    loop limit
        array_get to_sort j curr
        set next_j j
        add next_j 1
        array_get to_sort next_j next_val

        if curr > next_val
# Swap
            array_set to_sort j next_val
            array_set to_sort next_j curr
            set swapped 1
        end

        add j 1
    end

    add passes 1

    if swapped == 0
# Early exit if sorted
    end
end

print "    After sort:"
set k 0
loop 5
    array_get to_sort k sorted_val
    print sorted_val
    add k 1
end
print ""

print "=== Demo Complete ==="