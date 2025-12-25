# Context Managers

Context managers in TechLang provide resource management with automatic setup and cleanup, similar to Python's `with` statement.

## Basic Usage

The `with` statement ensures resources are properly acquired and released:

```techlang
with <context_type> [args...] do
    # code using the resource
end
# resource is automatically cleaned up
```

## Built-in Context Managers

### Timer Context

Measures execution time of a code block:

```techlang
with timer do
    # code to time
    set x 0
    loop 1000 do
        add x 1
    end
end
# Output: [Timer] Block completed in X.XXXs
```

### Suppress Context

Catches and suppresses errors within the block:

```techlang
with suppress do
    print "Before error"
    crash "This error is suppressed"
    print "This won't print"
end
print "Execution continues"
# Output:
# Before error
# Execution continues
```

### File Context

Automatically handles file opening and closing:

```techlang
with file "data.txt" do
    file_write "data.txt" "Hello, World!"
    file_read "data.txt" content
    print content
end
# File handle automatically cleaned up
```

### Transaction Context

Groups database operations with rollback on error:

```techlang
with transaction do
    db_exec "INSERT INTO users VALUES (1, 'Alice')"
    db_exec "INSERT INTO users VALUES (2, 'Bob')"
    # If any operation fails, all are rolled back
end
```

### Lock Context

Provides thread-safe mutex locking:

```techlang
mutex_create my_lock
with lock my_lock do
    # Thread-safe code
    add shared_counter 1
end
# Lock automatically released
```

## Custom Context Managers

Define your own context managers with enter/exit blocks:

```techlang
context <name> enter exit do
    # enter block - runs at start
    print "Entering context"
    
    # exit block - runs at end (even on error)
    print "Exiting context"
end

# Use the custom context
with <name> do
    print "Inside context"
end
```

### Full Example

```techlang
# Define a database connection context
context db_connection enter exit do
    # Enter: open connection
    print "Opening database connection..."
    db_connect "app.db"
    
    # Exit: close connection
    print "Closing database connection..."
end

# Use it
with db_connection do
    db_exec "CREATE TABLE IF NOT EXISTS users (id INT, name TEXT)"
    db_exec "INSERT INTO users VALUES (1, 'Alice')"
end
# Connection automatically closed
```

## Nested Contexts

Contexts can be nested:

```techlang
with timer do
    with suppress do
        with file "log.txt" do
            file_write "log.txt" "Operation started"
            # nested operations
        end
    end
end
```

## Error Handling

Context managers guarantee cleanup even when errors occur:

```techlang
context cleanup_test enter exit do
    print "Resource acquired"
    print "Resource released"  # Always runs
end

with cleanup_test do
    print "Working..."
    crash "Something went wrong"
    print "This won't print"
end
# Output:
# Resource acquired
# Working...
# Resource released (cleanup still happens!)
```

## Use Cases

- **File I/O**: Automatic file closing
- **Database**: Connection management and transactions
- **Threading**: Mutex lock/unlock
- **Timing**: Performance measurement
- **Error handling**: Graceful error suppression
- **Resource cleanup**: Custom resource management
