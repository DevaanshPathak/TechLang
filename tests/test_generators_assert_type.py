"""
Tests for Python-like features: Generators, Assert, Type Checking
Todo 16: Generators/iterators
Todo 17: Assert command  
Todo 18: Type checking (isinstance, type)
"""
import pytest
from techlang.interpreter import run


class TestGeneratorCreate:
    """Test generator_create command."""
    
    def test_generator_create_from_array(self):
        """Test creating generator from array."""
        code = '''array_create nums 3
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
generator_create gen nums
is_generator gen result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"
    
    def test_generator_create_error_no_array(self):
        """Test error when array doesn't exist."""
        code = '''generator_create gen missing'''
        output = run(code).strip()
        assert "does not exist" in output


class TestGeneratorNext:
    """Test generator_next command."""
    
    def test_generator_next_iterate(self):
        """Test iterating through generator."""
        code = '''array_create nums 3
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
generator_create gen nums
generator_next gen val done
print val
print done'''
        output = run(code).strip().splitlines()
        assert output[-2] == "10"
        assert output[-1] == "0"
    
    def test_generator_next_exhausted(self):
        """Test generator exhaustion."""
        code = '''array_create nums 2
array_set nums 0 1
array_set nums 1 2
generator_create gen nums
generator_next gen val done
generator_next gen val done
generator_next gen val done
print done'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"
    
    def test_generator_next_full_iteration(self):
        """Test iterating through all values."""
        code = '''array_create nums 3
array_set nums 0 5
array_set nums 1 10
array_set nums 2 15
generator_create gen nums
generator_next gen v1 d1
generator_next gen v2 d2
generator_next gen v3 d3
generator_next gen v4 d4
print v1
print v2
print v3
print d4'''
        output = run(code).strip().splitlines()
        assert output[-4] == "5"
        assert output[-3] == "10"
        assert output[-2] == "15"
        assert output[-1] == "1"  # exhausted


class TestGeneratorReset:
    """Test generator_reset command."""
    
    def test_generator_reset(self):
        """Test resetting generator."""
        code = '''array_create nums 2
array_set nums 0 100
array_set nums 1 200
generator_create gen nums
generator_next gen v1 d1
generator_next gen v2 d2
generator_reset gen
generator_next gen v3 d3
print v3
print d3'''
        output = run(code).strip().splitlines()
        assert output[-2] == "100"  # Back to first value
        assert output[-1] == "0"


class TestGeneratorToArray:
    """Test generator_to_array command."""
    
    def test_generator_to_array_full(self):
        """Test collecting all values."""
        code = '''array_create src 3
array_set src 0 1
array_set src 1 2
array_set src 2 3
generator_create gen src
generator_to_array gen result
array_get result 0 v0
array_get result 2 v2
print v0
print v2'''
        output = run(code).strip().splitlines()
        assert output[-2] == "1"
        assert output[-1] == "3"
    
    def test_generator_to_array_partial(self):
        """Test collecting remaining values after iteration."""
        code = '''array_create src 4
array_set src 0 10
array_set src 1 20
array_set src 2 30
array_set src 3 40
generator_create gen src
generator_next gen v d
generator_to_array gen result
array_get result 0 first
print first'''
        output = run(code).strip().splitlines()
        assert output[-1] == "20"  # First remaining value


class TestGeneratorFromRange:
    """Test generator_from_range command."""
    
    def test_generator_from_range_simple(self):
        """Test basic range generator."""
        code = '''generator_from_range gen 0 5
generator_next gen v d
print v
generator_next gen v d
print v'''
        output = run(code).strip().splitlines()
        assert output[-2] == "0"
        assert output[-1] == "1"
    
    def test_generator_from_range_with_step(self):
        """Test range generator with step."""
        code = '''generator_from_range gen 0 10 2
generator_to_array gen result
array_get result 0 v0
array_get result 2 v2
print v0
print v2'''
        output = run(code).strip().splitlines()
        assert output[-2] == "0"
        assert output[-1] == "4"
    
    def test_generator_from_range_negative_step(self):
        """Test range generator with negative step."""
        code = '''generator_from_range gen 10 0 -2
generator_next gen v d
print v
generator_next gen v d
print v'''
        output = run(code).strip().splitlines()
        assert output[-2] == "10"
        assert output[-1] == "8"


class TestGeneratorTake:
    """Test generator_take command."""
    
    def test_generator_take(self):
        """Test taking n values from generator."""
        code = '''generator_from_range gen 0 100
generator_take gen 3 result
array_get result 0 v0
array_get result 2 v2
print v0
print v2'''
        output = run(code).strip().splitlines()
        assert output[-2] == "0"
        assert output[-1] == "2"
    
    def test_generator_take_less_than_available(self):
        """Test taking when fewer values available."""
        code = '''array_create src 2
array_set src 0 1
array_set src 1 2
generator_create gen src
generator_take gen 5 result
array_get result 0 v0
array_get result 1 v1
print v0
print v1'''
        output = run(code).strip().splitlines()
        assert output[-2] == "1"
        assert output[-1] == "2"


