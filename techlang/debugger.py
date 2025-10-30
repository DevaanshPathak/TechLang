"""
Debugger operations for TechLang.
Provides breakpoints, stepping, and state inspection during execution.
"""

from typing import List
from .core import InterpreterState


class DebuggerHandler:
    """
    Handles debugging operations: breakpoints, stepping, inspection.
    Like a debugger in other languages - helps you see what's happening inside your program.
    """
    
    @staticmethod
    def handle_breakpoint(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Set a breakpoint at the current command position.
        Execution will pause here on next run through.
        Example: breakpoint
        """
        # Add current command position as breakpoint
        state.breakpoints.add(state.command_count)
        state.add_output(f"[Breakpoint set at command #{state.command_count}]")
        return 0
    
    @staticmethod
    def handle_step(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Enable step mode - pause after each command.
        Example: step
        """
        state.stepping = True
        state.debug_mode = True
        state.add_output("[Step mode enabled - will pause after each command]")
        return 0
    
    @staticmethod
    def handle_continue(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Continue execution from a paused state.
        Example: continue
        """
        if state.paused:
            state.paused = False
            state.stepping = False
            state.add_output("[Continuing execution...]")
        else:
            state.add_output("[Not currently paused]")
        return 0
    
    @staticmethod
    def handle_inspect(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Show detailed state information at current point.
        Like debug but more focused on debugging context.
        Example: inspect
        """
        state.add_output(f"=== Debug Inspection (Command #{state.command_count}) ===")
        
        # Stack
        if state.stack:
            state.add_output(f"Stack[{len(state.stack)}]: {state.stack}")
        else:
            state.add_output("Stack: empty")
        
        # Current value
        state.add_output(f"Current Value: {state.value}")
        
        # Variables (only show watched or recent changes if many)
        if state.watched_vars:
            state.add_output(f"Watched Variables:")
            for var in sorted(state.watched_vars):
                if var in state.variables:
                    state.add_output(f"  {var} = {state.variables[var]}")
                elif var in state.strings:
                    state.add_output(f"  {var} = \"{state.strings[var]}\"")
                else:
                    state.add_output(f"  {var} = <not defined>")
        else:
            var_count = len(state.variables)
            if var_count > 0:
                state.add_output(f"Variables[{var_count}]: {dict(list(state.variables.items())[:5])}")
                if var_count > 5:
                    state.add_output(f"  ... and {var_count - 5} more")
        
        # Arrays
        if state.arrays:
            state.add_output(f"Arrays: {list(state.arrays.keys())}")
        
        # Strings
        if state.strings and not state.watched_vars:
            string_count = len(state.strings)
            if string_count > 0:
                state.add_output(f"Strings[{string_count}]: {list(state.strings.keys())[:5]}")
                if string_count > 5:
                    state.add_output(f"  ... and {string_count - 5} more")
        
        # Dictionaries
        if state.dictionaries:
            state.add_output(f"Dictionaries: {list(state.dictionaries.keys())}")
        
        # Breakpoints
        if state.breakpoints:
            state.add_output(f"Breakpoints: {sorted(state.breakpoints)}")
        
        # Debug mode status
        if state.stepping:
            state.add_output("Mode: STEPPING")
        elif state.debug_mode:
            state.add_output("Mode: DEBUG")
        
        state.add_output("=" * 40)
        return 0
    
    @staticmethod
    def handle_watch(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Add a variable to the watch list.
        Watched variables are shown in inspect output.
        Example: watch myvar
        """
        if index + 1 >= len(tokens):
            state.add_error("watch requires a variable name. Use: watch <variable>")
            return 0
        
        var_name = tokens[index + 1]
        state.watched_vars.add(var_name)
        state.add_output(f"[Watching variable '{var_name}']")
        return 1
    
    @staticmethod
    def handle_unwatch(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Remove a variable from the watch list.
        Example: unwatch myvar
        """
        if index + 1 >= len(tokens):
            state.add_error("unwatch requires a variable name. Use: unwatch <variable>")
            return 0
        
        var_name = tokens[index + 1]
        if var_name in state.watched_vars:
            state.watched_vars.remove(var_name)
            state.add_output(f"[Stopped watching '{var_name}']")
        else:
            state.add_output(f"[Variable '{var_name}' was not being watched]")
        return 1
    
    @staticmethod
    def handle_clear_breakpoints(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Clear all breakpoints.
        Example: clear_breakpoints
        """
        count = len(state.breakpoints)
        state.breakpoints.clear()
        state.add_output(f"[Cleared {count} breakpoint(s)]")
        return 0
    
    @staticmethod
    def check_breakpoint(state: InterpreterState) -> bool:
        """
        Check if we should pause at current command.
        Returns True if execution should pause.
        """
        # Check if we hit a breakpoint
        if state.command_count in state.breakpoints:
            state.paused = True
            state.add_output(f"[Hit breakpoint at command #{state.command_count}]")
            return True
        
        # Check if we're stepping
        if state.stepping and state.command_count > 0:
            state.paused = True
            state.add_output(f"[Step: command #{state.command_count}]")
            return True
        
        return False
    
    @staticmethod
    def watch_variable_change(state: InterpreterState, var_name: str, old_value, new_value) -> None:
        """
        Report when a watched variable changes.
        """
        if var_name in state.watched_vars:
            state.add_output(f"[Watch] {var_name}: {old_value} → {new_value}")
