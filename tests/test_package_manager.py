"""
Tests for TechLang Package Manager (tlpm)
"""

import os
import sys
import json
import pytest
import shutil
import tempfile
from pathlib import Path

from techlang.package_manager import (
    PackageManager, 
    PackageInfo, 
    ProjectManifest,
    LockFile,
    LockEntry,
    MANIFEST_FILENAME,
    LOCKFILE_FILENAME,
    get_global_packages_dir,
    get_project_packages_dir,
)
from techlang.imports import get_package_search_paths
from techlang.interpreter import run


class TestPackageInfo:
    """Test PackageInfo dataclass."""
    
    def test_package_info_defaults(self):
        info = PackageInfo(name="test")
        assert info.name == "test"
        assert info.version == "1.0.0"
        assert info.main == "__init__.tl"
    
    def test_package_info_to_dict(self):
        info = PackageInfo(name="mypackage", version="2.0.0", description="A test")
        data = info.to_dict()
        assert data["name"] == "mypackage"
        assert data["version"] == "2.0.0"
        assert data["description"] == "A test"
    
    def test_package_info_from_dict(self):
        data = {"name": "loaded", "version": "3.0.0", "author": "Test User"}
        info = PackageInfo.from_dict(data)
        assert info.name == "loaded"
        assert info.version == "3.0.0"
        assert info.author == "Test User"


class TestProjectManifest:
    """Test ProjectManifest dataclass."""
    
    def test_manifest_defaults(self):
        manifest = ProjectManifest(name="myproject")
        assert manifest.name == "myproject"
        assert manifest.version == "1.0.0"
        assert manifest.main == "main.tl"
        assert manifest.dependencies == {}
    
    def test_manifest_save_and_load(self, tmp_path):
        manifest = ProjectManifest(
            name="testproject",
            version="1.2.3",
            dependencies={"utils": "1.0.0"}
        )
        
        manifest_path = tmp_path / MANIFEST_FILENAME
        manifest.save(manifest_path)
        
        loaded = ProjectManifest.load(manifest_path)
        assert loaded.name == "testproject"
        assert loaded.version == "1.2.3"
        assert loaded.dependencies == {"utils": "1.0.0"}


class TestPackageManager:
    """Test PackageManager operations."""
    
    def test_init_creates_manifest(self, tmp_path):
        os.chdir(tmp_path)
        pm = PackageManager(project_dir=tmp_path)
        pm.init(name="testproject", interactive=False)
        
        manifest_path = tmp_path / MANIFEST_FILENAME
        assert manifest_path.exists()
        
        manifest = ProjectManifest.load(manifest_path)
        assert manifest.name == "testproject"
    
    def test_init_creates_tl_packages_dir(self, tmp_path):
        os.chdir(tmp_path)
        pm = PackageManager(project_dir=tmp_path)
        pm.init(name="testproject", interactive=False)
        
        packages_dir = tmp_path / "tl_packages"
        assert packages_dir.exists()
    
    def test_init_creates_main_file(self, tmp_path):
        os.chdir(tmp_path)
        pm = PackageManager(project_dir=tmp_path)
        pm.init(name="testproject", interactive=False)
        
        main_path = tmp_path / "main.tl"
        assert main_path.exists()
    
    def test_install_from_local(self, tmp_path):
        # Create source package
        source_pkg = tmp_path / "mylib"
        source_pkg.mkdir()
        (source_pkg / "__init__.tl").write_text('def greet do\n    print "Hello"\nend\nexport greet\n')
        (source_pkg / MANIFEST_FILENAME).write_text(json.dumps({
            "name": "mylib",
            "version": "1.0.0"
        }))
        
        # Create project
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        os.chdir(project_dir)
        
        pm = PackageManager(project_dir=project_dir)
        pm.init(name="myproject", interactive=False)
        
        # Install package
        success = pm.install(str(source_pkg), save=False)
        assert success
        
        # Check installed
        installed_path = project_dir / "tl_packages" / "mylib"
        assert installed_path.exists()
        assert (installed_path / "__init__.tl").exists()
    
    def test_uninstall_removes_package(self, tmp_path):
        # Create and install package
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        os.chdir(project_dir)
        
        pm = PackageManager(project_dir=project_dir)
        pm.init(name="myproject", interactive=False)
        
        # Manually create a package
        pkg_dir = project_dir / "tl_packages" / "testpkg"
        pkg_dir.mkdir(parents=True)
        (pkg_dir / "__init__.tl").write_text("# test package\n")
        
        # Uninstall
        success = pm.uninstall("testpkg")
        assert success
        assert not pkg_dir.exists()
    
    def test_list_packages_local(self, tmp_path):
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        os.chdir(project_dir)
        
        pm = PackageManager(project_dir=project_dir)
        pm.init(name="myproject", interactive=False)
        
        # Create packages
        pkg1 = project_dir / "tl_packages" / "pkg1"
        pkg1.mkdir(parents=True)
        (pkg1 / "__init__.tl").write_text("# pkg1\n")
        
        pkg2 = project_dir / "tl_packages" / "pkg2"
        pkg2.mkdir(parents=True)
        (pkg2 / "__init__.tl").write_text("# pkg2\n")
        
        packages = pm.list_packages()
        assert "pkg1" in packages
        assert "pkg2" in packages


