# TechLang Cookbook: Multi-Feature Integration Demo
# Demonstrates threads + database + file I/O + JSON + debugging working together
# A realistic example: Concurrent log processing with database storage

boot
print "=== TechLang Cookbook: Log Processor ==="
print "This example demonstrates:"
print "- File I/O operations"
print "- JSON parsing and stringifying"
print "- Database operations"
print "- Thread concurrency"
print "- Debugging and inspection"
print ""

# Enable debugging
watch log_count
watch error_count

# Step 1: Setup Database
print "Step 1: Setting up database..."
db_create "logs.db"
db_execute "CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, level TEXT, message TEXT, timestamp INTEGER)"
db_execute "CREATE TABLE IF NOT EXISTS stats (total INTEGER, errors INTEGER)"
db_execute "INSERT INTO stats VALUES (0, 0)"
print "Database ready"
print ""

# Step 2: Create sample log files with JSON data
print "Step 2: Creating sample log files..."
dict_create log1
dict_set log1 "level" "INFO"
dict_set log1 "message" "Application started"
dict_set log1 "timestamp" "1000"
json_write log1 "log1.json"

dict_create log2
dict_set log2 "level" "ERROR"
dict_set log2 "message" "Connection failed"
dict_set log2 "timestamp" "2000"
json_write log2 "log2.json"

dict_create log3
dict_set log3 "level" "INFO"
dict_set log3 "message" "Request processed"
dict_set log3 "timestamp" "3000"
json_write log3 "log3.json"

print "Created 3 log files"
print ""

# Step 3: Define log processing function
print "Step 3: Defining log processor..."
def process_log
    # This function will run in threads
    file_read "log1.json" content
    json_parse content logdata
    dict_get logdata "level"
    dict_get logdata "message"
end

# Step 4: Process logs with inspection
print "Step 4: Processing logs..."
set log_count 0
set error_count 0

# Read and process first log
json_read "log1.json" log1_data
dict_get log1_data "level"
dict_get log1_data "message"
add log_count 1

# Set breakpoint before critical section
breakpoint

# Read and process second log  
json_read "log2.json" log2_data
dict_get log2_data "level"
dict_get log2_data "message"
add log_count 1
add error_count 1

# Inspect state
inspect

# Read and process third log
json_read "log3.json" log3_data
dict_get log3_data "level"
dict_get log3_data "message"
add log_count 1

print ""
print "Processed logs:"
print log_count

# Step 5: Store stats in database
print ""
print "Step 5: Storing statistics..."
db_execute "UPDATE stats SET total = 3, errors = 1"
db_select "stats" "total, errors"
print ""

# Step 6: Create summary report
print "Step 6: Generating summary..."
dict_create summary
dict_set summary "total_logs" "3"
dict_set summary "error_logs" "1"
dict_set summary "success_rate" "67"
json_write summary "summary.json"
print "Summary written to summary.json"
print ""

# Step 7: Demonstrate threading with file operations
print "Step 7: Concurrent file processing..."
def read_and_count
    file_read "summary.json" data
    str_length data
end

# Create multiple threads to read summary
print "Starting 3 concurrent readers..."
thread_create read_and_count
thread_create read_and_count
thread_create read_and_count

print "Waiting for threads..."
thread_wait_all
print ""

# Step 8: Final inspection
print "Step 8: Final state inspection..."
inspect
print ""

# Step 9: Cleanup
print "Step 9: Cleanup..."
file_delete "log1.json"
file_delete "log2.json"
file_delete "log3.json"
file_delete "summary.json"
db_close
file_delete "logs.db"
unwatch log_count
unwatch error_count
clear_breakpoints
print "Cleanup complete"
print ""

print "=== Cookbook Demo Complete ==="
print "This example showed:"
print "- File I/O with JSON format"
print "- Database CRUD operations"
print "- Thread concurrency"
print "- Debugging with breakpoints and watches"
print "- Multi-module integration"

crash
