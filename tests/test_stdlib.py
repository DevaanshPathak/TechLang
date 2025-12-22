"""
Test suite for TechLang Standard Template Library modules
Tests all STL functions: strings, math, collections, validation
"""

import sys
import pytest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from techlang.interpreter import run


def test_stl_strings_capitalize(base_dir: str):
    """Test strings.capitalize function"""
    code = """
    package use stl/strings
    str_create src "hello"
    call stl.strings.capitalize src result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "Hello"


def test_stl_strings_title_case(base_dir: str):
    """Test strings.title_case function"""
    code = """
    package use stl/strings
    str_create src "hello world test"
    call stl.strings.title_case src result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "Hello World Test"


def test_stl_strings_repeat(base_dir: str):
    """Test strings.repeat function"""
    code = """
    package use stl/strings
    str_create char "x"
    call stl.strings.repeat char 5 result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "xxxxx"


def test_stl_strings_pad_left(base_dir: str):
    """Test strings.pad_left function"""
    code = """
    package use stl/strings
    str_create num "42"
    call stl.strings.pad_left num 5 "0" result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "00042"


def test_stl_strings_pad_right(base_dir: str):
    """Test strings.pad_right function"""
    code = """
    package use stl/strings
    str_create text "hi"
    call stl.strings.pad_right text 5 "." result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "hi..."


def test_stl_strings_starts_with(base_dir: str):
    """Test strings.starts_with function"""
    code = """
    package use stl/strings
    str_create filename "report.pdf"
    call stl.strings.starts_with filename "report" result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "1"


def test_stl_strings_ends_with(base_dir: str):
    """Test strings.ends_with function"""
    code = """
    package use stl/strings
    str_create filename "report.pdf"
    call stl.strings.ends_with filename ".pdf" result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "1"


def test_stl_strings_count_char(base_dir: str):
    """Test strings.count_char function"""
    code = """
    package use stl/strings
    str_create text "banana"
    str_create search "a"
    call stl.strings.count_char text search result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "3"


def test_stl_math_min(base_dir: str):
    """Test math.min function"""
    code = """
    package use stl/math
    set x 15
    set y 42
    call stl.math.min x y result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "15"


def test_stl_math_max(base_dir: str):
    """Test math.max function"""
    code = """
    package use stl/math
    set x 15
    set y 42
    call stl.math.max x y result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "42"


def test_stl_math_abs(base_dir: str):
    """Test math.abs function"""
    code = """
    package use stl/math
    set n -25
    call stl.math.abs n result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "25"


def test_stl_math_clamp(base_dir: str):
    """Test math.clamp function"""
    code = """
    package use stl/math
    set val 150
    set min_val 0
    set max_val 100
    call stl.math.clamp val min_val max_val result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "100"


def test_stl_math_sign(base_dir: str):
    """Test math.sign function"""
    code = """
    package use stl/math
    set pos 10
    call stl.math.sign pos result1
    print result1
    set neg -5
    call stl.math.sign neg result2
    print result2
    set zero 0
    call stl.math.sign zero result3
    print result3
    """
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert output == ["1", "-1", "0"]


def test_stl_math_is_even(base_dir: str):
    """Test math.is_even function"""
    code = """
    package use stl/math
    set n 8
    call stl.math.is_even n result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "1"


def test_stl_math_is_odd(base_dir: str):
    """Test math.is_odd function"""
    code = """
    package use stl/math
    set n 7
    call stl.math.is_odd n result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "1"


def test_stl_math_sum_range(base_dir: str):
    """Test math.sum_range function"""
    code = """
    package use stl/math
    set start 1
    set end 10
    call stl.math.sum_range start end result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "55"  # 1+2+3+4+5+6+7+8+9+10 = 55


def test_stl_math_factorial(base_dir: str):
    """Test math.factorial function"""
    code = """
    package use stl/math
    set n 5
    call stl.math.factorial n result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "120"  # 5! = 120


def test_stl_math_gcd(base_dir: str):
    """Test math.gcd function"""
    code = """
    package use stl/math
    set a 48
    set b 18
    call stl.math.gcd a b result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "6"


def test_stl_math_lerp(base_dir: str):
    """Test math.lerp function"""
    code = """
    package use stl/math
    set a 0
    set b 100
    set t 50
    call stl.math.lerp a b t result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    # 0 + (100-0) * 0.5 = 50
    # But t=50 is treated as 50 (not 0.5), so result is 0 + 100*50 = 5000
    # Actually: lerp multiplies diff by t, so 100 * 50 = 5000, then 0 + 5000 = 5000
    assert output == "5000"


def test_stl_collections_array_sum(base_dir: str):
    """Test collections.array_sum function"""
    code = """
    package use stl/collections
    array_create nums
    array_push nums 5
    array_push nums 10
    array_push nums 15
    call stl.collections.array_sum nums result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "30"


def test_stl_collections_array_product(base_dir: str):
    """Test collections.array_product function"""
    code = """
    package use stl/collections
    array_create nums
    array_push nums 2
    array_push nums 3
    array_push nums 4
    call stl.collections.array_product nums result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "24"


def test_stl_collections_array_min(base_dir: str):
    """Test collections.array_min function"""
    code = """
    package use stl/collections
    array_create nums
    array_push nums 15
    array_push nums 5
    array_push nums 20
    array_push nums 10
    call stl.collections.array_min nums result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "5"


def test_stl_collections_array_max(base_dir: str):
    """Test collections.array_max function"""
    code = """
    package use stl/collections
    array_create nums
    array_push nums 15
    array_push nums 5
    array_push nums 20
    array_push nums 10
    call stl.collections.array_max nums result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "20"


