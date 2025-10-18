# String operations example for TechLang
# Demonstrates string creation, manipulation, and access

# Create strings
str_create greeting "Hello"
str_create name "TechLang"
str_create punctuation "!"

# Concatenate strings
str_concat greeting " "
str_concat greeting name
str_concat greeting punctuation

# Print the final greeting
print "Final greeting:"
print greeting

# Get string length
str_length greeting

# Create a longer string for substring operations
str_create sentence "The quick brown fox jumps over the lazy dog"

# Get substring from position 4 to 9 (0-indexed)
str_substring sentence 4 9

# Get substring from position 16 to 19
str_substring sentence 16 19

# Get substring from position 20 to 24
str_substring sentence 20 24

# Show string length
str_length sentence

# Interpolate a greeting using placeholders
str_create first_name "Ada"
str_create title "Engineer"
string_interpolate intro "Hello {first_name}, brilliant {title}!"

print "Interpolated greeting:"
print intro

# Run regex matches to detect words
string_match "fox" sentence containsfox
print "Contains 'fox'?"
print containsfox

string_match "cat" sentence containscat
print "Contains 'cat'?"
print containscat
