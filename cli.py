import sys
import os
import argparse

# Try to import readline for history support (may not be available on all platforms)
try:
    import readline
    HAS_READLINE = True
except ImportError:
    HAS_READLINE = False

from techlang.interpreter import run


def run_file(path: str, verbose: bool = False):
    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()
    if verbose:
        print(f"[Running {path} ({len(code)} bytes)]")
    base_dir = os.path.dirname(os.path.abspath(path))
    out = run(code, base_dir=base_dir)
    print(out)


def _setup_history():
    """Set up readline history persistence."""
    if not HAS_READLINE:
        return None
    
    history_file = os.path.expanduser("~/.techlang_history")
    try:
        if os.path.exists(history_file):
            readline.read_history_file(history_file)
        # Limit history to 1000 entries
        readline.set_history_length(1000)
    except (IOError, OSError):
        pass  # History won't work, but REPL still functional
    return history_file


def _save_history(history_file):
    """Save readline history to file."""
    if not HAS_READLINE or history_file is None:
        return
    
    try:
        readline.write_history_file(history_file)
    except (IOError, OSError):
        pass  # Silently fail if we can't save


def _calculate_indent(buffer):
    """Calculate auto-indent level based on block depth."""
    depth = 0
    block_keywords = {'loop', 'if', 'def', 'while', 'switch', 'try', 'match', 'macro', 'struct'}
    
    for line in buffer:
        tokens = line.strip().split()
        if not tokens:
            continue
        
        # Count block starts and ends on this line
        line_depth_change = 0
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token in block_keywords:
                # Check if struct with operation (doesn't start block)
                if token == 'struct' and i + 1 < len(tokens) and tokens[i + 1] in {'new', 'set', 'get', 'dump'}:
                    i += 1
                    continue
                line_depth_change += 1
            elif token == 'end':
                line_depth_change -= 1
            
            i += 1
        
        depth = max(0, depth + line_depth_change)
    
    return '    ' * depth  # 4 spaces per indent level


def _show_repl_help():
    """Display REPL meta-commands."""
    help_text = """
TechLang REPL Meta-Commands:
  :load <file.tl>      Load and execute a TechLang file
  :loadmacro <file>    Load macros from a file (without executing)
  :help                Show this help message
  :clear               Clear the current buffer
  :history             Show command history
  :state               Show current interpreter state (variables, strings, etc.)
  :macros              List all defined macros
  :reset               Reset the interpreter state (clear all variables, etc.)
  exit / quit          Exit the REPL (or Ctrl-D)

For TechLang language help, use: help
For specific command help, use: help <command>
""".strip()
    print(help_text)


