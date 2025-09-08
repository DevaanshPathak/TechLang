# Dictionary operations example for TechLang
# Demonstrates dictionary creation, key-value pairs, and access

# Create a dictionary
dict_create user_info

# Set key-value pairs
dict_set user_info "name" "Alice"
dict_set user_info "age" "25"
dict_set user_info "city" "New York"
dict_set user_info "occupation" "Developer"

# Get values by key
print "User information:"
dict_get user_info "name"
dict_get user_info "age"
dict_get user_info "city"
dict_get user_info "occupation"

# Show all keys
dict_keys user_info

# Create another dictionary for demonstration
dict_create scores
dict_set scores "math" "95"
dict_set scores "science" "87"
dict_set scores "english" "92"

print "Student scores:"
dict_get scores "math"
dict_get scores "science"
dict_get scores "english"

# Show all keys in scores dictionary
dict_keys scores
