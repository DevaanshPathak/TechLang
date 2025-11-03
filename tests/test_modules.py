import os
from techlang.interpreter import run


def write_module(tmpdir, name, content):
    path = os.path.join(tmpdir, f"{name}.tl")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content.strip() + "\n")
    return path


def test_package_use_namespace(tmp_path):
    module_code = """
    package name helper
    def increment
        add x 1
    end
    export increment
    """
    write_module(str(tmp_path), "helper", module_code)

    program = """
    set x 2
    package use helper
    call helper.increment
    print x
    """
    output = run(program, base_dir=str(tmp_path)).strip().splitlines()
    assert output[-1] == "3"


def test_package_use_missing_function(tmp_path):
    module_code = """
    def greet
        print "hi"
    end
    """
    write_module(str(tmp_path), "helper", module_code)

    program = """
    package use helper
    call helper.wave
    """
    output = run(program, base_dir=str(tmp_path)).strip()
    assert "[Error: Module 'helper' has no function 'wave'.]" in output


def test_package_use_missing_module(tmp_path):
    program = """
    package use missing_mod
    """
    output = run(program, base_dir=str(tmp_path)).strip()
    assert "[Module Error: Module 'missing_mod' not found." in output


def test_stdlib_alias_for_stl():
    """Test that 'stdlib' works as an alias for 'stl'"""
    # Test 1: Load with stl, call with stl
    code1 = """
    package use stl/validation
    set n 5
    call stl.validation.is_positive n result
    print result
    """
    output1 = run(code1, base_dir="d:/TechLang").strip()
    assert output1 == "1"
    
    # Test 2: Load with stl, call with stdlib
    code2 = """
    package use stl/validation
    set n -3
    call stdlib.validation.is_negative n result
    print result
    """
    output2 = run(code2, base_dir="d:/TechLang").strip()
    assert output2 == "1"
    
    # Test 3: Load with stdlib, call with stl
    code3 = """
    package use stdlib/validation
    set n 0
    call stl.validation.is_zero n result
    print result
    """
    output3 = run(code3, base_dir="d:/TechLang").strip()
    assert output3 == "1"
    
    # Test 4: Test with :: separator
    code4 = """
    package use stl/validation
    set n 10
    call stl::validation::is_positive n result
    print result
    """
    output4 = run(code4, base_dir="d:/TechLang").strip()
    assert output4 == "1"
