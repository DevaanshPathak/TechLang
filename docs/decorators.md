# Decorators

Decorators in TechLang provide a way to wrap functions with additional behavior, similar to Python's `@decorator` syntax.

## Defining a Decorator

Use the `decorator` command to define a decorator:

```techlang
decorator <name> <before|after|both> do
    # code to run before/after the decorated function
end
```

### Decorator Modes

- `before` - Code runs before the original function
- `after` - Code runs after the original function  
- `both` - Code runs both before and after (use markers to separate)

### Example

```techlang
# Define a logging decorator
decorator logger before after do
    print "[LOG] Function starting"
    # original function executes here
    print "[LOG] Function finished"
end

# Define a function
def greet name do
    print "Hello,"
    print name
end

# Apply the decorator
decorate greet logger

# Call the decorated function
call greet "World"
# Output:
# [LOG] Function starting
# Hello,
# World
# [LOG] Function finished
```

## Applying Decorators

Use `decorate` to apply a decorator to an existing function:

```techlang
decorate <function_name> <decorator_name>
```

### Multiple Decorators

You can apply multiple decorators to a function:

```techlang
decorator auth do
    print "Checking authentication..."
end

decorator log do
    print "Logging call..."
end

def api_call do
    print "API response"
end

decorate api_call auth
decorate api_call log

call api_call
# Output:
# Checking authentication...
# Logging call...
# API response
```

## Built-in Decorators

TechLang provides built-in decorators:

### @log
Logs function entry and exit with timing:
```techlang
decorate my_func log
```

### @time
Measures and reports function execution time:
```techlang
decorate my_func time
```

## Use Cases

- **Logging**: Add consistent logging to functions
- **Timing**: Measure function performance
- **Validation**: Check preconditions before execution
- **Caching**: Memoize function results
- **Authentication**: Verify permissions before execution