class TestPackageSearchPaths:
    """Test package search path resolution."""
    
    def test_search_paths_includes_base_dir(self, tmp_path):
        paths = get_package_search_paths(str(tmp_path))
        assert str(tmp_path) in paths
    
    def test_search_paths_includes_tl_packages(self, tmp_path):
        # Create tl_packages directory
        tl_packages = tmp_path / "tl_packages"
        tl_packages.mkdir()
        
        paths = get_package_search_paths(str(tmp_path))
        assert str(tl_packages) in paths
    
    def test_search_paths_includes_stl(self, tmp_path):
        paths = get_package_search_paths(str(tmp_path))
        # At least one path should contain 'stl'
        assert any('stl' in p for p in paths)


class TestPackageImportIntegration:
    """Test that installed packages can be imported."""
    
    def test_import_from_tl_packages(self, tmp_path):
        # Create project with tl_packages
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        
        # Create package in tl_packages
        pkg_dir = project_dir / "tl_packages" / "mylib"
        pkg_dir.mkdir(parents=True)
        # TechLang syntax: def name [params]\n body\n end (NO 'do' keyword)
        init_code = "def get_value\nset result 42\nreturn result\nend\nexport get_value\n"
        (pkg_dir / "__init__.tl").write_text(init_code)
        
        # Create main file that imports the package
        # call syntax: call func [args] result_var
        main_code = "import mylib\ncall mylib.get_value val\nprint val\n"
        output = run(main_code, base_dir=str(project_dir))
        assert "42" in output
    
    def test_from_import_tl_packages(self, tmp_path):
        # Create project with tl_packages
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        
        # Create package in tl_packages
        pkg_dir = project_dir / "tl_packages" / "utils"
        pkg_dir.mkdir(parents=True)
        # TechLang function with parameter
        init_code = "def add_ten n\nadd n 10\nreturn n\nend\nexport add_ten\n"
        (pkg_dir / "__init__.tl").write_text(init_code)
        
        # Create main file that uses from...import
        main_code = "from utils import add_ten\nset x 5\ncall add_ten x result\nprint result\n"
        output = run(main_code, base_dir=str(project_dir))
        assert "15" in output
    
    def test_import_nested_package(self, tmp_path):
        # Create project with nested package structure
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        
        # Create nested package
        pkg_dir = project_dir / "tl_packages" / "mylib"
        pkg_dir.mkdir(parents=True)
        (pkg_dir / "__init__.tl").write_text("# mylib main\n")
        
        sub_dir = pkg_dir / "mathutils"  # Renamed to avoid conflict with built-in 'math'
        sub_dir.mkdir()
        sub_code = "def double n\nmul n 2\nreturn n\nend\nexport double\n"
        (sub_dir / "__init__.tl").write_text(sub_code)
        
        # Import nested module
        main_code = "from mylib import mathutils\nset x 7\ncall mathutils.double x result\nprint result\n"
        output = run(main_code, base_dir=str(project_dir))
        assert "14" in output
        assert "14" in output


