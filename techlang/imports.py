import os
from dataclasses import dataclass
from typing import List, Callable
from .core import InterpreterState
from .parser import parse


class ImportHandler:
    # Import .tl files safely and inline their tokens
    
    @staticmethod
    def handle_import(state: InterpreterState, tokens: List[str], index: int, base_dir: str) -> int:
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'import' command. Use: import <filename>")
            return 0
        
        filename_token = tokens[index + 1]
        imported_tokens = ImportHandler._import_file(filename_token, state, base_dir)
        
        # If import was successful, insert the imported tokens into the current block
        if imported_tokens and not any(token.startswith("[IMPORT ERROR") for token in imported_tokens):
            tokens[index+2:index+2] = imported_tokens
            return 1  # Consume filename token
        else:
            for token in imported_tokens:
                state.add_output(token)
            return 1  # Consume filename token
    
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
