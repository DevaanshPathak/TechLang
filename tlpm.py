#!/usr/bin/env python3
"""
TechLang Package Manager (tlpm) - CLI

Usage:
    tlpm init                      Initialize a new project
    tlpm install [package]         Install package(s)
    tlpm install -g <package>      Install package globally
    tlpm uninstall <package>       Remove a package
    tlpm update [package]          Update package(s) to latest
    tlpm outdated                  Check for outdated packages
    tlpm search <query>            Search for packages
    tlpm create <name>             Create new package from template
    tlpm list                      List local packages
    tlpm list -g                   List global packages
    tlpm list -a                   List all packages
    tlpm info <package>            Show package information
    tlpm run <script>              Run a script from tlpackage.json
    tlpm link                      Link current package globally
    tlpm unlink [package]          Remove global link
    tlpm help                      Show this help
"""

import sys
import os
import argparse
from pathlib import Path

from techlang.package_manager import PackageManager, MANIFEST_FILENAME


def print_banner():
    print("""
╔════════════════════════════════════════════╗
║   tlpm - TechLang Package Manager v1.0.0   ║
╚════════════════════════════════════════════╝
""")


def cmd_init(args):
    """Initialize a new TechLang project."""
    pm = PackageManager(verbose=args.verbose)
    pm.init(name=args.name, interactive=not args.yes)


def cmd_install(args):
    """Install package(s)."""
    pm = PackageManager(verbose=args.verbose)
    
    if args.package:
        # Install specific package
        pm.install(
            args.package,
            global_install=args.glob,
            save=not args.no_save,
            dev=args.dev
        )
    else:
        # Install all from manifest
        pm.install_all(global_install=args.glob)


def cmd_uninstall(args):
    """Uninstall a package."""
    pm = PackageManager(verbose=args.verbose)
    pm.uninstall(args.package, global_uninstall=args.glob)


def cmd_list(args):
    """List installed packages."""
    pm = PackageManager(verbose=args.verbose)
    pm.list_packages(global_list=args.glob, all_list=args.all)


def cmd_info(args):
    """Show package information."""
    pm = PackageManager(verbose=args.verbose)
    pm.info(args.package)


def cmd_run(args):
    """Run a script."""
    pm = PackageManager(verbose=args.verbose)
    exit_code = pm.run_script(args.script)
    sys.exit(exit_code)


def cmd_link(args):
    """Link package globally."""
    pm = PackageManager(verbose=args.verbose)
    pm.link(Path(args.path) if args.path else None)


def cmd_unlink(args):
    """Unlink package."""
    pm = PackageManager(verbose=args.verbose)
    pm.unlink(args.package)


def cmd_update(args):
    """Update package(s)."""
    pm = PackageManager(verbose=args.verbose)
    pm.update(args.package, global_update=args.glob)


def cmd_outdated(args):
    """Check for outdated packages."""
    pm = PackageManager(verbose=args.verbose)
    pm.outdated(global_check=args.glob)


def cmd_search(args):
    """Search for packages."""
    pm = PackageManager(verbose=args.verbose)
    source = "all"
    if args.local:
        source = "local"
    elif args.glob:
        source = "global"
    elif args.stl:
        source = "stl"
    elif args.github:
        source = "github"
    pm.search(args.query, source=source)


def cmd_create(args):
    """Create a new package from template."""
    pm = PackageManager(verbose=args.verbose)
    if args.list_templates:
        pm.list_templates()
    else:
        from pathlib import Path
        pm.create(
            name=args.name,
            template=args.template,
            interactive=not args.yes,
            directory=Path(args.path),
        )


def cmd_help(args):
    """Show help."""
    print(__doc__)
    print("""
Commands:
    init        Create a new tlpackage.json
    install     Install packages (alias: i, add)
    uninstall   Remove packages (alias: un, remove, rm)
    update      Update packages (alias: up)
    outdated    Check for outdated packages
    search      Search for packages
    create      Create new package from template (alias: new)
    list        List installed packages (alias: ls)
    info        Show package details
    run         Execute a script from tlpackage.json
    link        Link local package globally for development
    unlink      Remove global link

Options:
    -g, --global    Use global packages (~/.techlang/packages/)
    -D, --dev       Add to devDependencies
    --no-save       Don't update tlpackage.json
    -v, --verbose   Show detailed output
    -y, --yes       Skip prompts (use defaults)

Examples:
    tlpm init                           # Create new project
    tlpm install ./mylib                # Install local package
    tlpm install -g ./mylib             # Install globally  
    tlpm install https://github.com/user/pkg.git  # From git
    tlpm install                        # Install all deps from tlpackage.json
    tlpm update                         # Update all packages
    tlpm update mylib                   # Update specific package
    tlpm outdated                       # Check for outdated packages
    tlpm search utils                   # Search for packages
    tlpm search utils --stl             # Search only in stl
    tlpm create mylib                   # Create new package
    tlpm create mylib --template cli    # Create CLI app
    tlpm list -a                        # List all packages
    tlpm run start                      # Run 'start' script
    tlpm link                           # Link current dir globally
""")


