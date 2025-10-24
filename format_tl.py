#!/usr/bin/env python3
"""
TechLang formatter and linter CLI tool.

Usage:
    python format_tl.py --check file.tl           # Check if file needs formatting
    python format_tl.py --fix file.tl             # Format file in place
    python format_tl.py --lint file.tl            # Lint file for issues
    python format_tl.py --check --lint file.tl    # Check formatting and lint
    python format_tl.py --fix --lint examples/    # Format all .tl files in directory
"""

import sys
import os
import argparse
from pathlib import Path
from typing import List, Tuple
from techlang.formatter import format_file, format_string
from techlang.linter import lint_file, lint_string, LintIssue


def find_tl_files(path: str) -> List[str]:
    """Find all .tl files in a path (file or directory)."""
    path_obj = Path(path)
    
    if path_obj.is_file():
        if path_obj.suffix == '.tl':
            return [str(path_obj)]
        else:
            print(f"Warning: {path} is not a .tl file", file=sys.stderr)
            return []
    elif path_obj.is_dir():
        return [str(p) for p in path_obj.rglob('*.tl')]
    else:
        print(f"Error: {path} does not exist", file=sys.stderr)
        return []


def check_formatting(filepath: str) -> Tuple[bool, str]:
    """
    Check if a file needs formatting.
    
    Returns:
        (needs_formatting, formatted_content)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()
    
    formatted = format_file(filepath)
    
    # Normalize line endings for comparison
    original_normalized = original.replace('\r\n', '\n').rstrip() + '\n'
    formatted_normalized = formatted.rstrip() + '\n'
    
    needs_formatting = original_normalized != formatted_normalized
    
    return needs_formatting, formatted


def format_and_fix(filepath: str, indent_size: int = 4) -> bool:
    """
    Format a file and write changes.
    
    Returns:
        True if file was modified
    """
    needs_formatting, formatted = check_formatting(filepath)
    
    if needs_formatting:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(formatted)
        return True
    
    return False


def lint_code(filepath: str) -> List[LintIssue]:
    """Lint a file and return issues."""
    return lint_file(filepath)


def main():
    parser = argparse.ArgumentParser(
        prog='format_tl',
        description='Format and lint TechLang (.tl) files'
    )
    parser.add_argument(
        'paths',
        nargs='+',
        help='Files or directories to process'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check if files need formatting (exit 1 if changes needed)'
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Format files in place'
    )
    parser.add_argument(
        '--lint',
        action='store_true',
        help='Lint files for issues'
    )
    parser.add_argument(
        '--indent',
        type=int,
        default=4,
        help='Number of spaces per indent level (default: 4)'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress output except for errors'
    )
    
    args = parser.parse_args()
    
    # Default to --check if nothing specified
    if not args.check and not args.fix and not args.lint:
        args.check = True
    
    # Collect all files
    all_files = []
    for path in args.paths:
        all_files.extend(find_tl_files(path))
    
    if not all_files:
        print("No .tl files found", file=sys.stderr)
        return 1
    
    exit_code = 0
    files_need_formatting = []
    files_with_issues = []
    
    # Process each file
    for filepath in sorted(all_files):
        if not args.quiet:
            print(f"Processing {filepath}...")
        
        # Check/fix formatting
        if args.check or args.fix:
            if args.fix:
                modified = format_and_fix(filepath, indent_size=args.indent)
                if modified:
                    if not args.quiet:
                        print(f"  ✓ Formatted {filepath}")
            else:  # check mode
                needs_formatting, _ = check_formatting(filepath)
                if needs_formatting:
                    files_need_formatting.append(filepath)
                    print(f"  ✗ {filepath} needs formatting")
                    exit_code = 1
                elif not args.quiet:
                    print(f"  ✓ {filepath} is properly formatted")
        
        # Lint
        if args.lint:
            issues = lint_code(filepath)
            if issues:
                files_with_issues.append((filepath, issues))
                exit_code = 1
                
                # Print issues
                for issue in issues:
                    severity_symbol = {
                        'error': '✗',
                        'warning': '⚠',
                        'info': 'ℹ'
                    }.get(issue.severity, '•')
                    
                    print(f"  {severity_symbol} {issue}")
            elif not args.quiet:
                print(f"  ✓ No lint issues in {filepath}")
    
    # Summary
    if not args.quiet:
        print()
        print("=" * 60)
        print("Summary:")
        print(f"  Processed {len(all_files)} file(s)")
        
        if args.check and files_need_formatting:
            print(f"  {len(files_need_formatting)} file(s) need formatting")
        elif args.fix:
            print(f"  Formatting complete")
        
        if args.lint and files_with_issues:
            total_issues = sum(len(issues) for _, issues in files_with_issues)
            print(f"  {total_issues} issue(s) found in {len(files_with_issues)} file(s)")
        elif args.lint:
            print(f"  No lint issues found")
        
        print("=" * 60)
    
    if exit_code != 0:
        if args.check and files_need_formatting:
            print("\nRun with --fix to automatically format files", file=sys.stderr)
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
