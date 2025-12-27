"""
Dataclasses / Named Tuples for TechLang.

Provides dataclass-like structures with:
- dataclass <Name> ... end - Define a dataclass
- dataclass_new <Type> <instance> [field=value ...] - Create instance
- dataclass_get <instance> <field> <target> - Get field value
- dataclass_set <instance> <field> <value> - Set field value
- dataclass_eq <a> <b> <result> - Compare equality
- dataclass_str <instance> <target> - Get string representation
- dataclass_to_dict <instance> <target> - Convert to dictionary
"""

from typing import Dict, List, Optional, Any, Tuple
from .core import InterpreterState


class DataclassDefinition:
    """Represents a dataclass definition in TechLang."""
    
    def __init__(self, name: str):
        self.name = name
        self.fields: Dict[str, Tuple[str, Any]] = {}  # field_name -> (type, default_value)
    
    def __repr__(self):
        return f"DataclassDefinition({self.name}, fields={self.fields})"


class DataclassInstance:
    """Represents an instance of a dataclass."""
    
    def __init__(self, class_name: str, fields: Dict[str, Any]):
        self.class_name = class_name
        self.fields = fields
    
    def __repr__(self):
        field_strs = ", ".join(f"{k}={v}" for k, v in self.fields.items())
        return f"{self.class_name}({field_strs})"
    
    def __eq__(self, other):
        if not isinstance(other, DataclassInstance):
            return False
        return self.class_name == other.class_name and self.fields == other.fields


