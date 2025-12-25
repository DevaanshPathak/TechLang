# Async/Await

TechLang provides async/await syntax for concurrent programming, allowing non-blocking operations and parallel task execution.

## Defining Async Functions

Use `async def` to define an asynchronous function (coroutine):

```techlang
async def <name> [params...] do
    # async function body
    return value
end
```

### Example

```techlang
async def fetch_data url do
    print "Fetching from:"
    print url
    await sleep 100  # Simulates network delay
    set result 42
    return result
end
```

## Awaiting Results

Use `await` to wait for an async operation and optionally capture the result:

```techlang
await <coroutine_name> [args...] -> result_var
```

### Example

```techlang
# Define async function
async def compute x do
    mul x 2
    return x
end

# Call and await result
await compute 10 -> result
print result  # Output: 20
```

## Built-in Async Operations

### Sleep

Pause execution for a specified time (milliseconds):

```techlang
await sleep 1000  # Wait 1 second
await sleep 500 -> elapsed  # Capture elapsed time
```

## Spawning Tasks

Use `spawn` to start a task in the background (non-blocking):

```techlang
spawn <coroutine_name> [args...] -> task_id
```

### Example

```techlang
async def long_task do
    await sleep 1000
    set result 100
    return result
end

# Start task in background
spawn long_task -> task1

# Continue other work while task runs
print "Task started, doing other work..."

# Later, check task status
task_status task1 -> status
print status  # "completed" or "running"
```

## Task Management

### Check Task Status

```techlang
task_status <task_id> -> status_var
# status is: "pending", "running", "completed", "failed", or "cancelled"
```

### Cancel a Task

```techlang
task_cancel <task_id>
```

## Gathering Multiple Tasks

Use `gather` to wait for multiple tasks to complete:

```techlang
gather task1 task2 task3 -> results
```

### Example

```techlang
async def process item do
    await sleep 100
    mul item 10
    return item
end

# Spawn multiple tasks
spawn process 1 -> t1
spawn process 2 -> t2
spawn process 3 -> t3

# Wait for all to complete
gather t1 t2 t3 -> all_results

# Check individual results
task_status t1 -> s1
task_status t2 -> s2
task_status t3 -> s3
```

## Async with Parameters

Async functions can accept parameters:

```techlang
async def add_async a b do
    add a b
    return a
end

await add_async 5 3 -> sum
print sum  # Output: 8
```

## Error Handling in Async

Use try/catch around async operations:

```techlang
try do
    await risky_operation -> result
catch do
    print "Operation failed"
end
```

## Practical Examples

### Parallel API Calls

```techlang
async def api_call endpoint do
    print "Calling:"
    print endpoint
    await sleep 200  # Simulate API latency
    set result 200
    return result
end

# Start multiple API calls in parallel
spawn api_call "/users" -> t1
spawn api_call "/posts" -> t2
spawn api_call "/comments" -> t3

# Wait for all to complete
await sleep 500

# Check results
task_status t1 -> s1
task_status t2 -> s2
task_status t3 -> s3
```

### Sequential vs Parallel

```techlang
# Sequential (slow - 3 seconds total)
await slow_op -> r1
await slow_op -> r2
await slow_op -> r3

# Parallel (fast - ~1 second total)
spawn slow_op -> t1
spawn slow_op -> t2  
spawn slow_op -> t3
gather t1 t2 t3 -> results
```

### Producer-Consumer Pattern

```techlang
# Producer
async def produce do
    loop 5 do
        queue_push work_queue "item"
        await sleep 100
    end
end

# Consumer
async def consume do
    loop 5 do
        queue_pop work_queue -> item
        print item
        await sleep 50
    end
end

# Create queue and run
queue_create work_queue
spawn produce -> producer
spawn consume -> consumer
```

## Best Practices

1. **Use `await` for I/O-bound operations** - Network calls, file operations, database queries
2. **Use `spawn` for parallel work** - When tasks can run independently
3. **Use `gather` to synchronize** - When you need all results before continuing
4. **Handle errors** - Wrap async calls in try/catch
5. **Avoid blocking** - Use async versions of operations when available

## Technical Notes

- Async functions execute in the TechLang event loop
- Spawned tasks run in a thread pool
- `await` is non-blocking for sleep and I/O operations
- Task results are stored until garbage collected
