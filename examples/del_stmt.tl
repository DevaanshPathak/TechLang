# del Statement Demo
# ===============================
# Delete variables, array elements, and dictionary keys like Python's del

# === DEL - DELETE VARIABLES ===
print "=== Deleting variables ==="

set x 42
print x
del x
# x no longer exists - would error if we tried to print it

set y 100
str_create msg "hello"
del y
del msg
print "Variables deleted successfully"

# === DEL_ARRAY - DELETE ARRAY ELEMENTS ===
print ""
print "=== Deleting array elements ==="

array_create nums
array_push nums 10
array_push nums 20
array_push nums 30
array_push nums 40
array_push nums 50

print "Before deletion:"
array_get nums 0
array_get nums 1
array_get nums 2
array_get nums 3
array_get nums 4

del_array nums 2

print "After deleting index 2:"
array_get nums 0
array_get nums 1
array_get nums 2
array_get nums 3
# Index 4 no longer exists (array reindexed)

# === DEL_DICT - DELETE DICTIONARY KEYS ===
print ""
print "=== Deleting dictionary keys ==="

dict_create person
dict_set person "name" "Alice"
dict_set person "age" 30
dict_set person "city" "NYC"
dict_set person "temp" "delete_me"

print "Before deletion:"
dict_keys person keys
print keys

del_dict person "temp"

print "After deleting 'temp':"
dict_keys person keys2
print keys2

# === PRACTICAL USE CASE: CACHE CLEANUP ===
print ""
print "=== Cache cleanup example ==="

dict_create cache
dict_set cache "user_1" "data1"
dict_set cache "user_2" "data2"
dict_set cache "expired_1" "old"
dict_set cache "expired_2" "old"
dict_set cache "user_3" "data3"

# Clean up expired entries
del_dict cache "expired_1"
del_dict cache "expired_2"

dict_len cache size
print "Cache entries after cleanup:"
print size

# === DELETE AND RECREATE ===
print ""
print "=== Delete and recreate ==="

set counter 0
add counter 5
print counter

del counter

set counter 100
print counter

print ""
print "Demo complete!"
