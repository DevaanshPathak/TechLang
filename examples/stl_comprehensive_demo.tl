# TechLang Standard Library Demo
# Comprehensive demonstration of all stl modules

boot
print "=== TechLang Standard Library Demo ==="
print ""

# ============================================
# STRING UTILITIES
# ============================================

print "--- String Utilities (stl/strings) ---"
package use stl/strings

# Test capitalize
str_create greeting "hello world"
call stl.strings.capitalize greeting cap_greeting
print "Capitalize: hello world -> "
print cap_greeting

# Test title case
str_create title "the quick brown fox"
call stl.strings.title_case title title_result
print "Title case: the quick brown fox -> "
print title_result

# Test repeat
str_create dash "-"
call stl.strings.repeat dash 10 line
print "Repeat '-' 10 times: "
print line

# Test padding
str_create num "42"
call stl.strings.pad_left num 5 "0" padded_num
print "Pad left '42' to width 5 with '0': "
print padded_num

str_create word "hello"
call stl.strings.pad_right word 10 "." padded_word
print "Pad right 'hello' to width 10 with '.': "
print padded_word

# Test starts_with / ends_with
str_create filename "report.pdf"
call stl.strings.starts_with filename "report" starts_result
print "Does 'report.pdf' start with 'report'? "
print starts_result

call stl.strings.ends_with filename ".pdf" ends_result
print "Does 'report.pdf' end with '.pdf'? "
print ends_result

# Test count_char
str_create text "banana"
str_create search_char "a"
call stl.strings.count_char text search_char count
print "Count 'a' in 'banana': "
print count

print ""

# ============================================
# MATH UTILITIES
# ============================================

print "--- Math Utilities (stl/math) ---"
package use stl/math

# Test min/max
set x 15
set y 42
call stl.math.min x y min_result
print "Min(15, 42): "
print min_result

call stl.math.max x y max_result
print "Max(15, 42): "
print max_result

# Test abs
set negative -25
call stl.math.abs negative abs_result
print "Abs(-25): "
print abs_result

# Test clamp
set value 150
set min_bound 0
set max_bound 100
call stl.math.clamp value min_bound max_bound clamped
print "Clamp(150, 0, 100): "
print clamped

# Test sign
set pos 10
call stl.math.sign pos sign_result
print "Sign(10): "
print sign_result

set neg -5
call stl.math.sign neg sign_result2
print "Sign(-5): "
print sign_result2

# Test even/odd
set num 8
call stl.math.is_even num even_result
print "Is 8 even? "
print even_result

call stl.math.is_odd num odd_result
print "Is 8 odd? "
print odd_result

# Test sum_range
set range_start 1
set range_end 10
call stl.math.sum_range range_start range_end sum_result
print "Sum(1 to 10): "
print sum_result

# Test factorial
set fact_input 5
call stl.math.factorial fact_input fact_result
print "Factorial(5): "
print fact_result

# Test GCD
set a 48
set b 18
call stl.math.gcd a b gcd_result
print "GCD(48, 18): "
print gcd_result

# Test lerp
set lerp_start 0
set lerp_end 100
set lerp_t 50
call stl.math.lerp lerp_start lerp_end lerp_t lerp_result
print "Lerp(0, 100, 0.5): "
print lerp_result

print ""

# ============================================
# COLLECTIONS UTILITIES
# ============================================

print "--- Collections Utilities (stl/collections) ---"
package use stl/collections

# Create test array
array_create numbers
array_push numbers 5
array_push numbers 10
array_push numbers 15
array_push numbers 20
array_push numbers 3

# Test array_sum
call stl.collections.array_sum numbers sum_arr
print "Array sum [5,10,15,20,3]: "
print sum_arr

# Test array_product
array_create factors
array_push factors 2
array_push factors 3
array_push factors 4
call stl.collections.array_product factors product
print "Array product [2,3,4]: "
print product

# Test array_min / array_max
call stl.collections.array_min numbers min_arr
print "Array min [5,10,15,20,3]: "
print min_arr

call stl.collections.array_max numbers max_arr
print "Array max [5,10,15,20,3]: "
print max_arr

