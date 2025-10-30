# TechLang Cookbook

This cookbook demonstrates real-world scenarios combining multiple TechLang features. Each recipe shows how different modules work together to solve practical problems.

---

## Recipe 1: Log File Processor

**Features**: File I/O + JSON + Database + Debugging

A system that reads log files, parses JSON entries, stores them in a database, and provides debugging visibility.

```techlang
boot
print "=== Log Processor ==="

# Enable debugging
watch processed
watch errors

# Setup database
db_create "logs.db"
db_execute "CREATE TABLE logs (level TEXT, message TEXT, time INTEGER)"

# Process logs
set processed 0
set errors 0

# Read JSON log file
json_read "app.log" logdata
dict_get logdata "level"
dict_get logdata "message"

breakpoint  # Pause before database insert

# Store in database
db_insert "logs" "level,message,time" "'INFO','Started',1000"
add processed 1

inspect  # Check state

# Query and report
db_select "logs" "level,count(*)"
print "Processed:"
print processed

# Cleanup
db_close
clear_breakpoints
crash
```

---

## Recipe 2: Concurrent Data Pipeline

**Features**: Threads + Arrays + File I/O + Math

A multi-threaded data processing pipeline that transforms input data concurrently.

```techlang
boot
print "=== Data Pipeline ==="

# Create input data
array_create input 10
set i 0
loop 10
    array_set input i i
    add i 1
end

# Define processing function
def transform
    array_create result 10
    set j 0
    loop 10
        array_get input j
        mul value 2
        array_set result j value
        add j 1
    end
end

# Process in parallel
print "Starting 3 workers..."
thread_create transform
thread_create transform
thread_create transform

# Wait for completion
thread_wait_all

# Verify results
array_get result 5
print "Sample result:"
print value

crash
```

---

## Recipe 3: Configuration Manager

**Features**: JSON + Dictionary + File I/O + Strings

Load, validate, and save application configuration with JSON.

```techlang
boot
print "=== Config Manager ==="

# Create default config
dict_create config
dict_set config "host" "localhost"
dict_set config "port" "8080"
dict_set config "debug" "true"

# Save to file
json_write config "config.json"
print "Config saved"

# Load from file
json_read "config.json" loaded
dict_keys loaded

# Validate
dict_get loaded "host"
str_length hostval

# Update config
dict_set loaded "port" "9000"
json_write loaded "config.json"

# Clean up
file_delete "config.json"
crash
```

---

## Recipe 4: Database ETL Pipeline

**Features**: Database + Arrays + Math + Control Flow

Extract, transform, and load data from one database to another.

```techlang
boot
print "=== ETL Pipeline ==="

# Source database
db_create "source.db"
db_execute "CREATE TABLE users (id INTEGER, age INTEGER)"
db_insert "users" "id,age" "1,25"
db_insert "users" "id,age" "2,30"
db_insert "users" "id,age" "3,35"

# Extract
db_select "users" "age"

# Transform: calculate statistics
set total 0
set count 0
array_create ages 3
array_set ages 0 25
array_set ages 1 30
array_set ages 2 35

loop 3
    array_get ages count
    add total value
    add count 1
end

div total count
set average value

# Load to target
db_create "target.db"
db_execute "CREATE TABLE stats (metric TEXT, value INTEGER)"
db_insert "stats" "metric,value" "'average_age',28"

# Verify
db_select "stats" "*"

# Cleanup
db_close
file_delete "source.db"
file_delete "target.db"
crash
```

---

## Recipe 5: Web API Client

**Features**: Network + JSON + Error Handling + Arrays

Fetch data from an API, parse JSON response, and handle errors.

```techlang
boot
print "=== API Client ==="

# Make request
try
    http_get "https://api.example.com/data" response
    http_status response
    
    # Parse JSON response
    json_parse response data
    dict_keys data
    
    # Process data
    dict_get data "items"
    array_get items 0
    
    print "First item:"
    print value
catch error
    print "API Error:"
    print error
end

crash
```

---

## Recipe 6: Memory-Backed Cache

**Features**: Memory + Dictionary + Math

Implement a simple cache using TechLang's memory system.

```techlang
boot
print "=== Memory Cache ==="

# Allocate cache space
mem_alloc 100
set cache_base value

# Store values
set offset 0
loop 10
    add offset 1
    add cache_base offset
    mem_write value offset
end

# Retrieve values
set lookup 5
add cache_base lookup
mem_read value

print "Cached value at 5:"
print value

# Show cache
mem_dump

# Cleanup
mem_free cache_base
crash
```

