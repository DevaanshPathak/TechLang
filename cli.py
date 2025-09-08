import sys
import os
import argparse
import readline  # noqa: F401 (POSIX; on Windows, pyreadline may be needed)
from techlang.interpreter import run


def run_file(path: str, verbose: bool = False):
    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()
    if verbose:
        print(f"[Running {path} ({len(code)} bytes)]")
    base_dir = os.path.dirname(os.path.abspath(path))
    out = run(code, base_dir=base_dir)
    print(out)


def repl(verbose: bool = False):
    print("TechLang REPL. Type 'exit' or Ctrl-D to quit. Use 'help' for commands.")
    buffer = []
    while True:
        try:
            line = input('tl> ' if not buffer else '... ')
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if line.strip() in {"exit", "quit"}:
            break
        if not line.strip():
            continue
        buffer.append(line)
        # Simple block detection: run when balanced 'end' likely reached
        if line.strip() == 'end' or not any(kw in ' '.join(buffer) for kw in ('loop', 'if', 'def', 'while', 'switch', 'try')):
            code = '\n'.join(buffer)
            buffer.clear()
            out = run(code)
            print(out)


def main():
    parser = argparse.ArgumentParser(prog='tl', description='TechLang CLI')
    parser.add_argument('file', nargs='?', help='TechLang source file (.tl)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
    parser.add_argument('-i', '--interactive', action='store_true', help='Start REPL')
    args = parser.parse_args()

    if args.interactive or not args.file:
        return repl(verbose=args.verbose)
    if not os.path.exists(args.file):
        print(f"File not found: {args.file}")
        return 1
    run_file(args.file, verbose=args.verbose)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
