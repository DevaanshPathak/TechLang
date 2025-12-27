# TechLang Dict Methods
# ==================================
# Additional Pythonic dictionary methods

print "=== Dict Methods Demo ==="
print ""

# dict_setdefault - Set if not exists
print "1. dict_setdefault - Set Default Value"
dict_create config
dict_setdefault config "host" "localhost"
dict_setdefault config "port" 8080
dict_setdefault config "debug" 0
print "   Config after setdefaults:"
dict_get config "host" h
dict_get config "port" p
dict_get config "debug" d
print "   host:"
print h
print "   port:"
print p
print "   debug:"
print d

# Try to set again - should NOT override
dict_setdefault config "host" "example.com"
dict_get config "host" h2
print "   After trying to setdefault 'host' again:"
print h2
print ""

# dict_copy - Shallow copy
print "2. dict_copy - Create Copy"
dict_create original
dict_set original "name" "Alice"
dict_set original "age" 30
dict_copy original backup
print "   Created backup of original dict"

# Modify original - backup unchanged
dict_set original "age" 31
dict_get original "age" orig_age
dict_get backup "age" backup_age
print "   Original age (modified):"
print orig_age
print "   Backup age (unchanged):"
print backup_age
print ""

# dict_fromkeys - Create dict from array keys
print "3. dict_fromkeys - Create Dict From Keys"
array_create fields
array_push fields "name"
array_push fields "email"
array_push fields "phone"
dict_fromkeys fields "" user_template
print "   Created user template with empty values:"
dict_keys user_template keys_arr
array_get keys_arr 0 k0
array_get keys_arr 1 k1
array_get keys_arr 2 k2
print "   Keys:"
print k0
print k1
print k2
print ""

# dict_fromkeys with default value
print "4. dict_fromkeys With Default Values"
array_create counters
array_push counters "clicks"
array_push counters "views"
array_push counters "shares"
dict_fromkeys counters 0 stats
print "   Created stats counter initialized to 0:"
dict_get stats "clicks" clicks
dict_get stats "views" views
dict_get stats "shares" shares
print "   clicks:"
print clicks
print "   views:"
print views
print "   shares:"
print shares
print ""

# dict_merge - Merge two dicts
print "5. dict_merge - Merge Dictionaries"
dict_create defaults
dict_set defaults "theme" "light"
dict_set defaults "language" "en"
dict_set defaults "font_size" 14

dict_create user_prefs
dict_set user_prefs "theme" "dark"
dict_set user_prefs "font_size" 16

dict_merge defaults user_prefs final_config
print "   Defaults: theme=light, language=en, font_size=14"
print "   User prefs: theme=dark, font_size=16"
print "   Merged (user wins):"
dict_get final_config "theme" theme
dict_get final_config "language" lang
dict_get final_config "font_size" fs
print "   theme:"
print theme
print "   language:"
print lang
print "   font_size:"
print fs
print ""

# Practical example: Configuration system
print "6. Practical Example: Config System"
# Define default config
dict_create default_config
dict_setdefault default_config "db_host" "localhost"
dict_setdefault default_config "db_port" 5432
dict_setdefault default_config "db_name" "mydb"
dict_setdefault default_config "max_connections" 10

# User overrides
dict_create env_config
dict_set env_config "db_host" "prod.example.com"
dict_set env_config "max_connections" 100

# Merge to get final config
dict_merge default_config env_config app_config
print "   Final application config:"
dict_get app_config "db_host" db_h
dict_get app_config "db_port" db_p
dict_get app_config "db_name" db_n
dict_get app_config "max_connections" mc
print "   db_host:"
print db_h
print "   db_port:"
print db_p
print "   db_name:"
print db_n
print "   max_connections:"
print mc
print ""

# Practical example: Counter initialization
print "7. Practical Example: Counter Pattern"
array_create items
array_push items "apple"
array_push items "banana"
array_push items "apple"
array_push items "cherry"
array_push items "apple"
array_push items "banana"

# Initialize all counters to 0
array_create unique_items
array_push unique_items "apple"
array_push unique_items "banana"
array_push unique_items "cherry"
dict_fromkeys unique_items 0 counter

# Count occurrences (manually since we don't have increment in dict)
dict_get counter "apple" a_cnt
set a_cnt 3
dict_set counter "apple" a_cnt
dict_get counter "banana" b_cnt
set b_cnt 2
dict_set counter "banana" b_cnt
dict_get counter "cherry" c_cnt
set c_cnt 1
dict_set counter "cherry" c_cnt

print "   Item counts:"
dict_get counter "apple" apple_count
dict_get counter "banana" banana_count
dict_get counter "cherry" cherry_count
print "   apple:"
print apple_count
print "   banana:"
print banana_count
print "   cherry:"
print cherry_count
print ""

print "=== Demo Complete ==="