def repl(verbose: bool = False):
    print("TechLang REPL v1.1 - Enhanced Edition")
    print("Type 'exit' or Ctrl-D to quit. Type ':help' for meta-commands.")
    
    # Set up history persistence
    history_file = _setup_history()
    
    # Import here to avoid circular dependency
    from techlang.core import InterpreterState
    from techlang.parser import parse
    from techlang.macros import MacroHandler
    from techlang.aliases import AliasHandler
    from techlang.executor import CommandExecutor
    
    # Persistent state for REPL session
    repl_state = InterpreterState()
    from techlang.interpreter import initialize_state
    initialize_state(repl_state)
    
    buffer = []
    block_depth = 0
    
    try:
        while True:
            try:
                # Calculate prompt and auto-indent
                if not buffer:
                    prompt = 'tl> '
                    indent = ''
                else:
                    prompt = '... '
                    indent = _calculate_indent(buffer)
                
                line = input(prompt + indent)
                
                # Handle meta-commands (starting with :)
                if line.strip().startswith(':'):
                    cmd_parts = line.strip()[1:].split(maxsplit=1)
                    meta_cmd = cmd_parts[0].lower()
                    
                    if meta_cmd == 'help':
                        _show_repl_help()
                        continue
                    elif meta_cmd == 'clear':
                        buffer.clear()
                        block_depth = 0
                        print("[Buffer cleared]")
                        continue
                    elif meta_cmd == 'reset':
                        from techlang.interpreter import initialize_state
                        repl_state = InterpreterState()
                        initialize_state(repl_state)
                        buffer.clear()
                        block_depth = 0
                        print("[Interpreter state reset]")
                        continue
                    elif meta_cmd == 'state':
                        print("\n=== Interpreter State ===")
                        print(f"Value: {repl_state.value}")
                        if repl_state.variables:
                            print(f"Variables: {dict(list(repl_state.variables.items())[:10])}")
                            if len(repl_state.variables) > 10:
                                print(f"  ... and {len(repl_state.variables) - 10} more")
                        if repl_state.strings:
                            print(f"Strings: {dict(list(repl_state.strings.items())[:5])}")
                            if len(repl_state.strings) > 5:
                                print(f"  ... and {len(repl_state.strings) - 5} more")
                        if repl_state.arrays:
                            print(f"Arrays: {list(repl_state.arrays.keys())}")
                        if repl_state.dictionaries:
                            print(f"Dictionaries: {list(repl_state.dictionaries.keys())}")
                        if repl_state.functions:
                            print(f"Functions: {list(repl_state.functions.keys())}")
                        print()
                        continue
                    elif meta_cmd == 'macros':
                        if not repl_state.macros:
                            print("[No macros defined]")
                        else:
                            print("\n=== Defined Macros ===")
                            for name, macro in repl_state.macros.items():
                                params = ', '.join(macro.parameters) if macro.parameters else 'none'
                                cond = f" [if {macro.condition}]" if macro.condition else ""
                                print(f"  {name}({params}){cond}")
                            print()
                        continue
                    elif meta_cmd == 'history':
                        if not HAS_READLINE:
                            print("[History not available on this platform]")
                            continue
                        # Show last 20 history entries
                        history_len = readline.get_current_history_length()
                        start = max(1, history_len - 19)
                        for i in range(start, history_len + 1):
                            item = readline.get_history_item(i)
                            if item:
                                print(f"{i:4d}  {item}")
                        continue
                    elif meta_cmd == 'loadmacro':
                        if len(cmd_parts) < 2:
                            print("[Error: :loadmacro requires a filename]")
                            continue
                        filename = cmd_parts[1]
                        if not filename.endswith('.tl'):
                            filename += '.tl'
                        base_dir = os.path.dirname(os.path.abspath(filename)) if '/' in filename or '\\' in filename else '.'
                        lib_name = os.path.splitext(os.path.basename(filename))[0]
                        if MacroHandler.load_macro_library(lib_name, repl_state, base_dir):
                            print(f"[Loaded macros from {filename}]")
                        else:
                            print(f"[Failed to load macros from {filename}]")
                        continue
                    elif meta_cmd == 'load':
                        if len(cmd_parts) < 2:
                            print("[Error: :load requires a filename]")
                            continue
                        filename = cmd_parts[1]
                        if not filename.endswith('.tl'):
                            filename += '.tl'
                        try:
                            if not os.path.exists(filename):
                                print(f"[Error: File '{filename}' not found]")
                                continue
                            print(f"[Loading {filename}...]")
                            run_file(filename, verbose=verbose)
                        except Exception as e:
                            print(f"[Error loading file: {e}]")
                        continue
                    else:
                        print(f"[Unknown meta-command: :{meta_cmd}. Type ':help' for available commands]")
                        continue
                
                # Handle normal exit commands
                if line.strip() in {"exit", "quit"}:
                    break
                
                # Skip empty lines
                if not line.strip():
                    continue
                
                # Add to buffer (preserve user's actual input, not the indented version)
                buffer.append(line)
                
                # Track block depth for better detection
                tokens = line.strip().split()
                if tokens:
                    first_token = tokens[0]
                    block_keywords = {'loop', 'if', 'def', 'while', 'switch', 'try', 'match', 'macro'}
                    
                    if first_token in block_keywords:
                        block_depth += 1
                    elif first_token == 'struct' and len(tokens) > 1 and tokens[1] not in {'new', 'set', 'get', 'dump'}:
                        block_depth += 1
                    elif first_token == 'end':
                        block_depth = max(0, block_depth - 1)
                
                # Execute when block is complete or no blocks present
                if block_depth == 0:
                    code = '\n'.join(buffer)
                    buffer.clear()
                    
                    # Execute with persistent state
                    try:
                        tokens = parse(code)
                        tokens = MacroHandler.process_macros(tokens, repl_state)
                        tokens = AliasHandler.process_aliases(repl_state, tokens)
                        executor = CommandExecutor(repl_state, os.getcwd())
                        executor.execute_block(tokens)
                        
                        # Display output
                        if repl_state.output:
                            for line in repl_state.output:
                                print(line)
                            repl_state.output.clear()
                    except Exception as e:
                        print(f"[Error: {e}]")
                        if verbose:
                            import traceback
                            traceback.print_exc()
                        
            except (EOFError, KeyboardInterrupt):
                print()
                break
    finally:
        # Save history on exit
        _save_history(history_file)


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
