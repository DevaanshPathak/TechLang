"""
Tests for String Methods
"""

import pytest
from techlang.interpreter import run


class TestStrJoin:
    """Test str_join command"""
    
    def test_str_join(self):
        """Test str_join array elements"""
        code = """
        array_create words
        array_push words "hello"
        array_push words "world"
        array_push words "test"
        str_join words "-" result
        print result
        """
        assert run(code).strip() == "hello-world-test"


class TestStrZfill:
    """Test str_zfill command"""
    
    def test_str_zfill(self):
        """Test str_zfill zero-padding"""
        code = """
        str_create num "42"
        str_zfill num 5 padded
        print padded
        """
        assert run(code).strip() == "00042"


class TestStrCenter:
    """Test str_center command"""
    
    def test_str_center(self):
        """Test str_center padding"""
        code = """
        str_create text "hi"
        str_center text 6 centered
        str_length centered len
        print len
        """
        # Check length instead of content (since strip removes padding)
        assert run(code).strip() == "6"


class TestStrJustify:
    """Test str_ljust and str_rjust commands"""
    
    def test_str_ljust(self):
        """Test str_ljust left justify"""
        code = """
        str_create text "hi"
        str_ljust text 5 left
        str_length left len
        print len
        """
        assert run(code).strip() == "5"
    
    def test_str_rjust(self):
        """Test str_rjust right justify"""
        code = """
        str_create text "hi"
        str_rjust text 5 right
        str_length right len
        print len
        """
        # Check length instead of content
        assert run(code).strip() == "5"


class TestStrCase:
    """Test case manipulation commands"""
    
    def test_str_title(self):
        """Test str_title title case"""
        code = """
        str_create text "hello world"
        str_title text titled
        print titled
        """
        assert run(code).strip() == "Hello World"
    
    def test_str_capitalize(self):
        """Test str_capitalize first letter"""
        code = """
        str_create text "hello world"
        str_capitalize text cap
        print cap
        """
        assert run(code).strip() == "Hello world"
    
    def test_str_swapcase(self):
        """Test str_swapcase swap upper/lower"""
        code = """
        str_create text "Hello World"
        str_swapcase text swapped
        print swapped
        """
        assert run(code).strip() == "hELLO wORLD"


class TestStrChecks:
    """Test string check commands"""
    
    def test_str_isupper(self):
        """Test str_isupper check uppercase"""
        code = """
        str_create text "HELLO"
        str_isupper text result
        print result
        """
        assert run(code).strip() == "1"
    
    def test_str_islower(self):
        """Test str_islower check lowercase"""
        code = """
        str_create text "hello"
        str_islower text result
        print result
        """
        assert run(code).strip() == "1"
    
    def test_str_isspace(self):
        """Test str_isspace check whitespace"""
        code = """
        str_create text "   "
        str_isspace text result
        print result
        """
        assert run(code).strip() == "1"


class TestStrStrip:
    """Test strip commands"""
    
    def test_str_lstrip(self):
        """Test str_lstrip left strip"""
        code = """
        str_create text "   hello"
        str_lstrip text stripped
        print stripped
        """
        assert run(code).strip() == "hello"
    
    def test_str_rstrip(self):
        """Test str_rstrip right strip"""
        code = """
        str_create text "hello   "
        str_rstrip text stripped
        str_length stripped len
        print len
        """
        assert run(code).strip() == "5"
    
    def test_str_strip_chars(self):
        """Test str_strip_chars specific chars"""
        code = """
        str_create text "xxhelloxx"
        str_strip_chars text "x" stripped
        print stripped
        """
        assert run(code).strip() == "hello"


class TestStringMethodsIntegration:
    """Integration tests for string methods"""
    
    def test_string_and_array_methods(self):
        """Test combining string and array methods"""
        code = """
        array_create names
        array_push names "alice"
        array_push names "bob"
        array_push names "charlie"
        str_create sep ", "
        str_join names sep result
        str_title result titled
        print titled
        """
        assert run(code).strip() == "Alice, Bob, Charlie"
