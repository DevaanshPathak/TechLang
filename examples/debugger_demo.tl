# TechLang Debugger Demo
# Shows how to use debugging features to inspect program execution

boot
print "=== Debugger Features Demo ==="

# Basic inspection
print ""
print "1. Basic State Inspection"
set counter 0
set max 5
inspect

# Watching variables
print ""
print "2. Watching Variables"
watch counter
watch max
set counter 1
inspect

# Setting breakpoints
print ""
print "3. Setting Breakpoints"
set x 10
breakpoint
set x 20
breakpoint
set x 30

# Show breakpoint info
print ""
print "Breakpoints have been set"

# Inspect with different data types
print ""
print "4. Inspecting Complex State"
array_create numbers 3
array_set numbers 0 100
array_set numbers 1 200
array_set numbers 2 300

str_create message "Hello Debugger"

dict_create config
dict_set config "debug" "true"
dict_set config "level" "verbose"

inspect

# Step through a loop
print ""
print "5. Stepping Through Code"
set i 0
loop 3
    add i 1
    print i
end

# Watch variable changes
print ""
print "6. Monitoring Changes"
watch result
set result 0
loop 5
    add result 10
end
print "Final result:"
print result

# Clean up
print ""
print "7. Clearing Debug State"
unwatch counter
unwatch max
unwatch result
clear_breakpoints

# Final inspection
print ""
print "8. Final State"
inspect

print ""
print "=== Debugger Demo Complete ==="
crash
