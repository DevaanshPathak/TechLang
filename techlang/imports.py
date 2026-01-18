import os
from dataclasses import dataclass
from typing import List, Callable, Optional, Tuple
from pathlib import Path
from .core import InterpreterState
from .parser import parse


def get_package_search_paths(base_dir: str) -> List[str]:
    """
    Get list of directories to search for packages.
    Order: current dir -> tl_packages -> global packages -> stl
    """
    paths = [base_dir]
    
    # Project-local packages (tl_packages/)
    local_packages = os.path.join(base_dir, "tl_packages")
    if os.path.isdir(local_packages):
        paths.append(local_packages)
    
    # Global packages (~/.techlang/packages/)
    home = os.path.expanduser("~")
    global_packages = os.path.join(home, ".techlang", "packages")
    if os.path.isdir(global_packages):
        paths.append(global_packages)
    
    # Built-in stl
    stl_dir = os.path.join(os.path.dirname(__file__), "..", "stl")
    if os.path.isdir(stl_dir):
        paths.append(os.path.abspath(stl_dir))
    
    return paths


class ImportHandler:
    # Import .tl files safely and inline their tokens
    
    @staticmethod
    def _resolve_relative_import(module_name: str, base_dir: str) -> str:
        """
        Resolve relative imports like . and .. to absolute module paths.
        
        Examples:
        - "." -> current directory module
        - ".sibling" -> sibling module in same directory
        - ".." -> parent directory module
        - "..parent_sibling" -> sibling of parent
        """
        # Count leading dots
        dots = 0
        for c in module_name:
            if c == '.':
                dots += 1
            else:
                break
        
        remainder = module_name[dots:]  # The part after the dots
        
        # Start from base_dir and go up (dots - 1) levels
        current_path = Path(base_dir).resolve()
        for _ in range(dots - 1):
            current_path = current_path.parent
        
        # Build the module name based on the resolved path
        if remainder:
            # .module or ..module
            return remainder
        else:
            # Just . or .. - import from that directory's __init__.tl
            return current_path.name
    
    @staticmethod
    def handle_import(state: InterpreterState, tokens: List[str], index: int, base_dir: str) -> int:
        """
        Handle Python-like import statements:
        - import module_name          (loads module_name.tl or module_name/__init__.tl)
        - import module_name as alias (loads module and creates alias)
        - import module.submodule     (loads module/submodule.tl or module/submodule/__init__.tl)
        """
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'import' command. Use: import <module_name> [as <alias>]")
            return 0
        
        module_name = tokens[index + 1]
        consumed = 1
        
        # Check for "as" alias
        alias_name = None
        if index + 3 < len(tokens) and tokens[index + 2] == "as":
            alias_name = tokens[index + 3]
            consumed = 3
        
        # Try to load as package (folder with __init__.tl) or as module file
        success = ImportHandler._load_module_or_package(state, module_name, base_dir, alias_name)
        
        if not success:
            # Fallback to old behavior - inline tokens (for backwards compatibility)
            imported_tokens = ImportHandler._import_file(module_name, state, base_dir)
            if imported_tokens and not any(token.startswith("[IMPORT ERROR") for token in imported_tokens):
                tokens[index + consumed + 1:index + consumed + 1] = imported_tokens
            else:
                for token in imported_tokens:
                    state.add_output(token)
        
        return consumed
    
    @staticmethod
    def _load_module_or_package(state: InterpreterState, module_name: str, base_dir: str, 
                                  alias_name: Optional[str] = None) -> bool:
        """
        Try to load module as:
        1. A folder package (folder_name/__init__.tl)
        2. A single file (module_name.tl)
        3. A nested package (parent/child/__init__.tl or parent/child.tl)
        
        Searches in: current dir -> tl_packages -> global packages -> stl
        """
        # Normalize module name: module.submodule -> module/submodule
        path_parts = module_name.replace("::", ".").replace(".", os.sep).split(os.sep)
        relative_path = os.sep.join(path_parts)
        
        # Search in all package paths
        search_paths = get_package_search_paths(base_dir)
        
        target_path = None
        is_package = False
        found_in_dir = None
        
        for search_dir in search_paths:
            # Check for package (folder with __init__.tl)
            package_init_path = os.path.join(search_dir, relative_path, "__init__.tl")
            module_file_path = os.path.join(search_dir, relative_path + ".tl")
            
            if os.path.isfile(package_init_path):
                target_path = package_init_path
                is_package = True
                found_in_dir = search_dir
                break
            elif os.path.isfile(module_file_path):
                target_path = module_file_path
                is_package = False
                found_in_dir = search_dir
                break
        
        if target_path is None:
            return False  # Neither package nor module found in any path
        
        full_path = os.path.abspath(target_path)
        
        # Load the module
        normalized_name = module_name.replace("::", ".").replace("/", ".").replace(os.sep, ".")
        register_name = alias_name if alias_name else normalized_name
        
        # Check if already loaded
        if normalized_name in state.loaded_modules:
            # If alias requested, just add the alias
            if alias_name and normalized_name in state.modules:
                state.modules[alias_name] = state.modules[normalized_name]
            return True
        
        # Load module using ModuleHandler
        ModuleHandler._load_module_from_path(state, normalized_name, full_path, found_in_dir, register_name, is_package)
        return True
    
    @staticmethod
    def handle_from_import(state: InterpreterState, tokens: List[str], index: int, base_dir: str) -> int:
        """
        Handle Python-like from...import statements:
        - from module import func1, func2    (import specific functions)
        - from module import *               (import all exported functions)
        - from module import submodule       (import submodule from package)
        - from module import func as alias   (import with alias)
        - from . import sibling              (relative import from current package)
        - from .. import parent              (relative import from parent package)
        - from .submodule import func        (relative import from submodule)
        """
        # Syntax: from <module> import <target1> [as alias1], <target2> [as alias2], ...
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'from' command. Use: from <module> import <name> [, <name2>, ...]")
            return 0
        
        module_name = tokens[index + 1]
        
        # Handle relative imports (. and ..)
        if module_name.startswith("."):
            module_name = ImportHandler._resolve_relative_import(module_name, base_dir)
        
        if tokens[index + 2] != "import":
            state.add_error(f"Expected 'import' after 'from {module_name}', got '{tokens[index + 2]}'")
            return 1
        
        consumed = 2  # module_name + "import"
        
        # Collect targets to import
        targets = []
        i = index + 3
        while i < len(tokens):
            target = tokens[i]
            
            # Stop at known commands
            from .basic_commands import BasicCommandHandler
            if target in BasicCommandHandler.KNOWN_COMMANDS and target not in ["as"]:
                break
            
            alias = None
            consumed += 1
            
            # Check for "as" alias
            if i + 2 < len(tokens) and tokens[i + 1] == "as":
                alias = tokens[i + 2]
                consumed += 2
                i += 3
            else:
                i += 1
            
            # Skip commas (optional separator)
            if i < len(tokens) and tokens[i] == ",":
                consumed += 1
                i += 1
            
            targets.append((target, alias))
            
            # Stop if we hit a newline-equivalent (next command)
            if i < len(tokens) and tokens[i] in BasicCommandHandler.KNOWN_COMMANDS:
                break
        
        if not targets:
            state.add_error("No targets specified for 'from...import'. Use: from <module> import <name>")
            return consumed
        
        # Process the import
        ImportHandler._process_from_import(state, module_name, targets, base_dir)
        
        return consumed
    
    @staticmethod
    def _process_from_import(state: InterpreterState, module_name: str, 
                               targets: List[Tuple[str, Optional[str]]], base_dir: str) -> None:
        """Process a from...import statement"""
        
        # First, check if it's a package or module
        normalized_name = module_name.replace("::", ".").replace("/", ".")
        path_parts = normalized_name.split(".")
        relative_path = os.sep.join(path_parts)
        
        # Search in all package paths
        search_paths = get_package_search_paths(base_dir)
        
        package_dir = None
        package_init = None
        module_file = None
        is_package = False
        found_dir = base_dir
        
        for search_dir in search_paths:
            check_package_dir = os.path.join(search_dir, relative_path)
            check_package_init = os.path.join(check_package_dir, "__init__.tl")
            check_module_file = os.path.join(search_dir, relative_path + ".tl")
            
            if os.path.isdir(check_package_dir) and os.path.isfile(check_package_init):
                package_dir = check_package_dir
                package_init = check_package_init
                is_package = True
                found_dir = search_dir
                break
            elif os.path.isfile(check_module_file):
                module_file = check_module_file
                found_dir = search_dir
                break
        
        # Handle each target
        for target, alias in targets:
            register_name = alias if alias else target
            
            if target == "*":
                # Import all exported functions from module
                ImportHandler._import_star(state, module_name, base_dir)
            elif is_package and package_dir and os.path.isdir(os.path.join(package_dir, target)):
                # Target is a subpackage
                subpackage_name = f"{normalized_name}.{target}"
                ImportHandler._load_module_or_package(state, subpackage_name, base_dir, register_name)
            elif is_package and package_dir and os.path.isfile(os.path.join(package_dir, target + ".tl")):
                # Target is a submodule file
                submodule_name = f"{normalized_name}.{target}"
                ImportHandler._load_module_or_package(state, submodule_name, base_dir, register_name)
            elif is_package and package_init:
                # Target is a function/variable from the package's __init__.tl
                ImportHandler._import_names_from_module(state, module_name, [(target, alias)], base_dir)
            elif module_file:
                # Target is a function/variable from module
                ImportHandler._import_names_from_module(state, module_name, [(target, alias)], base_dir)
            else:
                state.add_error(f"Cannot import '{target}' from '{module_name}': not found")
    
    @staticmethod
    def _import_star(state: InterpreterState, module_name: str, base_dir: str) -> None:
        """Import all exported functions from a module (respects __all__ if defined)"""
        # First ensure module is loaded
        ImportHandler._load_module_or_package(state, module_name, base_dir, None)
        
        normalized_name = module_name.replace("::", ".").replace("/", ".")
        module_info = state.modules.get(normalized_name)
        
        if module_info is None:
            state.add_error(f"Module '{module_name}' could not be loaded")
            return
        
        module_state = module_info.state
        
        # Check for __all__ array which defines public API
        if "__all__" in module_state.arrays:
            allowed_names = set(module_state.arrays["__all__"])
        else:
            # Fallback to exported_functions
            allowed_names = module_state.exported_functions
        
        # Import functions
        for func_name in allowed_names:
            if func_name in module_state.functions:
                state.functions[func_name] = module_state.functions[func_name]
                state.exported_functions.add(func_name)
        
        # Import variables (if in __all__)
        if "__all__" in module_state.arrays:
            for name in allowed_names:
                if name in module_state.variables and name not in module_state.functions:
                    state.variables[name] = module_state.variables[name]
                if name in module_state.strings:
                    state.strings[name] = module_state.strings[name]
                if name in module_state.arrays and name != "__all__":
                    state.arrays[name] = module_state.arrays[name]
                if name in module_state.dictionaries:
                    state.dictionaries[name] = module_state.dictionaries[name]
    
    @staticmethod
    def _import_names_from_module(state: InterpreterState, module_name: str, 
                                    targets: List[Tuple[str, Optional[str]]], base_dir: str) -> None:
        """Import specific names from a module"""
        # First ensure module is loaded
        ImportHandler._load_module_or_package(state, module_name, base_dir, None)
        
        normalized_name = module_name.replace("::", ".").replace("/", ".")
        module_info = state.modules.get(normalized_name)
        
        if module_info is None:
            state.add_error(f"Module '{module_name}' could not be loaded")
            return
        
        module_state = module_info.state
        
        for target, alias in targets:
            register_name = alias if alias else target
            
            # Check if it's an exported function
            if target in module_state.exported_functions and target in module_state.functions:
                state.functions[register_name] = module_state.functions[target]
                state.exported_functions.add(register_name)
            # Check if it's a variable
            elif target in module_state.variables:
                state.variables[register_name] = module_state.variables[target]
            # Check if it's a string
            elif target in module_state.strings:
                state.strings[register_name] = module_state.strings[target]
            # Check if it's an array
            elif target in module_state.arrays:
                state.arrays[register_name] = module_state.arrays[target]
            # Check if it's a dict
            elif target in module_state.dictionaries:
                state.dictionaries[register_name] = module_state.dictionaries[target]
            else:
                state.add_error(f"Cannot import '{target}' from '{module_name}': name not found or not exported")

    @staticmethod
    def _import_file(filename_token: str, state: InterpreterState, base_dir: str) -> List[str]:
        # Ensure .tl extension and resolve within allowed base directory
        if not filename_token.endswith(".tl"):
            filename_token += ".tl"
        
        if filename_token in state.loaded_files:
            return []
        
        try:
            full_path = os.path.abspath(os.path.join(base_dir, filename_token))
            
            # Prevent path traversal outside the sandboxed base_dir
            if not full_path.startswith(base_dir):
                return [f"[IMPORT ERROR: Security violation - file '{filename_token}' is outside the allowed directory.]"]
            
            if not os.path.isfile(full_path):
                return [f"[IMPORT ERROR: File '{filename_token}' not found. Searched in: {base_dir}]"]
            
            state.loaded_files.add(filename_token)
            
            with open(full_path, "r", encoding="utf-8") as f:
                imported_code: str = f.read()
            return parse(imported_code)
            
        except (OSError, IOError) as e:
            return [f"[IMPORT ERROR: Cannot read file '{filename_token}': {str(e)}]"]
        except Exception as e:
            return [f"[IMPORT ERROR: Unexpected error importing '{filename_token}': {str(e)}]"]


