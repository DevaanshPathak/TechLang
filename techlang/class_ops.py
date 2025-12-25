"""
Object-Oriented Programming support for TechLang.

This module implements:
- Class definitions with inheritance
- Constructor support (__init__)
- Instance methods with self/this
- Static methods
- Method overriding
"""

from typing import Dict, List, Optional, Tuple, Callable, Union, Any
from .core import InterpreterState
from .blocks import BlockCollector


class ClassDefinition:
    """Represents a class definition in TechLang."""
    
    def __init__(self, name: str, parent: Optional[str] = None):
        self.name = name
        self.parent = parent  # Parent class name for inheritance
        self.fields: Dict[str, Tuple[str, Any]] = {}  # field_name -> (type, default_value)
        self.methods: Dict[str, Dict] = {}  # method_name -> {params, body, is_static}
        self.constructor: Optional[Dict] = None  # {params, body}
    
    def get_all_fields(self, class_defs: Dict[str, 'ClassDefinition']) -> Dict[str, Tuple[str, Any]]:
        """Get all fields including inherited ones."""
        all_fields = {}
        if self.parent and self.parent in class_defs:
            all_fields.update(class_defs[self.parent].get_all_fields(class_defs))
        all_fields.update(self.fields)
        return all_fields
    
    def get_method(self, method_name: str, class_defs: Dict[str, 'ClassDefinition']) -> Optional[Tuple[Dict, str]]:
        """Get a method, checking parent classes if not found. Returns (method_def, defining_class_name)."""
        if method_name in self.methods:
            return (self.methods[method_name], self.name)
        if self.parent and self.parent in class_defs:
            return class_defs[self.parent].get_method(method_name, class_defs)
        return None
    
    def get_constructor(self, class_defs: Dict[str, 'ClassDefinition']) -> Optional[Tuple[Dict, str]]:
        """Get constructor, checking parent if not found. Returns (constructor_def, defining_class_name)."""
        if self.constructor:
            return (self.constructor, self.name)
        if self.parent and self.parent in class_defs:
            return class_defs[self.parent].get_constructor(class_defs)
        return None


class ClassInstance:
    """Represents an instance of a class."""
    
    def __init__(self, class_name: str, fields: Dict[str, Any]):
        self.class_name = class_name
        self.fields = fields  # field_name -> value


