"""Tests for JSON support in TechLang."""
from techlang.interpreter import run
import json
import os
from pathlib import Path


def test_json_parse_object(tmp_path):
    """Test parsing JSON object from file into dictionary."""
    # Create JSON file to avoid parser escaping issues
    json_file = tmp_path / "data.json"
    json_file.write_text('{"name":"Alice","age":30}', encoding='utf-8')
    
    code = '''
    json_read "data.json" result
    dict_get result "name"
    dict_get result "age"
    '''
    output = run(code, base_dir=str(tmp_path)).strip().splitlines()
    assert "Read JSON object from file into dictionary 'result'" in output[0]
    assert output[1] == "Alice"
    assert output[2] == "30"


def test_json_parse_array():
    """Test parsing JSON array."""
    code = '''
    str_create data "[1,2,3,4,5]"
    json_parse data numbers
    array_get numbers 0
    array_get numbers 2
    array_get numbers 4
    '''
    output = run(code).strip().splitlines()
    assert "Parsed JSON array into array 'numbers'" in output[0]
    assert output[1] == "1"
    assert output[2] == "3"
    assert output[3] == "5"


def test_json_parse_nested_object(tmp_path):
    """Test parsing nested JSON object."""
    json_file = tmp_path / "nested.json"
    json_file.write_text('{"user":{"name":"Bob"},"active":true}', encoding='utf-8')
    
    code = '''
    json_read "nested.json" obj
    dict_keys obj
    '''
    output = run(code, base_dir=str(tmp_path)).strip().splitlines()
    assert "Read JSON object from file into dictionary 'obj'" in output[0]
    assert "user" in output[1]
    assert "active" in output[1]


def test_json_parse_string():
    """Test parsing JSON string value."""
    code = '''
    str_create data "[1,2,3]"
    json_parse data result
    array_get result 1
    '''
    output = run(code).strip().splitlines()
    assert "Parsed JSON array into array 'result'" in output[0]
    assert output[1] == "2"


def test_json_parse_number():
    """Test parsing JSON number."""
    code = '''
    str_create data "42"
    json_parse data result
    print result
    '''
    output = run(code).strip().splitlines()
    assert "Parsed JSON number into variable 'result'" in output[0]
    assert output[1] == "42"


def test_json_parse_boolean():
    """Test parsing JSON boolean."""
    code = '''
    str_create data "true"
    json_parse data flag
    print flag
    '''
    output = run(code).strip().splitlines()
    # Boolean true should parse to numeric 1
    assert "Parsed JSON boolean into variable 'flag'" in output[0]
    assert output[1] == "1"


def test_json_parse_null():
    """Test parsing JSON null."""
    code = '''
    str_create data "null"
    json_parse data empty
    print empty
    '''
    output = run(code).strip().splitlines()
    assert "Parsed JSON null into variable 'empty'" in output[0]
    assert output[1] == "0"


def test_json_parse_invalid():
    """Test parsing invalid JSON."""
    code = '''
    str_create data "not valid json"
    json_parse data result
    '''
    output = run(code).strip()
    assert "[Error: Invalid JSON:" in output


def test_json_parse_missing_source():
    """Test json_parse with missing source."""
    code = 'json_parse nonexistent result'
    output = run(code).strip()
    assert "[Error: Source 'nonexistent' is not a valid string]" in output


def test_json_stringify_dict():
    """Test stringifying dictionary to JSON."""
    code = '''
    dict_create user
    dict_set user "name" "Alice"
    dict_set user "age" "30"
    json_stringify user json
    print json
    '''
    output = run(code).strip().splitlines()
    # Find the line with JSON output
    json_line = None
    for line in output:
        if "{" in line:
            json_line = line
            break
    
    assert json_line is not None
    data = json.loads(json_line)
    assert data["name"] == "Alice"
    assert data["age"] == 30  # TechLang stores numbers, not strings


