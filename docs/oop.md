# Object-Oriented Programming in TechLang

TechLang supports full object-oriented programming with classes, inheritance, methods, and more.

---

## Class Definition

Define a class with fields and methods:

```techlang
class ClassName
    field fieldName type default_value
    
    init param1 param2
        # Constructor body
        set_field self fieldName param1
    end
    
    method methodName param1
        # Method body
        get_field self fieldName localVar
        return localVar
    end
    
    static staticMethod param1
        # Static method (no self)
        return param1
    end
end
```

### Fields

Fields define the data stored in each instance:

```techlang
field x int 0           # Integer field, default 0
field name string ""    # String field, default empty
field data any None     # Any type, default None
```

### Constructors

The `init` block is called when creating a new instance:

```techlang
class Point
    field x int 0
    field y int 0
    
    init px py
        set_field self x px
        set_field self y py
    end
end

# Create instance - calls init with 3, 4
new Point p 3 4
```

---

## Creating Objects

Use `new` to instantiate a class:

```techlang
new ClassName varName arg1 arg2 ...
```

### Examples

```techlang
# No constructor arguments
new Widget w

# With constructor arguments
new Point p 10 20

# Arguments are passed to init block
```

---

## Accessing Fields

### Get Field Value

```techlang
get_field instance fieldName targetVar
```

### Set Field Value

```techlang
set_field instance fieldName value
```

### Examples

```techlang
new Point p 5 10

# Get x into local variable
get_field p x myX
print myX  # Output: 5

# Update y
set_field p y 20
get_field p y myY
print myY  # Output: 20
```

---

## Calling Methods

### Instance Methods

```techlang
call instance.methodName arg1 arg2 ... [-> resultVar]
```

### Static Methods

```techlang
call ClassName.staticMethod arg1 arg2 ... [-> resultVar]
```

### Examples

```techlang
class Calculator
    field value int 0
    
    init v
        set_field self value v
    end
    
    method add n
        get_field self value curr
        add curr n
        set_field self value curr
        return curr
    end
    
    static multiply a b
        set result a
        mul result b
        return result
    end
end

# Instance method
new Calculator calc 10
call calc.add 5 -> result
print result  # Output: 15

# Static method (no instance needed)
call Calculator.multiply 6 7 -> product
print product  # Output: 42
```

---

## Inheritance

Classes can inherit from parent classes using `extends`:

```techlang
class Parent
    field name string ""
    
    method greet
        print "Hello from Parent"
    end
end

class Child extends Parent
    field age int 0
    
    # Override parent method
    method greet
        print "Hello from Child"
    end
    
    # New method
    method play
        print "Playing!"
    end
end

new Child c
call c.greet  # Output: Hello from Child
call c.play   # Output: Playing!
```

### Inherited Features

- Child classes inherit all fields from parent
- Child classes inherit all methods from parent
- Methods can be overridden by defining same name in child
- Use `instanceof` to check type hierarchy

---

## Type Checking

### instanceof

Check if an object is an instance of a class (including parent classes):

```techlang
instanceof object ClassName resultVar
```

### Example

```techlang
class Animal end
class Dog extends Animal end

new Dog d

instanceof d Dog isDog
instanceof d Animal isAnimal
instanceof d Cat isCat

print isDog    # Output: 1 (true)
print isAnimal # Output: 1 (true, Dog extends Animal)
print isCat    # Output: 0 (false)
```

---

## Complete Example: Shape Hierarchy

```techlang
# Base shape class
class Shape
    field name string "Shape"
    
    method describe
        get_field self name n
        print "I am a"
        print n
    end
    
    method area
        return 0
    end
end

# Rectangle extends Shape
class Rectangle extends Shape
    field width int 0
    field height int 0
    
    init w h
        set_field self name "Rectangle"
        set_field self width w
        set_field self height h
    end
    
    method area
        get_field self width w
        get_field self height h
        set a w
        mul a h
        return a
    end
end

# Circle extends Shape
class Circle extends Shape
    field radius int 0
    
    init r
        set_field self name "Circle"
        set_field self radius r
    end
    
    method area
        get_field self radius r
        set a r
        mul a r
        mul a 3
        return a
    end
end

# Usage
new Rectangle rect 5 10
new Circle circ 7

call rect.describe
call rect.area -> rectArea
print rectArea  # Output: 50

call circ.describe
call circ.area -> circArea
print circArea  # Output: 147
```

---

## Static Methods

Static methods belong to the class, not instances. They cannot access `self`:

```techlang
class MathUtils
    static max a b
        if a > b
            return a
        end
        return b
    end
    
    static min a b
        if a < b
            return a
        end
        return b
    end
    
    static abs n
        if n < 0
            set result 0
            sub result n
            return result
        end
        return n
    end
end

# Call without creating instance
call MathUtils.max 10 20 -> m
print m  # Output: 20

call MathUtils.abs -5 -> a
print a  # Output: 5
```

---

## Best Practices

### 1. Initialize All Fields in Constructor

```techlang
class User
    field name string ""
    field age int 0
    field active int 1
    
    init n a
        set_field self name n
        set_field self age a
        # active uses default (1)
    end
end
```

### 2. Use Descriptive Method Names

```techlang
class BankAccount
    method deposit amount end
    method withdraw amount end
    method getBalance end
    method transfer toAccount amount end
end
```

### 3. Keep Classes Focused

Each class should have a single responsibility.

### 4. Prefer Composition Over Deep Inheritance

```techlang
# Instead of deep inheritance:
# Vehicle -> Car -> SportsCar -> Ferrari

# Use composition:
class Car
    field engine Engine
    field wheels Wheels
end
```

---

## Command Reference

| Command | Syntax | Description |
|---------|--------|-------------|
| `class` | `class Name ... end` | Define a class |
| `extends` | `class Child extends Parent` | Inherit from parent |
| `field` | `field name type default` | Define instance field |
| `init` | `init params ... end` | Constructor block |
| `method` | `method name params ... end` | Instance method |
| `static` | `static name params ... end` | Static method |
| `new` | `new Class var args...` | Create instance |
| `get_field` | `get_field inst field var` | Read field value |
| `set_field` | `set_field inst field val` | Write field value |
| `instanceof` | `instanceof obj Class var` | Type check |
