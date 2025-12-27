# pass Statement Demo
# ================================
# The pass statement does nothing - useful as a placeholder

# === EMPTY FUNCTION PLACEHOLDER ===
print "=== Empty function with pass ==="

def not_implemented_yet do
    pass
end

def another_stub do
    pass
end

# Can call them safely
call not_implemented_yet
call another_stub
print "Stub functions called safely"

# === IF BLOCK PLACEHOLDER ===
print ""
print "=== Pass in if blocks ==="

set x 5

if x > 10 do
    print "x is big"
    else
    pass
end

print "Continued after if"

# === LOOP PLACEHOLDER ===
print ""
print "=== Pass in loops ==="

loop 5 do
    pass
end

print "Loop with pass completed"

# === MIXED WITH CODE ===
print ""
print "=== Pass mixed with other code ==="

set counter 0
pass
add counter 1
pass
add counter 1
pass
add counter 1
print counter

# === COMMON PATTERN: Stub class methods ===
print ""
print "=== Pass as method placeholder ==="

def base_method do
    pass
end

def derived_method do
    print "I do something!"
end

call base_method
call derived_method

print ""
print "Demo complete!"