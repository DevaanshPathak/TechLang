# TechLang Chained Comparisons
# ========================================
# The if_chain command enables Python-like chained comparisons
# for elegant range and boundary checks.

print "=== Chained Comparisons Demo ==="
print ""

# Basic range check: 0 < x < 100
print "1. Basic Range Check"
set x 50
if_chain 0 < x < 100 do
print "   x = 50 is in range (0, 100)"
end

set y 150
if_chain 0 < y < 100 do
print "   y is in range"
end
print "   y = 150 is NOT in range (0, 100)"
print ""

# Ascending sequence check: a < b < c
print "2. Triple Comparison (Ascending Check)"
set a 1
set b 5
set c 10
if_chain a < b < c do
print "   a=1, b=5, c=10: a < b < c is TRUE"
end

set d 20
set e 15
set f 10
if_chain d < e < f do
print "   This won't print"
end
print "   d=20, e=15, f=10: d < e < f is FALSE"
print ""

# Mixed comparison operators
print "3. Mixed Operators (<= and >=)"
set val 0
if_chain 0 <= val <= 100 do
print "   val = 0 is in range [0, 100] (inclusive)"
end

set val2 100
if_chain 0 <= val2 <= 100 do
print "   val2 = 100 is in range [0, 100] (inclusive)"
end
print ""

# Equality chains
print "4. Equality Chains"
set p 5
set q 5
set r 5
if_chain p == q == r do
print "   p=q=r=5: All equal!"
end
print ""

# Practical example: grading system
print "5. Practical Example: Grade Calculator"
set score 85
if_chain 90 <= score <= 100 do
print "   Score 85: Grade A"
end
if_chain 80 <= score < 90 do
print "   Score 85: Grade B"
end
if_chain 70 <= score < 80 do
print "   Score 85: Grade C"
end
if_chain 60 <= score < 70 do
print "   Score 85: Grade D"
end
if_chain 0 <= score < 60 do
print "   Score 85: Grade F"
end
print ""

# Using chained comparisons in loops
print "6. Chained Comparisons in Loops"
print "   Counting values in range [5, 15):"
set count 0
set idx 0
loop 20
    if_chain 5 <= idx < 15 do
    add count 1
end
add idx 1
end
print "   Found"
print count
print "   values in range"
print ""

print "=== Demo Complete ==="