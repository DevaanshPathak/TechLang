# TechLang - Advanced Function Features Demo
# This demonstrates parameters, return values, and local scope

print "=== Advanced Function Features ==="
print ""

# 1. Simple Function with Parameters
print "1. Function with Parameters"
def double x
    mul x 2
    return x
end

set num 5
call double num result
print result
print ""

# 2. Multiple Return Values
print "2. Multiple Return Values"
def swap a b
    return b a
end

set x 10
set y 20
call swap x y first second
print first
print second
print ""

# 3. String Parameters
print "3. String Parameters"
def make_greeting name
    str_create greeting_msg "Hello "
    str_concat greeting_msg name
    return greeting_msg
end

str_create username "Alice"
call make_greeting username greeting
print greeting
print ""

# 4. Local Scope
print "4. Local Scope Isolation"
set global 100
def modify x
    set x 999
    return x
end

call modify global local
print local
print global
print ""

# 5. Literal Arguments
print "5. Literal Arguments"
def square n
    mul n n
    return n
end

call square 7 sq
print sq
print ""

# 6. Nested Calls
print "6. Nested Function Calls"
def triple n
    mul n 3
    return n
end

set val 4
call double val doubled
call triple doubled answer
print answer
print ""

# 7. Math with Conditionals
print "7. Math with Conditionals"
def abs_value n
    if n lt 0
        set n 0
        sub n 42
    end
    return n
end

set positive_val 42
call abs_value positive_val result
print result
print ""

# 8. Working with Strings
print "8. String Manipulation"
def uppercase_text input_text
    str_upper input_text
    return input_text
end

str_create word "hello"
call uppercase_text word final
print final
print ""

print "=== Demo Complete ==="
