"""
Global/Nonlocal Keywords

Provides scope control for variables in nested functions.

Commands:
- global <var> - Declare variable as global (use outer/module-level scope)
- nonlocal <var> - Declare variable from enclosing (non-global) scope

Like Python's global and nonlocal keywords for controlling variable scope.
"""

from typing import List, Set
from .core import InterpreterState


class ScopeOpsHandler:
    """Handler for global/nonlocal scope declarations."""
    
    @staticmethod
    def handle_global(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Declare a variable as global.
        
        Syntax: global <var_name> [var_name2 ...]
        
        Variables declared global will use/modify the global scope value
        instead of creating a local variable.
        
        Example:
            set counter 0
            
            def increment do
                global counter
                add counter 1
            end
        """
        if index + 1 >= len(tokens):
            state.add_error("global requires at least one variable name. Use: global <var> [var2 ...]")
            return 0
        
        # Collect variable names (until we hit a known command or end of tokens)
        from .basic_commands import BasicCommandHandler
        
        consumed = 0
        var_index = index + 1
        
        while var_index < len(tokens):
            var_name = tokens[var_index]
            
            # Stop if we hit a known command
            if var_name in BasicCommandHandler.KNOWN_COMMANDS:
                break
            
            # Stop if we hit a quoted string
            if var_name.startswith('"'):
                break
            
            # Add to global scope declarations
            state.global_vars.add(var_name)
            consumed += 1
            var_index += 1
        
        if consumed == 0:
            state.add_error("global requires at least one variable name. Use: global <var> [var2 ...]")
            return 0
        
        return consumed
    
    @staticmethod
    def handle_nonlocal(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Declare a variable from enclosing (non-global) scope.
        
        Syntax: nonlocal <var_name> [var_name2 ...]
        
        Variables declared nonlocal will use/modify the enclosing function's
        scope instead of creating a local variable.
        
        Example:
            def outer do
                set x 10
                
                def inner do
                    nonlocal x
                    add x 5
                end
                
                call inner
                print x  # 15
            end
        """
        if index + 1 >= len(tokens):
            state.add_error("nonlocal requires at least one variable name. Use: nonlocal <var> [var2 ...]")
            return 0
        
        # Collect variable names
        from .basic_commands import BasicCommandHandler
        
        consumed = 0
        var_index = index + 1
        
        while var_index < len(tokens):
            var_name = tokens[var_index]
            
            # Stop if we hit a known command
            if var_name in BasicCommandHandler.KNOWN_COMMANDS:
                break
            
            # Stop if we hit a quoted string
            if var_name.startswith('"'):
                break
            
            # Add to nonlocal declarations
            state.nonlocal_vars.add(var_name)
            consumed += 1
            var_index += 1
        
        if consumed == 0:
            state.add_error("nonlocal requires at least one variable name. Use: nonlocal <var> [var2 ...]")
            return 0
        
        return consumed
