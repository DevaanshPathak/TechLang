"""
Property Decorators (Getters/Setters) for TechLang.

Provides property-like behavior with:
- property <name> get do ... end - Define getter
- property <name> set <param> do ... end - Define setter
- get_property <instance> <property> <target> - Get property value
- set_property <instance> <property> <value> - Set property value
"""

from typing import Dict, List, Optional, Any, Callable
from .core import InterpreterState


class PropertyDefinition:
    """Represents a property with getter and/or setter."""
    
    def __init__(self, name: str):
        self.name = name
        self.getter_body: Optional[List[str]] = None
        self.setter_body: Optional[List[str]] = None
        self.setter_param: Optional[str] = None


class PropertyHandler:
    """Handles property operations in TechLang."""
    
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
        value = PropertyHandler._resolve_value(state, value_token)
        
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
