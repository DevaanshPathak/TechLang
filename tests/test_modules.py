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
