# Global/Nonlocal Keywords Demo
# ==========================================
# Control variable scope in functions like Python's global and nonlocal

# === GLOBAL KEYWORD ===
# Use global to access/modify variables from the outer/module scope

# Example 1: Counter with global
print "=== Counter with global ==="
set counter 0

def increment do
    global counter
    add counter 1
end

call increment
call increment
call increment
print counter

# Example 2: Multiple global variables
print ""
print "=== Multiple globals ==="
set x 10
set y 20

def swap_globals do
    global x y
    set temp x
    set x y
    set y temp
end

print x
print y
call swap_globals
print "After swap:"
print x
print y

# Example 3: Global string variable
print ""
print "=== Global with strings ==="
str_create status "Starting"

def update_status new_status do
    global status
    set status new_status
end

print status
call update_status "Processing"
print status
call update_status "Complete"
print status

# Example 4: Accumulator pattern
print ""
print "=== Accumulator pattern ==="
set total 0

def accumulate value do
    global total
    add total value
end

call accumulate 10
call accumulate 20
call accumulate 30
print total

# === NONLOCAL KEYWORD ===
# Use nonlocal to access/modify variables from enclosing function scope
# (Useful in nested functions)

print ""
print "=== Nonlocal in nested functions ==="

def outer do
    set local_var 100

    def inner do
        nonlocal local_var
        add local_var 50
    end

    print local_var
    call inner
    print local_var
end

call outer

print ""
print "Demo complete!"