# Test array_contains
set search_val 15
call stl.collections.array_contains numbers search_val contains_result
print "Array contains 15? "
print contains_result

# Test array_index_of
call stl.collections.array_index_of numbers search_val index_result
print "Index of 15: "
print index_result

# Test array_count
call stl.collections.array_count numbers count_result
print "Array count: "
print count_result

# Test array_fill
array_create filled
call stl.collections.array_fill filled 7 5
print "Array filled with 7 (5 elements): "
set i 0
loop 5
    array_get filled i val
    print val
    add i 1
end

print ""

# ============================================
# VALIDATION UTILITIES
# ============================================

print "--- Validation Utilities (stl/validation) ---"
package use stl/validation

# Test numeric validation
set positive_num 42
call stl.validation.is_positive positive_num pos_result
print "Is 42 positive? "
print pos_result

set negative_num -10
call stl.validation.is_negative negative_num neg_result
print "Is -10 negative? "
print neg_result

set zero_num 0
call stl.validation.is_zero zero_num zero_result
print "Is 0 zero? "
print zero_result

# Test range validation
set age 25
set min_age 18
set max_age 65
call stl.validation.is_in_range age min_age max_age range_result
print "Is 25 in range [18, 65]? "
print range_result

# Test string validation
str_create password "secret123"
set min_length 8
call stl.validation.min_length password min_length len_result
print "Does 'secret123' meet min length 8? "
print len_result

str_create short_pass "abc"
set max_length 5
call stl.validation.max_length short_pass max_length max_len_result
print "Is 'abc' within max length 5? "
print max_len_result

# Test email validation
str_create email "user@example.com"
call stl.validation.is_email email email_result
print "Is 'user@example.com' valid email? "
print email_result

str_create invalid_email "notanemail"
call stl.validation.is_email invalid_email invalid_result
print "Is 'notanemail' valid email? "
print invalid_result

# Test URL validation
str_create url "https://github.com"
call stl.validation.is_url url url_result
print "Is 'https://github.com' valid URL? "
print url_result

# Test logical validators
set cond1 1
set cond2 1
call stl.validation.require_all cond1 cond2 all_result
print "Require all (1 AND 1): "
print all_result

set cond3 0
set cond4 1
call stl.validation.require_any cond3 cond4 any_result
print "Require any (0 OR 1): "
print any_result

print ""

# ============================================
# COMBINED EXAMPLE - USER REGISTRATION
# ============================================

print "--- Combined Example: User Registration Validator ---"

# Simulate user input
str_create username "alice"
str_create user_email "alice@example.com"
str_create user_password "mysecret123"
set user_age 25

print "Validating registration data..."

# Validate username length
set username_min 3
set username_max 20
call stl.validation.length_between username username_min username_max username_valid
if username_valid eq 1
    print "  Username length: VALID"
end
if username_valid eq 0
    print "  Username length: INVALID"
end

# Validate email format
call stl.validation.is_email user_email email_valid
if email_valid eq 1
    print "  Email format: VALID"
end
if email_valid eq 0
    print "  Email format: INVALID"
end

# Validate password length
set pass_min 8
call stl.validation.min_length user_password pass_min pass_valid
if pass_valid eq 1
    print "  Password strength: VALID"
end
if pass_valid eq 0
    print "  Password strength: INVALID"
end

# Validate age range
set age_min 18
set age_max 120
call stl.validation.is_in_range user_age age_min age_max age_valid
if age_valid eq 1
    print "  Age: VALID"
end
if age_valid eq 0
    print "  Age: INVALID"
end

# Check all validations passed
call stl.validation.require_all username_valid email_valid temp1
call stl.validation.require_all temp1 pass_valid temp2
call stl.validation.require_all temp2 age_valid all_valid

print ""
if all_valid eq 1
    print "Registration: SUCCESS"
    
    # Format welcome message with title case
    str_create welcome "welcome, "
    call stl.strings.capitalize username cap_username
    str_concat welcome cap_username
    str_concat welcome "!"
    print welcome
end
if all_valid eq 0
    print "Registration: FAILED - Please check validation errors"
end

print ""
print "=== Demo Complete ==="