class TestManifestScripts:
    """Test running scripts from manifest."""
    
    def test_run_script(self, tmp_path):
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        os.chdir(project_dir)
        
        # Create manifest with scripts
        manifest = ProjectManifest(
            name="myproject",
            scripts={"echo": "echo hello"}
        )
        manifest.save(project_dir / MANIFEST_FILENAME)
        
        pm = PackageManager(project_dir=project_dir)
        exit_code = pm.run_script("echo")
        assert exit_code == 0
    
    def test_run_nonexistent_script(self, tmp_path):
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        os.chdir(project_dir)
        
        manifest = ProjectManifest(name="myproject", scripts={})
        manifest.save(project_dir / MANIFEST_FILENAME)
        
        pm = PackageManager(project_dir=project_dir)
        exit_code = pm.run_script("nonexistent")
        assert exit_code == 1


class TestPackageLink:
    """Test linking packages for development."""
    
    def test_link_creates_symlink(self, tmp_path):
        # Create package to link
        pkg_dir = tmp_path / "mypackage"
        pkg_dir.mkdir()
        (pkg_dir / MANIFEST_FILENAME).write_text(json.dumps({"name": "mypackage"}))
        (pkg_dir / "__init__.tl").write_text("# my package\n")
        
        pm = PackageManager(project_dir=pkg_dir)
        
        # Link requires global dir to exist
        pm.global_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            success = pm.link()
            if success:  # May fail on Windows without admin rights
                link_path = pm.global_dir / "mypackage"
                assert link_path.exists()
        except OSError:
            pytest.skip("Symlinks require elevated permissions on Windows")


class TestLockFile:
    """Test lock file functionality."""
    
    def test_lock_entry_creation(self):
        entry = LockEntry(
            name="mylib",
            version="1.0.0",
            resolved="./mylib",
            integrity="sha256-abcd1234"
        )
        assert entry.name == "mylib"
        assert entry.version == "1.0.0"
        assert entry.resolved == "./mylib"
        assert entry.integrity == "sha256-abcd1234"
    
    def test_lock_entry_to_dict(self):
        entry = LockEntry(name="test", version="2.0.0", resolved="https://git.example.com/test.git")
        data = entry.to_dict()
        assert data["name"] == "test"
        assert data["version"] == "2.0.0"
        assert data["resolved"] == "https://git.example.com/test.git"
    
    def test_lock_file_save_and_load(self, tmp_path):
        lockfile = LockFile()
        lockfile.packages["mylib"] = LockEntry(
            name="mylib",
            version="1.0.0",
            resolved="./mylib",
            integrity="sha256-test"
        )
        
        lock_path = tmp_path / LOCKFILE_FILENAME
        lockfile.save(lock_path)
        
        loaded = LockFile.load(lock_path)
        assert "mylib" in loaded.packages
        assert loaded.packages["mylib"].version == "1.0.0"
        assert loaded.packages["mylib"].integrity == "sha256-test"
    
    def test_install_creates_lockfile(self, tmp_path):
        # Create source package
        source_pkg = tmp_path / "testlib"
        source_pkg.mkdir()
        (source_pkg / "__init__.tl").write_text('def hello do\n    print "Hi"\nend\nexport hello\n')
        (source_pkg / MANIFEST_FILENAME).write_text(json.dumps({
            "name": "testlib",
            "version": "1.0.0"
        }))
        
        # Create project
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        os.chdir(project_dir)
        
        pm = PackageManager(project_dir=project_dir)
        pm.init(name="myproject", interactive=False)
        
        # Install package
        pm.install(str(source_pkg), save=False)
        
        # Check lockfile was created
        lock_path = project_dir / LOCKFILE_FILENAME
        assert lock_path.exists()
        
        lockfile = LockFile.load(lock_path)
        assert "testlib" in lockfile.packages
        assert lockfile.packages["testlib"].version == "1.0.0"
    
    def test_uninstall_removes_from_lockfile(self, tmp_path):
        # Create project with lockfile
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        os.chdir(project_dir)
        
        pm = PackageManager(project_dir=project_dir)
        pm.init(name="myproject", interactive=False)
        
        # Create lockfile with entry
        lockfile = LockFile()
        lockfile.packages["testpkg"] = LockEntry(
            name="testpkg",
            version="1.0.0",
            resolved="./testpkg"
        )
        lockfile.save(project_dir / LOCKFILE_FILENAME)
        
        # Create the package to uninstall
        pkg_dir = project_dir / "tl_packages" / "testpkg"
        pkg_dir.mkdir(parents=True)
        (pkg_dir / "__init__.tl").write_text("# test\n")
        
        # Uninstall
        pm.uninstall("testpkg")
        
        # Check lockfile was updated
        updated_lockfile = LockFile.load(project_dir / LOCKFILE_FILENAME)
        assert "testpkg" not in updated_lockfile.packages


