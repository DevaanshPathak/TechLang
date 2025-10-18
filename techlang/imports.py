import os
from dataclasses import dataclass
from typing import List
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
        normalized_name = module_name.replace("::", ".")
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
        module_tokens = ModuleHandler._strip_header(module_tokens, normalized_name.split(".")[-1], state)

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
        module_state.loaded_files = host_state.loaded_files
        module_state.loaded_modules = host_state.loaded_modules
        module_state.modules = host_state.modules
        module_state.parent_state = host_state

    @staticmethod
    def call_module_function(state: InterpreterState, module_name: str, func_name: str) -> bool:
        normalized_name = module_name.replace("::", ".")
        module_info = state.modules.get(normalized_name)
        if module_info is None:
            state.add_error(f"Module '{module_name}' is not loaded. Use 'package use {module_name}' first.")
            return False

        module_state = module_info.state
        ModuleHandler._bridge_state(module_state, state)

        func_block = module_state.functions.get(func_name)
        if func_block is None:
            state.add_error(f"Module '{module_name}' has no function '{func_name}'.")
            return False

        from .executor import CommandExecutor  # local import to avoid circular dependency

        executor = CommandExecutor(module_state, module_info.base_dir)
        executor.execute_block(func_block)
        ModuleHandler._sync_back(module_state, state)
        return True

    @staticmethod
    def _sync_back(module_state: InterpreterState, host_state: InterpreterState) -> None:
        host_state.value = module_state.value
        host_state.next_address = module_state.next_address
        host_state.next_thread_id = module_state.next_thread_id
        host_state.next_process_id = module_state.next_process_id
