# TechLang String Methods
# ====================================
# Python-like string manipulation methods

print "=== String Methods Demo ==="
print ""

# str_join - join array elements with separator
print "1. str_join - Join Array Elements"
array_create words
array_push words "hello"
array_push words "world"
array_push words "from"
array_push words "TechLang"
str_create sep " "
str_join words sep joined
print "   Join with space:"
print joined

str_create sep2 "-"
str_join words sep2 joined2
print "   Join with dash:"
print joined2

str_create sep3 ", "
str_join words sep3 joined3
print "   Join with comma-space:"
print joined3
print ""

# str_zfill - zero-fill padding
print "2. str_zfill - Zero Padding"
str_create num "42"
str_zfill num 5 padded
print "   '42' zfill to width 5:"
print padded

str_create num2 "7"
str_zfill num2 3 padded2
print "   '7' zfill to width 3:"
print padded2
print ""

# str_center, str_ljust, str_rjust - alignment
print "3. String Alignment"
str_create txt "Hi"
str_center txt 10 centered
str_ljust txt 10 left_aligned
str_rjust txt 10 right_aligned
print "   Center 'Hi' in width 10:"
str_length centered clen
print "   ["
print centered
print "   ] (length ="
print clen
print "   )"

print "   Left justify 'Hi' in width 10:"
print "   ["
print left_aligned
print "   ]"

print "   Right justify 'Hi' in width 10:"
print "   ["
print right_aligned
print "   ]"
print ""

# str_title - title case
print "4. str_title - Title Case"
str_create sentence "hello world from techlang"
str_title sentence titled
print "   Original: hello world from techlang"
print "   Titled:"
print titled
print ""

# str_capitalize - capitalize first letter
print "5. str_capitalize - Capitalize First Letter"
str_create phrase "hello everyone"
str_capitalize phrase capitalized
print "   Original: hello everyone"
print "   Capitalized:"
print capitalized
print ""

# str_swapcase - swap upper/lower case
print "6. str_swapcase - Swap Case"
str_create mixed "HeLLo WoRLd"
str_swapcase mixed swapped
print "   Original: HeLLo WoRLd"
print "   Swapped:"
print swapped
print ""

# Case check methods
print "7. Case Check Methods"
str_create upper "HELLO"
str_create lower "hello"
str_create mixed2 "Hello"
str_isupper upper is_up
str_islower lower is_low
str_isupper mixed2 mixed_up
print "   'HELLO' isupper:"
print is_up
print "   'hello' islower:"
print is_low
print "   'Hello' isupper:"
print mixed_up
print ""

# str_isspace - check if all whitespace
print "8. str_isspace - Check Whitespace"
str_create spaces "   "
str_create text "hello"
str_create mixed_ws "  a  "
str_isspace spaces sp1
str_isspace text sp2
str_isspace mixed_ws sp3
print "   '   ' (3 spaces) isspace:"
print sp1
print "   'hello' isspace:"
print sp2
print "   '  a  ' isspace:"
print sp3
print ""

# Strip methods
print "9. Strip Methods"
str_create padded "   hello world   "
str_lstrip padded left_stripped
str_rstrip padded right_stripped
str_trim padded both_stripped
print "   Original: '   hello world   '"
print "   lstrip (left):"
print left_stripped
print "   rstrip (right):"
print right_stripped
print "   trim (both):"
print both_stripped
print ""

# str_strip_chars - strip specific characters
print "10. str_strip_chars - Strip Specific Characters"
str_create decorated "***IMPORTANT***"
str_strip_chars decorated "*" clean
print "    Original: ***IMPORTANT***"
print "    Strip '*':"
print clean

str_create bracketed "<<<message>>>"
str_strip_chars bracketed "<>" clean2
print "    Original: <<<message>>>"
print "    Strip '<>':"
print clean2
print ""

# Practical example: Formatting output
print "11. Practical Example: Formatted Table"
str_create header1 "Name"
str_create header2 "Age"
str_create header3 "City"

str_ljust header1 15 h1
str_ljust header2 5 h2
str_ljust header3 12 h3
print h1
print h2
print h3
print "----------------------------"

str_create name1 "Alice"
str_create age1 "25"
str_create city1 "New York"
str_ljust name1 15 n1
str_rjust age1 5 a1
str_ljust city1 12 c1
print n1
print a1
print c1

str_create name2 "Bob"
str_create age2 "30"
str_create city2 "LA"
str_ljust name2 15 n2
str_rjust age2 5 a2
str_ljust city2 12 c2
print n2
print a2
print c2
print ""

# Practical example: CSV line parsing (conceptual)
print "12. Practical Example: Building CSV Line"
array_create data
array_push data "John"
array_push data "Doe"
array_push data "john@email.com"
str_create comma ","
str_join data comma csv_line
print "    CSV line:"
print csv_line
print ""

print "=== Demo Complete ==="
