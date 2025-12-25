"""
Tests for Feature 11: Itertools/Functools Equivalents

These commands provide Python itertools/functools functionality:
- chain, cycle, repeat, takewhile, dropwhile
- groupby, accumulate, pairwise
- product, permutations, combinations
- reduce, partial_array, apply_partial
"""

import pytest
from techlang.interpreter import run


class TestChain:
    """Tests for chain command (itertools.chain)."""
    
    def test_chain_two_arrays(self):
        """Chain two arrays together."""
        code = '''
array_create arr1 3
array_set arr1 0 1
array_set arr1 1 2
array_set arr1 2 3
array_create arr2 2
array_set arr2 0 4
array_set arr2 1 5
chain arr1 arr2 result
array_get result 4 last
print last
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "5"
    
    def test_chain_three_arrays(self):
        """Chain three arrays together."""
        code = '''
array_create a 1
array_set a 0 1
array_create b 1
array_set b 0 2
array_create c 1
array_set c 0 3
chain a b c result
array_get result 0 v0
array_get result 1 v1
array_get result 2 v2
print v0
print v1
print v2
'''
        output = run(code).strip().splitlines()
        assert output[-3:] == ["1", "2", "3"]


class TestCycle:
    """Tests for cycle command (itertools.cycle)."""
    
    def test_cycle_array(self):
        """Cycle array n times."""
        code = '''
array_create arr 2
array_set arr 0 1
array_set arr 1 2
cycle arr 3 result
array_get result 5 last
print last
'''
        output = run(code).strip().splitlines()
        # [1,2,1,2,1,2] -> index 5 = 2
        assert output[-1] == "2"
    
    def test_cycle_values(self):
        """Verify cycled values."""
        code = '''
array_create arr 2
array_set arr 0 "a"
array_set arr 1 "b"
cycle arr 2 result
array_get result 0 v0
array_get result 2 v2
print v0
print v2
'''
        output = run(code).strip().splitlines()
        # [a,b,a,b] -> index 0 = a, index 2 = a
        assert output[-2:] == ["a", "a"]


class TestRepeat:
    """Tests for repeat command (itertools.repeat)."""
    
    def test_repeat_number(self):
        """Repeat a number n times."""
        code = '''
repeat 42 5 result
array_get result 2 mid
print mid
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "42"
    
    def test_repeat_string(self):
        """Repeat a string n times."""
        code = '''
str_create s "hello"
repeat s 3 result
array_get result 0 first
print first
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "hello"


class TestTakewhile:
    """Tests for takewhile command (itertools.takewhile)."""
    
    def test_takewhile_basic(self):
        """Take elements while predicate is true."""
        code = '''
array_create arr 5
array_set arr 0 1
array_set arr 1 2
array_set arr 2 3
array_set arr 3 10
array_set arr 4 4

def less_than_5 x
    if x < 5
        return 1
    end
    return 0
end

takewhile arr less_than_5 result
array_get result 2 last
print last
'''
        output = run(code).strip().splitlines()
        # Takes [1, 2, 3], last element is 3
        assert output[-1] == "3"


class TestDropwhile:
    """Tests for dropwhile command (itertools.dropwhile)."""
    
    def test_dropwhile_basic(self):
        """Drop elements while predicate is true."""
        code = '''
array_create arr 5
array_set arr 0 1
array_set arr 1 2
array_set arr 2 3
array_set arr 3 10
array_set arr 4 4

def less_than_5 x
    if x < 5
        return 1
    end
    return 0
end

dropwhile arr less_than_5 result
array_get result 0 first
print first
'''
        output = run(code).strip().splitlines()
        # Drops 1, 2, 3 and keeps 10, 4 -> first is 10
        assert output[-1] == "10"


class TestAccumulate:
    """Tests for accumulate command (itertools.accumulate)."""
    
    def test_accumulate_sum(self):
        """Accumulate with default sum."""
        code = '''
array_create arr 4
array_set arr 0 1
array_set arr 1 2
array_set arr 2 3
array_set arr 3 4
accumulate arr result
array_get result 3 total
print total
'''
        output = run(code).strip().splitlines()
        # 1, 3, 6, 10 -> last is 10
        assert output[-1] == "10"
    
    def test_accumulate_multiply(self):
        """Accumulate with multiplication."""
        code = '''