def test_stl_collections_array_contains(base_dir: str):
    """Test collections.array_contains function"""
    code = """
    package use stl/collections
    array_create nums
    array_push nums 5
    array_push nums 10
    array_push nums 15
    set target 10
    call stl.collections.array_contains nums target result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "1"


def test_stl_collections_array_index_of(base_dir: str):
    """Test collections.array_index_of function"""
    code = """
    package use stl/collections
    array_create nums
    array_push nums 5
    array_push nums 10
    array_push nums 15
    set target 15
    call stl.collections.array_index_of nums target result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "2"


def test_stl_collections_array_count(base_dir: str):
    """Test collections.array_count function"""
    code = """
    package use stl/collections
    array_create nums
    array_push nums 5
    array_push nums 10
    array_push nums 15
    call stl.collections.array_count nums result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "3"


def test_stl_collections_array_fill(base_dir: str):
    """Test collections.array_fill function"""
    code = """
    package use stl/collections
    array_create nums
    call stl.collections.array_fill nums 7 3
    array_get nums 0 val0
    array_get nums 1 val1
    array_get nums 2 val2
    print val0
    print val1
    print val2
    """
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert output == ["7", "7", "7"]


def test_stl_validation_is_positive(base_dir: str):
    """Test validation.is_positive function"""
    code = """
    package use stl/validation
    set n 42
    call stl.validation.is_positive n result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "1"


def test_stl_validation_is_negative(base_dir: str):
    """Test validation.is_negative function"""
    code = """
    package use stl/validation
    set n -10
    call stl.validation.is_negative n result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "1"


def test_stl_validation_is_zero(base_dir: str):
    """Test validation.is_zero function"""
    code = """
    package use stl/validation
    set n 0
    call stl.validation.is_zero n result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "1"


def test_stl_validation_is_in_range(base_dir: str):
    """Test validation.is_in_range function"""
    code = """
    package use stl/validation
    set val 25
    set min_val 18
    set max_val 65
    call stl.validation.is_in_range val min_val max_val result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "1"


def test_stl_validation_min_length(base_dir: str):
    """Test validation.min_length function"""
    code = """
    package use stl/validation
    str_create text "hello world"
    set min_len 5
    call stl.validation.min_length text min_len result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "1"


def test_stl_validation_max_length(base_dir: str):
    """Test validation.max_length function"""
    code = """
    package use stl/validation
    str_create text "hello"
    set max_len 10
    call stl.validation.max_length text max_len result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "1"


def test_stl_validation_length_between(base_dir: str):
    """Test validation.length_between function"""
    code = """
    package use stl/validation
    str_create text "hello"
    set min_len 3
    set max_len 10
    call stl.validation.length_between text min_len max_len result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "1"


def test_stl_validation_is_email(base_dir: str):
    """Test validation.is_email function"""
    code = """
    package use stl/validation
    str_create email "user@example.com"
    call stl.validation.is_email email result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "1"


def test_stl_validation_is_url(base_dir: str):
    """Test validation.is_url function"""
    code = """
    package use stl/validation
    str_create url "https://github.com"
    call stl.validation.is_url url result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "1"


def test_stl_validation_is_numeric_string(base_dir: str):
    code = """
    package use stl/validation
    str_create s1 "123456"
    call stl.validation.is_numeric_string s1 ok1
    print ok1

    str_create s2 "12a3"
    call stl.validation.is_numeric_string s2 ok2
    print ok2
    """
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert output == ["1", "0"]


def test_stl_validation_is_alpha_string(base_dir: str):
    code = """
    package use stl/validation
    str_create s1 "AbcXYZ"
    call stl.validation.is_alpha_string s1 ok1
    print ok1

    str_create s2 "abc123"
    call stl.validation.is_alpha_string s2 ok2
    print ok2
    """
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert output == ["1", "0"]


def test_stl_validation_is_alphanumeric_string(base_dir: str):
    code = """
    package use stl/validation
    str_create s1 "abc123XYZ"
    call stl.validation.is_alphanumeric_string s1 ok1
    print ok1

    str_create s2 "abc-123"
    call stl.validation.is_alphanumeric_string s2 ok2
    print ok2
    """
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert output == ["1", "0"]


def test_stl_validation_require_all(base_dir: str):
    """Test validation.require_all function"""
    code = """
    package use stl/validation
    set c1 1
    set c2 1
    call stl.validation.require_all c1 c2 result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "1"


def test_stl_validation_require_any(base_dir: str):
    """Test validation.require_any function"""
    code = """
    package use stl/validation
    set c1 0
    set c2 1
    call stl.validation.require_any c1 c2 result
    print result
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "1"


def test_stl_combined_usage(base_dir: str):
    """Test using multiple stl modules together"""
    code = """
    package use stl/math
    package use stl/validation
    
    set x 150
    set min_val 0
    set max_val 100
    
    call stl.validation.is_in_range x min_val max_val valid
    if valid eq 0
        call stl.math.clamp x min_val max_val clamped
        set x clamped
    end
    print x
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "100"


def test_stl_multiple_calls(base_dir: str):
    """Test calling stl functions multiple times"""
    code = """
    package use stl/strings
    
    str_create src1 "hello"
    call stl.strings.capitalize src1 result1
    print result1
    
    str_create src2 "world"
    call stl.strings.capitalize src2 result2
    print result2
    """
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert output == ["Hello", "World"]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

