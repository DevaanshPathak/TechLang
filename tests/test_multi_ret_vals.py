"""
Tests for Multiple Return Values (Tuple Unpacking)
"""

import pytest
from techlang.interpreter import run


class TestMultipleReturns:
    """Test returning multiple values from functions."""
    
    def test_return_multi_basic(self):
        """Test returning two values."""
        code = """
def divmod_fn a b do
    set q a
    div q b
    set r a
    math_mod r b
    return_multi q r
end
call divmod_fn 17 5 quotient remainder
print quotient
print remainder
"""
        output = run(code).strip().splitlines()
        # divmod(17, 5) = (3, 2)
        assert "3" in output
        assert "2" in output
    
    def test_return_multi_three_values(self):
        """Test returning three values."""
        code = """
def get_stats do
    return_multi 10 20 30
end
call get_stats a b c
print a
print b
print c
"""
        output = run(code).strip().splitlines()
        assert "10" in output
        assert "20" in output
        assert "30" in output


class TestPackUnpack:
    """Test pack and unpack operations."""
    
    def test_pack_basic(self):
        """Test packing values into array."""
        code = """
set x 10
set y 20
set z 30
pack result x y z
"""
        output = run(code).strip()
        # pack should work without errors
        assert "[Error:" not in output
    
    def test_unpack_basic(self):
        """Test unpacking array into variables."""
        code = """
array_create arr 3
array_set arr 0 100
array_set arr 1 200
array_set arr 2 300
unpack arr a b c
print a
print b
print c
"""
        output = run(code).strip().splitlines()
        assert output[-3] == "100"
        assert output[-2] == "200"
        assert output[-1] == "300"
    
    def test_pack_unpack_roundtrip(self):
        """Test pack followed by unpack."""
        code = """
set x 5
set y 10
pack mydata x y
unpack mydata p q
print p
print q
"""
        output = run(code).strip().splitlines()
        assert output[-2] == "5"
        assert output[-1] == "10"


class TestIntegration:
    """Integration tests for multiple return values."""
    
    def test_pack_basics(self):
        """Test basic pack functionality."""
        code = """
set a 5
set b 15
pack myresult a b
unpack myresult x y
print x
print y
"""
        output = run(code).strip().splitlines()
        assert "5" in output
        assert "15" in output


class TestEdgeCases:
    """Test edge cases for pack/unpack."""
    
    def test_unpack_partial(self):
        """Test unpack with fewer variables than array elements."""
        code = """
array_create arr 5
array_set arr 0 1
array_set arr 1 2
array_set arr 2 3
array_set arr 3 4
array_set arr 4 5
unpack arr first second
print first
print second
"""
        output = run(code).strip().splitlines()
        assert output[-2] == "1"
        assert output[-1] == "2"