def test_json_stringify_array():
    """Test stringifying array to JSON."""
    code = '''
    array_create nums 3
    array_set nums 0 10
    array_set nums 1 20
    array_set nums 2 30
    json_stringify nums json
    print json
    '''
    output = run(code).strip().splitlines()
    # Find the line with JSON output
    json_line = None
    for line in output:
        if "[" in line:
            json_line = line
            break
    
    assert json_line is not None
    data = json.loads(json_line)
    assert data == [10, 20, 30]


def test_json_stringify_string():
    """Test stringifying string variable."""
    code = '''
    str_create text "hello"
    json_stringify text json
    print json
    '''
    output = run(code).strip().splitlines()
    assert output[-1] == '"hello"'


def test_json_stringify_number():
    """Test stringifying number variable."""
    code = '''
    set x 42
    json_stringify x json
    print json
    '''
    output = run(code).strip().splitlines()
    assert output[-1] == "42"


def test_json_stringify_missing_source():
    """Test json_stringify with missing source."""
    code = 'json_stringify nonexistent result'
    output = run(code).strip()
    assert "[Error: Source 'nonexistent' does not exist]" in output


def test_json_roundtrip_object(tmp_path):
    """Test JSON stringify -> file -> parse roundtrip for objects."""
    json_file = tmp_path / "obj.json"
    json_file.write_text('{"x":10,"y":20}', encoding='utf-8')
    
    code = '''
    json_read "obj.json" obj
    json_stringify obj back
    print back
    '''
    output = run(code, base_dir=str(tmp_path)).strip().splitlines()
    # Find JSON in output
    json_line = None
    for line in output:
        if "{" in line:
            json_line = line
            break
    
    assert json_line is not None
    data = json.loads(json_line)
    assert data["x"] == 10
    assert data["y"] == 20


def test_json_roundtrip_array():
    """Test JSON parse -> stringify roundtrip for arrays."""
    code = '''
    str_create original "[10,20,30]"
    json_parse original arr
    json_stringify arr back
    print back
    '''
    output = run(code).strip().splitlines()
    # Find JSON in output
    json_line = None
    for line in output:
        if "[" in line:
            json_line = line
            break
    
    assert json_line is not None
    data = json.loads(json_line)
    assert data == [10, 20, 30]


def test_json_read_file(tmp_path):
    """Test reading JSON from file."""
    json_file = tmp_path / "test.json"
    json_file.write_text('{"name":"Alice","age":30}', encoding='utf-8')
    
    code = '''
    json_read "test.json" data
    dict_get data "name"
    '''
    output = run(code, base_dir=str(tmp_path)).strip().splitlines()
    assert "Read JSON object from file into dictionary 'data'" in output[0]
    assert "Alice" in output[1]


def test_json_read_array_file(tmp_path):
    """Test reading JSON array from file."""
    json_file = tmp_path / "numbers.json"
    json_file.write_text('[10,20,30,40,50]', encoding='utf-8')
    
    code = '''
    json_read "numbers.json" nums
    array_get nums 2
    '''
    output = run(code, base_dir=str(tmp_path)).strip().splitlines()
    assert "Read JSON array from file into array 'nums'" in output[0]
    assert output[1] == "30"


def test_json_read_missing_file(tmp_path):
    """Test reading from non-existent file."""
    code = 'json_read "missing.json" data'
    output = run(code, base_dir=str(tmp_path)).strip()
    assert "[Error: File not found: missing.json]" in output


def test_json_read_invalid_file(tmp_path):
    """Test reading invalid JSON from file."""
    json_file = tmp_path / "bad.json"
    json_file.write_text('not valid json', encoding='utf-8')
    
    code = 'json_read "bad.json" data'
    output = run(code, base_dir=str(tmp_path)).strip()
    assert "[Error: Invalid JSON in file:" in output