@dataclass
class ModuleInfo:
    name: str
    path: str
    base_dir: str
    state: InterpreterState


class ModuleHandler:
    """Handle TechLang module loading and namespaced dispatch."""

    @staticmethod
    def handle_package(state: InterpreterState, tokens: List[str], index: int, base_dir: str) -> int:
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'package' command. Use: package use <module>")
            return 0

        action = tokens[index + 1]
        if action == "use":
            if index + 2 >= len(tokens):
                state.add_error("Invalid 'package use' command. Use: package use <module>")
                return 1
            module_name = tokens[index + 2]
            ModuleHandler._load_module(state, module_name, base_dir)
            return 2

        state.add_error(f"Unknown 'package' directive '{action}'. Supported directives: use")
        return 1

    @staticmethod
    def _load_module(state: InterpreterState, module_name: str, base_dir: str) -> None:
        # Support 'stdlib' as alias for 'stl' (Standard Template Library)
        if module_name.startswith("stdlib/") or module_name.startswith("stdlib.") or module_name == "stdlib":
            module_name = module_name.replace("stdlib", "stl", 1)
        
        normalized_name = module_name.replace("::", ".").replace("/", ".")
        if normalized_name in state.loaded_modules:
            return

        relative_path = normalized_name.replace(".", os.sep) + ".tl"
        full_path = os.path.abspath(os.path.join(base_dir, relative_path))

        if not full_path.startswith(base_dir):
            state.add_output(f"[Module Error: Security violation - module '{module_name}' is outside the allowed directory]")
            return

        if not os.path.isfile(full_path):
            state.add_output(f"[Module Error: Module '{module_name}' not found. Searched in: {base_dir}]")
            return

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                source = f.read()
        except (OSError, IOError) as exc:
            state.add_output(f"[Module Error: Cannot read module '{module_name}': {exc}]")
            return

        module_tokens = parse(source)
        module_base_dir = os.path.dirname(full_path)

        module_state = InterpreterState()
        ModuleHandler._bridge_state(module_state, state)

        # Remove optional 'package name <id>' header
        module_tokens = ModuleHandler._strip_header(module_tokens, normalized_name, state)

        module_tokens = ModuleHandler._expand_aliases(module_tokens, module_state)

        from .executor import CommandExecutor  # local import to avoid circular dependency

        state.loaded_modules.add(normalized_name)
        executor = CommandExecutor(module_state, module_base_dir)
        executor.execute_block(module_tokens)
        ModuleHandler._sync_back(module_state, state)

        state.modules[normalized_name] = ModuleInfo(
            name=normalized_name,
            path=full_path,
            base_dir=module_base_dir,
            state=module_state,
        )

    @staticmethod
    def _load_module_from_path(state: InterpreterState, normalized_name: str, full_path: str, 
                                 base_dir: str, register_name: str, is_package: bool = False) -> None:
        """Load a module from a specific file path (used by new import system)"""
        
        if normalized_name in state.loaded_modules:
            # Just add alias if needed
            if register_name != normalized_name and normalized_name in state.modules:
                state.modules[register_name] = state.modules[normalized_name]
            return
        
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                source = f.read()
        except (OSError, IOError) as exc:
            state.add_error(f"[Module Error: Cannot read module '{normalized_name}': {exc}]")
            return
        
        module_tokens = parse(source)
        
        # For packages, base_dir is the package folder; for modules, it's the parent folder
        if is_package:
            module_base_dir = os.path.dirname(full_path)
        else:
            module_base_dir = os.path.dirname(full_path)
        
        module_state = InterpreterState()
        ModuleHandler._bridge_state(module_state, state)
        
        # Remove optional 'package name <id>' header
        module_tokens = ModuleHandler._strip_header(module_tokens, normalized_name, state)
        module_tokens = ModuleHandler._expand_aliases(module_tokens, module_state)
        
        from .executor import CommandExecutor
        
        state.loaded_modules.add(normalized_name)
        executor = CommandExecutor(module_state, module_base_dir)
        executor.execute_block(module_tokens)
        ModuleHandler._sync_back(module_state, state)
        
        module_info = ModuleInfo(
            name=normalized_name,
            path=full_path,
            base_dir=module_base_dir,
            state=module_state,
        )
        
        state.modules[normalized_name] = module_info
        
        # Also register with alias name if different
        if register_name != normalized_name:
            state.modules[register_name] = module_info

    @staticmethod
    def _strip_header(tokens: List[str], expected_name: str, state: InterpreterState) -> List[str]:
        if len(tokens) >= 3 and tokens[0] == "package" and tokens[1] == "name":
            declared = tokens[2]
            if declared != expected_name:
                state.add_output(f"[Module Error: Declared module '{declared}' does not match requested '{expected_name}']")
            return tokens[3:]
        return tokens

    @staticmethod
    def _expand_aliases(tokens: List[str], module_state: InterpreterState) -> List[str]:
        if not tokens:
            return tokens
        from .aliases import AliasHandler  # local import to avoid circular

        return AliasHandler.process_aliases(tokens, module_state)

    @staticmethod
    def _bridge_state(module_state: InterpreterState, host_state: InterpreterState) -> None:
        module_state.output = host_state.output
        module_state.variables = host_state.variables
        module_state.arrays = host_state.arrays
        module_state.dynamic_arrays = host_state.dynamic_arrays
        module_state.strings = host_state.strings
        module_state.dictionaries = host_state.dictionaries
        module_state.struct_defs = host_state.struct_defs
        module_state.structs = host_state.structs
        module_state.memory = host_state.memory
        module_state.next_address = host_state.next_address
        module_state.stack = host_state.stack
        module_state.value = host_state.value
        module_state.input_queue = host_state.input_queue
        module_state.aliases = host_state.aliases
        module_state.threads = host_state.threads
        module_state.thread_results = host_state.thread_results
        module_state.next_thread_id = host_state.next_thread_id
        module_state.processes = host_state.processes
        module_state.next_process_id = host_state.next_process_id
        module_state.process_start_times = host_state.process_start_times
        module_state.loaded_files = host_state.loaded_files
        module_state.loaded_modules = host_state.loaded_modules
        module_state.modules = host_state.modules
        module_state.parent_state = host_state

    @staticmethod
    def call_module_function(state: InterpreterState, module_name: str, func_name: str, 
                           args: List[str] = None, return_vars: List[str] = None, 
                           execute_block: Callable = None) -> bool:
        if args is None:
            args = []
        if return_vars is None:
            return_vars = []
        
        # Support 'stdlib' as alias for 'stl' in function calls
        # Normalize the module name first
        normalized_name = module_name.replace("::", ".").replace("/", ".")
        
        # Try with stdlib -> stl conversion if using stdlib prefix
        if normalized_name.startswith("stdlib.") or normalized_name == "stdlib":
            normalized_name = normalized_name.replace("stdlib", "stl", 1)
            
        module_info = state.modules.get(normalized_name)
        if module_info is None:
            state.add_error(f"Module '{module_name}' is not loaded. Use 'package use {module_name}' first.")
            return False

        module_state = module_info.state
        ModuleHandler._bridge_state(module_state, state)

        func_data = module_state.functions.get(func_name)
        if func_data is None:
            state.add_error(f"Module '{module_name}' has no function '{func_name}'.")
            return False

        # Check if function is exported (public API)
        if func_name not in module_state.exported_functions:
            state.add_error(f"Function '{func_name}' in module '{module_name}' is private. Use 'export {func_name}' to make it public.")
            return False

        # Handle both old format (list) and new format (dict with params/body)
        if isinstance(func_data, list):
            func_block = func_data
            # Old format: just execute
            from .executor import CommandExecutor
            executor = CommandExecutor(module_state, module_info.base_dir)
            executor.execute_block(func_block)
        elif isinstance(func_data, dict):
            params = func_data.get('params', [])
            func_block = func_data.get('body', [])
            
            # Validate argument count
            if len(args) < len(params):
                state.add_error(f"Function '{func_name}' expects {len(params)} arguments, got {len(args)}")
                return False
            
            # If function has parameters, use local scope; otherwise use shared scope
            if params:
                # Import helper function to resolve arguments
                from .control_flow import ControlFlowHandler
                
                # Save current state for local scope
                saved_vars = dict(module_state.variables)
                saved_strings = dict(module_state.strings)

                # Save any parameter names that already exist as arrays/dicts (so we can cleanly restore/cleanup)
                saved_param_arrays = {p: module_state.arrays[p] for p in params if p in module_state.arrays}
                saved_param_dicts = {p: module_state.dictionaries[p] for p in params if p in module_state.dictionaries}
                saved_param_dynamic = {p: (p in module_state.dynamic_arrays) for p in params}
                
                # Bind arguments to parameters
                for param_name, arg_token in zip(params, args):
                    # Arrays and dictionaries are passed by name (alias the underlying container)
                    if arg_token in module_state.arrays:
                        module_state.arrays[param_name] = module_state.arrays[arg_token]
                        if arg_token in module_state.dynamic_arrays:
                            module_state.dynamic_arrays.add(param_name)
                        else:
                            module_state.dynamic_arrays.discard(param_name)
                        continue
                    if arg_token in module_state.dictionaries:
                        module_state.dictionaries[param_name] = module_state.dictionaries[arg_token]
                        continue

                    arg_value = ControlFlowHandler._resolve_arg_value(state, arg_token)
                    if isinstance(arg_value, str):
                        module_state.strings[param_name] = arg_value
                    else:
                        module_state.variables[param_name] = arg_value
                
                # Clear should_return flag for this function call
                module_state.should_return = False
                
                # Execute function body
                from .executor import CommandExecutor
                executor = CommandExecutor(module_state, module_info.base_dir)
                executor.execute_block(func_block)
                
                # Clear should_return flag after function execution
                module_state.should_return = False
                
                # Restore saved state (clean up local parameters but keep other changes)
                # Remove parameters from module state
                for param_name in params:
                    module_state.variables.pop(param_name, None)
                    module_state.strings.pop(param_name, None)
                    module_state.arrays.pop(param_name, None)
                    module_state.dictionaries.pop(param_name, None)
                    # Remove dynamic-array aliases unless they existed before
                    if not saved_param_dynamic.get(param_name, False):
                        module_state.dynamic_arrays.discard(param_name)
                
                # Restore original values for variables that existed before
                for var_name, var_value in saved_vars.items():
                    module_state.variables[var_name] = var_value
                for str_name, str_value in saved_strings.items():
                    module_state.strings[str_name] = str_value

                # Restore any array/dict entries that were shadowed by parameter names
                for name, arr in saved_param_arrays.items():
                    module_state.arrays[name] = arr
                for name, dct in saved_param_dicts.items():
                    module_state.dictionaries[name] = dct
                for name, was_dynamic in saved_param_dynamic.items():
                    if was_dynamic:
                        module_state.dynamic_arrays.add(name)
                    else:
                        module_state.dynamic_arrays.discard(name)
            else:
                # No parameters: use shared scope (backward compatibility)
                # Clear should_return flag for this function call
                module_state.should_return = False
                
                from .executor import CommandExecutor
                executor = CommandExecutor(module_state, module_info.base_dir)
                executor.execute_block(func_block)
                
                # Clear should_return flag after function execution
                module_state.should_return = False
            
            # Handle return values
            if module_state.return_values:
                for i, ret_var in enumerate(return_vars):
                    if i < len(module_state.return_values):
                        ret_val = module_state.return_values[i]
                        if isinstance(ret_val, str):
                            state.strings[ret_var] = ret_val
                        else:
                            state.variables[ret_var] = ret_val
                module_state.return_values.clear()
        else:
            state.add_error(f"Invalid function format for '{func_name}'")
            return False

        ModuleHandler._sync_back(module_state, state)
        return True

    @staticmethod
    def _sync_back(module_state: InterpreterState, host_state: InterpreterState) -> None:
        host_state.value = module_state.value
        host_state.next_address = module_state.next_address
        host_state.next_thread_id = module_state.next_thread_id
        host_state.next_process_id = module_state.next_process_id
