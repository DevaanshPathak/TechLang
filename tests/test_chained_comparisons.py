"""
Tests for Chained Comparisons (if_chain)
"""

import pytest
from techlang.interpreter import run


class TestChainedComparisons:
    """Chained Comparisons (if_chain)"""
    
    def test_if_chain_basic_range(self):
        """Test basic range check: 0 < x < 10"""
        code = """
        set x 5
        if_chain 0 < x < 10 do
            print "in range"
        end
        """
        assert run(code).strip() == "in range"
    
    def test_if_chain_not_in_range(self):
        """Test when value is out of range"""
        code = """
        set x 15
        if_chain 0 < x < 10 do
            print "in range"
        end
        print "done"
        """
        assert run(code).strip() == "done"
    
    def test_if_chain_triple_comparison(self):
        """Test triple comparison: a < b < c < d"""
        code = """
        set a 1
        set b 2
        set c 3
        if_chain a < b < c do
            print "ascending"
        end
        """
        assert run(code).strip() == "ascending"
    
    def test_if_chain_mixed_operators(self):
        """Test with mixed comparison operators"""
        code = """
        set x 5
        if_chain 0 <= x <= 10 do
            print "in range"
        end
        """
        assert run(code).strip() == "in range"
    
    def test_if_chain_equals(self):
        """Test chained equality"""
        code = """
        set a 5
        set b 5
        if_chain 5 == a == b do
            print "all equal"
        end
        """
        assert run(code).strip() == "all equal"
    
    def test_if_chain_literals(self):
        """Test with literal values"""
        code = """
        if_chain 1 < 2 < 3 do
            print "ascending"
        end
        """
        assert run(code).strip() == "ascending"
    
    def test_if_chain_fail_middle(self):
        """Test when middle comparison fails"""
        code = """
        set x 10
        if_chain 0 < x < 5 do
            print "in range"
        end
        print "out"
        """
        assert run(code).strip() == "out"


class TestChainedComparisonsIntegration:
    """Integration tests for chained comparisons"""
    
    def test_chained_comparison_with_loop(self):
        """Test if_chain inside a loop"""
        code = """
        set count 0
        set lower 5
        set upper 15
        set idx 0
        loop 20
            if_chain lower <= idx < upper do
                add count 1
            end
            add idx 1
        end
        print count
        """
        assert run(code).strip() == "10"