def main():
    parser = argparse.ArgumentParser(
        prog='tlpm',
        description='TechLang Package Manager'
    )
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # init
    init_parser = subparsers.add_parser('init', help='Initialize project')
    init_parser.add_argument('name', nargs='?', help='Project name')
    init_parser.add_argument('-y', '--yes', action='store_true', help='Use defaults')
    init_parser.set_defaults(func=cmd_init)
    
    # install (with aliases)
    install_parser = subparsers.add_parser('install', aliases=['i', 'add'], help='Install packages')
    install_parser.add_argument('package', nargs='?', help='Package to install')
    install_parser.add_argument('-g', '--global', dest='glob', action='store_true', help='Install globally')
    install_parser.add_argument('-D', '--dev', action='store_true', help='Add to devDependencies')
    install_parser.add_argument('--no-save', action='store_true', help="Don't update manifest")
    install_parser.set_defaults(func=cmd_install)
    
    # uninstall (with aliases)
    uninstall_parser = subparsers.add_parser('uninstall', aliases=['un', 'remove', 'rm'], help='Uninstall packages')
    uninstall_parser.add_argument('package', help='Package to uninstall')
    uninstall_parser.add_argument('-g', '--global', dest='glob', action='store_true', help='Uninstall globally')
    uninstall_parser.set_defaults(func=cmd_uninstall)
    
    # list (with alias)
    list_parser = subparsers.add_parser('list', aliases=['ls'], help='List packages')
    list_parser.add_argument('-g', '--global', dest='glob', action='store_true', help='List global packages')
    list_parser.add_argument('-a', '--all', action='store_true', help='List all packages')
    list_parser.set_defaults(func=cmd_list)
    
    # info
    info_parser = subparsers.add_parser('info', help='Show package info')
    info_parser.add_argument('package', help='Package name')
    info_parser.set_defaults(func=cmd_info)
    
    # run
    run_parser = subparsers.add_parser('run', help='Run script')
    run_parser.add_argument('script', help='Script name')
    run_parser.set_defaults(func=cmd_run)
    
    # link
    link_parser = subparsers.add_parser('link', help='Link package globally')
    link_parser.add_argument('path', nargs='?', help='Path to package')
    link_parser.set_defaults(func=cmd_link)
    
    # unlink
    unlink_parser = subparsers.add_parser('unlink', help='Unlink global package')
    unlink_parser.add_argument('package', nargs='?', help='Package name')
    unlink_parser.set_defaults(func=cmd_unlink)
    
    # update
    update_parser = subparsers.add_parser('update', aliases=['up'], help='Update packages')
    update_parser.add_argument('package', nargs='?', help='Package to update (all if not specified)')
    update_parser.add_argument('-g', '--global', dest='glob', action='store_true', help='Update global packages')
    update_parser.set_defaults(func=cmd_update)
    
    # outdated
    outdated_parser = subparsers.add_parser('outdated', help='Check for outdated packages')
    outdated_parser.add_argument('-g', '--global', dest='glob', action='store_true', help='Check global packages')
    outdated_parser.set_defaults(func=cmd_outdated)
    
    # search
    search_parser = subparsers.add_parser('search', aliases=['find'], help='Search for packages')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('-l', '--local', action='store_true', help='Search local packages only')
    search_parser.add_argument('-g', '--global', dest='glob', action='store_true', help='Search global packages only')
    search_parser.add_argument('--stl', action='store_true', help='Search stl only')
    search_parser.add_argument('--github', action='store_true', help='Search GitHub only')
    search_parser.set_defaults(func=cmd_search)
    
    # create (with alias 'new')
    create_parser = subparsers.add_parser('create', aliases=['new'], help='Create new package')
    create_parser.add_argument('name', nargs='?', help='Package name')
    create_parser.add_argument('-t', '--template', default='basic', 
                               choices=['basic', 'library', 'cli', 'web'],
                               help='Template to use (default: basic)')
    create_parser.add_argument('-l', '--list-templates', action='store_true', 
                               help='List available templates')
    create_parser.add_argument('-p', '--path', default='.', 
                               help='Directory to create package in (default: current dir)')
    create_parser.add_argument('-y', '--yes', action='store_true', help='Use defaults')
    create_parser.set_defaults(func=cmd_create)
    
    # help
    help_parser = subparsers.add_parser('help', help='Show help')
    help_parser.set_defaults(func=cmd_help)
    help_parser.set_defaults(func=cmd_help)
    
    args = parser.parse_args()
    
    if args.command is None:
        print_banner()
        parser.print_help()
        sys.exit(0)
    
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