class TestAssert:
    """Test assert command (Todo 17)."""
    
    def test_assert_equal_pass(self):
        """Test assert with equal values passes."""
        code = '''set x 5
assert x == 5 "x should be 5"
print "passed"'''
        output = run(code).strip()
        assert "passed" in output
        assert "AssertionError" not in output
    
    def test_assert_equal_fail(self):
        """Test assert with unequal values fails."""
        code = '''set x 5
assert x == 10 "x should be 10"'''
        output = run(code).strip()
        assert "AssertionError" in output
        assert "x should be 10" in output
    
    def test_assert_greater_than(self):
        """Test assert with greater than."""
        code = '''set x 10
assert x > 5 "x must be > 5"
print "ok"'''
        output = run(code).strip()
        assert "ok" in output
    
    def test_assert_less_than_fail(self):
        """Test assert less than fails."""
        code = '''set x 10
assert x < 5 "x must be < 5"'''
        output = run(code).strip()
        assert "AssertionError" in output
    
    def test_assert_not_equal(self):
        """Test assert not equal."""
        code = '''set x 5
assert x != 10 "x must not be 10"
print "ok"'''
        output = run(code).strip()
        assert "ok" in output
    
    def test_assert_with_variables(self):
        """Test assert comparing two variables."""
        code = '''set x 5
set y 5
assert x == y "x and y should be equal"
print "equal"'''
        output = run(code).strip()
        assert "equal" in output
    
    def test_assert_string(self):
        """Test assert with strings."""
        code = '''str_create msg "hello"
assert msg == "hello" "message check"
print "string ok"'''
        output = run(code).strip()
        assert "string ok" in output


class TestTypeOf:
    """Test type_of command (Todo 18)."""
    
    def test_type_of_number(self):
        """Test type_of for numeric variable."""
        code = '''set x 42
type_of x result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "number"
    
    def test_type_of_string(self):
        """Test type_of for string."""
        code = '''str_create msg "hello"
type_of msg result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "string"
    
    def test_type_of_array(self):
        """Test type_of for array."""
        code = '''array_create arr 5
type_of arr result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "array"
    
    def test_type_of_dict(self):
        """Test type_of for dictionary."""
        code = '''dict_create d
type_of d result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "dict"
    
    def test_type_of_undefined(self):
        """Test type_of for undefined name."""
        code = '''type_of nonexistent result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "undefined"


class TestIsNumber:
    """Test is_number command."""
    
    def test_is_number_true(self):
        """Test is_number returns 1 for number."""
        code = '''set x 42
is_number x result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"
    
    def test_is_number_false(self):
        """Test is_number returns 0 for non-number."""
        code = '''str_create msg "hello"
is_number msg result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "0"


class TestIsString:
    """Test is_string command."""
    
    def test_is_string_true(self):
        """Test is_string returns 1 for string."""
        code = '''str_create msg "hello"
is_string msg result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"
    
    def test_is_string_false(self):
        """Test is_string returns 0 for non-string."""
        code = '''set x 42
is_string x result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "0"


class TestIsArray:
    """Test is_array command."""
    
    def test_is_array_true(self):
        """Test is_array returns 1 for array."""
        code = '''array_create arr 5
is_array arr result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"
    
    def test_is_array_false(self):
        """Test is_array returns 0 for non-array."""
        code = '''set x 42
is_array x result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "0"


class TestIsDict:
    """Test is_dict command."""
    
    def test_is_dict_true(self):
        """Test is_dict returns 1 for dictionary."""
        code = '''dict_create d
is_dict d result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"
    
    def test_is_dict_false(self):
        """Test is_dict returns 0 for non-dict."""
        code = '''set x 42
is_dict x result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "0"


class TestIsSet:
    """Test is_set command."""
    
    def test_is_set_true(self):
        """Test is_set returns 1 for set."""
        code = '''set_create s
is_set s result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"
    
    def test_is_set_false(self):
        """Test is_set returns 0 for non-set."""
        code = '''set x 42
is_set x result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "0"


class TestIsGenerator:
    """Test is_generator command."""
    
    def test_is_generator_true(self):
        """Test is_generator returns 1 for generator."""
        code = '''array_create arr 3
generator_create gen arr
is_generator gen result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"
    
    def test_is_generator_false(self):
        """Test is_generator returns 0 for non-generator."""
        code = '''set x 42
is_generator x result
print result'''
        output = run(code).strip().splitlines()
        assert output[-1] == "0"


class TestIntegration:
    """Integration tests combining features."""
    
    def test_generator_with_type_check(self):
        """Test using generator with type checking."""
        code = '''array_create nums 3
array_set nums 0 1
array_set nums 1 2
array_set nums 2 3
generator_create gen nums
type_of gen result
is_generator gen is_gen
print is_gen'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"
    
    def test_assert_with_generator_values(self):
        """Test asserting on generator values."""
        code = '''generator_from_range gen 0 5
generator_next gen val done
assert val == 0 "first value should be 0"
generator_next gen val done
assert val == 1 "second value should be 1"
print "assertions passed"'''
        output = run(code).strip()
        assert "assertions passed" in output
    
    def test_generator_loop_pattern(self):
        """Test common generator iteration pattern."""
        code = '''array_create nums 3
array_set nums 0 10
array_set nums 1 20
array_set nums 2 30
generator_create gen nums
set sum 0
set done 0
while done == 0
    generator_next gen val done
    if done == 0
        add sum val
    end
end
print sum'''
        output = run(code).strip().splitlines()
        assert output[-1] == "60"  # 10 + 20 + 30
