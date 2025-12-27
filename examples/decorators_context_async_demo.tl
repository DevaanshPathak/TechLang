# TechLang Decorators, Context Managers, and Async/Await Demo
# This demonstrates features 4, 5, and 6 of Python parity

boot
print "=== TechLang Advanced Features Demo ==="
print ""

# ============================================
# PART 1: DECORATORS
# ============================================
print "--- PART 1: Decorators ---"
print ""

# Define a logging decorator
decorator logger before after do
print "[LOG] Entering function"
# original function runs here
print "[LOG] Exiting function"
end

# Define a simple function
def greet name do
    print "Hello,"
    print name
end

# Apply decorator to function
decorate greet logger

# Call the decorated function
call greet "World"

print ""
print "Decorator successfully wraps function with before/after logging"
print ""

# ============================================
# PART 2: CONTEXT MANAGERS
# ============================================
print "--- PART 2: Context Managers ---"
print ""

# Timer context - measures execution time
print "Using timer context:"
with timer do
set x 0
loop 100 do
    add x 1
end
print "Looped 100 times"
end

print ""

# Suppress context - catches and suppresses errors
print "Using suppress context:"
with suppress do
print "This prints"
# Error inside suppress won't crash program
crash "This error is suppressed"
print "This won't print"
end
print "Execution continues after suppress block"

print ""

# Custom context manager
context my_resource enter exit do
# enter block
print "Acquiring resource..."
set acquired 1
# exit block
print "Releasing resource..."
set acquired 0
end

print "Using custom context manager:"
with my_resource do
print "Resource is in use"
end
print "Resource released"

print ""

# ============================================
# PART 3: ASYNC/AWAIT
# ============================================
print "--- PART 3: Async/Await ---"
print ""

# Define async function (coroutine)
async def fetch_data url do
    print "Fetching data from:"
    print url
    await sleep 100
    set result 42
    return result
end

# Call async function with await
print "Calling async function:"
await fetch_data "https://api.example.com" -> response
print "Response:"
print response

print ""

# Define another async function
async def compute value do
    mul value 2
    return value
end

# Spawn tasks for parallel execution
print "Spawning parallel tasks:"
spawn compute 10 -> task1
spawn compute 20 -> task2
spawn compute 30 -> task3

print "Tasks spawned, gathering results..."

# Wait a moment for tasks to complete
await sleep 200

# Check task statuses
task_status task1 -> status1
task_status task2 -> status2
task_status task3 -> status3

print "Task 1 status:"
print status1
print "Task 2 status:"
print status2
print "Task 3 status:"
print status3

print ""

# ============================================
# INTEGRATION EXAMPLE
# ============================================
print "--- Integration Example ---"
print ""

# Combining all features
decorator timed do
# Uses timer context internally
end

async def process_item item do
    print "Processing:"
    print item
    await sleep 50
    mul item 10
    return item
end

print "Processing items with async..."
await process_item 5 -> result1
await process_item 7 -> result2

print "Results:"
print result1
print result2

print ""
print "=== Demo Complete ==="