class ClassOpsHandler:
    """Handles class-related commands in TechLang."""
    
    @staticmethod
    def handle_class(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Handle class definition:
        class <Name> [extends <Parent>]
            field <name> <type> [default]
            method <name> [params...] ... end
            static <name> [params...] ... end
            init [params...] ... end
        end
        """
        if index + 1 >= len(tokens):
            state.add_error("Invalid 'class' command. Use: class <Name> [extends <Parent>] ... end")
            return 0
        
        class_name = tokens[index + 1]
        if not class_name.isidentifier():
            state.add_error(f"Invalid class name '{class_name}'. Use alphanumeric characters and underscores.")
            return 0
        
        cursor = index + 2
        parent_class = None
        
        # Check for inheritance
        if cursor < len(tokens) and tokens[cursor] == "extends":
            if cursor + 1 >= len(tokens):
                state.add_error("Expected parent class name after 'extends'")
                return 0
            parent_class = tokens[cursor + 1]
            if parent_class not in state.class_defs:
                state.add_error(f"Parent class '{parent_class}' is not defined.")
                return 0
            cursor += 2
        
        # Create class definition
        class_def = ClassDefinition(class_name, parent_class)
        
        # Find the end of the class definition
        end_index = None
        depth = 1
        i = cursor
        while i < len(tokens):
            t = tokens[i]
            if t in {"class", "def", "if", "loop", "while", "switch", "try", "match", "macro", "struct", "method", "static", "init"}:
                depth += 1
            elif t == "end":
                depth -= 1
                if depth == 0:
                    end_index = i
                    break
            i += 1
        
        if end_index is None:
            state.add_error("Class definition missing 'end'.")
            return 0
        
        # Parse class body
        body_tokens = tokens[cursor:end_index]
        j = 0
        while j < len(body_tokens):
            token = body_tokens[j]
            
            if token == "field":
                # field <name> <type> [default_value]
                if j + 2 >= len(body_tokens):
                    state.add_error("Invalid 'field' definition. Use: field <name> <type> [default]")
                    return end_index - index
                
                field_name = body_tokens[j + 1]
                field_type = body_tokens[j + 2]
                default_value = ClassOpsHandler._default_for_type(field_type)
                
                # Check for optional default value
                if j + 3 < len(body_tokens) and body_tokens[j + 3] not in {"field", "method", "static", "init", "end"}:
                    default_token = body_tokens[j + 3]
                    if field_type == "int":
                        try:
                            default_value = int(default_token)
                        except ValueError:
                            pass
                    elif field_type == "string":
                        if default_token.startswith('"') and default_token.endswith('"'):
                            default_value = default_token[1:-1]
                        else:
                            default_value = default_token
                    j += 1
                
                class_def.fields[field_name] = (field_type, default_value)
                j += 3
            
            elif token == "method":
                # method <name> [params...] ... end
                if j + 1 >= len(body_tokens):
                    state.add_error("Invalid 'method' definition. Use: method <name> [params...] ... end")
                    return end_index - index
                
                method_name = body_tokens[j + 1]
                method_def, method_end = ClassOpsHandler._parse_method(body_tokens, j + 2)
                if method_def is None:
                    state.add_error(f"Failed to parse method '{method_name}'")
                    return end_index - index
                
                method_def['is_static'] = False
                class_def.methods[method_name] = method_def
                j = method_end + 1
            
            elif token == "static":
                # static <name> [params...] ... end
                if j + 1 >= len(body_tokens):
                    state.add_error("Invalid 'static' definition. Use: static <name> [params...] ... end")
                    return end_index - index
                
                method_name = body_tokens[j + 1]
                method_def, method_end = ClassOpsHandler._parse_method(body_tokens, j + 2)
                if method_def is None:
                    state.add_error(f"Failed to parse static method '{method_name}'")
                    return end_index - index
                
                method_def['is_static'] = True
                class_def.methods[method_name] = method_def
                j = method_end + 1
            
            elif token == "init":
                # init [params...] ... end
                method_def, method_end = ClassOpsHandler._parse_method(body_tokens, j + 1)
                if method_def is None:
                    state.add_error("Failed to parse constructor")
                    return end_index - index
                
                class_def.constructor = method_def
                j = method_end + 1
            
            else:
                j += 1
        
        # Store class definition
        state.class_defs[class_name] = class_def
        return end_index - index
    
    @staticmethod
    def handle_new(state: InterpreterState, tokens: List[str], index: int, execute_block: Callable) -> int:
        """
        Handle object instantiation:
        new <ClassName> <instance_name> [args...]
        """
        if index + 2 >= len(tokens):
            state.add_error("Invalid 'new' command. Use: new <ClassName> <instance_name> [args...]")
            return 0
        
        class_name = tokens[index + 1]
        instance_name = tokens[index + 2]
        
        if class_name not in state.class_defs:
            state.add_error(f"Class '{class_name}' is not defined.")
            return 2
        
        class_def = state.class_defs[class_name]
        
        # Collect constructor arguments
        args = []
        consumed = 2  # class_name and instance_name
        from .basic_commands import BasicCommandHandler
        
        # Get constructor to know how many args to expect
        constructor_info = class_def.get_constructor(state.class_defs)
        if constructor_info:
            constructor_def, _ = constructor_info
            param_count = len(constructor_def.get('params', []))
            for _ in range(param_count):
                if index + 1 + consumed >= len(tokens):
                    break
                arg_token = tokens[index + 1 + consumed]
                if arg_token in BasicCommandHandler.KNOWN_COMMANDS:
                    break
                args.append(arg_token)
                consumed += 1
        
        # Initialize fields with defaults (including inherited fields)
        all_fields = class_def.get_all_fields(state.class_defs)
        fields = {}
        for field_name, (field_type, default_value) in all_fields.items():
            fields[field_name] = default_value
        
        # Create instance
        instance = ClassInstance(class_name, fields)
        state.instances[instance_name] = instance
        
        # Call constructor if defined
        if constructor_info:
            constructor_def, _ = constructor_info
            ClassOpsHandler._call_method(
                state, instance_name, "__init__", constructor_def, args, execute_block
            )
        
        return consumed
    
    @staticmethod
    def handle_method_call(state: InterpreterState, tokens: List[str], index: int, execute_block: Callable) -> int:
        """
        Handle method call:
        <instance>.<method> [args...] [return_vars...]
        OR: call <instance>.<method> [args...] [return_vars...]
        """
        # Check if this is a method call pattern
        func_token = tokens[index + 1] if index + 1 < len(tokens) else ""
        
        if "." not in func_token:
            return -1  # Not a method call
        
        parts = func_token.split(".", 1)
        instance_name = parts[0]
        method_name = parts[1]
        
        # Check if it's an instance
        if instance_name not in state.instances:
            # Check if it's a static method call (ClassName.method)
            if instance_name in state.class_defs:
                return ClassOpsHandler._handle_static_call(
                    state, instance_name, method_name, tokens, index, execute_block
                )
            return -1  # Not an instance method call
        
        instance = state.instances[instance_name]
        class_def = state.class_defs[instance.class_name]
        
        # Find method (including inherited methods)
        method_info = class_def.get_method(method_name, state.class_defs)
        if method_info is None:
            state.add_error(f"Method '{method_name}' not found in class '{instance.class_name}'")
            return 1
        
        method_def, _ = method_info
        
        if method_def.get('is_static', False):
            state.add_error(f"Cannot call static method '{method_name}' on instance. Use {instance.class_name}.{method_name} instead.")
            return 1
        
        # Collect arguments
        args = []
        consumed = 1  # method token
        from .basic_commands import BasicCommandHandler
        
        param_count = len(method_def.get('params', []))
        for _ in range(param_count):
            if index + 1 + consumed >= len(tokens):
                break
            arg_token = tokens[index + 1 + consumed]
            if arg_token in BasicCommandHandler.KNOWN_COMMANDS:
                break
            args.append(arg_token)
            consumed += 1
        
        # Collect return variable names
        return_vars = []
        while index + 1 + consumed < len(tokens):
            ret_token = tokens[index + 1 + consumed]
            if ret_token in BasicCommandHandler.KNOWN_COMMANDS:
                break
            return_vars.append(ret_token)
            consumed += 1
        
        # Call the method
        ClassOpsHandler._call_method(state, instance_name, method_name, method_def, args, execute_block, return_vars)
        
        return consumed
    
    @staticmethod
    def _handle_static_call(state: InterpreterState, class_name: str, method_name: str, 
                           tokens: List[str], index: int, execute_block: Callable) -> int:
        """Handle static method call: ClassName.method [args...]"""
        class_def = state.class_defs[class_name]
        
        if method_name not in class_def.methods:
            state.add_error(f"Static method '{method_name}' not found in class '{class_name}'")
            return 1
        
        method_def = class_def.methods[method_name]
        
        if not method_def.get('is_static', False):
            state.add_error(f"Method '{method_name}' is not static. Create an instance first.")
            return 1
        
        # Collect arguments
        args = []
        consumed = 1
        from .basic_commands import BasicCommandHandler
        
        param_count = len(method_def.get('params', []))
        for _ in range(param_count):
            if index + 1 + consumed >= len(tokens):
                break
            arg_token = tokens[index + 1 + consumed]
            if arg_token in BasicCommandHandler.KNOWN_COMMANDS:
                break
            args.append(arg_token)
            consumed += 1
        
        # Collect return variables
        return_vars = []
        while index + 1 + consumed < len(tokens):
            ret_token = tokens[index + 1 + consumed]
            if ret_token in BasicCommandHandler.KNOWN_COMMANDS:
                break
            return_vars.append(ret_token)
            consumed += 1
        
        # Call static method (no instance context)
        ClassOpsHandler._call_static_method(state, method_def, args, execute_block, return_vars)
        
        return consumed
    
    @staticmethod
    def _call_method(state: InterpreterState, instance_name: str, method_name: str,
                    method_def: Dict, args: List[str], execute_block: Callable,
                    return_vars: List[str] = None):
        """Execute an instance method with self binding."""
        instance = state.instances[instance_name]
        params = method_def.get('params', [])
        body = method_def.get('body', [])
        
        # Save current state
        saved_vars = {}
        saved_strings = {}
        saved_self = state.variables.get('self')
        saved_this = state.variables.get('this')
        
        # Save parameters
        for param in params:
            if param in state.variables:
                saved_vars[param] = state.variables[param]
            if param in state.strings:
                saved_strings[param] = state.strings[param]
        
        # Bind 'self' and 'this' to instance name
        state.variables['self'] = instance_name
        state.variables['this'] = instance_name
        
        # Bind instance fields to variables
        for field_name, value in instance.fields.items():
            saved_key = f"__field_{field_name}"
            if field_name in state.variables:
                saved_vars[saved_key] = state.variables[field_name]
            if isinstance(value, str):
                state.strings[field_name] = value
            else:
                state.variables[field_name] = value
        
        # Bind arguments to parameters
        for i, param in enumerate(params):
            if i < len(args):
                arg_value = ClassOpsHandler._resolve_arg(state, args[i])
                if isinstance(arg_value, str):
                    state.strings[param] = arg_value
                else:
                    state.variables[param] = arg_value
        
        # Clear return values
        state.return_values.clear()
        state.should_return = False
        
        # Execute method body
        execute_block(body)
        
        # Copy back modified field values to instance
        for field_name in instance.fields:
            if field_name in state.variables:
                instance.fields[field_name] = state.variables[field_name]
            elif field_name in state.strings:
                instance.fields[field_name] = state.strings[field_name]
        
        # Store return values in return_vars
        if return_vars:
            for i, var_name in enumerate(return_vars):
                if i < len(state.return_values):
                    ret_val = state.return_values[i]
                    if isinstance(ret_val, str):
                        state.strings[var_name] = ret_val
                    else:
                        state.variables[var_name] = ret_val
        
        # Restore state
        state.variables['self'] = saved_self
        state.variables['this'] = saved_this
        for param in params:
            if param in saved_vars:
                state.variables[param] = saved_vars[param]
            elif param in state.variables:
                del state.variables[param]
            if param in saved_strings:
                state.strings[param] = saved_strings[param]
            elif param in state.strings:
                del state.strings[param]
        
        state.should_return = False
    
    @staticmethod
    def _call_static_method(state: InterpreterState, method_def: Dict, args: List[str],
                           execute_block: Callable, return_vars: List[str] = None):
        """Execute a static method (no self binding)."""
        params = method_def.get('params', [])
        body = method_def.get('body', [])
        
        # Save current state
        saved_vars = {}
        saved_strings = {}
        for param in params:
            if param in state.variables:
                saved_vars[param] = state.variables[param]
            if param in state.strings:
                saved_strings[param] = state.strings[param]
        
        # Bind arguments to parameters
        for i, param in enumerate(params):
            if i < len(args):
                arg_value = ClassOpsHandler._resolve_arg(state, args[i])
                if isinstance(arg_value, str):
                    state.strings[param] = arg_value
                else:
                    state.variables[param] = arg_value
        
        # Clear return values
        state.return_values.clear()
        state.should_return = False
        
        # Execute method body
        execute_block(body)
        
        # Store return values
        if return_vars:
            for i, var_name in enumerate(return_vars):
                if i < len(state.return_values):
                    ret_val = state.return_values[i]
                    if isinstance(ret_val, str):
                        state.strings[var_name] = ret_val
                    else:
                        state.variables[var_name] = ret_val
        
        # Restore state
        for param in params:
            if param in saved_vars:
                state.variables[param] = saved_vars[param]
            elif param in state.variables:
                del state.variables[param]
            if param in saved_strings:
                state.strings[param] = saved_strings[param]
            elif param in state.strings:
                del state.strings[param]
        
        state.should_return = False
    
    @staticmethod
    def handle_get_field(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get field value: get_field <instance> <field> [target]
        """
        if index + 2 >= len(tokens):
            state.add_error("Invalid 'get_field' command. Use: get_field <instance> <field> [target]")
            return 0
        
        instance_name = tokens[index + 1]
        field_name = tokens[index + 2]
        target = tokens[index + 3] if index + 3 < len(tokens) else None
        
        if instance_name not in state.instances:
            state.add_error(f"Instance '{instance_name}' does not exist.")
            return 2
        
        instance = state.instances[instance_name]
        
        if field_name not in instance.fields:
            state.add_error(f"Field '{field_name}' does not exist on instance '{instance_name}'.")
            return 2
        
        value = instance.fields[field_name]
        
        if target:
            if isinstance(value, str):
                state.strings[target] = value
            else:
                state.variables[target] = value
            return 3
        else:
            state.add_output(str(value))
            return 2
    
    @staticmethod
    def handle_set_field(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Set field value: set_field <instance> <field> <value>
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'set_field' command. Use: set_field <instance> <field> <value>")
            return 0
        
        instance_name = tokens[index + 1]
        field_name = tokens[index + 2]
        value_token = tokens[index + 3]
        
        if instance_name not in state.instances:
            state.add_error(f"Instance '{instance_name}' does not exist.")
            return 3
        
        instance = state.instances[instance_name]
        class_def = state.class_defs[instance.class_name]
        all_fields = class_def.get_all_fields(state.class_defs)
        
        if field_name not in all_fields:
            state.add_error(f"Field '{field_name}' does not exist on class '{instance.class_name}'.")
            return 3
        
        field_type, _ = all_fields[field_name]
        value = ClassOpsHandler._resolve_typed_value(state, value_token, field_type)
        instance.fields[field_name] = value
        
        return 3
    
    @staticmethod
    def handle_instanceof(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check instance type: instanceof <instance> <ClassName> <target>
        Returns 1 if instance is of class (or inherits from it), 0 otherwise.
        """
        if index + 3 >= len(tokens):
            state.add_error("Invalid 'instanceof' command. Use: instanceof <instance> <ClassName> <target>")
            return 0
        
        instance_name = tokens[index + 1]
        class_name = tokens[index + 2]
        target = tokens[index + 3]
        
        if instance_name not in state.instances:
            state.variables[target] = 0
            return 3
        
        instance = state.instances[instance_name]
        
        # Check if instance is of the specified class or inherits from it
        result = ClassOpsHandler._is_instance_of(state, instance.class_name, class_name)
        state.variables[target] = 1 if result else 0
        
        return 3
    
    @staticmethod
    def _is_instance_of(state: InterpreterState, instance_class: str, target_class: str) -> bool:
        """Check if instance_class is or inherits from target_class."""
        if instance_class == target_class:
            return True
        
        if instance_class not in state.class_defs:
            return False
        
        class_def = state.class_defs[instance_class]
        if class_def.parent:
            return ClassOpsHandler._is_instance_of(state, class_def.parent, target_class)
        
        return False
    
    @staticmethod
    def _parse_method(tokens: List[str], start: int) -> Tuple[Optional[Dict], int]:
        """Parse a method definition from tokens, returning (method_def, end_index)."""
        params = []
        cursor = start
        
        # Collect parameters (tokens before method body)
        from .basic_commands import BasicCommandHandler
        while cursor < len(tokens):
            token = tokens[cursor]
            if token == "end" or (token in BasicCommandHandler.KNOWN_COMMANDS and token != "end"):
                break
            if token.startswith('"'):
                break
            params.append(token)
            cursor += 1
        
        # Find method body and end
        body_start = cursor
        depth = 1
        i = body_start
        while i < len(tokens):
            t = tokens[i]
            if t in {"def", "if", "loop", "while", "switch", "try", "match", "method", "static", "init"}:
                depth += 1
            elif t == "end":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        
        if i >= len(tokens):
            return None, start
        
        body = tokens[body_start:i]
        
        return {'params': params, 'body': body}, i
    
    @staticmethod
    def _default_for_type(field_type: str) -> Any:
        """Get default value for a type."""
        if field_type == "int":
            return 0
        if field_type == "string":
            return ""
        if field_type == "bool":
            return 0
        if field_type == "float":
            return 0.0
        return None
    
    @staticmethod
    def _resolve_arg(state: InterpreterState, token: str) -> Union[int, str]:
        """Resolve an argument token to its value."""
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        if token in state.strings:
            return state.strings[token]
        if token in state.variables:
            return state.variables[token]
        try:
            return int(token)
        except ValueError:
            pass
        try:
            return float(token)
        except ValueError:
            pass
        return token
    
    @staticmethod
    def _resolve_typed_value(state: InterpreterState, token: str, field_type: str) -> Any:
        """Resolve a value token according to expected type."""
        if field_type == "int":
            try:
                return int(token)
            except ValueError:
                if token in state.variables:
                    val = state.variables[token]
                    if isinstance(val, int):
                        return val
                return 0
        elif field_type == "string":
            if token.startswith('"') and token.endswith('"'):
                return token[1:-1]
            if token in state.strings:
                return state.strings[token]
            return token
        elif field_type == "float":
            try:
                return float(token)
            except ValueError:
                return 0.0
        elif field_type == "bool":
            if token.lower() in {"true", "1"}:
                return 1
            if token.lower() in {"false", "0"}:
                return 0
            return 0
        return token
