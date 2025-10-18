from .core import InterpreterState


class StackHandler:
    """
    Handles stack operations in TechLang.
    A stack is like a stack of plates - you can only add or remove from the top.
    This class manages pushing and popping values to/from the stack.
    """
    
    @staticmethod
    def handle_upload(state: InterpreterState) -> None:
        state.push_stack(state.value)
    
    @staticmethod
    def handle_download(state: InterpreterState) -> None:
        try:
            state.value = state.pop_stack()
        except IndexError:
            # Friendly error when users try to pop with nothing on the stack
            state.add_error("Cannot download from empty stack. Use 'upload' to add values to the stack first.")
    
    @staticmethod
    def handle_fork(state: InterpreterState) -> None:
        state.push_stack(state.value)
    
    @staticmethod
    def handle_debug(state: InterpreterState) -> None:
        # Quick snapshot of runtime state to help troubleshoot scripts
        state.add_output(f"Stack: {state.stack}")
        state.add_output(f"Vars: {state.variables}")
        state.add_output(f"Arrays: {state.arrays}")
        state.add_output(f"Strings: {state.strings}")
        state.add_output(f"Dictionaries: {state.dictionaries}")
        state.add_output(f"Structs: {state.structs}")
        # Note: this prints raw structures so you can see exact values
