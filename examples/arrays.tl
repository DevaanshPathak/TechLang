# Array operations example for TechLang
# Demonstrates array creation, manipulation, and access

# Create an array with 5 elements
array_create mylist 5

# Set values at specific indices
array_set mylist 0 10
array_set mylist 1 20
array_set mylist 2 30
array_set mylist 3 40
array_set mylist 4 50

# Get and print values
print "Array values:"
array_get mylist 0
array_get mylist 1
array_get mylist 2
array_get mylist 3
array_get mylist 4

# Push new values to the end
array_push mylist 60
array_push mylist 70

print "After pushing 60 and 70:"
array_get mylist 5
array_get mylist 6

# Pop values from the end
print "Popped values:"
array_pop mylist
array_pop mylist

# Show final array state
print "Final array state:"
array_get mylist 0
array_get mylist 1
array_get mylist 2
array_get mylist 3
array_get mylist 4

# Map the array to create doubled values
array_map mylist doubled double

print "Doubled values:"
array_get doubled 0
array_get doubled 1
array_get doubled 2
array_get doubled 3
array_get doubled 4

# Filter doubled values greater than 50
array_filter doubled big gt 50

print "Values greater than 50:"
array_get big 0
array_get big 1
array_get big 2