class DataclassHandler:
    """Handles dataclass operations in TechLang."""
    
    @staticmethod
    def _default_for_type(type_name: str) -> Any:
        """Return default value for a type."""
        if type_name in ("int", "number", "float"):
            return 0
        elif type_name in ("string", "str"):
            return ""
        elif type_name in ("bool", "boolean"):
            return 0
        elif type_name == "list" or type_name == "array":
            return []
        elif type_name == "dict":
            return {}
        return None
    
    @staticmethod
    def _parse_value(token: str, field_type: str, state: InterpreterState = None) -> Any:
        """Parse a value token into the appropriate Python type."""
        # Check if it's a quoted string
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        
        # Check if it's a variable reference
        if state is not None:
            if token in state.variables:
                return state.variables[token]
            if token in state.strings:
                return state.strings[token]
        
        # Try numeric parsing based on type
        if field_type in ("int", "number"):
            try:
                return int(token)
            except ValueError:
                try:
                    return float(token)
                except ValueError:
                    return 0
        elif field_type == "float":
            try:
                return float(token)
            except ValueError:
                return 0.0
        elif field_type in ("bool", "boolean"):
            return 1 if token.lower() in ("true", "1", "yes") else 0
        elif field_type in ("string", "str"):
            return token
        
        # Default: try int, then float, then string
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return token
    
    @staticmethod
    def _resolve_value(state: InterpreterState, token: str) -> Any:
        """Resolve a token to its actual value."""
        # Check if it's a quoted string
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        
        # Check variables
        if token in state.variables:
            return state.variables[token]
        
        # Check strings
        if token in state.strings:
            return state.strings[token]
        
        # Try numeric parsing
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return token
    
    @staticmethod
    def handle_dataclass(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Handle dataclass definition:
        dataclass <Name>
            field <name> <type> [default]
            ...
        end
        """
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'dataclass' command. Use: dataclass <Name> ... end")
            return 0
        
        class_name = tokens[index + 1]
        if not class_name.isidentifier():
            state.add_error(f"Invalid dataclass name '{class_name}'.")
            return 0
        
        cursor = index + 2
        
        # Find end of dataclass
        end_index = None
        depth = 1
        i = cursor
        while i < len(tokens):
            t = tokens[i]
            if t in {"dataclass", "class", "def", "if", "loop", "while", "switch", "try", "match", "macro", "struct"}:
                depth += 1
            elif t == "end":
                depth -= 1
                if depth == 0:
                    end_index = i
                    break
            i += 1
        
        if end_index is None:
            state.add_error("Dataclass definition missing 'end'.")
            return 0
        
        # Parse dataclass body
        dc = DataclassDefinition(class_name)
        body_tokens = tokens[cursor:end_index]
        j = 0
        
        while j < len(body_tokens):
            token = body_tokens[j]
            
            if token == "field":
                if j + 2 >= len(body_tokens):
                    state.add_error("Invalid 'field' definition. Use: field <name> <type> [default]")
                    return end_index - index
                
                field_name = body_tokens[j + 1]
                field_type = body_tokens[j + 2]
                default_value = DataclassHandler._default_for_type(field_type)
                
                # Check for default value
                if j + 3 < len(body_tokens) and body_tokens[j + 3] not in {"field", "end"}:
                    default_token = body_tokens[j + 3]
                    default_value = DataclassHandler._parse_value(default_token, field_type)
                    j += 1
                
                dc.fields[field_name] = (field_type, default_value)
                j += 3
            else:
                j += 1
        
        # Store dataclass definition
        if not hasattr(state, 'dataclass_defs') or state.dataclass_defs is None:
            state.dataclass_defs = {}
        state.dataclass_defs[class_name] = dc
        
        return end_index - index
    
    @staticmethod
    def handle_dataclass_new(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Create a dataclass instance:
        dataclass_new <Type> <instance_name> [field=value ...]
        """
        if index + 2 >= len(tokens):
            state.add_error("Invalid 'dataclass_new'. Use: dataclass_new <Type> <instance> [field=value ...]")
            return 0
        
        class_name = tokens[index + 1]
        instance_name = tokens[index + 2]
        
        if not hasattr(state, 'dataclass_defs') or state.dataclass_defs is None:
            state.dataclass_defs = {}
        
        if class_name not in state.dataclass_defs:
            state.add_error(f"Dataclass '{class_name}' is not defined.")
            return 2
        
        dc = state.dataclass_defs[class_name]
        
        # Initialize with defaults
        fields = {}
        for field_name, (field_type, default_value) in dc.fields.items():
            fields[field_name] = default_value
        
        # Parse field=value assignments
        consumed = 2
        from .basic_commands import BasicCommandHandler
        
        i = index + 3
        while i < len(tokens):
            token = tokens[i]
            if token in BasicCommandHandler.KNOWN_COMMANDS or token == "end":
                break
            
            # Check for field=value syntax
            if "=" in token:
                parts = token.split("=", 1)
                if len(parts) == 2:
                    field_name, value_str = parts
                    if field_name in fields:
                        field_type, _ = dc.fields[field_name]
                        fields[field_name] = DataclassHandler._parse_value(value_str, field_type, state)
                consumed += 1
                i += 1
            else:
                break
        
        # Create instance
        if not hasattr(state, 'dataclass_instances') or state.dataclass_instances is None:
            state.dataclass_instances = {}
        
        instance = DataclassInstance(class_name, fields)
        state.dataclass_instances[instance_name] = instance
        
        return consumed
    
    @staticmethod
    def handle_dataclass_get(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get a field from a dataclass instance:
        dataclass_get <instance> <field> <target>
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'dataclass_get'. Use: dataclass_get <instance> <field> <target>")
            return 0
        
        instance_name = tokens[index + 1]
        field_name = tokens[index + 2]
        target = tokens[index + 3]
        
        if not hasattr(state, 'dataclass_instances') or state.dataclass_instances is None:
            state.dataclass_instances = {}
        
        if instance_name not in state.dataclass_instances:
            state.add_error(f"Dataclass instance '{instance_name}' does not exist.")
            return 3
        
        instance = state.dataclass_instances[instance_name]
        
        if field_name not in instance.fields:
            state.add_error(f"Field '{field_name}' does not exist in dataclass '{instance.class_name}'.")
            return 3
        
        value = instance.fields[field_name]
        
        # Store in appropriate container
        if isinstance(value, str):
            state.strings[target] = value
        else:
            state.set_variable(target, value)
        
        return 3
    
    @staticmethod
    def handle_dataclass_set(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Set a field in a dataclass instance:
        dataclass_set <instance> <field> <value>
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'dataclass_set'. Use: dataclass_set <instance> <field> <value>")
            return 0
        
        instance_name = tokens[index + 1]
        field_name = tokens[index + 2]
        value_token = tokens[index + 3]
        
        if not hasattr(state, 'dataclass_instances') or state.dataclass_instances is None:
            state.dataclass_instances = {}
        
        if instance_name not in state.dataclass_instances:
            state.add_error(f"Dataclass instance '{instance_name}' does not exist.")
            return 3
        
        instance = state.dataclass_instances[instance_name]
        
        if field_name not in instance.fields:
            state.add_error(f"Field '{field_name}' does not exist in dataclass '{instance.class_name}'.")
            return 3
        
        # Resolve value
        value = DataclassHandler._resolve_value(state, value_token)
        instance.fields[field_name] = value
        
        return 3
    
    @staticmethod
    def handle_dataclass_eq(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Compare two dataclass instances for equality:
        dataclass_eq <instance1> <instance2> <result>
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'dataclass_eq'. Use: dataclass_eq <a> <b> <result>")
            return 0
        
        name1 = tokens[index + 1]
        name2 = tokens[index + 2]
        target = tokens[index + 3]
        
        if not hasattr(state, 'dataclass_instances') or state.dataclass_instances is None:
            state.dataclass_instances = {}
        
        if name1 not in state.dataclass_instances:
            state.add_error(f"Dataclass instance '{name1}' does not exist.")
            return 3
        
        if name2 not in state.dataclass_instances:
            state.add_error(f"Dataclass instance '{name2}' does not exist.")
            return 3
        
        inst1 = state.dataclass_instances[name1]
        inst2 = state.dataclass_instances[name2]
        
        result = 1 if inst1 == inst2 else 0
        state.set_variable(target, result)
        
        return 3
    
    @staticmethod
    def handle_dataclass_str(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get string representation of a dataclass instance:
        dataclass_str <instance> <target>
        """
        if index + 2 >= len(tokens):
            state.add_error("Invalid 'dataclass_str'. Use: dataclass_str <instance> <target>")
            return 0
        
        instance_name = tokens[index + 1]
        target = tokens[index + 2]
        
        if not hasattr(state, 'dataclass_instances') or state.dataclass_instances is None:
            state.dataclass_instances = {}
        
        if instance_name not in state.dataclass_instances:
            state.add_error(f"Dataclass instance '{instance_name}' does not exist.")
            return 2
        
        instance = state.dataclass_instances[instance_name]
        state.strings[target] = str(instance)
        
        return 2
    
    @staticmethod
    def handle_dataclass_to_dict(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Convert a dataclass instance to a dictionary:
        dataclass_to_dict <instance> <target>
        """
        if index + 2 >= len(tokens):
            state.add_error("Invalid 'dataclass_to_dict'. Use: dataclass_to_dict <instance> <target>")
            return 0
        
        instance_name = tokens[index + 1]
        target = tokens[index + 2]
        
        if not hasattr(state, 'dataclass_instances') or state.dataclass_instances is None:
            state.dataclass_instances = {}
        
        if instance_name not in state.dataclass_instances:
            state.add_error(f"Dataclass instance '{instance_name}' does not exist.")
            return 2
        
        instance = state.dataclass_instances[instance_name]
        state.dictionaries[target] = dict(instance.fields)
        
        return 2
