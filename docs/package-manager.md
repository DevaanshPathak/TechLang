# TechLang Package Manager (tlpm)

The TechLang Package Manager (`tlpm`) helps you manage global and project-wide packages for TechLang projects.

## Quick Start

```bash
# Initialize a new project
tlpm init

# Install a package from local path
tlpm install ./mylib

# Install a package globally
tlpm install -g ./mylib

# Install from git repository
tlpm install https://github.com/user/package.git

# List installed packages
tlpm list

# Run a script
tlpm run start
```

## Installation

After installing TechLang, `tlpm` is available as a command-line tool:

```bash
# If installed via pip
tlpm --help

# Or run directly
python tlpm.py --help
```

## Commands

### `tlpm init`

Initialize a new TechLang project in the current directory.

```bash
tlpm init                 # Interactive mode
tlpm init myproject       # Specify name
tlpm init -y              # Use defaults (non-interactive)
```

Creates:
- `tlpackage.json` - Project manifest
- `tl_packages/` - Local packages directory
- `main.tl` - Entry point (if not exists)

### `tlpm install [package]`

Install packages.

```bash
# Install all dependencies from tlpackage.json
tlpm install

# Install specific package
tlpm install ./mylib                          # From local path
tlpm install https://github.com/user/pkg.git  # From git
tlpm install https://github.com/user/pkg.git#v1.0.0  # From git tag/branch
tlpm install global:mylib                     # From global packages

# Options
tlpm install -g ./mylib      # Install globally
tlpm install -D ./mylib      # Add to devDependencies
tlpm install --no-save ./x   # Don't update tlpackage.json
```

### `tlpm uninstall <package>`

Remove a package.

```bash
tlpm uninstall mylib        # Remove local package
tlpm uninstall -g mylib     # Remove global package
```

### `tlpm list`

List installed packages.

```bash
tlpm list           # List local packages
tlpm list -g        # List global packages
tlpm list -a        # List all packages
```

### `tlpm info <package>`

Show package information.

```bash
tlpm info mylib
```

### `tlpm run <script>`

Run a script defined in `tlpackage.json`.

```bash
tlpm run start
tlpm run test
```

### `tlpm link`

Link a local package to global packages for development.

```bash
cd mypackage
tlpm link           # Link current directory globally
tlpm link ./other   # Link specific path
```

### `tlpm unlink [package]`

Remove a global package link.

```bash
tlpm unlink         # Unlink current directory
tlpm unlink mylib   # Unlink specific package
```

## Project Structure

After `tlpm init`, your project will have this structure:

```
myproject/
├── tlpackage.json      # Project manifest
├── tl_packages/        # Installed packages
│   ├── package1/
│   └── package2/
└── main.tl             # Entry point
```

## Package Manifest (tlpackage.json)

The manifest file describes your project and its dependencies:

```json
{
  "name": "myproject",
  "version": "1.0.0",
  "description": "My TechLang project",
  "author": "Your Name",
  "main": "main.tl",
  "dependencies": {
    "utils": "1.0.0",
    "helpers": "./local/helpers"
  },
  "dev_dependencies": {
    "testing": "1.0.0"
  },
  "scripts": {
    "start": "tl main.tl",
    "test": "tl tests/test.tl"
  }
}
```

## Creating a Package

To create a reusable package:

1. Create a directory with your package code:

```
mypackage/
├── tlpackage.json
├── __init__.tl        # Main entry point
└── utils.tl           # Additional modules
```

2. Add a manifest (`tlpackage.json`):

```json
{
  "name": "mypackage",
  "version": "1.0.0",
  "description": "My reusable package",
  "main": "__init__.tl"
}
```

3. Export functions in `__init__.tl`:

```techlang
def greet name
    str_create msg "Hello, "
    str_concat msg name
    print msg
end
export greet

def add_numbers a b
    set result a
    add result b
    return result
end
export add_numbers
```

4. Share your package:
   - Publish to GitHub
   - Share the folder path
   - Link globally for local development

## Using Packages

Once installed, packages can be imported in your TechLang code:

```techlang
# Import the whole package
import mypackage
call mypackage.greet "World"

# Import with alias
import mypackage as mp
call mp.greet "World"

# Import specific functions
from mypackage import greet
call greet "World"

# Import multiple functions
from mypackage import greet, add_numbers
call greet "User"
set x 5
call add_numbers x 10 result
print result
```

## Package Resolution Order

When you import a package, TechLang searches in this order:

1. **Current directory** - Relative imports
2. **`tl_packages/`** - Project-local packages
3. **`~/.techlang/packages/`** - Global packages
4. **Built-in `stl/`** - Standard library

## Global Packages Directory

Global packages are stored in `~/.techlang/packages/` (or `%USERPROFILE%\.techlang\packages` on Windows).

Use global packages for:
- Utilities you use across multiple projects
- Development tools
- Packages you're developing (via `tlpm link`)

## Tips

### Development Workflow

1. Create your package in a separate directory
2. Use `tlpm link` to make it globally available
3. Import it in your projects during development
4. When ready, publish or share the package

### Version Control

Add to your `.gitignore`:
```
tl_packages/
```

This is automatically done by `tlpm init`.

### Scripts

Define common tasks in `tlpackage.json`:

```json
{
  "scripts": {
    "start": "tl main.tl",
    "test": "tl tests/run_tests.tl",
    "build": "tl scripts/build.tl",
    "lint": "python format_tl.py --lint *.tl"
  }
}
```

Run with `tlpm run <script>`.

## Troubleshooting

### "Package not found"

- Check the package is installed: `tlpm list`
- Verify the import path matches the package name
- Check search paths by importing in code

### "Cannot create symlink" (Windows)

`tlpm link` requires either:
- Administrator privileges, or
- Developer Mode enabled in Windows Settings

### Module not loading

Ensure your package has:
- An `__init__.tl` file for folder packages
- Or a `.tl` extension for file modules
- Functions are exported with `export`

## See Also

- [Python-like Imports](general.md#python-like-imports) - Import syntax details
- [Modules](general.md#modules) - Module system overview
- [Standard Library](stl.md) - Built-in stl packages
