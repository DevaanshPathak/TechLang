# TechLang JSON Demo
# Demonstrates JSON parsing, stringifying, and file operations

boot
print "=== JSON Parse Demo ==="

# Parse simple JSON string
str_create num_data "42"
json_parse num_data result
print "Parsed number:"
print result

# Parse JSON array
str_create arr_data "[10,20,30,40,50]"
json_parse arr_data numbers
print "Parsed array, first element:"
array_get numbers 0

# Parse boolean and null
str_create bool_data "true"
json_parse bool_data flag
print "Parsed boolean (true=1, false=0):"
print flag

str_create null_data "null"
json_parse null_data empty
print "Parsed null (becomes 0):"
print empty

print ""
print "=== JSON Stringify Demo ==="

# Stringify dictionary
dict_create user
dict_set user "name" "Alice"
dict_set user "age" "30"
dict_set user "city" "Hackerville"
json_stringify user output
print "User as JSON:"
print output

# Stringify array
array_create scores 4
array_set scores 0 95
array_set scores 1 87
array_set scores 2 92
array_set scores 3 88
json_stringify scores output
print "Scores as JSON:"
print output

print ""
print "=== JSON File Operations Demo ==="

# Write JSON to file
print "Writing user data to file..."
dict_create profile
dict_set profile "username" "hacker42"
dict_set profile "level" "10"
dict_set profile "active" "1"
json_write profile "profile.json"

# Read JSON from file
print "Reading back from file..."
json_read "profile.json" loaded_profile
dict_get loaded_profile "username"
dict_get loaded_profile "level"

# Roundtrip test
print ""
print "=== Roundtrip Test ==="
array_create data 3
array_set data 0 100
array_set data 1 200
array_set data 2 300
json_write data "data.json"
json_read "data.json" restored
array_get restored 1
print "Middle value after roundtrip:"

print ""
print "=== Unicode Support ==="
dict_create international
dict_set international "greeting" "こんにちは"
dict_set international "emoji" "🚀"
json_write international "unicode.json"
json_read "unicode.json" restored_unicode
dict_get restored_unicode "greeting"
dict_get restored_unicode "emoji"

print ""
print "JSON demo complete!"
crash
