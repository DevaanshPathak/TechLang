from dataclasses import dataclass
from typing import Dict, List, Optional
from .core import InterpreterState
from .blocks import BlockCollector


@dataclass
class MacroDefinition:
    name: str
    parameters: List[str]
    body: List[str]
    condition: Optional[str] = None  # Optional condition for conditional expansion


class MacroHandler:
    """Collects and expands compile-time macros before execution with conditional expansion support."""

    @staticmethod
    def process_macros(tokens: List[str], state: InterpreterState, expand_inline: bool = True) -> List[str]:
        """
        Process macro definitions and optionally expand inline calls.
        
        Args:
            tokens: List of tokens to process
            state: Interpreter state
            expand_inline: If True, expand inline calls immediately. If False, leave them for runtime expansion.
        """
        macros, without_definitions = MacroHandler._collect_macros(tokens, state)
        state.macros = macros
        
        if expand_inline:
            return MacroHandler._expand_macros(without_definitions, state)
        else:
            return without_definitions

    @staticmethod
    def load_macro_library(library_name: str, state: InterpreterState, base_dir: Optional[str] = None) -> bool:
        """Load macros from a .tl file into the state's macro collection."""
        import os
        from .parser import parse
        
        # Resolve library path
        if base_dir:
            library_path = os.path.join(base_dir, f"{library_name}.tl")
        else:
            library_path = f"{library_name}.tl"
        
        if not os.path.exists(library_path):
            state.add_error(f"Macro library '{library_name}' not found at {library_path}")
            return False
        
        try:
            with open(library_path, 'r', encoding='utf-8') as f:
                library_code = f.read()
            
            # Parse and collect macros from library
            library_tokens = parse(library_code)
            library_macros, _ = MacroHandler._collect_macros(library_tokens, state)
            
            # Merge into state's macros
            if state.macros is None:
                state.macros = {}
            state.macros.update(library_macros)
            
            return True
        except Exception as e:
            state.add_error(f"Error loading macro library '{library_name}': {e}")
            return False

    @staticmethod
    def _collect_macros(tokens: List[str], state: InterpreterState) -> tuple[Dict[str, MacroDefinition], List[str]]:
        macros: Dict[str, MacroDefinition] = {}
        output: List[str] = []
        i = 0
        length = len(tokens)

        while i < length:
            token = tokens[i]
            if token != "macro":
                output.append(token)
                i += 1
                continue

            if i + 1 >= length:
                state.add_error("Invalid 'macro' definition. Use: macro <name> [params...] do ... end")
                i += 1
                continue

            name = tokens[i + 1]
            params: List[str] = []
            cursor = i + 2
            has_do = False

            while cursor < length:
                current = tokens[cursor]
                if current == "do":
                    cursor += 1
                    has_do = True
                    break
                if current == "end":
                    state.add_error(f"Macro '{name}' is missing a 'do' keyword before its body.")
                    break
                params.append(current)
                cursor += 1
            else:
                state.add_error(f"Macro '{name}' definition is not terminated with 'end'.")
                i = length
                continue

            if cursor > length:
                state.add_error(f"Macro '{name}' definition is incomplete.")
                i = length
                continue

            if not has_do:
                # Skip storing invalid macro; move past the discovered 'end'
                body_tokens, end_index = BlockCollector.collect_block(cursor, tokens)
                i = end_index + 1
                continue

            body_tokens, end_index = BlockCollector.collect_block(cursor, tokens)
            
            # Check for conditional macro (if condition specified before 'do')
            condition = None
            if params and params[0] == 'if' and len(params) > 1:
                # Extract condition: macro name if condition do ... end
                condition = params[1]
                params = params[2:]  # Remove 'if' and condition from params
            
            macros[name] = MacroDefinition(name=name, parameters=params, body=body_tokens, condition=condition)
            i = end_index + 1

        return macros, output

    @staticmethod
    def _expand_macros(tokens: List[str], state: InterpreterState) -> List[str]:
        return MacroHandler._expand_tokens(tokens, state, [])

    @staticmethod
    def _expand_tokens(tokens: List[str], state: InterpreterState, stack: List[str]) -> List[str]:
        result: List[str] = []
        i = 0
        length = len(tokens)

        while i < length:
            token = tokens[i]
            if token != "inline":
                result.append(token)
                i += 1
                continue

            if i + 1 >= length:
                state.add_error("inline requires a macro name")
                i += 1
                continue

            macro_name = tokens[i + 1]
            macro = state.macros.get(macro_name)
            if macro is None:
                state.add_error(f"Macro '{macro_name}' is not defined.")
                i += 2
                continue

            # Check conditional expansion
            if macro.condition:
                condition_met = MacroHandler._check_condition(macro.condition, state)
                if not condition_met:
                    # Skip macro expansion if condition not met
                    i += 2 + len(macro.parameters)
                    continue

            arg_count = len(macro.parameters)
            args = tokens[i + 2 : i + 2 + arg_count]
            if len(args) < arg_count:
                state.add_error(
                    f"Macro '{macro_name}' expects {arg_count} argument(s) but got {len(args)}."
                )
                i += 2 + len(args)
                continue

            if macro_name in stack:
                cycle = " -> ".join(stack + [macro_name])
                state.add_error(f"Recursive macro expansion detected: {cycle}")
                i += 2 + arg_count
                continue

            substitution = {
                param: arg
                for param, arg in zip(macro.parameters, args)
            }

            substituted = [
                substitution.get(token[1:], token)
                if token.startswith("$") and token[1:] in substitution
                else token
                for token in macro.body
            ]

            expanded_body = MacroHandler._expand_tokens(substituted, state, stack + [macro_name])
            result.extend(expanded_body)
            i += 2 + arg_count

        return result

    @staticmethod
    def _check_condition(condition: str, state: InterpreterState) -> bool:
        """Check if a conditional macro should be expanded based on a variable value."""
        # Simple condition check: variable exists and is non-zero
        if condition in state.variables:
            return state.variables[condition] != 0
        return False