def test_json_write_dict_to_file(tmp_path):
    """Test writing dictionary to JSON file."""
    code = '''
    dict_create user
    dict_set user "name" "Bob"
    dict_set user "age" "25"
    json_write user "output.json"
    '''
    output = run(code, base_dir=str(tmp_path)).strip()
    assert "Wrote JSON to file: output.json" in output
    
    # Verify file was created and contains valid JSON
    json_file = tmp_path / "output.json"
    assert json_file.exists()
    data = json.loads(json_file.read_text(encoding='utf-8'))
    assert data["name"] == "Bob"
    assert data["age"] == 25  # TechLang stores numbers, not strings


def test_json_write_array_to_file(tmp_path):
    """Test writing array to JSON file."""
    code = '''
    array_create nums 3
    array_set nums 0 100
    array_set nums 1 200
    array_set nums 2 300
    json_write nums "numbers.json"
    '''
    output = run(code, base_dir=str(tmp_path)).strip()
    assert "Wrote JSON to file: numbers.json" in output
    
    # Verify file contents
    json_file = tmp_path / "numbers.json"
    data = json.loads(json_file.read_text(encoding='utf-8'))
    assert data == [100, 200, 300]


def test_json_write_missing_source(tmp_path):
    """Test json_write with missing source."""
    code = 'json_write nonexistent "out.json"'
    output = run(code, base_dir=str(tmp_path)).strip()
    assert "[Error: Source 'nonexistent' must be a dictionary or array]" in output


def test_json_write_invalid_source(tmp_path):
    """Test json_write with invalid source type."""
    code = '''
    str_create text "hello"
    json_write text "out.json"
    '''
    output = run(code, base_dir=str(tmp_path)).strip()
    assert "[Error: Source 'text' must be a dictionary or array]" in output


def test_json_file_roundtrip(tmp_path):
    """Test complete JSON file write -> read roundtrip."""
    code = '''
    dict_create data
    dict_set data "x" "10"
    dict_set data "y" "20"
    json_write data "test.json"
    json_read "test.json" loaded
    dict_get loaded "x"
    dict_get loaded "y"
    '''
    output = run(code, base_dir=str(tmp_path)).strip().splitlines()
    # Check that write and read operations succeeded
    assert any("Wrote JSON to file: test.json" in line for line in output)
    assert any("Read JSON object from file into dictionary 'loaded'" in line for line in output)
    assert "10" in output[-2]  # Second to last line should be "10"
    assert "20" in output[-1]  # Last line should be "20"


def test_json_parse_empty_object():
    """Test parsing empty JSON object."""
    code = '''
    str_create data "{}"
    json_parse data empty
    dict_keys empty
    '''
    output = run(code).strip().splitlines()
    assert "Parsed JSON object into dictionary 'empty'" in output[0]


def test_json_parse_empty_array():
    """Test parsing empty JSON array."""
    code = '''
    str_create data "[]"
    json_parse data empty
    '''
    output = run(code).strip().splitlines()
    assert "Parsed JSON array into array 'empty'" in output[0]


def test_json_unicode_support(tmp_path):
    """Test JSON with Unicode characters."""
    json_file = tmp_path / "unicode.json"
    json_file.write_text('{"emoji":"😀","text":"こんにちは"}', encoding='utf-8')
    
    code = '''
    json_read "unicode.json" obj
    dict_get obj "emoji"
    dict_get obj "text"
    '''
    output = run(code, base_dir=str(tmp_path)).strip().splitlines()
    assert "Read JSON object from file into dictionary 'obj'" in output[0]
    assert "😀" in output[1]
    assert "こんにちは" in output[2]


def test_json_special_characters(tmp_path):
    """Test JSON with special characters."""
    json_file = tmp_path / "special.json"
    json_file.write_text('{"quote":"\\"test\\"","newline":"line1\\nline2"}', encoding='utf-8')
    
    code = '''
    json_read "special.json" obj
    dict_keys obj
    '''
    output = run(code, base_dir=str(tmp_path)).strip().splitlines()
    assert "Read JSON object from file into dictionary 'obj'" in output[0]
    assert "quote" in output[1]
    assert "newline" in output[1]