---

## Recipe 7: Text Processing Pipeline

**Features**: Strings + Arrays + File I/O + Control Flow

Read a text file, process lines, and generate a report.

```techlang
boot
print "=== Text Processor ==="

# Create sample data
str_create text "Line 1: Hello\nLine 2: World\nLine 3: Test"
file_write "input.txt" text

# Read and parse
file_read "input.txt" content

# Split into lines
str_split content "\n" lines

# Process each line
set line_count 0
set char_total 0

loop 3
    array_get lines line_count
    str_length linetext
    add char_total value
    add line_count 1
end

# Generate report
dict_create report
dict_set report "lines" line_count
dict_set report "chars" char_total
json_write report "report.json"

print "Report generated"

# Cleanup
file_delete "input.txt"
file_delete "report.json"
crash
```

---

## Recipe 8: Debugging Complex Logic

**Features**: Debugger + Variables + Control Flow

Step through complex logic to find and fix bugs.

```techlang
boot
print "=== Debug Session ==="

# Setup watches
watch accumulator
watch counter
watch limit

# Initialize
set accumulator 0
set counter 1
set limit 5

# Set checkpoint
breakpoint

# Complex calculation
loop limit
    # Inspect each iteration
    inspect
    
    mul counter 2
    add accumulator value
    add counter 1
end

# Verify result
breakpoint
inspect

print "Final accumulator:"
print accumulator

# Cleanup
unwatch accumulator
unwatch counter
unwatch limit
clear_breakpoints
crash
```

---

## Recipe 9: Struct-Based Data Model

**Features**: Structs + Arrays + File I/O + JSON

Model and persist structured data.

```techlang
boot
print "=== Data Modeling ==="

# Define structure
struct Person name:string age:int end

# Create instances
struct new Person alice
struct set alice name "Alice"
struct set alice age 30

struct new Person bob
struct set bob name "Bob"
struct set bob age 25

# Display
struct dump alice
struct dump bob

# Store metadata
dict_create metadata
dict_set metadata "count" "2"
dict_set metadata "type" "Person"
json_write metadata "model.json"

# Cleanup
file_delete "model.json"
crash
```

---

## Recipe 10: Multi-Module Integration

**Features**: All major features combined

The ultimate integration example using threads, database, files, JSON, debugging, and more.

See `examples/cookbook_multifeature.tl` for the complete implementation.

**Summary**: This comprehensive example demonstrates:
- Concurrent file processing with threads
- JSON data serialization and deserialization
- Database CRUD operations
- Debugging with watches and breakpoints
- Error handling
- File I/O operations
- Cross-module data flow

---

## Tips for Combining Features

1. **File + JSON**: Always use JSON for structured data persistence
2. **Threads + Database**: Use mutexes to protect shared database access
3. **Debug + Threads**: Watch variables across thread boundaries
4. **Arrays + Loops**: Process collections efficiently
5. **Structs + Dict**: Convert between structured and flexible data
6. **Memory + Arrays**: Use memory for fixed-size, high-performance data
7. **Strings + Files**: Parse text files line by line
8. **Math + Database**: Calculate statistics from query results

---

## Common Patterns

### Pattern 1: Try-Process-Cleanup

```techlang
try
    # Open resources
    file_read "data.txt" content
    
    # Process
    str_length content
    
catch error
    print "Error:"
    print error
end

# Always cleanup
file_delete "temp.txt"
```

### Pattern 2: Producer-Consumer with Threads

```techlang
# Producer
def produce
    loop 10
        queue_push work i
    end
end

# Consumer
def consume
    loop 10
        queue_pop work item
        # Process item
    end
end

# Run concurrently
thread_create produce
thread_create consume
thread_wait_all
```

### Pattern 3: Debug-Fix-Verify

```techlang
watch problematic_var

breakpoint  # Set before suspicious code

# Run problematic section
inspect     # Check state

# Fix if needed
# ...

# Verify fix
inspect
clear_breakpoints
```

---

## Next Steps

After mastering these recipes, try creating your own combinations:

- Build a web scraper (network + files + JSON)
- Create a task scheduler (threads + time + database)
- Implement a data analyzer (files + arrays + math + database)
- Design a configuration system (JSON + files + structs)
- Develop a monitoring tool (loops + database + threads + debugging)

For detailed documentation on each feature:
- [File I/O](file-io.md)
- [Database](database.md)
- [Concurrency](concurrency.md)
- [Debugging](debugging.md)
- [Data Types](data-types.md)
- [Network](network.md)
