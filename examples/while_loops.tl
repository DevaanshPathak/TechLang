# While loops example for TechLang
# Demonstrates the while loop functionality

print "=== While Loops Demo ==="

# Example 1: Countdown from 5 to 1
print "1. Countdown from 5 to 1:"
set x 5
while x > 0
    print x
    sub x 1
end

print "Blast off!"

# Example 2: Sum numbers from 1 to 10
print "2. Sum numbers from 1 to 10:"
set sum 0
set i 1
while i <= 10
    add sum i
    add i 1
end
print "Sum is:"
print sum

# Example 3: Find factorial of 5
print "3. Factorial of 5:"
set n 5
set factorial 1
while n > 0
    mul factorial n
    sub n 1
end
print "5! ="
print factorial

# Example 4: While loop with array
print "4. Fill array with while loop:"
array_create numbers 5
set i 0
while i < 5
    array_set numbers i i
    add i 1
end

print "Array contents:"
array_get numbers 0
array_get numbers 1
array_get numbers 2
array_get numbers 3
array_get numbers 4

print "=== Demo Complete ==="
