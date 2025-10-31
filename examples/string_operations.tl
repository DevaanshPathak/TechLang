# TechLang String Operations Example
# Demonstrates the new string manipulation commands

// Create a test string
str_create message "  Hello World  "
print message

// Trim whitespace
str_trim message
print message

// Convert to uppercase
str_upper message
print message

// Convert to lowercase
str_lower message
print message

/* Test string replacement */
str_replace message "world" "universe"
print message

// Split string into array
str_create csv "apple,banana,cherry,date"
str_split csv "," fruits

// Get individual elements
array_get fruits 0
array_get fruits 2

// Check if substring exists
    str_create text "techlang is awesome"
    str_contains text "lang"
    str_contains text "python"

    // Reverse a string
    str_create palindrome "racecar"
    str_reverse palindrome
    print palindrome // Still a palindrome!

    // Chaining operations
    str_create data "  MIXED Case Text  "
    str_trim data
    str_lower data
    str_replace data "mixed" "proper"
    print data

    // Split and process
    str_create sentence "the quick brown fox"
    str_split sentence " " words
    array_get words 0
    array_get words 1
    array_get words 2
    array_get words 3