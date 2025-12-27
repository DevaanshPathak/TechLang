# TechLang Loop Else
# ==============================
# Python-like loop-else with break and continue
# The 'else' block runs only if the loop completes without break

print "=== Loop Else Demo ==="
print ""

# Basic loop_else - else runs when loop completes
print "1. Basic loop_else (no break)"
set sum 0
loop_else 5 do
add sum 1
print i
else
print "   Loop completed normally!"
print "   Sum ="
print sum
end
print ""

# loop_else with break - else does NOT run
print "2. loop_else with break"
print "   Searching for value 3..."
loop_else 10 do
if i == 3
    print "   Found 3! Breaking..."
    break
end
else
print "   Not found (this won't print)"
end
print "   After the loop"
print ""

# Search pattern: find item in array
print "3. Search Pattern - Found"
array_create nums
array_push nums 10
array_push nums 20
array_push nums 30
array_push nums 40
set target 30
loop_else 4 do
array_get nums i val
if val == target
    print "   Found target 30 at index"
    print i
    break
end
else
print "   Target not found"
end
print ""

# Search pattern: item not found
print "4. Search Pattern - Not Found"
set target 99
loop_else 4 do
array_get nums i val
if val == target
    print "   Found!"
    break
end
else
print "   Target 99 not found in array"
end
print ""

# while_else - else runs when condition becomes false
print "5. while_else Example"
set x 0
print "   Counting up to 5:"
while_else x < 5 do
print x
add x 1
else
print "   While loop completed! x ="
print x
end
print ""

# while_else with break
print "6. while_else with break"
set y 0
while_else y < 100 do
if y == 5
    print "   Breaking at y = 5"
    break
end
add y 1
else
print "   This won't print"
end
print "   Final y ="
print y
print ""

# Practical example: Finding prime factors
print "7. Practical Example: Check if Number is Prime"
set num 17
set divisor 2
set is_prime 1
while_else divisor < num do
set remainder num
while remainder >= divisor
    sub remainder divisor
end
if remainder == 0
    print "   17 is NOT prime (divisible by"
    print divisor
    print "   )"
    set is_prime 0
    break
end
add divisor 1
else
print "   17 IS PRIME! No divisors found."
end
print ""

# Nested loop with break
print "8. Nested Loops - Inner Break Only"
set found 0
loop_else 3 do
set outer_i i
loop_else 3 do
set inner_j i
if inner_j == 1
    print "   Inner loop breaking at j=1 (outer i="
    print outer_i
    print "   )"
    break
end
else
print "   Inner loop completed (won't show)"
end
else
print "   Outer loop completed normally!"
end
print ""

print "=== Demo Complete ==="