"""
is / is_not (Identity Check)

Provides identity checking for objects like Python's 'is' and 'is not'.

Commands:
- is <obj1> <obj2> <result> - Check if two names refer to the same object (1 if same, 0 if different)
- is_not <obj1> <obj2> <result> - Check if two names refer to different objects (1 if different, 0 if same)
"""

from typing import List
from .core import InterpreterState


class IdentityHandler:
    """Handler for identity check commands (is, is_not)."""
    
    @staticmethod
    def handle_is(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if two names refer to the same object (identity check).
        
        Syntax: is <obj1> <obj2> <result>
        
        Sets result to 1 if obj1 and obj2 reference the same object,
        0 if they are different objects (even if equal in value).
        
        For primitives (numbers), identity is based on the same variable name
        or same literal value. For collections (arrays, dicts), checks if
        they're the same underlying object.
        
        Example:
            array_create a
            array_set a b
            is a b result  # result = 1 (same object)
            
            array_create c
            is a c result  # result = 0 (different objects)
        """
        if index + 3 >= len(tokens):
            state.add_error("is requires: is <obj1> <obj2> <result>")
            return 0
        
        obj1_name = tokens[index + 1]
        obj2_name = tokens[index + 2]
        result_name = tokens[index + 3]
        
        # Strip quotes if present
        if obj1_name.startswith('"') and obj1_name.endswith('"'):
            obj1_name = obj1_name[1:-1]
        if obj2_name.startswith('"') and obj2_name.endswith('"'):
            obj2_name = obj2_name[1:-1]
        
        # Get the actual objects
        obj1 = IdentityHandler._get_object(state, obj1_name)
        obj2 = IdentityHandler._get_object(state, obj2_name)
        
        # Check identity using Python's 'is'
        if obj1 is not None and obj2 is not None:
            result = 1 if obj1 is obj2 else 0
        elif obj1 is None and obj2 is None:
            # Both don't exist - check if same name
            result = 1 if obj1_name == obj2_name else 0
        else:
            result = 0
        
        state.variables[result_name] = result
        return 3
    
    @staticmethod
    def handle_is_not(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if two names refer to different objects (inverse identity check).
        
        Syntax: is_not <obj1> <obj2> <result>
        
        Sets result to 1 if obj1 and obj2 are different objects,
        0 if they reference the same object.
        
        Example:
            array_create a
            array_create b
            is_not a b result  # result = 1 (different objects)
        """
        if index + 3 >= len(tokens):
            state.add_error("is_not requires: is_not <obj1> <obj2> <result>")
            return 0
        
        obj1_name = tokens[index + 1]
        obj2_name = tokens[index + 2]
        result_name = tokens[index + 3]
        
        # Strip quotes if present
        if obj1_name.startswith('"') and obj1_name.endswith('"'):
            obj1_name = obj1_name[1:-1]
        if obj2_name.startswith('"') and obj2_name.endswith('"'):
            obj2_name = obj2_name[1:-1]
        
        # Get the actual objects
        obj1 = IdentityHandler._get_object(state, obj1_name)
        obj2 = IdentityHandler._get_object(state, obj2_name)
        
        # Check non-identity
        if obj1 is not None and obj2 is not None:
            result = 0 if obj1 is obj2 else 1
        elif obj1 is None and obj2 is None:
            # Both don't exist - check if same name
            result = 0 if obj1_name == obj2_name else 1
        else:
            result = 1
        
        state.variables[result_name] = result
        return 3
    
    @staticmethod
    def _get_object(state: InterpreterState, name: str):
        """
        Get the actual Python object for a TechLang name.
        Returns the object or None if not found.
        """
        # Check arrays first (most common use case for identity)
        if name in state.arrays:
            return state.arrays[name]
        
        # Check dictionaries
        if name in state.dictionaries:
            return state.dictionaries[name]
        
        # Check sets
        if hasattr(state, 'sets') and name in state.sets:
            return state.sets[name]
        
        # Check strings
        if name in state.strings:
            return state.strings[name]
        
        # Check variables (primitives)
        if name in state.variables:
            return state.variables[name]
        
        # Check class instances
        if hasattr(state, 'instances') and name in state.instances:
            return state.instances[name]
        
        # Check structs
        if hasattr(state, 'struct_instances') and name in state.struct_instances:
            return state.struct_instances[name]
        
        return None
