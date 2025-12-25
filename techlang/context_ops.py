"""
Context Manager support for TechLang.

This module implements Python-like context managers using the 'with' statement.
Context managers handle setup and teardown automatically, ensuring resources
are properly released even if errors occur.

Syntax:
    with <resource> as <name> do
        ... use resource ...
    end

Built-in context managers:
    - file_context: Auto-close files
    - timer_context: Measure execution time
    - transaction: Database transactions with auto-commit/rollback
    - lock_context: Mutex locking with auto-unlock
"""

from typing import Dict, List, Optional, Any, Callable
from .core import InterpreterState
import time


class ContextManager:
    """Represents a context manager definition."""
    
    def __init__(self, name: str, params: List[str], 
                 enter_body: List[str], exit_body: List[str],
                 resource_var: str = "_resource"):
        self.name = name
        self.params = params
        self.enter_body = enter_body  # Executed on entry
        self.exit_body = exit_body    # Executed on exit (always, even on error)
        self.resource_var = resource_var  # Variable holding the resource
    
    def __repr__(self):
        return f"<context_manager {self.name}>"


class ContextOpsHandler:
    """Handles context manager operations in TechLang."""
    
    @staticmethod
    def handle_context_def(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Define a context manager:
        context <name> [params...] do
            enter do
                ... setup code ...
            end
            exit do
                ... cleanup code ...
            end
        end
        """
        if index + 1 >= len(tokens):
            state.add_error("Invalid context definition. Use: context <name> [params...] do ... end")
            return 0
        
        name = tokens[index + 1]
        cursor = index + 2
        
        # Collect parameters until 'do'
        params = []
        while cursor < len(tokens) and tokens[cursor] != "do":
            params.append(tokens[cursor])
            cursor += 1
        
        if cursor >= len(tokens) or tokens[cursor] != "do":
            state.add_error("Expected 'do' in context definition")
            return cursor - index
        
        cursor += 1  # Skip 'do'
        
        # Parse enter and exit blocks
        enter_body = []
        exit_body = []
        
        while cursor < len(tokens):
            if tokens[cursor] == "enter":
                cursor += 1
                if cursor < len(tokens) and tokens[cursor] == "do":
                    cursor += 1
                
                # Collect enter body
                depth = 1
                while cursor < len(tokens):
                    t = tokens[cursor]
                    if t in {"def", "fn", "if", "loop", "while", "switch", "try", "match", "do", "enter", "exit"}:
                        depth += 1
                        enter_body.append(t)
                    elif t == "end":
                        depth -= 1
                        if depth == 0:
                            cursor += 1
                            break
                        enter_body.append(t)
                    else:
                        enter_body.append(t)
                    cursor += 1
            
            elif tokens[cursor] == "exit":
                cursor += 1
                if cursor < len(tokens) and tokens[cursor] == "do":
                    cursor += 1
                
                # Collect exit body
                depth = 1
                while cursor < len(tokens):
                    t = tokens[cursor]
                    if t in {"def", "fn", "if", "loop", "while", "switch", "try", "match", "do", "enter", "exit"}:
                        depth += 1
                        exit_body.append(t)
                    elif t == "end":
                        depth -= 1
                        if depth == 0:
                            cursor += 1
                            break
                        exit_body.append(t)
                    else:
                        exit_body.append(t)
                    cursor += 1
            
            elif tokens[cursor] == "end":
                # End of context definition
                break
            else:
                cursor += 1
        
        # Store context manager
        if not hasattr(state, 'context_managers') or state.context_managers is None:
            state.context_managers = {}
        
        ctx = ContextManager(name, params, enter_body, exit_body)
        state.context_managers[name] = ctx
        
        return cursor - index
    
    @staticmethod
    def handle_with(state: InterpreterState, tokens: List[str], index: int,
                   execute_block: Callable) -> int:
        """
        Execute a with statement:
        with <context_or_resource> [args...] as <name> do
            ... body ...
        end
        
        Or for files:
        with file "path" as f do
            ... use f ...
        end
        """
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'with' statement")
            return 0
        
        resource_type = tokens[index + 1]
        cursor = index + 2
        
        # Collect arguments until 'as'
        args = []
        while cursor < len(tokens) and tokens[cursor] != "as":
            args.append(tokens[cursor])
            cursor += 1
        
        if cursor >= len(tokens) or tokens[cursor] != "as":
            state.add_error("with statement requires 'as <name>'")
            return cursor - index
        
        cursor += 1  # Skip 'as'
        
        if cursor >= len(tokens):
            state.add_error("with statement requires variable name after 'as'")
            return cursor - index
        
        var_name = tokens[cursor]
        cursor += 1
        
        # Check for 'do'
        if cursor >= len(tokens) or tokens[cursor] != "do":
            state.add_error("with statement requires 'do'")
            return cursor - index
        
        cursor += 1  # Skip 'do'
        
        # Collect body until 'end'
        body_start = cursor
        depth = 1
        while cursor < len(tokens):
            t = tokens[cursor]
            if t in {"def", "fn", "if", "loop", "while", "switch", "try", "match", "do", "with", "class", "context"}:
                depth += 1
            elif t == "end":
                depth -= 1
                if depth == 0:
                    break
            cursor += 1
        
        if cursor >= len(tokens):
            state.add_error("with statement missing 'end'")
            return cursor - index
        
        body = tokens[body_start:cursor]
        
        # Execute based on resource type
        if resource_type == "file":
            return ContextOpsHandler._with_file(state, args, var_name, body, execute_block, cursor - index)
        elif resource_type == "timer":
            return ContextOpsHandler._with_timer(state, args, var_name, body, execute_block, cursor - index)
        elif resource_type == "transaction" or resource_type == "db_transaction":
            return ContextOpsHandler._with_transaction(state, args, var_name, body, execute_block, cursor - index)
        elif resource_type == "lock":
            return ContextOpsHandler._with_lock(state, args, var_name, body, execute_block, cursor - index)
        else:
            # Check for user-defined context manager
            if hasattr(state, 'context_managers') and state.context_managers:
                ctx = state.context_managers.get(resource_type)
                if ctx:
                    return ContextOpsHandler._with_custom(state, ctx, args, var_name, body, execute_block, cursor - index)
            
            state.add_error(f"Unknown context manager: '{resource_type}'")
            return cursor - index
    
    @staticmethod
    def _with_file(state: InterpreterState, args: List[str], var_name: str,
                  body: List[str], execute_block: Callable, consumed: int) -> int:
        """Handle with file context - auto-close file."""
        if len(args) < 1:
            state.add_error("with file requires a file path")
            return consumed
        
        file_path = args[0].strip('"')
        mode = args[1].strip('"') if len(args) > 1 else "r"
        
        # Store file info for the body to use
        state.strings[var_name] = file_path
        state.variables[f"{var_name}_mode"] = mode
        
        error_occurred = False
        try:
            # Execute body
            execute_block(body)
        except Exception as e:
            error_occurred = True
            state.add_error(f"Error in with block: {e}")
        finally:
            # Cleanup - remove temporary variables
            if var_name in state.strings:
                del state.strings[var_name]
            if f"{var_name}_mode" in state.variables:
                del state.variables[f"{var_name}_mode"]
        
        return consumed
    
    @staticmethod
    def _with_timer(state: InterpreterState, args: List[str], var_name: str,
                   body: List[str], execute_block: Callable, consumed: int) -> int:
        """Handle with timer context - measure execution time."""
        start_time = time.time()
        
        # Store timer name
        state.strings[var_name] = "timer"
        
        error_occurred = False
        try:
            execute_block(body)
        except Exception as e:
            error_occurred = True
            state.add_error(f"Error in with block: {e}")
        finally:
            end_time = time.time()
            elapsed = end_time - start_time
            elapsed_ms = int(elapsed * 1000)
            
            # Store elapsed time
            state.variables[f"{var_name}_elapsed"] = elapsed_ms
            state.add_output(f"[Timer: {elapsed_ms}ms]")
            
            # Cleanup
            if var_name in state.strings:
                del state.strings[var_name]
        
        return consumed
    
    @staticmethod
    def _with_transaction(state: InterpreterState, args: List[str], var_name: str,
                         body: List[str], execute_block: Callable, consumed: int) -> int:
        """Handle with transaction context - auto commit/rollback."""
        from .database import DatabaseHandler
        
        # Begin transaction
        DatabaseHandler.handle_db_begin(state)
        state.strings[var_name] = "transaction"
        
        error_occurred = False
        try:
            execute_block(body)
        except Exception as e:
            error_occurred = True
            state.add_error(f"Transaction error: {e}")
        finally:
            if error_occurred:
                # Rollback on error
                DatabaseHandler.handle_db_rollback(state)
                state.add_output("[Transaction rolled back]")
            else:
                # Commit on success
                DatabaseHandler.handle_db_commit(state)
                state.add_output("[Transaction committed]")
            
            # Cleanup
            if var_name in state.strings:
                del state.strings[var_name]
        
        return consumed
    
    @staticmethod
    def _with_lock(state: InterpreterState, args: List[str], var_name: str,
                  body: List[str], execute_block: Callable, consumed: int) -> int:
        """Handle with lock context - auto lock/unlock mutex."""
        if len(args) < 1:
            state.add_error("with lock requires a mutex name")
            return consumed
        
        mutex_name = args[0]
        
        # Acquire lock
        from .thread_ops import ThreadOpsHandler
        if mutex_name not in state.mutexes:
            state.add_error(f"Mutex '{mutex_name}' not found")
            return consumed
        
        mutex = state.mutexes[mutex_name]
        mutex.acquire()
        state.strings[var_name] = mutex_name
        
        try:
            execute_block(body)
        except Exception as e:
            state.add_error(f"Error in locked block: {e}")
        finally:
            # Always release lock
            mutex.release()
            if var_name in state.strings:
                del state.strings[var_name]
        
        return consumed
    
    @staticmethod
    def _with_custom(state: InterpreterState, ctx: ContextManager, args: List[str],
                    var_name: str, body: List[str], execute_block: Callable,
                    consumed: int) -> int:
        """Handle user-defined context manager."""
        # Set up parameters
        for i, param in enumerate(ctx.params):
            if i < len(args):
                arg_val = args[i]
                # Try to parse as number, else store as string
                try:
                    state.variables[param] = int(arg_val)
                except ValueError:
                    state.strings[param] = arg_val.strip('"')
        
        # Execute enter block
        try:
            execute_block(ctx.enter_body)
        except Exception as e:
            state.add_error(f"Context enter error: {e}")
            return consumed
        
        # Store resource reference
        state.strings[var_name] = ctx.name
        
        error_occurred = False
        try:
            execute_block(body)
        except Exception as e:
            error_occurred = True
            state.add_error(f"Error in context block: {e}")
        finally:
            # Always execute exit block
            try:
                execute_block(ctx.exit_body)
            except Exception as e:
                state.add_error(f"Context exit error: {e}")
            
            # Cleanup parameter variables
            for param in ctx.params:
                if param in state.variables:
                    del state.variables[param]
                if param in state.strings:
                    del state.strings[param]
            
            if var_name in state.strings:
                del state.strings[var_name]
        
        return consumed


def register_builtin_contexts(state: InterpreterState) -> None:
    """Register built-in context managers."""
    if not hasattr(state, 'context_managers') or state.context_managers is None:
        state.context_managers = {}
    
    # These are handled specially in _with_* methods, but we register them
    # for documentation purposes
    pass