class TestWildcardImport:
    """Test wildcard imports (from module import *)."""
    
    def test_import_star_with_all(self, tmp_path):
        # Create module with __all__
        module_dir = tmp_path / "mymodule"
        module_dir.mkdir()
        (module_dir / "__init__.tl").write_text('''
array_create __all__ 0
array_push __all__ "public_func"

def public_func
    print "public"
end
export public_func

def private_func
    print "private"
end
''')
        
        # Create main file
        main_code = '''
from mymodule import *
call public_func
'''
        (tmp_path / "main.tl").write_text(main_code)
        
        result = run(main_code, base_dir=str(tmp_path))
        assert "public" in result
    
    def test_import_star_exports_variables(self, tmp_path):
        # Create module with __all__ including variables
        module_dir = tmp_path / "varmodule"
        module_dir.mkdir()
        (module_dir / "__init__.tl").write_text('''
array_create __all__ 0
array_push __all__ "VERSION"
array_push __all__ "greet"

set VERSION 42

def greet
    print "Hello"
end
export greet
''')
        
        main_code = '''
from varmodule import *
print VERSION
'''
        
        result = run(main_code, base_dir=str(tmp_path))
        assert "42" in result


class TestRelativeImport:
    """Test relative imports (from . import x)."""
    
    def test_relative_import_sibling(self, tmp_path):
        # Create package with submodules
        pkg_dir = tmp_path / "mypkg"
        pkg_dir.mkdir()
        
        (pkg_dir / "__init__.tl").write_text('''
def pkg_main
    print "main"
end
export pkg_main
''')
        
        (pkg_dir / "utils.tl").write_text('''
def helper
    print "helper"
end
export helper
''')
        
        # Create a submodule that uses relative import
        (pkg_dir / "sub.tl").write_text('''
from .utils import helper

def use_helper
    call helper
end
export use_helper
''')
        
        # Test importing from top level
        main_code = '''
from mypkg.sub import use_helper
call use_helper
'''
        
        result = run(main_code, base_dir=str(tmp_path))
        assert "helper" in result


class TestUpdateAndOutdated:
    """Test update and outdated commands."""
    
    def test_update_local_package_no_op(self, tmp_path, capsys):
        # Create project
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        os.chdir(project_dir)
        
        pm = PackageManager(project_dir=project_dir)
        pm.init(name="myproject", interactive=False)
        
        # Create a local package
        pkg_dir = project_dir / "tl_packages" / "localpkg"
        pkg_dir.mkdir(parents=True)
        (pkg_dir / "__init__.tl").write_text("# local\n")
        (pkg_dir / MANIFEST_FILENAME).write_text(json.dumps({
            "name": "localpkg",
            "version": "1.0.0"
        }))
        
        # Update should say it's a local package
        pm.update("localpkg")
        
        captured = capsys.readouterr()
        assert "local package" in captured.out.lower() or "up to date" in captured.out.lower()
    
    def test_outdated_shows_packages(self, tmp_path, capsys):
        # Create project with packages
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        os.chdir(project_dir)
        
        pm = PackageManager(project_dir=project_dir)
        pm.init(name="myproject", interactive=False)
        
        # Create a package
        pkg_dir = project_dir / "tl_packages" / "testpkg"
        pkg_dir.mkdir(parents=True)
        (pkg_dir / "__init__.tl").write_text("# test\n")
        (pkg_dir / MANIFEST_FILENAME).write_text(json.dumps({
            "name": "testpkg",
            "version": "1.0.0"
        }))
        
        # Check outdated
        result = pm.outdated()
        
        captured = capsys.readouterr()
        assert "testpkg" in captured.out
        assert "1.0.0" in captured.out


