# Python-like Package Import Demo
# ================================
# This demonstrates TechLang's Python-like module system

print "=== Python-like Package Imports ==="
print ""

# -------------------------------------------
# 1. Basic import (loads myutils/__init__.tl)
# -------------------------------------------
print "1. Basic package import:"
import myutils
call myutils.get_version
print ""

# -------------------------------------------
# 2. Import submodule with dot notation
# -------------------------------------------
print "2. Import submodule (myutils.math):"
import myutils.math
set x 5
call myutils.math.double x result
print result
print ""

# -------------------------------------------
# 3. from...import specific function
# -------------------------------------------
print "3. From import specific function:"
from myutils.text import greet
str_create name "TechLang User"
call greet name
print ""

# -------------------------------------------
# 4. from...import with alias
# -------------------------------------------
print "4. From import with alias:"
from myutils.math import triple as x3
set y 4
call x3 y result2
print result2
print ""

# -------------------------------------------
# 5. from...import multiple functions
# -------------------------------------------
print "5. From import multiple:"
from myutils.text import shout whisper
str_create msg1 "hello"
str_create msg2 "WORLD"
call shout msg1
call whisper msg2
print ""

# -------------------------------------------
# 6. Import nested subpackage
# -------------------------------------------
print "6. Import nested package:"
import myutils.helpers
call myutils.helpers.nested_helper
print ""

# -------------------------------------------
# 7. from package import submodule
# -------------------------------------------
print "7. From package import submodule:"
from myutils import text
str_create greeting "Hi there"
call text.shout greeting
print ""

print "=== Demo Complete ==="
