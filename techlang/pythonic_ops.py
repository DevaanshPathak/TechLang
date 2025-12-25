"""
Pythonic Operations for TechLang.

This module implements Python-like features:
- Feature 1: Dataclasses / Named Tuples
- Feature 2: Property Decorators (Getters/Setters)
- Feature 3: in / not in operators
"""

from typing import Dict, List, Optional, Any, Tuple, Callable
from .core import InterpreterState
from .blocks import BlockCollector


# ============================================================================
# Feature 1: Dataclasses / Named Tuples
# ============================================================================

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


# ============================================================================
# Feature 2: Property Decorators
# ============================================================================

class PropertyDefinition:
    """Represents a property with getter and/or setter."""
    
    def __init__(self, name: str):
        self.name = name
        self.getter_body: Optional[List[str]] = None
        self.setter_body: Optional[List[str]] = None
        self.setter_param: Optional[str] = None


# ============================================================================
# Handler Class
# ============================================================================

class PythonicOpsHandler:
    """Handles Pythonic operations in TechLang."""
    
    # ========================================================================
    # Feature 1: Dataclasses
    # ========================================================================
    
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
                default_value = PythonicOpsHandler._default_for_type(field_type)
                
                # Check for default value
                if j + 3 < len(body_tokens) and body_tokens[j + 3] not in {"field", "end"}:
                    default_token = body_tokens[j + 3]
                    default_value = PythonicOpsHandler._parse_value(default_token, field_type)
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
                        fields[field_name] = PythonicOpsHandler._parse_value(value_str, field_type, state)
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
        value = PythonicOpsHandler._resolve_value(state, value_token)
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
    
    # ========================================================================
    # Feature 2: Property Decorators
    # ========================================================================
    
    @staticmethod
    def handle_property_def(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Define a property getter or setter inside a class (parsed during class definition).
        This is called from within class parsing context.
        
        Syntax:
        property <name> get do ... end
        property <name> set <param> do ... end
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'property' definition.")
            return 0
        
        prop_name = tokens[index + 1]
        mode = tokens[index + 2]  # "get" or "set"
        
        if mode not in ("get", "set"):
            state.add_error(f"Property mode must be 'get' or 'set', got '{mode}'")
            return 0
        
        # This function is primarily for use within class parsing
        # For now, store in a temporary location
        return 0
    
    @staticmethod
    def handle_get_property(state: InterpreterState, tokens: List[str], index: int, execute_block: Callable) -> int:
        """
        Get a property value from an instance:
        get_property <instance> <property> <target>
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'get_property'. Use: get_property <instance> <property> <target>")
            return 0
        
        instance_name = tokens[index + 1]
        prop_name = tokens[index + 2]
        target = tokens[index + 3]
        
        # Check regular class instances first
        if instance_name in state.instances:
            instance = state.instances[instance_name]
            class_def = state.class_defs.get(instance.class_name)
            
            if class_def and hasattr(class_def, 'properties') and prop_name in class_def.properties:
                prop = class_def.properties[prop_name]
                if prop.getter_body:
                    # Execute getter with self bound
                    old_self = state.strings.get('self')
                    state.strings['self'] = instance_name
                    
                    # Execute getter body
                    execute_block(prop.getter_body)
                    
                    # Get return value
                    if state.return_values:
                        value = state.return_values.pop()
                        if isinstance(value, str):
                            state.strings[target] = value
                        else:
                            state.set_variable(target, value)
                    
                    # Restore self
                    if old_self is not None:
                        state.strings['self'] = old_self
                    else:
                        state.strings.pop('self', None)
                    
                    state.should_return = False
                    return 3
                else:
                    state.add_error(f"Property '{prop_name}' has no getter defined.")
                    return 3
            
            # Fall back to regular field access
            if prop_name in instance.fields:
                value = instance.fields[prop_name]
                if isinstance(value, str):
                    state.strings[target] = value
                else:
                    state.set_variable(target, value)
                return 3
        
        state.add_error(f"Instance '{instance_name}' not found or property '{prop_name}' not defined.")
        return 3
    
    @staticmethod
    def handle_set_property(state: InterpreterState, tokens: List[str], index: int, execute_block: Callable) -> int:
        """
        Set a property value on an instance:
        set_property <instance> <property> <value>
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'set_property'. Use: set_property <instance> <property> <value>")
            return 0
        
        instance_name = tokens[index + 1]
        prop_name = tokens[index + 2]
        value_token = tokens[index + 3]
        
        # Resolve the value
        value = PythonicOpsHandler._resolve_value(state, value_token)
        
        # Check regular class instances
        if instance_name in state.instances:
            instance = state.instances[instance_name]
            class_def = state.class_defs.get(instance.class_name)
            
            if class_def and hasattr(class_def, 'properties') and prop_name in class_def.properties:
                prop = class_def.properties[prop_name]
                if prop.setter_body and prop.setter_param:
                    # Execute setter with self and value bound
                    old_self = state.strings.get('self')
                    state.strings['self'] = instance_name
                    
                    # Bind the value parameter
                    if isinstance(value, str):
                        state.strings[prop.setter_param] = value
                    else:
                        state.set_variable(prop.setter_param, value)
                    
                    # Execute setter body
                    execute_block(prop.setter_body)
                    
                    # Restore self
                    if old_self is not None:
                        state.strings['self'] = old_self
                    else:
                        state.strings.pop('self', None)
                    
                    state.should_return = False
                    return 3
                else:
                    state.add_error(f"Property '{prop_name}' has no setter defined.")
                    return 3
            
            # Fall back to regular field access
            instance.fields[prop_name] = value
            return 3
        
        state.add_error(f"Instance '{instance_name}' not found.")
        return 3
    
    # ========================================================================
    # Feature 3: in / not in operators
    # ========================================================================
    
    @staticmethod
    def handle_in(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if a value exists in a container (array, dict, string, set).
        Syntax: in <value> <container> <result>
        
        Examples:
            in 5 myarray found      # found=1 if 5 is in myarray
            in "key" mydict found   # found=1 if "key" is a key in mydict
            in "sub" mystring found # found=1 if "sub" is substring of mystring
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'in' command. Use: in <value> <container> <result>")
            return 0
        
        value_token = tokens[index + 1]
        container_name = tokens[index + 2]
        target = tokens[index + 3]
        
        # Resolve the value to search for
        search_value = PythonicOpsHandler._resolve_value(state, value_token)
        
        result = 0
        
        # Check arrays
        if container_name in state.arrays:
            arr = state.arrays[container_name]
            result = 1 if search_value in arr else 0
        
        # Check dictionaries (check keys)
        elif container_name in state.dictionaries:
            d = state.dictionaries[container_name]
            search_key = str(search_value) if not isinstance(search_value, str) else search_value
            result = 1 if search_key in d else 0
        
        # Check strings (substring search)
        elif container_name in state.strings:
            s = state.strings[container_name]
            search_str = str(search_value) if not isinstance(search_value, str) else search_value
            result = 1 if search_str in s else 0
        
        # Check sets
        elif container_name in state.sets:
            st = state.sets[container_name]
            result = 1 if search_value in st else 0
        
        else:
            state.add_error(f"Container '{container_name}' not found (not an array, dict, string, or set).")
            return 3
        
        state.set_variable(target, result)
        return 3
    
    @staticmethod
    def handle_not_in(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if a value does NOT exist in a container.
        Syntax: not_in <value> <container> <result>
        
        Examples:
            not_in 5 myarray found      # found=1 if 5 is NOT in myarray
            not_in "key" mydict found   # found=1 if "key" is NOT a key in mydict
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'not_in' command. Use: not_in <value> <container> <result>")
            return 0
        
        value_token = tokens[index + 1]
        container_name = tokens[index + 2]
        target = tokens[index + 3]
        
        # Resolve the value to search for
        search_value = PythonicOpsHandler._resolve_value(state, value_token)
        
        result = 1  # Default to "not found"
        
        # Check arrays
        if container_name in state.arrays:
            arr = state.arrays[container_name]
            result = 0 if search_value in arr else 1
        
        # Check dictionaries (check keys)
        elif container_name in state.dictionaries:
            d = state.dictionaries[container_name]
            search_key = str(search_value) if not isinstance(search_value, str) else search_value
            result = 0 if search_key in d else 1
        
        # Check strings (substring search)
        elif container_name in state.strings:
            s = state.strings[container_name]
            search_str = str(search_value) if not isinstance(search_value, str) else search_value
            result = 0 if search_str in s else 1
        
        # Check sets
        elif container_name in state.sets:
            st = state.sets[container_name]
            result = 0 if search_value in st else 1
        
        else:
            state.add_error(f"Container '{container_name}' not found (not an array, dict, string, or set).")
            return 3
        
        state.set_variable(target, result)
        return 3
    
    @staticmethod
    def handle_contains(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Alternative syntax: contains <container> <value> <result>
        (container first, like Python's `value in container` but reads left-to-right)
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'contains' command. Use: contains <container> <value> <result>")
            return 0
        
        container_name = tokens[index + 1]
        value_token = tokens[index + 2]
        target = tokens[index + 3]
        
        # Resolve the value to search for
        search_value = PythonicOpsHandler._resolve_value(state, value_token)
        
        result = 0
        
        # Check arrays
        if container_name in state.arrays:
            arr = state.arrays[container_name]
            result = 1 if search_value in arr else 0
        
        # Check dictionaries (check keys)
        elif container_name in state.dictionaries:
            d = state.dictionaries[container_name]
            search_key = str(search_value) if not isinstance(search_value, str) else search_value
            result = 1 if search_key in d else 0
        
        # Check strings (substring search)
        elif container_name in state.strings:
            s = state.strings[container_name]
            search_str = str(search_value) if not isinstance(search_value, str) else search_value
            result = 1 if search_str in s else 0
        
        # Check sets
        elif container_name in state.sets:
            st = state.sets[container_name]
            result = 1 if search_value in st else 0
        
        else:
            state.add_error(f"Container '{container_name}' not found (not an array, dict, string, or set).")
            return 3
        
        state.set_variable(target, result)
        return 3
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
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
