# Comprehensive data types demonstration for TechLang
# Shows arrays, strings, and dictionaries working together

print "=== TechLang Data Types Demo ==="

# === ARRAYS ===
print "1. Array Operations:"
array_create numbers 3
array_set numbers 0 100
array_set numbers 1 200
array_set numbers 2 300

print "Array values:"
array_get numbers 0
array_get numbers 1
array_get numbers 2

array_push numbers 400
print "After pushing 400:"
array_get numbers 3

# === STRINGS ===
print "2. String Operations:"
str_create message "Welcome to "
str_concat message "TechLang"
str_concat message "!"

print "Message:"
print message
str_length message

# === DICTIONARIES ===
print "3. Dictionary Operations:"
dict_create config
dict_set config "language" "TechLang"
dict_set config "version" "1.0"
dict_set config "features" "Arrays, Strings, Dictionaries"

print "Configuration:"
dict_get config "language"
dict_get config "version"
dict_get config "features"

# === COMBINED EXAMPLE ===
print "4. Combined Example - Student Records:"

# Create array of student names
array_create students 2
array_set students 0 "Alice"
array_set students 1 "Bob"

# Create dictionary for each student's grades
dict_create alice_grades
dict_set alice_grades "math" "95"
dict_set alice_grades "science" "87"

dict_create bob_grades
dict_set bob_grades "math" "78"
dict_set bob_grades "science" "92"

# Display student information
print "Student Records:"
print "Student 1:"
array_get students 0
print "Alice's grades:"
dict_get alice_grades "math"
dict_get alice_grades "science"

print "Student 2:"
array_get students 1
print "Bob's grades:"
dict_get bob_grades "math"
dict_get bob_grades "science"

print "=== Demo Complete ==="
