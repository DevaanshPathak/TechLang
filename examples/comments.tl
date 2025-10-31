# TechLang Comments Example
# This demonstrates all three comment styles supported in TechLang

/*
==============================================
Multi-line Comment Block
==============================================
This is a program that demonstrates
TechLang's comment capabilities:
- Hash comments (single-line)
- Double-slash comments (C-style)
- Block comments like this one
==============================================
*/

// Initialize a counter variable
set counter 0

# Loop 5 times
loop 5
    add counter 1 // increment the counter
    print counter  # display current value
end

/*
Calculate the sum of two numbers
This shows how comments work with math operations
*/
set a 10  # first number
set b 20 // second number
add a b
print a /* should print 30 */

// String demonstration
str_create message "Comments make code readable!"  # create a string
print message

/*
Function with comments
*/
def greet
    // This function prints a greeting
    print "Hello from TechLang!"  # output greeting
end

call greet /* invoke the function */

# End of demonstration
// Program complete!