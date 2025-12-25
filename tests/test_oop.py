"""
Tests for Object-Oriented Programming features in TechLang.
Tests classes, inheritance, methods, and object instantiation.
"""

import pytest
from techlang.interpreter import run


class TestClassDefinition:
    """Tests for class definition."""
    
    def test_simple_class_definition(self):
        code = """
class Animal
    field name string
    field age int
end
print "defined"
"""
        assert run(code).strip() == "defined"
    
    def test_class_with_method(self):
        code = """
class Counter
    field count int 0
    
    method increment
        add count 1
    end
    
    method get_count
        return count
    end
end
print "defined"
"""
        assert run(code).strip() == "defined"
    
    def test_class_with_init(self):
        code = """
class Person
    field name string
    field age int
    
    init n a
        set_field self name n
        set_field self age a
    end
end
print "defined"
"""
        assert run(code).strip() == "defined"


class TestObjectInstantiation:
    """Tests for creating objects from classes."""
    
    def test_new_simple_object(self):
        code = """
class Point
    field x int 0
    field y int 0
end

new Point p1
get_field p1 x
"""
        assert run(code).strip() == "0"
    
    def test_new_with_default_values(self):
        code = """
class Config
    field debug int 1
    field name string "default"
end

new Config cfg
get_field cfg debug result
print result
"""
        assert run(code).strip() == "1"
    
    def test_set_field_value(self):
        code = """
class Box
    field value int 0
end

new Box b
set_field b value 42
get_field b value
"""
        assert run(code).strip() == "42"


class TestMethodCalls:
    """Tests for calling methods on objects."""
    
    def test_simple_method_call(self):
        code = """
class Counter
    field count int 0
    
    method increment
        add count 1
    end
    
    method get_value
        return count
    end
end

new Counter c
call c.increment
call c.get_value result
print result
"""
        output = run(code).strip()
        # Check the last line is the result
        assert "1" in output
    
    def test_method_with_parameters(self):
        code = """
class Calculator
    field result int 0
    
    method add_num n
        add result n
    end
    
    method get_result
        return result
    end
end

new Calculator calc
call calc.add_num 5
call calc.add_num 3
call calc.get_result r
print r
"""
        output = run(code).strip()
        assert "8" in output


class TestInheritance:
    """Tests for class inheritance."""
    
    def test_simple_inheritance(self):
        code = """
class Animal
    field name string
end

class Dog extends Animal
    field breed string
end

new Dog d
set_field d name "Buddy"
set_field d breed "Labrador"
get_field d name
"""
        assert "Buddy" in run(code).strip()
    
    def test_instanceof_check(self):
        code = """
class Animal
    field name string
end

class Dog extends Animal
    field breed string
end

new Dog d
instanceof d Dog result1
instanceof d Animal result2
print result1
print result2
"""
        output = run(code).strip().splitlines()
        # Dog is a Dog
        assert "1" in output[-2]
        # Dog is also an Animal (inheritance)
        assert "1" in output[-1]


class TestStaticMethods:
    """Tests for static methods."""
    
    def test_static_method_definition(self):
        code = """
class MathUtils
    static add a b
        set sum a
        add sum b
        return sum
    end
end

call MathUtils.add 3 4 result
print result
"""
        output = run(code).strip()
        assert "7" in output


class TestExceptionHandling:
    """Tests for throw/raise commands."""
    
    def test_throw_basic(self):
        code = """
throw "Something went wrong"
"""
        output = run(code)
        assert "[Error:" in output
        assert "Something went wrong" in output
    
    def test_throw_with_type(self):
        code = """
throw "Invalid value" ValueError
"""
        output = run(code)
        assert "ValueError" in output
        assert "Invalid value" in output
    
    def test_raise_alias(self):
        code = """
raise "Test error"
"""
        output = run(code)
        assert "[Error:" in output
        assert "Test error" in output
    
    def test_throw_caught_by_try(self):
        code = """
try
    throw "Expected error"
catch err
    print "Caught:"
    print err
end
"""
        output = run(code).strip()
        assert "Caught:" in output


class TestFirstClassFunctions:
    """Tests for first-class functions and closures."""
    
    def test_fn_definition(self):
        code = """
fn double x do
    set result x
    mul result 2
    return result
end
print "defined"
"""
        assert run(code).strip() == "defined"
    
    def test_fn_call(self):
        code = """
fn add_ten n do
    set result n
    add result 10
    return result
end

fn_call add_ten 5 -> answer
print answer
"""
        output = run(code).strip()
        assert "15" in output
    
    def test_lambda_in_fn_values(self):
        code = """
lambda square x "x * x"
fn_call square 5 result
print result
"""
        output = run(code).strip()
        assert "25" in output
    
    def test_closure_captures_scope(self):
        code = """
set multiplier 3

fn multiply_by_captured n do
    set result n
    mul result multiplier
    return result
end

fn_call multiply_by_captured 7 -> answer
print answer
"""
        output = run(code).strip()
        assert "21" in output
    
    def test_map_fn(self):
        code = """
array_create nums 3
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3

lambda double x "x * 2"
map_fn nums double result

array_get result 0 v0
array_get result 1 v1
array_get result 2 v2
print v0
print v1
print v2
"""
        output = run(code).strip().splitlines()
        # Check doubled values
        assert "2" in output
        assert "4" in output
        assert "6" in output
    
    def test_filter_fn(self):
        code = """
array_create nums 5
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
array_set nums 3 4
array_set nums 4 5

lambda is_even x "x % 2 == 0"
filter_fn nums is_even result

array_get result 0 v0
array_get result 1 v1
print v0
print v1
"""
        output = run(code).strip().splitlines()
        # Only even numbers: 2 and 4
        assert "2" in output
        assert "4" in output
    
    def test_reduce_fn(self):
        code = """
array_create nums 4
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
array_set nums 3 4

fn add_two a b do
    set result a
    add result b
    return result
end

reduce_fn nums add_two 0 total
print total
"""
        output = run(code).strip()
        # Sum of 1+2+3+4 = 10
        assert "10" in output
    
    def test_partial_application(self):
        code = """
fn add a b do
    set result a
    add result b
    return result
end

partial add add5 a=5
fn_call add5 3 -> answer
print answer
"""
        output = run(code).strip()
        assert "8" in output
    
    def test_compose_functions(self):
        code = """
lambda double x "x * 2"
lambda add_one x "x + 1"

compose double add_one double_then_add
fn_call double_then_add 5 -> result
print result
"""
        output = run(code).strip()
        # double(add_one(5)) = double(6) = 12
        assert "12" in output


class TestFnRef:
    """Tests for function references."""
    
    def test_fn_ref_to_regular_function(self):
        code = """
def greet name
    str_create msg "Hello, "
    str_concat msg name
    print msg
end

fn_ref greet greet_fn
print "got reference"
"""
        output = run(code).strip()
        assert "got reference" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
