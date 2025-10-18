from dataclasses import dataclass
from typing import Dict, List
from .core import InterpreterState
from .blocks import BlockCollector


@dataclass
class MacroDefinition:
    name: str
    parameters: List[str]
    body: List[str]


class MacroHandler:
    """Collects and expands compile-time macros before execution."""

    @staticmethod
    def process_macros(tokens: List[str], state: InterpreterState) -> List[str]:
        macros, without_definitions = MacroHandler._collect_macros(tokens, state)
        state.macros = macros
        return MacroHandler._expand_macros(without_definitions, state)

    @staticmethod
    def _collect_macros(tokens: List[str], state: InterpreterState) -> (Dict[str, MacroDefinition], List[str]):
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
            macros[name] = MacroDefinition(name=name, parameters=params, body=body_tokens)
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