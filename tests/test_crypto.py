"""
Tests for crypto/encoding commands: base64, md5, sha256, sha512, uuid, hex
"""
import pytest
import re
from techlang.interpreter import run


class TestBase64:
    """Tests for base64 encoding/decoding"""

    def test_base64_encode_simple(self):
        code = '''
str_create text "hello"
base64_encode text result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "aGVsbG8="

    def test_base64_encode_with_spaces(self):
        code = '''
str_create text "hello world"
base64_encode text result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "aGVsbG8gd29ybGQ="

    def test_base64_decode_simple(self):
        code = '''
str_create encoded "aGVsbG8="
base64_decode encoded result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "hello"

    def test_base64_roundtrip(self):
        code = '''
str_create original "TechLang is awesome!"
base64_encode original encoded
base64_decode encoded decoded
print decoded
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "TechLang is awesome!"

    def test_base64_decode_invalid(self):
        code = '''
str_create bad "not-valid-base64!!!"
base64_decode bad result
'''
        output = run(code).strip()
        assert "Error" in output


class TestMD5:
    """Tests for MD5 hashing"""

    def test_md5_simple(self):
        code = '''
str_create text "hello"
md5 text result
print result
'''
        output = run(code).strip().splitlines()
        # MD5 of "hello" is 5d41402abc4b2a76b9719d911017c592
        assert output[-1] == "5d41402abc4b2a76b9719d911017c592"

    def test_md5_empty_string(self):
        code = '''
str_create text ""
md5 text result
print result
'''
        output = run(code).strip().splitlines()
        # MD5 of "" is d41d8cd98f00b204e9800998ecf8427e
        assert output[-1] == "d41d8cd98f00b204e9800998ecf8427e"

    def test_md5_length(self):
        code = '''
str_create text "test string"
md5 text result
str_length result len
print len
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "32"  # MD5 is always 32 hex chars


class TestSHA256:
    """Tests for SHA256 hashing"""

    def test_sha256_simple(self):
        code = '''
str_create text "hello"
sha256 text result
print result
'''
        output = run(code).strip().splitlines()
        # SHA256 of "hello"
        assert output[-1] == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

    def test_sha256_length(self):
        code = '''
str_create text "test"
sha256 text result
str_length result len
print len
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "64"  # SHA256 is always 64 hex chars


class TestSHA512:
    """Tests for SHA512 hashing"""

    def test_sha512_simple(self):
        code = '''
str_create text "hello"
sha512 text result
str_length result len
print len
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "128"  # SHA512 is always 128 hex chars

    def test_sha512_different_from_sha256(self):
        code = '''
str_create text "test"
sha256 text hash256
sha512 text hash512
str_length hash256 len256
str_length hash512 len512
print len256
print len512
'''
        output = run(code).strip().splitlines()
        assert output[-2] == "64"
        assert output[-1] == "128"


class TestUUID:
    """Tests for UUID generation"""

    def test_uuid_format(self):
        code = '''
uuid result
print result
'''
        output = run(code).strip().splitlines()
        # UUID format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        assert re.match(uuid_pattern, output[-1])

    def test_uuid_unique(self):
        code = '''
uuid id1
uuid id2
str_create comparison "different"
if id1 == id2
    str_create comparison "same"
end
print comparison
'''
        # UUIDs should be unique (virtually always)
        output = run(code).strip().splitlines()
        assert output[-1] == "different"

    def test_uuid_length(self):
        code = '''
uuid result
str_length result len
print len
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "36"  # UUID is 36 chars with dashes


class TestHex:
    """Tests for hex encoding/decoding"""

    def test_hex_encode_simple(self):
        code = '''
str_create text "hi"
hex_encode text result
print result
'''
        output = run(code).strip().splitlines()
        # "hi" = 0x68 0x69 = "6869"
        assert output[-1] == "6869"

    def test_hex_encode_hello(self):
        code = '''
str_create text "hello"
hex_encode text result
print result
'''
        output = run(code).strip().splitlines()
        # "hello" = 68656c6c6f
        assert output[-1] == "68656c6c6f"

    def test_hex_decode_simple(self):
        code = '''
str_create encoded "6869"
hex_decode encoded result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "hi"

    def test_hex_roundtrip(self):
        code = '''
str_create original "TechLang"
hex_encode original encoded
hex_decode encoded decoded
print decoded
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "TechLang"

    def test_hex_decode_invalid(self):
        code = '''
str_create bad "not-hex!"
hex_decode bad result
'''
        output = run(code).strip()
        assert "Error" in output


class TestCryptoIntegration:
    """Integration tests combining crypto commands"""

    def test_password_hashing(self):
        """Simulate simple password hashing"""
        code = '''
str_create password "secret123"
str_create salt "randomsalt"
str_concat password salt
sha256 password hashed
str_length hashed len
print len
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "64"

    def test_encode_chain(self):
        """Test encoding chain: text -> hex -> base64"""
        code = '''
str_create text "hi"
hex_encode text hexed
base64_encode hexed b64
print b64
'''
        output = run(code).strip().splitlines()
        # "hi" -> "6869" -> base64("6869") = "Njg2OQ=="
        assert output[-1] == "Njg2OQ=="

    def test_hash_comparison(self):
        """Compare two hashes"""
        code = '''
str_create text1 "hello"
str_create text2 "hello"
md5 text1 hash1
md5 text2 hash2
set same 0
if hash1 == hash2
    set same 1
end
print same
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "1"

    def test_unique_ids_for_records(self):
        """Generate unique IDs for multiple records"""
        code = '''
uuid id1
uuid id2
uuid id3
str_length id1 len
print len
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "36"
