# Identity Check Demo
# Demonstrates is and is_not commands

boot "Identity Check Demo"

# Test 1: Same array identity
print "=== Array Identity ==="
array_create arr1
array_push arr1 1
array_push arr1 2

is arr1 arr1 result
print "arr1 is arr1:"
print result

# Different arrays
array_create arr2
array_push arr2 1
array_push arr2 2

is arr1 arr2 result
print "arr1 is arr2 (same content, different object):"
print result

is_not arr1 arr2 result
print "arr1 is_not arr2:"
print result

# Test 2: Dictionary identity
print ""
print "=== Dict Identity ==="
dict_create dict1
dict_set dict1 "key" "value"

is dict1 dict1 result
print "dict1 is dict1:"
print result

dict_create dict2
is_not dict1 dict2 result
print "dict1 is_not dict2:"
print result

# Test 3: Variable identity
print ""
print "=== Variable Identity ==="
set x 42
set y 42

is x x result
print "x is x:"
print result

is x y result
print "x is y (same value):"
print result

# Test 4: String identity
print ""
print "=== String Identity ==="
str_create s1 "hello"
str_create s2 "hello"

is s1 s1 result
print "s1 is s1:"
print result

is s1 s2 result
print "s1 is s2 (same content):"
print result

print ""
print "Demo complete!"