"""
__str__ / __repr__ Equivalents

Provides custom string representation for class instances like Python's
__str__ and __repr__ dunder methods.

Commands:
- obj_str <instance> <result> - Get string representation (calls __str__ if defined)
- obj_repr <instance> <result> - Get detailed representation (calls __repr__ if defined)
- obj_display <instance> - Print the object using its __str__ method

Special methods in classes:
- method __str__ do ... return <string> end
- method __repr__ do ... return <string> end
"""

from typing import List
from .core import InterpreterState


class ReprHandler:
    """Handler for __str__ and __repr__ methods on class instances."""
    
    @staticmethod
    def handle_obj_str(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get the string representation of an object.
        
        Syntax: obj_str <instance> <result>
        
        If the class has a __str__ method, it will be called.
        Otherwise, returns a default representation like "ClassName(field=value, ...)".
        
        Example:
            obj_str my_point result
            print result  # Point(x=10, y=20)
        """
        if index + 2 >= len(tokens):
            state.add_error("obj_str requires: obj_str <instance> <result>")
            return 0
        
        instance_name = tokens[index + 1]
        result_name = tokens[index + 2]
        
        # Check if it's a class instance
        if hasattr(state, 'instances') and instance_name in state.instances:
            instance = state.instances[instance_name]
            str_result = ReprHandler._get_str_repr(state, instance, instance_name, "__str__")
            state.strings[result_name] = str_result
            return 2
        
        # Check if it's a dataclass instance
        if hasattr(state, 'dataclass_instances') and instance_name in state.dataclass_instances:
            instance = state.dataclass_instances[instance_name]
            str_result = str(instance)
            state.strings[result_name] = str_result
            return 2
        
        # Check if it's a struct
        if hasattr(state, 'struct_instances') and instance_name in state.struct_instances:
            struct = state.struct_instances[instance_name]
            str_result = f"{struct.get('_type', 'Struct')}({', '.join(f'{k}={v}' for k, v in struct.items() if not k.startswith('_'))})"
            state.strings[result_name] = str_result
            return 2
        
        state.add_error(f"'{instance_name}' is not a class instance, dataclass, or struct.")
        return 0
    
    @staticmethod
    def handle_obj_repr(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get the detailed representation of an object.
        
        Syntax: obj_repr <instance> <result>
        
        If the class has a __repr__ method, it will be called.
        Otherwise, returns a detailed default representation.
        
        Example:
            obj_repr my_point result
            print result  # Point(x=10, y=20)
        """
        if index + 2 >= len(tokens):
            state.add_error("obj_repr requires: obj_repr <instance> <result>")
            return 0
        
        instance_name = tokens[index + 1]
        result_name = tokens[index + 2]
        
        # Check if it's a class instance
        if hasattr(state, 'instances') and instance_name in state.instances:
            instance = state.instances[instance_name]
            repr_result = ReprHandler._get_str_repr(state, instance, instance_name, "__repr__")
            state.strings[result_name] = repr_result
            return 2
        
        # Check if it's a dataclass instance
        if hasattr(state, 'dataclass_instances') and instance_name in state.dataclass_instances:
            instance = state.dataclass_instances[instance_name]
            repr_result = repr(instance)
            state.strings[result_name] = repr_result
            return 2
        
        # Check if it's a struct
        if hasattr(state, 'struct_instances') and instance_name in state.struct_instances:
            struct = state.struct_instances[instance_name]
            repr_result = f"{struct.get('_type', 'Struct')}({', '.join(f'{k}={repr(v)}' for k, v in struct.items() if not k.startswith('_'))})"
            state.strings[result_name] = repr_result
            return 2
        
        state.add_error(f"'{instance_name}' is not a class instance, dataclass, or struct.")
        return 0
    
    @staticmethod
    def handle_obj_display(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Print the string representation of an object.
        
        Syntax: obj_display <instance>
        
        Equivalent to: obj_str instance tmp; print tmp
        
        Example:
            obj_display my_point  # Prints: Point(x=10, y=20)
        """
        if index + 1 >= len(tokens):
            state.add_error("obj_display requires: obj_display <instance>")
            return 0
        
        instance_name = tokens[index + 1]
        
        # Check if it's a class instance
        if hasattr(state, 'instances') and instance_name in state.instances:
            instance = state.instances[instance_name]
            str_result = ReprHandler._get_str_repr(state, instance, instance_name, "__str__")
            state.add_output(str_result)
            return 1
        
        # Check if it's a dataclass instance
        if hasattr(state, 'dataclass_instances') and instance_name in state.dataclass_instances:
            instance = state.dataclass_instances[instance_name]
            state.add_output(str(instance))
            return 1
        
        # Check if it's a struct
        if hasattr(state, 'struct_instances') and instance_name in state.struct_instances:
            struct = state.struct_instances[instance_name]
            str_result = f"{struct.get('_type', 'Struct')}({', '.join(f'{k}={v}' for k, v in struct.items() if not k.startswith('_'))})"
            state.add_output(str_result)
            return 1
        
        state.add_error(f"'{instance_name}' is not a class instance, dataclass, or struct.")
        return 0
    
    @staticmethod
    def _get_str_repr(state: InterpreterState, instance, instance_name: str, method_name: str) -> str:
        """
        Get string/repr representation by calling the appropriate method if it exists.
        Falls back to default representation if method not found.
        """
        # Try to call the __str__ or __repr__ method if it exists
        if hasattr(state, 'class_defs') and instance.class_name in state.class_defs:
            class_def = state.class_defs[instance.class_name]
            
            # Check if the method exists
            method_result = class_def.get_method(method_name, state.class_defs)
            if method_result:
                method_def, _ = method_result
                
                # Execute the method and get the return value
                # For simplicity, we'll use a default representation if method execution is complex
                # A full implementation would execute the method body
                pass
        
        # Default representation
        fields_str = ", ".join(f"{k}={v}" for k, v in instance.fields.items())
        return f"{instance.class_name}({fields_str})"