class TestSearch:
    """Test package search functionality."""
    
    def test_search_local_packages(self, tmp_path, capsys):
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        os.chdir(project_dir)
        
        pm = PackageManager(project_dir=project_dir)
        pm.init(name="myproject", interactive=False)
        
        # Create some packages
        pkg1 = project_dir / "tl_packages" / "my-utils"
        pkg1.mkdir(parents=True)
        (pkg1 / "__init__.tl").write_text("# utils\n")
        (pkg1 / MANIFEST_FILENAME).write_text(json.dumps({
            "name": "my-utils",
            "version": "1.0.0",
            "description": "Utility functions"
        }))
        
        pkg2 = project_dir / "tl_packages" / "my-helpers"
        pkg2.mkdir(parents=True)
        (pkg2 / "__init__.tl").write_text("# helpers\n")
        
        # Search for "my"
        results = pm.search("my", source="local")
        
        assert len(results) == 2
        names = [r["name"] for r in results]
        assert "my-utils" in names
        assert "my-helpers" in names
    
    def test_search_stl_modules(self, tmp_path, capsys):
        pm = PackageManager(project_dir=tmp_path)
        
        # Search for "math" in stl
        results = pm.search("math", source="stl")
        
        # Should find the math module
        names = [r["name"] for r in results]
        assert "math" in names
    
    def test_search_no_results(self, tmp_path, capsys):
        pm = PackageManager(project_dir=tmp_path)
        
        results = pm.search("nonexistent-package-xyz", source="local")
        
        captured = capsys.readouterr()
        assert "No packages found" in captured.out
        assert len(results) == 0


class TestCreate:
    """Test package creation with templates."""
    
    def test_create_basic_template(self, tmp_path):
        os.chdir(tmp_path)
        pm = PackageManager(project_dir=tmp_path)
        
        success = pm.create(name="mylib", template="basic", interactive=False)
        
        assert success
        pkg_dir = tmp_path / "mylib"
        assert pkg_dir.exists()
        assert (pkg_dir / "__init__.tl").exists()
        assert (pkg_dir / MANIFEST_FILENAME).exists()
        assert (pkg_dir / "README.md").exists()
        
        # Check manifest
        manifest_data = json.loads((pkg_dir / MANIFEST_FILENAME).read_text())
        assert manifest_data["name"] == "mylib"
    
    def test_create_library_template(self, tmp_path):
        os.chdir(tmp_path)
        pm = PackageManager(project_dir=tmp_path)
        
        success = pm.create(name="myutils", template="library", interactive=False)
        
        assert success
        pkg_dir = tmp_path / "myutils"
        assert (pkg_dir / "__init__.tl").exists()
        assert (pkg_dir / "core.tl").exists()
        assert (pkg_dir / "utils.tl").exists()
        assert (pkg_dir / "tests" / "__init__.tl").exists()
    
    def test_create_cli_template(self, tmp_path):
        os.chdir(tmp_path)
        pm = PackageManager(project_dir=tmp_path)
        
        success = pm.create(name="mycli", template="cli", interactive=False)
        
        assert success
        pkg_dir = tmp_path / "mycli"
        assert (pkg_dir / "__init__.tl").exists()
        assert (pkg_dir / "cli.tl").exists()
    
    def test_create_web_template(self, tmp_path):
        os.chdir(tmp_path)
        pm = PackageManager(project_dir=tmp_path)
        
        success = pm.create(name="myapi", template="web", interactive=False)
        
        assert success
        pkg_dir = tmp_path / "myapi"
        assert (pkg_dir / "__init__.tl").exists()
        assert (pkg_dir / "server.tl").exists()
        assert (pkg_dir / "routes.tl").exists()
    
    def test_create_fails_on_existing_nonempty_dir(self, tmp_path):
        # Create existing directory with content
        pkg_dir = tmp_path / "existing"
        pkg_dir.mkdir()
        (pkg_dir / "somefile.txt").write_text("content")
        
        pm = PackageManager(project_dir=tmp_path)
        success = pm.create(name="existing", template="basic", interactive=False)
        
        assert not success
    
    def test_list_templates(self, tmp_path, capsys):
        pm = PackageManager(project_dir=tmp_path)
        pm.list_templates()
        
        captured = capsys.readouterr()
        assert "basic" in captured.out
        assert "library" in captured.out
        assert "cli" in captured.out
        assert "web" in captured.out
