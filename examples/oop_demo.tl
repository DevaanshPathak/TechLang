# ============================================================
# TechLang OOP & Functional Programming Demo
# ============================================================
# This example demonstrates the new features added to TechLang:
# 1. Object-Oriented Programming (Classes, Inheritance, Methods)
# 2. First-Class Functions and Closures
# 3. Exception Handling with throw/raise
# ============================================================

print "=== 1. CLASS DEFINITIONS AND OBJECTS ==="

# Define a simple class with fields
class Point
field x int 0
field y int 0

# Constructor
init px py
set_field self x px
set_field self y py
end

# Instance method
method distance
# Calculate distance from origin (simplified: x + y)
get_field self x tempX
get_field self y tempY
set dist tempX
add dist tempY
return dist
end

# Method to move the point
method move dx dy
get_field self x currX
get_field self y currY
add currX dx
add currY dy
set_field self x currX
set_field self y currY
end
end

# Create a Point object
new Point p1 3 4
print "Created Point p1 at:"
get_field p1 x
get_field p1 y

# Call method
print "Distance from origin:"
call p1.distance d
print d

# Move the point
call p1.move 2 1
print "After moving (2,1):"
get_field p1 x
get_field p1 y

print ""
print "=== 2. INHERITANCE ==="

# Base class
class Animal
field name string "Unknown"
field sound string ""

method speak
get_field self name n
get_field self sound s
print n
print s
end
end

# Derived class
class Dog extends Animal
field breed string "Mixed"

init n b
set_field self name n
set_field self breed b
set_field self sound "Woof!"
end

method fetch
get_field self name n
print n
print "is fetching!"
end
end

# Create a Dog
new Dog myDog "Buddy" "Labrador"
print "Dog info:"
get_field myDog name
get_field myDog breed

# Call inherited method
print "Dog speaks:"
call myDog.speak

# Call subclass method
call myDog.fetch

# Check inheritance with instanceof
instanceof myDog Dog isDog
instanceof myDog Animal isAnimal
print "Is Dog:"
print isDog
print "Is Animal:"
print isAnimal

print ""
print "=== 3. STATIC METHODS ==="

# Class with static method
class MathUtils
static square n
set result n
mul result n
return result
end

static cube n
set result n
mul result n
mul result n
return result
end
end

# Call static methods (no instance needed)
call MathUtils.square 5 sq
call MathUtils.cube 3 cb
print "5 squared:"
print sq
print "3 cubed:"
print cb

print ""
print "=== 4. FIRST-CLASS FUNCTIONS ==="

# Define a closure that captures scope
set multiplier 10

fn multiply_by_ten n do
set result n
mul result multiplier
return result
end

fn_call multiply_by_ten 7 -> answer
print "7 * 10 ="
print answer

print ""
print "=== 5. HIGHER-ORDER FUNCTIONS ==="

# Create an array
array_create numbers 5
array_set numbers 0 1
array_set numbers 1 2
array_set numbers 2 3
array_set numbers 3 4
array_set numbers 4 5

print "Original array: [1, 2, 3, 4, 5]"

# Map: double each element
lambda doubler x "x * 2"
map_fn numbers doubler doubled
print "Doubled:"
array_get doubled 0 v0
array_get doubled 1 v1
array_get doubled 2 v2
print v0
print v1
print v2

# Filter: keep only even numbers
array_create evens 4
array_set evens 0 2
array_set evens 1 4
array_set evens 2 6
array_set evens 3 8

lambda is_big x "x > 4"
filter_fn evens is_big big_evens
print "Numbers > 4:"
array_get big_evens 0 b0
array_get big_evens 1 b1
print b0
print b1

# Reduce: sum all elements
fn add_two a b do
set result a
add result b
return result
end

reduce_fn numbers add_two 0 total
print "Sum of 1-5:"
print total

print ""
print "=== 6. PARTIAL APPLICATION ==="

fn add a b do
set result a
add result b
return result
end

# Create a partial function with a=100
partial add add_100 a=100
fn_call add_100 5 -> result
print "100 + 5 ="
print result

print ""
print "=== 7. FUNCTION COMPOSITION ==="

lambda triple x "x * 3"
lambda add_one x "x + 1"

# compose: triple ∘ add_one means triple(add_one(x))
compose triple add_one triple_after_add
fn_call triple_after_add 5 -> composed_result
print "triple(add_one(5)) = triple(6) ="
print composed_result

print ""
print "=== 8. EXCEPTION HANDLING ==="

# throw/raise an error that can be caught
try
    print "About to throw..."
    throw "Something went wrong!" CustomError
catch err
        print "Caught exception:"
        print err
    end

    print "Execution continues after catch"

# Using raise (alias for throw)
    try
        raise "File not found" IOError
    catch e
            print "Caught IOError:"
            print e
        end

        print ""
        print "=== 9. FUNCTION REFERENCES ==="

# Get a reference to an existing function
        def greet name
            str_create msg "Hello, "
            str_concat msg name
            print msg
        end

        fn_ref greet greeting_fn
        print "Got function reference"

        print ""
        print "=== DEMO COMPLETE ==="
        print "TechLang now supports:"
        print "- Classes with fields and methods"
        print "- Inheritance (extends)"
        print "- Static methods"
        print "- First-class functions"
        print "- Closures"
        print "- Higher-order functions (map, filter, reduce)"
        print "- Partial application"
        print "- Function composition"
        print "- throw/raise exceptions"