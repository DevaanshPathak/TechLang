from typing import Dict, List, Optional, Tuple
from .core import InterpreterState


class StructHandler:
    SUPPORTED_TYPES = {"int", "string"}

    @staticmethod
    def handle_struct(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'struct' command. Use: struct <Type> <fields...> end or struct <action> ...")
            return 0

        action = tokens[index + 1]
        if action == "new":
            return StructHandler._handle_new(state, tokens, index)
        if action == "set":
            return StructHandler._handle_set(state, tokens, index)
        if action == "get":
            return StructHandler._handle_get(state, tokens, index)
        if action == "dump":
            return StructHandler._handle_dump(state, tokens, index)

        return StructHandler._handle_definition(state, tokens, index)

    @staticmethod
    def _handle_definition(state: InterpreterState, tokens: List[str], index: int) -> int:
        type_name = tokens[index + 1]
        if not type_name.isidentifier():
            state.add_error(f"Invalid struct name '{type_name}'. Use alphanumeric characters and underscores only.")
            return 0

        fields: Dict[str, str] = {}
        cursor = index + 2
        end_index: Optional[int] = None

        while cursor < len(tokens):
            token = tokens[cursor]
            if token == "end":
                end_index = cursor
                break

            if token == "field":
                if cursor + 2 >= len(tokens):
                    state.add_error("Invalid field definition. Use: field <name> <type>")
                    return 0
                field_name = tokens[cursor + 1]
                field_type = tokens[cursor + 2]
                cursor += 3
            else:
                if ":" not in token:
                    state.add_error(f"Invalid field spec '{token}'. Use <name>:<type> or 'field <name> <type>'.")
                    return 0
                field_name, field_type = token.split(":", 1)
                cursor += 1

            if field_name in fields:
                state.add_error(f"Duplicate field '{field_name}' in struct '{type_name}'.")
                return 0
            if field_type not in StructHandler.SUPPORTED_TYPES:
                state.add_error(f"Unsupported field type '{field_type}'. Supported: {', '.join(sorted(StructHandler.SUPPORTED_TYPES))}.")
                return 0
            fields[field_name] = field_type

        if end_index is None:
            state.add_error("Struct definition missing 'end'.")
            return 0

        state.struct_defs[type_name] = fields
        return end_index - index

    @staticmethod
    def _handle_new(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'struct new' command. Use: struct new <Type> <instance>")
            return 0

        type_name = tokens[index + 2]
        instance_name = tokens[index + 3]

        if type_name not in state.struct_defs:
            state.add_error(f"Struct type '{type_name}' is not defined. Define it before creating instances.")
            return 0

        defaults = {
            field: StructHandler._default_for(field_type)
            for field, field_type in state.struct_defs[type_name].items()
        }
        state.structs[instance_name] = {"type": type_name, "fields": defaults}
        state.add_output(f"Struct '{instance_name}' of type '{type_name}' created")
        return 3

    @staticmethod
    def _handle_set(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 4 >= len(tokens):
            state.add_error("Invalid 'struct set' command. Use: struct set <instance> <field> <value>")
            return 0

        instance_name = tokens[index + 2]
        field_name = tokens[index + 3]
        value_token = tokens[index + 4]

        instance = StructHandler._get_instance(state, instance_name)
        if instance is None:
            return 0

        fields = instance["fields"]
        if field_name not in fields:
            state.add_error(f"Field '{field_name}' does not exist on struct '{instance_name}'.")
            return 0

        field_type = state.struct_defs[instance["type"]][field_name]
        value, ok = StructHandler._resolve_value(state, value_token, field_type)
        if not ok:
            return 4

        fields[field_name] = value
        return 4

    @staticmethod
    def _handle_get(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'struct get' command. Use: struct get <instance> <field>")
            return 0

        instance_name = tokens[index + 2]
        field_name = tokens[index + 3]
        instance = StructHandler._get_instance(state, instance_name)
        if instance is None:
            return 0

        fields = instance["fields"]
        if field_name not in fields:
            state.add_error(f"Field '{field_name}' does not exist on struct '{instance_name}'.")
            return 0

        value = fields[field_name]
        state.add_output(str(value))
        return 3

    @staticmethod
    def _handle_dump(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 2 >= len(tokens):
            state.add_error("Invalid 'struct dump' command. Use: struct dump <instance>")
            return 0

        instance_name = tokens[index + 2]
        instance = StructHandler._get_instance(state, instance_name)
        if instance is None:
            return 0

        state.add_output(StructHandler.format_instance(instance))
        return 2

    @staticmethod
    def format_instance(instance: Dict[str, object]) -> str:
        type_name = instance.get("type", "<unknown>")
        fields: Dict[str, object] = instance.get("fields", {})
        rendered_parts = []
        for field, value in fields.items():
            if isinstance(value, str):
                rendered_parts.append(f"{field}: \"{value}\"")
            else:
                rendered_parts.append(f"{field}: {value}")
        inner = ", ".join(rendered_parts)
        return f"{type_name}{{{inner}}}"

    @staticmethod
    def _default_for(field_type: str) -> object:
        if field_type == "int":
            return 0
        if field_type == "string":
            return ""
        return None

    @staticmethod
    def _resolve_value(state: InterpreterState, token: str, field_type: str) -> Tuple[object, bool]:
        if field_type == "int":
            try:
                return int(token), True
            except ValueError:
                if state.has_variable(token):
                    value = state.get_variable(token)
                    if isinstance(value, int):
                        return value, True
                state.add_error(f"Value '{token}' is not a valid integer for field type 'int'.")
                return 0, False

        # string handling
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1], True
        if token in state.strings:
            return state.strings[token], True
        if state.has_variable(token):
            value = state.get_variable(token)
            if isinstance(value, str):
                return value, True
            if isinstance(value, int):
                return str(value), True
        return token, True

    @staticmethod
    def _get_instance(state: InterpreterState, instance_name: str) -> Optional[Dict[str, object]]:
        instance = state.structs.get(instance_name)
        if instance is None:
            state.add_error(f"Struct instance '{instance_name}' does not exist.")
            return None
        return instance