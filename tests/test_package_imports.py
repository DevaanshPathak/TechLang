"""
Tests for Python-like package/module import system in TechLang.

This tests:
- import module (file-based modules)
- import module as alias
- import module.submodule (dot notation)
- from module import func (selective import)
- from module import func as alias (import with alias)
- from module import * (star import)
- Folder-based packages with __init__.tl
- from package import submodule
"""

import os
import pytest
from techlang.interpreter import run


def create_file(base_dir, relative_path, content):
    """Helper to create a file in the test directory"""
    full_path = os.path.join(base_dir, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    return full_path


# ============================================================================
# Basic import tests
# ============================================================================

def test_import_module_file(tmp_path):
    """Test basic import of a .tl file"""
    create_file(str(tmp_path), "helper.tl", """
        def greet
            print "Hello"
        end
        export greet
    """)
    
    code = """
        import helper
        call helper.greet
    """
    output = run(code, base_dir=str(tmp_path)).strip()
    assert output == "Hello"


def test_import_module_as_alias(tmp_path):
    """Test import with alias: import module as alias"""
    create_file(str(tmp_path), "helper.tl", """
        def greet
            print "Hi there!"
        end
        export greet
    """)
    
    code = """
        import helper as h
        call h.greet
    """
    output = run(code, base_dir=str(tmp_path)).strip()
    assert output == "Hi there!"


def test_import_nested_module(tmp_path):
    """Test import with dot notation: import utils.helpers"""
    create_file(str(tmp_path), "utils/helpers.tl", """
        def say_hello
            print "Hello from nested!"
        end
        export say_hello
    """)
    
    code = """
        import utils.helpers
        call utils.helpers.say_hello
    """
    output = run(code, base_dir=str(tmp_path)).strip()
    assert output == "Hello from nested!"


# ============================================================================
# Package (folder with __init__.tl) tests
# ============================================================================

def test_import_package_with_init(tmp_path):
    """Test importing a folder package with __init__.tl"""
    create_file(str(tmp_path), "mypackage/__init__.tl", """
        def package_func
            print "From package init!"
        end
        export package_func
    """)
    
    code = """
        import mypackage
        call mypackage.package_func
    """
    output = run(code, base_dir=str(tmp_path)).strip()
    assert output == "From package init!"


def test_import_subpackage(tmp_path):
    """Test importing a subpackage: import mypackage.subpkg"""
    create_file(str(tmp_path), "mypackage/__init__.tl", """
        # Main package
    """)
    create_file(str(tmp_path), "mypackage/subpkg/__init__.tl", """
        def sub_func
            print "From subpackage!"
        end
        export sub_func
    """)
    
    code = """
        import mypackage.subpkg
        call mypackage.subpkg.sub_func
    """
    output = run(code, base_dir=str(tmp_path)).strip()
    assert output == "From subpackage!"


# ============================================================================
# from...import tests
# ============================================================================

def test_from_import_function(tmp_path):
    """Test: from module import func"""
    create_file(str(tmp_path), "mathlib.tl", """
        def add_two x
            add x 2
            return x
        end
        export add_two
        
        def double x
            mul x 2
            return x
        end
        export double
    """)
    
    code = """
        from mathlib import add_two
        set n 5
        call add_two n answer
        print answer
    """
    output = run(code, base_dir=str(tmp_path)).strip()
    assert output == "7"


def test_from_import_with_alias(tmp_path):
    """Test: from module import func as alias"""
    create_file(str(tmp_path), "mathlib.tl", """
        def add_two x
            add x 2
            return x
        end
        export add_two
    """)
    
    code = """
        from mathlib import add_two as plus2
        set n 10
        call plus2 n answer
        print answer
    """
    output = run(code, base_dir=str(tmp_path)).strip()
    assert output == "12"


def test_from_import_multiple(tmp_path):
    """Test: from module import func1, func2"""
    create_file(str(tmp_path), "ops.tl", """
        def inc x
            add x 1
            return x
        end
        export inc
        
        def dec x
            sub x 1
            return x
        end
        export dec
    """)
    
    code = """
        from ops import inc dec
        set a 5
        set b 10
        call inc a a_out
        call dec b b_out
        print a_out
        print b_out
    """
    output = run(code, base_dir=str(tmp_path)).strip().splitlines()
    assert output == ["6", "9"]


def test_from_import_star(tmp_path):
    """Test: from module import *"""
    create_file(str(tmp_path), "allops.tl", """
        def func_a
            print "A"
        end
        export func_a
        
        def func_b
            print "B"
        end
        export func_b
        
        def private_func
            print "PRIVATE"
        end
        # Not exported
    """)
    
    code = """
        from allops import *
        call func_a
        call func_b
    """
    output = run(code, base_dir=str(tmp_path)).strip().splitlines()
    assert output == ["A", "B"]


def test_from_package_import_submodule(tmp_path):
    """Test: from package import submodule"""
    create_file(str(tmp_path), "mypkg/__init__.tl", """
        # Package init
    """)
    create_file(str(tmp_path), "mypkg/utils.tl", """
        def helper
            print "helper func"
        end
        export helper
    """)
    
    code = """
        from mypkg import utils
        call utils.helper
    """
    output = run(code, base_dir=str(tmp_path)).strip()
    assert output == "helper func"


def test_from_package_import_subpackage(tmp_path):
    """Test: from package import subpackage (folder)"""
    create_file(str(tmp_path), "mypkg/__init__.tl", """
        # Main package
    """)
    create_file(str(tmp_path), "mypkg/utils/__init__.tl", """
        def subpkg_func
            print "subpackage works!"
        end
        export subpkg_func
    """)
    
    code = """
        from mypkg import utils
        call utils.subpkg_func
    """
    output = run(code, base_dir=str(tmp_path)).strip()
    assert output == "subpackage works!"


def test_from_import_submodule_with_alias(tmp_path):
    """Test: from package import submodule as alias"""
    create_file(str(tmp_path), "pkg/__init__.tl", "")
    create_file(str(tmp_path), "pkg/tools.tl", """
        def tool_func
            print "tool works"
        end
        export tool_func
    """)
    
    code = """
        from pkg import tools as t
        call t.tool_func
    """
    output = run(code, base_dir=str(tmp_path)).strip()
    assert output == "tool works"


# ============================================================================
# Edge cases and error handling
# ============================================================================

def test_import_nonexistent_module(tmp_path):
    """Test error when importing non-existent module"""
    code = """
        import nonexistent_module
    """
    output = run(code, base_dir=str(tmp_path)).strip()
    # Should not crash, should show error
    assert "not found" in output.lower() or "error" in output.lower()


def test_from_import_nonexistent_name(tmp_path):
    """Test error when importing non-existent name from module"""
    create_file(str(tmp_path), "exists.tl", """
        def real_func
            print "real"
        end
        export real_func
    """)
    
    code = """
        from exists import fake_func
    """
    output = run(code, base_dir=str(tmp_path)).strip()
    assert "not found" in output.lower() or "error" in output.lower()


def test_from_import_private_function(tmp_path):
    """Test that private (non-exported) functions cannot be imported"""
    create_file(str(tmp_path), "private.tl", """
        def public_func
            print "public"
        end
        export public_func
        
        def private_func
            print "private"
        end
        # NOT exported
    """)
    
    code = """
        from private import private_func
    """
    output = run(code, base_dir=str(tmp_path)).strip()
    # Should show error about not exported
    assert "error" in output.lower() or "not found" in output.lower() or "not exported" in output.lower()


def test_module_prefers_package_over_file(tmp_path):
    """When both module.tl and module/__init__.tl exist, prefer package"""
    create_file(str(tmp_path), "conflict.tl", """
        def from_file
            print "from file"
        end
        export from_file
    """)
    create_file(str(tmp_path), "conflict/__init__.tl", """
        def from_package
            print "from package"
        end
        export from_package
    """)
    
    code = """
        import conflict
        call conflict.from_package
    """
    output = run(code, base_dir=str(tmp_path)).strip()
    assert output == "from package"


def test_deeply_nested_import(tmp_path):
    """Test deeply nested package: a.b.c.d"""
    create_file(str(tmp_path), "a/b/c/d.tl", """
        def deep_func
            print "very deep!"
        end
        export deep_func
    """)
    
    code = """
        import a.b.c.d
        call a.b.c.d.deep_func
    """
    output = run(code, base_dir=str(tmp_path)).strip()
    assert output == "very deep!"


def test_import_does_not_duplicate(tmp_path):
    """Test that importing twice doesn't duplicate execution"""
    create_file(str(tmp_path), "counter.tl", """
        set counter 0
        add counter 1
        print counter
        
        def get_count
            print counter
        end
        export get_count
    """)
    
    code = """
        set counter 0
        import counter
        import counter
        call counter.get_count
    """
    output = run(code, base_dir=str(tmp_path)).strip().splitlines()
    # Module should only execute once
    assert output.count("1") == 2  # First print from init, second from get_count


# ============================================================================
# Variables and data sharing
# ============================================================================

def test_from_import_variable(tmp_path):
    """Test importing variables from module"""
    create_file(str(tmp_path), "constants.tl", """
        set PI 314
        set E 271
    """)
    
    # Note: Variables aren't exported by default in TechLang modules
    # but they're shared through bridge_state
    code = """
        import constants
        print PI
    """
    output = run(code, base_dir=str(tmp_path)).strip()
    assert output == "314"
