# techlang/stack.py

from .core import InterpreterState


class StackHandler:
    """Handles stack operations in TechLang."""
    
    @staticmethod
    def handle_upload(state: InterpreterState) -> None:
        """
        Handle the 'upload' command to push current value onto stack.
        
        Args:
            state: The interpreter state
        """
        state.push_stack(state.value)
    
    @staticmethod
    def handle_download(state: InterpreterState) -> None:
        """
        Handle the 'download' command to pop value from stack.
        
        Args:
            state: The interpreter state
        """
        try:
            state.value = state.pop_stack()
        except IndexError:
            state.add_error("Cannot download from empty stack. Use 'upload' to add values to the stack first.")
    
    @staticmethod
    def handle_fork(state: InterpreterState) -> None:
        """
        Handle the 'fork' command to duplicate current value on stack.
        
        Args:
            state: The interpreter state
        """
        state.push_stack(state.value)
    
    @staticmethod
    def handle_debug(state: InterpreterState) -> None:
        """
        Handle the 'debug' command to display stack and variables.
        
        Args:
            state: The interpreter state
        """
        state.add_output(f"Stack: {state.stack}")
        state.add_output(f"Vars: {state.variables}")
