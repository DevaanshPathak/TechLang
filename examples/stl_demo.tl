# TechLang STL (Standard Template Library) Demo
# Demonstrates using 'stl' as the primary name and 'stdlib' as an alias
#
# NOTE: When using STL, modules are loaded relative to the script's directory
# For this example to work, either:
# 1. Copy stl/ into examples/ directory, OR
# 2. Run from Python: from techlang.interpreter import run; run(code, base_dir='.')

boot
print "=== STL Alias Demo ==="
print ""

# Load validation module using 'stl' prefix
package use stl/validation

# Test positive number
set num 42
call stl.validation.is_positive num result
print "Is 42 positive?"
print result

# Test negative number
set num -5
call stl.validation.is_negative num result
print "Is -5 negative?"
print result

# Test zero
set num 0
call stl.validation.is_zero num result
print "Is 0 zero?"
print result

# You can also use stdlib as an alias - they're interchangeable!
print ""
print "=== Using stdlib alias ==="

# Load with stl, call with stdlib (alias)
call stdlib.validation.is_positive 100 result
print "Is 100 positive (using stdlib alias)?"
print result

# Both separators work: . and ::
call stl::validation::is_positive 7 result
print "Is 7 positive (using :: separator)?"
print result

print ""
print "=== All STL variations work! ==="