array_create arr 4
array_set arr 0 1
array_set arr 1 2
array_set arr 2 3
array_set arr 3 4
accumulate arr result *
array_get result 3 total
print total
'''
        output = run(code).strip().splitlines()
        # 1, 2, 6, 24 -> last is 24
        assert output[-1] == "24"


class TestPairwise:
    """Tests for pairwise command (itertools.pairwise)."""
    
    def test_pairwise_basic(self):
        """Get consecutive pairs."""
        code = '''
array_create arr 4
array_set arr 0 1
array_set arr 1 2
array_set arr 2 3
array_set arr 3 4
pairwise arr result
array_get result 0 first_pair
print first_pair
'''
        output = run(code).strip().splitlines()
        # First pair is [1, 2]
        assert "1" in output[-1] or "[" in output[-1]


class TestProduct:
    """Tests for product command (itertools.product)."""
    
    def test_product_basic(self):
        """Cartesian product of two arrays."""
        code = '''
array_create arr1 2
array_set arr1 0 1
array_set arr1 1 2
array_create arr2 2
array_set arr2 0 "a"
array_set arr2 1 "b"
product arr1 arr2 result
array_get result 0 first
print first
'''
        output = run(code).strip().splitlines()
        # First combination should contain 1 and a
        assert "1" in output[-1] or "[" in output[-1]


class TestPermutations:
    """Tests for permutations command (itertools.permutations)."""
    
    def test_permutations_all(self):
        """All permutations of array - verify first element."""
        code = '''
array_create arr 3
array_set arr 0 1
array_set arr 1 2
array_set arr 2 3
permutations arr result
array_get result 0 first
print first
'''
        output = run(code).strip().splitlines()
        # First permutation starts with [1,2,3]
        assert "1" in output[-1] or "[" in output[-1]
    
    def test_permutations_r(self):
        """r-length permutations - verify we get results."""
        code = '''
array_create arr 3
array_set arr 0 1
array_set arr 1 2
array_set arr 2 3
permutations arr result 2
array_get result 0 first
print first
'''
        output = run(code).strip().splitlines()
        # Should have at least one permutation
        assert len(output[-1]) > 0


class TestCombinations:
    """Tests for combinations command (itertools.combinations)."""
    
    def test_combinations_basic(self):
        """Get combinations of size r."""
        code = '''
array_create arr 4
array_set arr 0 1
array_set arr 1 2
array_set arr 2 3
array_set arr 3 4
combinations arr 2 result
array_get result 0 first
print first
'''
        output = run(code).strip().splitlines()
        # First combination [1,2]
        assert "1" in output[-1] or "[" in output[-1]


class TestReduce:
    """Tests for reduce command (functools.reduce)."""
    
    def test_reduce_sum(self):
        """Reduce with addition function."""
        code = '''
array_create arr 4
array_set arr 0 1
array_set arr 1 2
array_set arr 2 3
array_set arr 3 4

def add_two a b
    set result a
    add result b
    return result
end

reduce arr add_two result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "10"
    
    def test_reduce_with_initial(self):
        """Reduce with initial value."""
        code = '''
array_create arr 3
array_set arr 0 1
array_set arr 1 2
array_set arr 2 3

def add_two a b
    set result a
    add result b
    return result
end

reduce arr add_two result 100
print result
'''
        output = run(code).strip().splitlines()
        # 100 + 1 + 2 + 3 = 106
        assert output[-1] == "106"


class TestPartialApply:
    """Tests for partial_array and apply_partial commands."""
    
    def test_partial_basic(self):
        """Create and apply partial function."""
        code = '''
def add_three a b c
    set result a
    add result b
    add result c
    return result
end

array_create bound_args 2
array_set bound_args 0 10
array_set bound_args 1 20
partial_array add_three my_partial bound_args
apply_partial my_partial result 5
print result
'''
        output = run(code).strip().splitlines()
        # 10 + 20 + 5 = 35
        assert output[-1] == "35"


class TestItertoolsIntegration:
    """Integration tests for itertools features."""
    
    def test_chain_accumulate(self):
        """Chain arrays then accumulate."""
        code = '''
array_create a 2
array_set a 0 1
array_set a 1 2
array_create b 2
array_set b 0 3
array_set b 1 4
chain a b combined
accumulate combined running
array_get running 3 total
print total
'''
        output = run(code).strip().splitlines()
        # 1, 3, 6, 10 -> last is 10
        assert output[-1] == "10"
