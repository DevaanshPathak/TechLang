"""
TechLang Package Manager (tlpm)

Manages global and project-wide TechLang packages.
"""

import os
import sys
import json
import shutil
import tempfile
import subprocess
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse


# Default directories
def get_global_packages_dir() -> Path:
    """Get the global packages directory (~/.techlang/packages)."""
    home = Path.home()
    tl_dir = home / ".techlang"
    packages_dir = tl_dir / "packages"
    return packages_dir


def get_project_packages_dir(project_dir: Path = None) -> Path:
    """Get the project-local packages directory (./tl_packages)."""
    if project_dir is None:
        project_dir = Path.cwd()
    return project_dir / "tl_packages"


def get_global_config_path() -> Path:
    """Get the global config file path (~/.techlang/config.json)."""
    return Path.home() / ".techlang" / "config.json"


# Package manifest
MANIFEST_FILENAME = "tlpackage.json"


@dataclass
class PackageInfo:
    """Information about a package."""
    name: str
    version: str = "1.0.0"
    description: str = ""
    author: str = ""
    license: str = "MIT"
    main: str = "__init__.tl"  # Entry point
    dependencies: Dict[str, str] = field(default_factory=dict)
    keywords: List[str] = field(default_factory=list)
    repository: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PackageInfo':
        return cls(
            name=data.get("name", "unnamed"),
            version=data.get("version", "1.0.0"),
            description=data.get("description", ""),
            author=data.get("author", ""),
            license=data.get("license", "MIT"),
            main=data.get("main", "__init__.tl"),
            dependencies=data.get("dependencies", {}),
            keywords=data.get("keywords", []),
            repository=data.get("repository", ""),
        )


@dataclass
class ProjectManifest:
    """Project manifest (tlpackage.json)."""
    name: str
    version: str = "1.0.0"
    description: str = ""
    author: str = ""
    main: str = "main.tl"
    dependencies: Dict[str, str] = field(default_factory=dict)  # name -> version/path/url
    dev_dependencies: Dict[str, str] = field(default_factory=dict)
    scripts: Dict[str, str] = field(default_factory=dict)  # name -> command
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProjectManifest':
        return cls(
            name=data.get("name", "unnamed"),
            version=data.get("version", "1.0.0"),
            description=data.get("description", ""),
            author=data.get("author", ""),
            main=data.get("main", "main.tl"),
            dependencies=data.get("dependencies", {}),
            dev_dependencies=data.get("dev_dependencies", {}),
            scripts=data.get("scripts", {}),
        )
    
    def save(self, path: Path):
        """Save manifest to file."""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, path: Path) -> 'ProjectManifest':
        """Load manifest from file."""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)


# Lock file constants
LOCKFILE_FILENAME = "tlpackage-lock.json"


@dataclass
class LockEntry:
    """A single entry in the lock file."""
    name: str
    version: str
    resolved: str  # How it was resolved (path, git url, etc.)
    integrity: str = ""  # SHA256 hash of the package
    dependencies: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LockEntry':
        return cls(
            name=data.get("name", ""),
            version=data.get("version", ""),
            resolved=data.get("resolved", ""),
            integrity=data.get("integrity", ""),
            dependencies=data.get("dependencies", {}),
        )


@dataclass
class LockFile:
    """Lock file for reproducible builds (tlpackage-lock.json)."""
    lockfile_version: int = 1
    packages: Dict[str, LockEntry] = field(default_factory=dict)  # name -> LockEntry
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "lockfileVersion": self.lockfile_version,
            "packages": {name: entry.to_dict() for name, entry in self.packages.items()}
        }
    
    def save(self, path: Path):
        """Save lock file."""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, path: Path) -> 'LockFile':
        """Load lock file."""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        packages = {}
        for name, entry_data in data.get("packages", {}).items():
            packages[name] = LockEntry.from_dict(entry_data)
        return cls(
            lockfile_version=data.get("lockfileVersion", 1),
            packages=packages,
        )


