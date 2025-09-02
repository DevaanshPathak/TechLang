from .core import InterpreterState


class StackHandler:
    # Stack commands for TechLang: push current value, pop to value, and inspect
    
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
        # Note: this prints raw structures so you can see exact values
