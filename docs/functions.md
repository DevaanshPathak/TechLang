# First-Class Functions and Closures in TechLang

TechLang supports first-class functions, closures, and functional programming patterns.

---

## First-Class Functions

Functions can be treated as values - stored in variables, passed as arguments, and returned from other functions.

### fn - Define a Named Function Value

```techlang
fn name params do
    # function body
    return value
end
```

### fn_ref - Get Reference to Existing Function

```techlang
def myFunc x
    # existing function
end

fn_ref myFunc funcVar
```

### fn_call - Call a Function Value

```techlang
fn_call funcName arg1 arg2 ... -> resultVar
```

### Example

```techlang
# Define a function value
fn double x do
    set result x
    mul result 2
    return result
end

# Call it
fn_call double 5 -> answer
print answer  # Output: 10
```

---

## Closures

Closures capture variables from their outer scope:

```techlang
set multiplier 10

fn multiply x do
    set result x
    mul result multiplier  # captures 'multiplier' from outer scope
    return result
end

fn_call multiply 5 -> answer
print answer  # Output: 50

# Even if multiplier changes later, closure uses captured value
set multiplier 100
fn_call multiply 5 -> answer2
print answer2  # Output: 50 (still uses 10)
```

### What Gets Captured

- Variables (`set x 5`)
- Strings (`str_create s "hello"`)
- Arrays (by reference)
- Dictionaries (by reference)

---

## Lambda Functions

Simple one-expression functions for use with higher-order functions:

```techlang
lambda name param "expression"
```

### Examples

```techlang
# Double a number
lambda doubler x "x * 2"

# Check if positive
lambda is_positive x "x > 0"

# Identity function
lambda identity x "x"
```

**Note:** Lambda expressions are limited to simple arithmetic and comparisons.

---

## Higher-Order Functions

### map_fn - Transform Each Element

Apply a function to every element in an array:

```techlang
map_fn sourceArray funcName resultArray
```

```techlang
array_create numbers 3
array_set numbers 0 1
array_set numbers 1 2
array_set numbers 2 3

lambda triple x "x * 3"
map_fn numbers triple tripled

# tripled = [3, 6, 9]
```

### filter_fn - Select Elements

Keep only elements that satisfy a predicate:

```techlang
filter_fn sourceArray predicateFunc resultArray
```

```techlang
array_create nums 5
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
array_set nums 3 4
array_set nums 4 5

lambda is_even x "x % 2 == 0"
filter_fn nums is_even evens

# evens = [2, 4]
```

### reduce_fn - Fold Elements

Combine all elements into a single value:

```techlang
reduce_fn sourceArray binaryFunc initialValue resultVar
```

```techlang
array_create nums 4
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
array_set nums 3 4

fn add a b do
    set result a
    add result b
    return result
end

reduce_fn nums add 0 total
print total  # Output: 10 (1+2+3+4)
```

---

## Partial Application

Create a new function with some arguments pre-filled:

```techlang
partial funcName newFuncName arg1=val1 arg2=val2
```

### Example

```techlang
fn add a b do
    set result a
    add result b
    return result
end

# Create add_10 that always adds 10
partial add add_10 a=10

fn_call add_10 5 -> result
print result  # Output: 15
```

### Multiple Bound Arguments

```techlang
fn greet prefix name suffix do
    str_create msg prefix
    str_concat msg name
    str_concat msg suffix
    print msg
end

partial greet hello_exclaim prefix="Hello, " suffix="!"
fn_call hello_exclaim "World" -> ignored
# Output: Hello, World!
```

---

## Function Composition

Combine two functions into a pipeline:

```techlang
compose outerFunc innerFunc composedName
```

When called, `composedName(x)` executes `outerFunc(innerFunc(x))`:

```techlang
lambda double x "x * 2"
lambda add_one x "x + 1"

# double ∘ add_one means: double(add_one(x))
compose double add_one double_after_add

fn_call double_after_add 5 -> result
print result  # Output: 12  (double(add_one(5)) = double(6) = 12)
```

### Composition Order

`compose f g` creates a function that:
1. First applies `g` to the input
2. Then applies `f` to the result

Mathematical notation: (f ∘ g)(x) = f(g(x))

---

## Combining Techniques

### Currying Pattern

```techlang
# Create a multiplier factory using partial
fn multiply a b do
    set result a
    mul result b
    return result
end

partial multiply times_2 a=2
partial multiply times_3 a=3
partial multiply times_10 a=10

fn_call times_2 5 -> r1
fn_call times_3 5 -> r2
fn_call times_10 5 -> r3

print r1  # 10
print r2  # 15
print r3  # 50
```

### Pipeline Processing

```techlang
# Process data through multiple transformations
array_create data 4
array_set data 0 1
array_set data 1 2
array_set data 2 3
array_set data 3 4

# Step 1: Double everything
lambda double x "x * 2"
map_fn data double doubled

# Step 2: Keep only values > 4
lambda gt_four x "x > 4"
filter_fn doubled gt_four filtered

# Step 3: Sum the results
fn add a b do
    set result a
    add result b
    return result
end
reduce_fn filtered add 0 total

print total  # 6 + 8 = 14
```

---

## Practical Examples

### Counter Factory

```techlang
set counter_value 0

fn create_counter do
    fn counter do
        add counter_value 1
        return counter_value
    end
    return counter
end
```

### Memoization Pattern

```techlang
# Store computed values in a dict
dict_create cache

fn fibonacci n do
    # Check cache
    dict_has cache n has_cached
    if has_cached == 1
        dict_get cache n cached
        return cached
    end
    
    # Base cases
    if n < 2
        dict_set cache n n
        return n
    end
    
    # Recursive case
    set n1 n
    sub n1 1
    fn_call fibonacci n1 -> fib1
    
    set n2 n
    sub n2 2
    fn_call fibonacci n2 -> fib2
    
    set result fib1
    add result fib2
    
    dict_set cache n result
    return result
end
```

---

## Command Reference

| Command | Syntax | Description |
|---------|--------|-------------|
| `fn` | `fn name params do ... end` | Define function value |
| `fn_ref` | `fn_ref funcName var` | Get reference to function |
| `fn_call` | `fn_call func args... -> var` | Call function value |
| `lambda` | `lambda name param "expr"` | Simple one-liner function |
| `partial` | `partial func new arg=val` | Partial application |
| `compose` | `compose f g composed` | Function composition |
| `map_fn` | `map_fn arr func result` | Transform array elements |
| `filter_fn` | `filter_fn arr pred result` | Filter array elements |
| `reduce_fn` | `reduce_fn arr func init var` | Fold array to value |