class PackageManager:
    """TechLang Package Manager."""
    
    def __init__(self, project_dir: Path = None, verbose: bool = False):
        self.project_dir = Path(project_dir) if project_dir else Path.cwd()
        self.verbose = verbose
        self.global_dir = get_global_packages_dir()
        self.local_dir = get_project_packages_dir(self.project_dir)
        self.manifest_path = self.project_dir / MANIFEST_FILENAME
        self.lockfile_path = self.project_dir / LOCKFILE_FILENAME
        
    def log(self, message: str):
        """Print message if verbose."""
        if self.verbose:
            print(f"  {message}")
    
    def ensure_dirs(self, global_install: bool = False):
        """Ensure package directories exist."""
        if global_install:
            self.global_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.local_dir.mkdir(parents=True, exist_ok=True)
    
    # ============================================
    # INIT - Initialize a new project
    # ============================================
    
    def init(self, name: str = None, interactive: bool = True) -> bool:
        """Initialize a new TechLang project."""
        if self.manifest_path.exists():
            print(f"Project already initialized ({MANIFEST_FILENAME} exists)")
            return False
        
        # Get project info
        if name is None:
            name = self.project_dir.name
        
        if interactive:
            print("Initializing TechLang project...")
            name = input(f"  Package name ({name}): ").strip() or name
            version = input("  Version (1.0.0): ").strip() or "1.0.0"
            description = input("  Description: ").strip()
            author = input("  Author: ").strip()
            main = input("  Entry point (main.tl): ").strip() or "main.tl"
        else:
            version = "1.0.0"
            description = ""
            author = ""
            main = "main.tl"
        
        manifest = ProjectManifest(
            name=name,
            version=version,
            description=description,
            author=author,
            main=main,
            dependencies={},
            dev_dependencies={},
            scripts={
                "start": f"tl {main}",
                "test": "tl tests/test.tl"
            }
        )
        
        manifest.save(self.manifest_path)
        print(f"\n✓ Created {MANIFEST_FILENAME}")
        
        # Create directories
        self.local_dir.mkdir(exist_ok=True)
        print(f"✓ Created tl_packages/")
        
        # Create main.tl if it doesn't exist
        main_path = self.project_dir / main
        if not main_path.exists():
            main_path.write_text('# TechLang Project\nboot\nprint "Hello, TechLang!"\n')
            print(f"✓ Created {main}")
        
        # Create .gitignore entry
        gitignore_path = self.project_dir / ".gitignore"
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            if "tl_packages/" not in content:
                with open(gitignore_path, 'a') as f:
                    f.write("\n# TechLang packages\ntl_packages/\n")
                print("✓ Updated .gitignore")
        
        print(f"\nProject '{name}' initialized successfully!")
        return True
    
    # ============================================
    # INSTALL - Install packages
    # ============================================
    
    def install(self, package_spec: str = None, global_install: bool = False, 
                save: bool = True, dev: bool = False) -> bool:
        """
        Install a package.
        
        package_spec can be:
        - Package name (from registry or global)
        - Local path (./mypackage or /path/to/package)
        - Git URL (https://github.com/user/repo.git)
        - Git URL with tag (https://github.com/user/repo.git#v1.0.0)
        """
        if package_spec is None:
            # Install all dependencies from manifest
            return self.install_all(global_install)
        
        self.ensure_dirs(global_install)
        target_dir = self.global_dir if global_install else self.local_dir
        
        print(f"Installing {package_spec}...")
        
        # Determine package source
        source_type = self._detect_source_type(package_spec)
        
        if source_type == "local":
            success, pkg_info = self._install_from_local(package_spec, target_dir)
        elif source_type == "git":
            success, pkg_info = self._install_from_git(package_spec, target_dir)
        elif source_type == "global":
            # Copy from global to local
            success, pkg_info = self._install_from_global(package_spec, target_dir)
        else:
            # Try to find in global packages or stl
            success, pkg_info = self._install_from_registry(package_spec, target_dir)
        
        if not success:
            print(f"✗ Failed to install {package_spec}")
            return False
        
        # Update manifest if saving
        if save and not global_install and self.manifest_path.exists():
            manifest = ProjectManifest.load(self.manifest_path)
            dep_dict = manifest.dev_dependencies if dev else manifest.dependencies
            dep_dict[pkg_info.name] = pkg_info.version if source_type != "local" else package_spec
            manifest.save(self.manifest_path)
            self.log(f"Updated {MANIFEST_FILENAME}")
        
        # Update lock file
        if not global_install:
            self._update_lockfile(pkg_info, package_spec, source_type)
        
        print(f"✓ Installed {pkg_info.name}@{pkg_info.version}")
        return True
    
    def install_all(self, global_install: bool = False) -> bool:
        """Install all dependencies from manifest."""
        if not self.manifest_path.exists():
            print(f"No {MANIFEST_FILENAME} found. Run 'tlpm init' first.")
            return False
        
        manifest = ProjectManifest.load(self.manifest_path)
        all_deps = {**manifest.dependencies, **manifest.dev_dependencies}
        
        if not all_deps:
            print("No dependencies to install.")
            return True
        
        print(f"Installing {len(all_deps)} dependencies...")
        
        success = True
        for name, spec in all_deps.items():
            if not self.install(spec if spec.startswith(('.', '/', 'http', 'git')) else name, 
                               global_install=global_install, save=False):
                success = False
        
        return success
    
    def _detect_source_type(self, spec: str) -> str:
        """Detect the type of package source."""
        if spec.startswith(('./', '../', '/', '\\')) or (len(spec) > 2 and spec[1] == ':'):
            return "local"
        if spec.startswith(('http://', 'https://', 'git://', 'git@')):
            return "git"
        if spec.startswith("global:"):
            return "global"
        return "registry"
    
    def _install_from_local(self, path: str, target_dir: Path) -> tuple:
        """Install from a local directory."""
        source_path = Path(path).resolve()
        
        if not source_path.exists():
            print(f"  Error: Path does not exist: {path}")
            return False, None
        
        # Check for package manifest
        manifest_path = source_path / MANIFEST_FILENAME
        if manifest_path.exists():
            pkg_info = PackageInfo.from_dict(json.loads(manifest_path.read_text()))
        else:
            # Create minimal info from directory name
            pkg_info = PackageInfo(name=source_path.name)
        
        # Copy to target
        dest_path = target_dir / pkg_info.name
        if dest_path.exists():
            shutil.rmtree(dest_path)
        
        shutil.copytree(source_path, dest_path)
        self.log(f"Copied {source_path} -> {dest_path}")
        
        return True, pkg_info
    
    def _install_from_git(self, url: str, target_dir: Path) -> tuple:
        """Install from a Git repository."""
        # Parse URL and optional tag/branch
        tag = None
        if '#' in url:
            url, tag = url.rsplit('#', 1)
        
        # Extract repo name
        parsed = urlparse(url)
        repo_name = Path(parsed.path).stem
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        
        # Clone to temp directory first
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir) / repo_name
            
            try:
                cmd = ['git', 'clone', '--depth', '1']
                if tag:
                    cmd.extend(['--branch', tag])
                cmd.extend([url, str(tmp_path)])
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"  Git clone failed: {result.stderr}")
                    return False, None
            except FileNotFoundError:
                print("  Error: git is not installed or not in PATH")
                return False, None
            
            # Read package info
            manifest_path = tmp_path / MANIFEST_FILENAME
            if manifest_path.exists():
                pkg_info = PackageInfo.from_dict(json.loads(manifest_path.read_text()))
            else:
                pkg_info = PackageInfo(name=repo_name, version=tag or "latest")
            
            # Copy to target (excluding .git)
            dest_path = target_dir / pkg_info.name
            if dest_path.exists():
                shutil.rmtree(dest_path)
            
            shutil.copytree(tmp_path, dest_path, ignore=shutil.ignore_patterns('.git'))
        
        return True, pkg_info
    
    def _install_from_global(self, spec: str, target_dir: Path) -> tuple:
        """Install from global packages."""
        name = spec.replace("global:", "")
        global_path = self.global_dir / name
        
        if not global_path.exists():
            print(f"  Error: Package '{name}' not found in global packages")
            return False, None
        
        return self._install_from_local(str(global_path), target_dir)
    
    def _install_from_registry(self, name: str, target_dir: Path) -> tuple:
        """Install from package registry or global."""
        # First check if it's in global packages
        global_path = self.global_dir / name
        if global_path.exists():
            return self._install_from_local(str(global_path), target_dir)
        
        # Check if it's a built-in stl module
        stl_path = Path(__file__).parent.parent / "stl" / name
        if not stl_path.exists():
            stl_path = Path(__file__).parent.parent / "stl" / f"{name}.tl"
        
        if stl_path.exists():
            print(f"  Note: '{name}' is a built-in stl module. Use 'package use stl/{name}' instead.")
            return False, None
        
        # TODO: Add support for remote registry
        print(f"  Error: Package '{name}' not found")
        print(f"  Hint: Install from local path, git URL, or global packages")
        return False, None
    
    # ============================================
    # LOCK FILE - Reproducible builds
    # ============================================
    
    def _compute_package_hash(self, package_path: Path) -> str:
        """Compute SHA256 hash of package contents."""
        import hashlib
        h = hashlib.sha256()
        
        if package_path.is_file():
            h.update(package_path.read_bytes())
        elif package_path.is_dir():
            # Hash all .tl files sorted by name
            for tl_file in sorted(package_path.rglob("*.tl")):
                h.update(tl_file.read_bytes())
        
        return f"sha256-{h.hexdigest()[:16]}"
    
    def _update_lockfile(self, pkg_info: PackageInfo, resolved: str, source_type: str) -> None:
        """Update the lock file with a package entry."""
        # Load existing lock file or create new
        if self.lockfile_path.exists():
            lockfile = LockFile.load(self.lockfile_path)
        else:
            lockfile = LockFile()
        
        # Compute hash
        pkg_path = self.local_dir / pkg_info.name
        integrity = self._compute_package_hash(pkg_path) if pkg_path.exists() else ""
        
        # Create lock entry
        entry = LockEntry(
            name=pkg_info.name,
            version=pkg_info.version,
            resolved=resolved,
            integrity=integrity,
            dependencies=pkg_info.dependencies,
        )
        
        lockfile.packages[pkg_info.name] = entry
        lockfile.save(self.lockfile_path)
        self.log(f"Updated {LOCKFILE_FILENAME}")
    
    def _remove_from_lockfile(self, package_name: str) -> None:
        """Remove a package from the lock file."""
        if not self.lockfile_path.exists():
            return
        
        lockfile = LockFile.load(self.lockfile_path)
        if package_name in lockfile.packages:
            del lockfile.packages[package_name]
            lockfile.save(self.lockfile_path)
            self.log(f"Removed {package_name} from {LOCKFILE_FILENAME}")
    
    # ============================================
    # UPDATE - Update packages
    # ============================================
    
    def update(self, package_name: str = None, global_update: bool = False) -> bool:
        """
        Update package(s) to latest versions.
        If no package specified, updates all packages.
        """
        if package_name:
            return self._update_single(package_name, global_update)
        else:
            return self._update_all(global_update)
    
    def _update_single(self, package_name: str, global_update: bool) -> bool:
        """Update a single package."""
        target_dir = self.global_dir if global_update else self.local_dir
        package_path = target_dir / package_name
        
        if not package_path.exists():
            print(f"Package '{package_name}' is not installed")
            return False
        
        # Get current version
        old_version = self._get_package_version(package_path)
        
        # Check if it's a git repo (has a .git marker or was installed from git)
        if self.lockfile_path.exists():
            lockfile = LockFile.load(self.lockfile_path)
            entry = lockfile.packages.get(package_name)
            if entry and entry.resolved.startswith(('http://', 'https://', 'git')):
                print(f"Updating {package_name} from {entry.resolved}...")
                # Remove old and reinstall
                shutil.rmtree(package_path)
                success, pkg_info = self._install_from_git(entry.resolved, target_dir)
                if success:
                    new_version = pkg_info.version
                    if old_version != new_version:
                        print(f"✓ Updated {package_name}: {old_version} → {new_version}")
                    else:
                        print(f"✓ {package_name} is already up to date ({new_version})")
                    if not global_update:
                        self._update_lockfile(pkg_info, entry.resolved, "git")
                    return True
        
        print(f"✓ {package_name}@{old_version} is a local package (no updates available)")
        return True
    
    def _update_all(self, global_update: bool) -> bool:
        """Update all packages."""
        target_dir = self.global_dir if global_update else self.local_dir
        
        if not target_dir.exists():
            print("No packages installed")
            return True
        
        packages = [p.name for p in target_dir.iterdir() if p.is_dir()]
        if not packages:
            print("No packages installed")
            return True
        
        print(f"Checking {len(packages)} package(s) for updates...")
        for pkg_name in packages:
            self._update_single(pkg_name, global_update)
        
        return True
    
    # ============================================
    # OUTDATED - Check for outdated packages
    # ============================================
    
    def outdated(self, global_check: bool = False) -> List[Dict[str, str]]:
        """
        Check for outdated packages.
        Returns list of {name, current, latest, type} for outdated packages.
        """
        target_dir = self.global_dir if global_check else self.local_dir
        outdated_list = []
        
        if not target_dir.exists():
            print("No packages installed")
            return outdated_list
        
        packages = [p for p in target_dir.iterdir() if p.is_dir()]
        if not packages:
            print("No packages installed")
            return outdated_list
        
        print(f"Checking {len(packages)} package(s)...\n")
        
        # Table header
        print(f"{'Package':<20} {'Current':<12} {'Type':<10} {'Status'}")
        print("-" * 55)
        
        for pkg_path in packages:
            pkg_name = pkg_path.name
            current_version = self._get_package_version(pkg_path)
            pkg_type = "local"
            status = "✓ up to date"
            
            # Check lock file for source info
            if self.lockfile_path.exists():
                lockfile = LockFile.load(self.lockfile_path)
                entry = lockfile.packages.get(pkg_name)
                if entry:
                    if entry.resolved.startswith(('http://', 'https://', 'git')):
                        pkg_type = "git"
                        # Could check remote for updates (future enhancement)
                        status = "⚡ run 'tlpm update' to check"
                    elif entry.resolved.startswith(('./', '../', '/')):
                        pkg_type = "local"
                        # Check if source has changed
                        source_path = Path(entry.resolved).resolve()
                        if source_path.exists():
                            source_hash = self._compute_package_hash(source_path)
                            if source_hash != entry.integrity:
                                status = "⚠ source changed"
                                outdated_list.append({
                                    "name": pkg_name,
                                    "current": current_version,
                                    "type": pkg_type,
                                    "status": "source changed"
                                })
            
            print(f"{pkg_name:<20} {current_version:<12} {pkg_type:<10} {status}")
        
        print()
        if outdated_list:
            print(f"Found {len(outdated_list)} package(s) that may need updating.")
            print("Run 'tlpm update' to update all packages.")
        else:
            print("All packages are up to date.")
        
        return outdated_list
    
    # ============================================
    # SEARCH - Search for packages
    # ============================================
    
    def search(self, query: str, source: str = "all") -> List[Dict[str, Any]]:
        """
        Search for packages.
        
        Sources:
        - "local": Search in tl_packages
        - "global": Search in ~/.techlang/packages
        - "stl": Search in built-in standard library
        - "github": Search GitHub for TechLang packages
        - "all": Search all sources
        
        Returns list of {name, version, description, source, path/url}
        """
        results = []
        query_lower = query.lower()
        
        # Search local packages
        if source in ("local", "all"):
            results.extend(self._search_directory(self.local_dir, query_lower, "local"))
        
        # Search global packages
        if source in ("global", "all"):
            results.extend(self._search_directory(self.global_dir, query_lower, "global"))
        
        # Search stl
        if source in ("stl", "all"):
            stl_dir = Path(__file__).parent.parent / "stl"
            results.extend(self._search_directory(stl_dir, query_lower, "stl"))
        
        # Search GitHub
        if source in ("github", "all"):
            results.extend(self._search_github(query))
        
        # Print results
        if not results:
            print(f"No packages found matching '{query}'")
            return results
        
        print(f"\nFound {len(results)} package(s) matching '{query}':\n")
        print(f"{'Package':<25} {'Version':<10} {'Source':<10} {'Description'}")
        print("-" * 70)
        
        for pkg in results:
            name = pkg.get("name", "unknown")[:24]
            version = pkg.get("version", "?")[:9]
            source_type = pkg.get("source", "?")[:9]
            desc = pkg.get("description", "")[:30]
            print(f"{name:<25} {version:<10} {source_type:<10} {desc}")
        
        print()
        return results
    
    def _search_directory(self, directory: Path, query: str, source_name: str) -> List[Dict[str, Any]]:
        """Search a directory for packages matching query."""
        results = []
        
        if not directory.exists():
            return results
        
        for item in directory.iterdir():
            if item.is_dir():
                # Check folder package
                if query in item.name.lower():
                    info = self._get_package_info(item)
                    results.append({
                        "name": item.name,
                        "version": info.version if info else "unknown",
                        "description": info.description if info else "",
                        "source": source_name,
                        "path": str(item),
                    })
            elif item.suffix == ".tl":
                # Check file module
                name = item.stem
                if query in name.lower():
                    results.append({
                        "name": name,
                        "version": "1.0.0",
                        "description": f"TechLang module ({item.name})",
                        "source": source_name,
                        "path": str(item),
                    })
        
        return results
    
    def _get_package_info(self, package_dir: Path) -> Optional[PackageInfo]:
        """Get PackageInfo from a package directory."""
        manifest_path = package_dir / MANIFEST_FILENAME
        if manifest_path.exists():
            try:
                data = json.loads(manifest_path.read_text())
                return PackageInfo.from_dict(data)
            except:
                pass
        return None
    
    def _search_github(self, query: str) -> List[Dict[str, Any]]:
        """Search GitHub for TechLang packages."""
        results = []
        
        try:
            import requests
        except ImportError:
            self.log("  Note: Install 'requests' to search GitHub")
            return results
        
        try:
            # Search GitHub for repos with "techlang" topic or in query
            search_query = f"{query} language:techlang OR {query} techlang in:name,description"
            url = f"https://api.github.com/search/repositories?q={search_query}&per_page=10"
            
            headers = {"Accept": "application/vnd.github.v3+json"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                for repo in data.get("items", []):
                    # Check if it looks like a TechLang package
                    if self._looks_like_tl_package(repo):
                        results.append({
                            "name": repo["name"],
                            "version": "latest",
                            "description": (repo.get("description") or "")[:50],
                            "source": "github",
                            "url": repo["clone_url"],
                            "stars": repo.get("stargazers_count", 0),
                        })
            else:
                self.log(f"  GitHub search failed: {response.status_code}")
        except Exception as e:
            self.log(f"  GitHub search error: {e}")
        
        return results
    
    def _looks_like_tl_package(self, repo: Dict) -> bool:
        """Check if a GitHub repo looks like a TechLang package."""
        name = repo.get("name", "").lower()
        desc = (repo.get("description") or "").lower()
        topics = repo.get("topics", [])
        
        # Check for TechLang indicators
        indicators = ["techlang", "tl-", "-tl", ".tl"]
        
        for ind in indicators:
            if ind in name or ind in desc:
                return True
        
        if "techlang" in topics:
            return True
        
        return False
    
    # ============================================
    # CREATE - Scaffold new packages
    # ============================================
    
    TEMPLATES = {
        "basic": {
            "description": "Basic package with minimal structure",
            "files": {
                "__init__.tl": '''# {name} - TechLang Package
# Version: {version}

# Export public functions
# export my_function

def hello
    print "Hello from {name}!"
end
export hello
''',
                "README.md": '''# {name}

{description}

## Installation

```bash
tlpm install ./{name}
```

## Usage

```techlang
import {name}
call {name}.hello
```

## License

{license}
''',
            }
        },
        "library": {
            "description": "Library package with utils and tests",
            "files": {
                "__init__.tl": '''# {name} - TechLang Library
# Version: {version}

# Re-export from submodules
from .utils import *
from .core import *
''',
                "core.tl": '''# Core functionality for {name}

def init
    print "[{name}] Initialized"
end
export init
''',
                "utils.tl": '''# Utility functions for {name}

def log msg
    print "[{name}]"
    print msg
end
export log
''',
                "tests/__init__.tl": '''# Tests for {name}

def run_tests
    print "Running {name} tests..."
    print "✓ All tests passed"
end
export run_tests
''',
                "README.md": '''# {name}

{description}

## Installation

```bash
tlpm install ./{name}
```

## Usage

```techlang
import {name}
call {name}.init
call {name}.log "Hello"
```

## Running Tests

```techlang
import {name}.tests
call {name}.tests.run_tests
```

## License

{license}
''',
            }
        },
        "cli": {
            "description": "CLI application with argument handling",
            "files": {
                "__init__.tl": '''# {name} - TechLang CLI Application
# Version: {version}

from .cli import main
export main
''',
                "cli.tl": '''# CLI entry point for {name}

def main
    print "╔════════════════════════════╗"
    print "║  {name} v{version}  ║"
    print "╚════════════════════════════╝"
    print ""
    call show_help
end
export main

def show_help
    print "Usage: tl {name}/cli.tl [command]"
    print ""
    print "Commands:"
    print "  help     Show this help"
    print "  version  Show version"
end
export show_help
''',
                "README.md": '''# {name}

{description}

## Installation

```bash
tlpm install -g ./{name}
```

## Usage

```bash
tl {name}/cli.tl
tl {name}/cli.tl help
```

## License

{license}
''',
            }
        },
        "web": {
            "description": "Web service with HTTP handlers",
            "files": {
                "__init__.tl": '''# {name} - TechLang Web Service
# Version: {version}

from .server import start
export start
''',
                "server.tl": '''# HTTP Server for {name}

def start
    print "Starting {name} server..."
    print "Listening on http://localhost:8080"
    
    # Note: Actual server implementation would use
    # TechLang's network capabilities
    # server_start 8080 handle_request
end
export start

def handle_request path
    print "Handling request:"
    print path
end
export handle_request
''',
                "routes.tl": '''# Route handlers for {name}

def home
    str_create response "Welcome to {name}!"
    print response
end
export home

def api_status
    str_create response "{{\\"status\\": \\"ok\\", \\"service\\": \\"{name}\\"}}"
    print response
end
export api_status
''',
                "README.md": '''# {name}

{description}

## Installation

```bash
tlpm install ./{name}
```

## Usage

```techlang
import {name}
call {name}.start
```

## API Endpoints

- `GET /` - Home page
- `GET /api/status` - Service status

## License

{license}
''',
            }
        },
    }
    
    def create(self, name: str = None, template: str = "basic", 
               directory: Path = None, interactive: bool = True) -> bool:
        """
        Create a new package from a template.
        
        Templates:
        - basic: Minimal package structure
        - library: Library with utils and tests
        - cli: CLI application
        - web: Web service
        """
        # Determine output directory
        if directory is None:
            directory = self.project_dir
        
        if name is None:
            name = directory.name
        
        package_dir = directory / name if name != directory.name else directory
        
        # Check if directory exists
        if package_dir.exists() and any(package_dir.iterdir()):
            print(f"Error: Directory '{package_dir}' already exists and is not empty")
            return False
        
        # Get template
        if template not in self.TEMPLATES:
            print(f"Error: Unknown template '{template}'")
            print(f"Available templates: {', '.join(self.TEMPLATES.keys())}")
            return False
        
        tmpl = self.TEMPLATES[template]
        
        # Gather info
        if interactive:
            print(f"\nCreating new TechLang package with '{template}' template\n")
            name = input(f"  Package name ({name}): ").strip() or name
            version = input("  Version (1.0.0): ").strip() or "1.0.0"
            description = input("  Description: ").strip() or f"A TechLang {template} package"
            author = input("  Author: ").strip() or ""
            license_type = input("  License (MIT): ").strip() or "MIT"
        else:
            version = "1.0.0"
            description = f"A TechLang {template} package"
            author = ""
            license_type = "MIT"
        
        # Create directory
        package_dir.mkdir(parents=True, exist_ok=True)
        
        # Template variables
        variables = {
            "name": name,
            "version": version,
            "description": description,
            "author": author,
            "license": license_type,
        }
        
        # Create files from template
        for filename, content in tmpl["files"].items():
            file_path = package_dir / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Replace template variables
            rendered = content.format(**variables)
            file_path.write_text(rendered, encoding='utf-8')
            self.log(f"Created {filename}")
        
        # Create tlpackage.json
        manifest = PackageInfo(
            name=name,
            version=version,
            description=description,
            author=author,
            license=license_type,
            main="__init__.tl",
        )
        manifest_path = package_dir / MANIFEST_FILENAME
        with open(manifest_path, 'w') as f:
            json.dump(manifest.to_dict(), f, indent=2)
        self.log(f"Created {MANIFEST_FILENAME}")
        
        print(f"\n✓ Created package '{name}' with '{template}' template")
        print(f"  Location: {package_dir}")
        print(f"\nNext steps:")
        print(f"  cd {name}")
        print(f"  # Edit your code in __init__.tl")
        print(f"  tlpm link  # Link globally for development")
        
        return True
    
    def list_templates(self) -> None:
        """List available package templates."""
        print("\nAvailable templates:\n")
        for name, tmpl in self.TEMPLATES.items():
            print(f"  {name:<12} - {tmpl['description']}")
        print(f"\nUsage: tlpm create <name> --template <template>")
    
    # ============================================
    # UNINSTALL - Remove packages
    # ============================================
    
    def uninstall(self, package_name: str, global_uninstall: bool = False) -> bool:
        """Uninstall a package."""
        target_dir = self.global_dir if global_uninstall else self.local_dir
        package_path = target_dir / package_name
        
        if not package_path.exists():
            print(f"Package '{package_name}' is not installed")
            return False
        
        shutil.rmtree(package_path)
        print(f"✓ Uninstalled {package_name}")
        
        # Update manifest
        if not global_uninstall and self.manifest_path.exists():
            manifest = ProjectManifest.load(self.manifest_path)
            if package_name in manifest.dependencies:
                del manifest.dependencies[package_name]
                manifest.save(self.manifest_path)
            elif package_name in manifest.dev_dependencies:
                del manifest.dev_dependencies[package_name]
                manifest.save(self.manifest_path)
        
        # Remove from lock file
        if not global_uninstall:
            self._remove_from_lockfile(package_name)
        
        return True
    
    # ============================================
    # LIST - List installed packages
    # ============================================
    
    def list_packages(self, global_list: bool = False, all_list: bool = False) -> List[str]:
        """List installed packages."""
        packages = []
        
        if all_list or not global_list:
            # Local packages
            if self.local_dir.exists():
                print("Local packages (tl_packages/):")
                for item in self.local_dir.iterdir():
                    if item.is_dir():
                        version = self._get_package_version(item)
                        print(f"  • {item.name}@{version}")
                        packages.append(item.name)
                if not packages:
                    print("  (none)")
            else:
                print("Local packages: (not initialized)")
        
        if all_list or global_list:
            # Global packages
            global_packages = []
            if self.global_dir.exists():
                print("\nGlobal packages (~/.techlang/packages/):")
                for item in self.global_dir.iterdir():
                    if item.is_dir():
                        version = self._get_package_version(item)
                        print(f"  • {item.name}@{version}")
                        global_packages.append(item.name)
                if not global_packages:
                    print("  (none)")
            else:
                print("\nGlobal packages: (not initialized)")
            packages.extend(global_packages)
        
        return packages
    
    def _get_package_version(self, package_dir: Path) -> str:
        """Get version of a package."""
        manifest_path = package_dir / MANIFEST_FILENAME
        if manifest_path.exists():
            try:
                data = json.loads(manifest_path.read_text())
                return data.get("version", "unknown")
            except:
                pass
        return "unknown"
    
    # ============================================
    # INFO - Show package information
    # ============================================
    
    def info(self, package_name: str) -> Optional[PackageInfo]:
        """Show information about a package."""
        # Check local first
        local_path = self.local_dir / package_name
        if local_path.exists():
            manifest_path = local_path / MANIFEST_FILENAME
            if manifest_path.exists():
                info = PackageInfo.from_dict(json.loads(manifest_path.read_text()))
                self._print_package_info(info, "local")
                return info
        
        # Check global
        global_path = self.global_dir / package_name
        if global_path.exists():
            manifest_path = global_path / MANIFEST_FILENAME
            if manifest_path.exists():
                info = PackageInfo.from_dict(json.loads(manifest_path.read_text()))
                self._print_package_info(info, "global")
                return info
        
        print(f"Package '{package_name}' not found")
        return None
    
    def _print_package_info(self, info: PackageInfo, location: str):
        """Print package information."""
        print(f"\n{info.name}@{info.version}")
        print(f"  Location: {location}")
        if info.description:
            print(f"  Description: {info.description}")
        if info.author:
            print(f"  Author: {info.author}")
        if info.license:
            print(f"  License: {info.license}")
        if info.repository:
            print(f"  Repository: {info.repository}")
        if info.main:
            print(f"  Main: {info.main}")
        if info.dependencies:
            print(f"  Dependencies: {', '.join(info.dependencies.keys())}")
        print()
    
    # ============================================
    # RUN - Run scripts from manifest
    # ============================================
    
    def run_script(self, script_name: str) -> int:
        """Run a script from the manifest."""
        if not self.manifest_path.exists():
            print(f"No {MANIFEST_FILENAME} found. Run 'tlpm init' first.")
            return 1
        
        manifest = ProjectManifest.load(self.manifest_path)
        
        if script_name not in manifest.scripts:
            print(f"Script '{script_name}' not found in {MANIFEST_FILENAME}")
            print(f"Available scripts: {', '.join(manifest.scripts.keys())}")
            return 1
        
        command = manifest.scripts[script_name]
        print(f"> {command}")
        
        result = subprocess.run(command, shell=True, cwd=self.project_dir)
        return result.returncode
    
    # ============================================
    # LINK - Link a local package globally
    # ============================================
    
    def link(self, package_dir: Path = None) -> bool:
        """Link a local package to global packages (for development)."""
        if package_dir is None:
            package_dir = self.project_dir
        
        package_dir = Path(package_dir).resolve()
        
        # Check for manifest
        manifest_path = package_dir / MANIFEST_FILENAME
        if manifest_path.exists():
            data = json.loads(manifest_path.read_text())
            name = data.get("name", package_dir.name)
        else:
            name = package_dir.name
        
        # Create global packages dir if needed
        self.global_dir.mkdir(parents=True, exist_ok=True)
        
        # Create symlink
        link_path = self.global_dir / name
        
        if link_path.exists():
            if link_path.is_symlink():
                link_path.unlink()
            else:
                print(f"Error: {link_path} exists and is not a symlink")
                return False
        
        try:
            link_path.symlink_to(package_dir, target_is_directory=True)
            print(f"✓ Linked {name} -> {package_dir}")
            return True
        except OSError as e:
            print(f"Error creating symlink: {e}")
            print("  Hint: On Windows, run as administrator or enable Developer Mode")
            return False
    
    # ============================================
    # UNLINK - Remove a global link
    # ============================================
    
    def unlink(self, package_name: str = None) -> bool:
        """Remove a global package link."""
        if package_name is None:
            # Use current directory name
            if self.manifest_path.exists():
                data = json.loads(self.manifest_path.read_text())
                package_name = data.get("name", self.project_dir.name)
            else:
                package_name = self.project_dir.name
        
        link_path = self.global_dir / package_name
        
        if not link_path.exists():
            print(f"Package '{package_name}' is not linked globally")
            return False
        
        if link_path.is_symlink():
            link_path.unlink()
            print(f"✓ Unlinked {package_name}")
            return True
        else:
            print(f"Error: {link_path} is not a symlink")
            return False


# ============================================
# Package path resolution for interpreter
# ============================================

def get_package_search_paths(project_dir: Path = None) -> List[Path]:
    """
    Get list of directories to search for packages.
    Order: local -> global -> stl
    """
    paths = []
    
    # Project-local packages
    local_dir = get_project_packages_dir(project_dir)
    if local_dir.exists():
        paths.append(local_dir)
    
    # Global packages
    global_dir = get_global_packages_dir()
    if global_dir.exists():
        paths.append(global_dir)
    
    # Built-in stl
    stl_dir = Path(__file__).parent.parent / "stl"
    if stl_dir.exists():
        paths.append(stl_dir)
    
    return paths


def find_package(package_name: str, project_dir: Path = None) -> Optional[Path]:
    """Find a package in the search paths."""
    for search_path in get_package_search_paths(project_dir):
        # Check for folder package
        folder_path = search_path / package_name
        if folder_path.is_dir():
            init_path = folder_path / "__init__.tl"
            if init_path.exists():
                return folder_path
        
        # Check for file module
        file_path = search_path / f"{package_name}.tl"
        if file_path.exists():
            return file_path
    
    return None
