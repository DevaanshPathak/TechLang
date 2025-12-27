"""
Protocols and Abstract Base Classes

Implements Python-like protocols (structural typing) and abstract base classes (ABCs).

Commands:
- protocol <name> ... end - Define a protocol with required methods
- abstract_class <name> ... end - Define an abstract class
- abstract_method <name> [params...] - Mark method as abstract (must be implemented)
- implements <class> <protocol> - Declare class implements protocol
- protocol_check <obj> <protocol> <result> - Runtime protocol conformance check
"""

from typing import List, Dict, Set, Any
from dataclasses import dataclass, field
from .core import InterpreterState


@dataclass
class Protocol:
    """Protocol definition with required methods."""
    name: str
    required_methods: Set[str] = field(default_factory=set)
    method_signatures: Dict[str, List[str]] = field(default_factory=dict)  # method_name -> params


@dataclass
class AbstractClass:
    """Abstract class definition."""
    name: str
    abstract_methods: Set[str] = field(default_factory=set)
    method_signatures: Dict[str, List[str]] = field(default_factory=dict)


class ProtocolHandler:
    """Handler for protocol and abstract base class operations."""
    
    @staticmethod
    def handle_protocol(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Define a protocol with required methods.
        
        Syntax:
            protocol Drawable
                abstract_method draw
                abstract_method resize width height
            end
        """
        if index + 1 >= len(tokens):
            state.add_error("protocol requires a name. Use: protocol <name> ... end")
            return 0
        
        protocol_name = tokens[index + 1]
        
        # Collect protocol body
        body, end_index = ProtocolHandler._collect_protocol_body(tokens, index + 2)
        
        # Parse abstract methods
        protocol = Protocol(name=protocol_name)
        i = 0
        while i < len(body):
            if body[i] == "abstract_method":
                if i + 1 < len(body):
                    method_name = body[i + 1]
                    params = []
                    j = i + 2
                    # Collect parameters until end of line or next command
                    while j < len(body) and body[j] not in ("abstract_method", "end"):
                        params.append(body[j])
                        j += 1
                    protocol.required_methods.add(method_name)
                    protocol.method_signatures[method_name] = params
                    i = j
                else:
                    i += 1
            else:
                i += 1
        
        # Store protocol
        if not hasattr(state, 'protocols'):
            state.protocols = {}
        state.protocols[protocol_name] = protocol
        
        state.add_output(f"[Protocol '{protocol_name}' defined with {len(protocol.required_methods)} required methods]")
        return end_index - index
    
    @staticmethod
    def handle_abstract_class(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Define an abstract class (cannot be instantiated until all abstract methods are implemented).
        
        Syntax:
            abstract_class Shape
                abstract_method area
                abstract_method perimeter
            end
        """
        if index + 1 >= len(tokens):
            state.add_error("abstract_class requires a name. Use: abstract_class <name> ... end")
            return 0
        
        class_name = tokens[index + 1]
        
        # Collect body
        body, end_index = ProtocolHandler._collect_protocol_body(tokens, index + 2)
        
        # Parse abstract methods
        abstract_class = AbstractClass(name=class_name)
        i = 0
        while i < len(body):
            if body[i] == "abstract_method":
                if i + 1 < len(body):
                    method_name = body[i + 1]
                    params = []
                    j = i + 2
                    # Collect parameters until next command
                    while j < len(body) and body[j] not in ("abstract_method", "end"):
                        params.append(body[j])
                        j += 1
                    abstract_class.abstract_methods.add(method_name)
                    abstract_class.method_signatures[method_name] = params
                    i = j
                else:
                    i += 1
            else:
                i += 1
        
        # Store abstract class
        if not hasattr(state, 'abstract_classes'):
            state.abstract_classes = {}
        state.abstract_classes[class_name] = abstract_class
        
        state.add_output(f"[Abstract class '{class_name}' defined with {len(abstract_class.abstract_methods)} abstract methods]")
        return end_index - index
    
    @staticmethod
    def handle_implements(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Declare that a class implements a protocol.
        
        Syntax:
            implements Rectangle Drawable
        
        This checks at declaration time that the class has all required methods.
        """
        if index + 2 >= len(tokens):
            state.add_error("implements requires a class and protocol. Use: implements <class> <protocol>")
            return 0
        
        class_name = tokens[index + 1]
        protocol_name = tokens[index + 2]
        
        # Check class exists
        if not hasattr(state, 'class_defs') or class_name not in state.class_defs:
            state.add_error(f"Class '{class_name}' not defined")
            return 2
        
        # Check protocol exists
        if not hasattr(state, 'protocols') or protocol_name not in state.protocols:
            state.add_error(f"Protocol '{protocol_name}' not defined")
            return 2
        
        class_def = state.class_defs[class_name]
        protocol = state.protocols[protocol_name]
        
        # Check that class implements all required methods
        missing_methods = []
        for method_name in protocol.required_methods:
            if method_name not in class_def.methods:
                missing_methods.append(method_name)
        
        if missing_methods:
            state.add_error(f"Class '{class_name}' does not implement required methods: {', '.join(missing_methods)}")
            return 2
        
        # Store implementation relationship
        if not hasattr(state, 'protocol_implementations'):
            state.protocol_implementations = {}
        if class_name not in state.protocol_implementations:
            state.protocol_implementations[class_name] = set()
        state.protocol_implementations[class_name].add(protocol_name)
        
        state.add_output(f"[Class '{class_name}' implements protocol '{protocol_name}']")
        return 2
    
    @staticmethod
    def handle_protocol_check(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Check if an object implements a protocol at runtime.
        
        Syntax:
            protocol_check rect Drawable result
        
        Stores 1 in result if object implements protocol, 0 otherwise.
        """
        if index + 3 >= len(tokens):
            state.add_error("protocol_check requires an object, protocol, and result var. Use: protocol_check <obj> <protocol> <result>")
            return 0
        
        obj_name = tokens[index + 1]
        protocol_name = tokens[index + 2]
        result_var = tokens[index + 3]
        
        # Check object exists
        if not hasattr(state, 'instances') or obj_name not in state.instances:
            state.variables[result_var] = 0
            return 3
        
        # Check protocol exists
        if not hasattr(state, 'protocols') or protocol_name not in state.protocols:
            state.add_error(f"Protocol '{protocol_name}' not defined")
            return 3
        
        instance = state.instances[obj_name]
        protocol = state.protocols[protocol_name]
        
        # Check if class implements protocol (by declaration)
        if hasattr(state, 'protocol_implementations'):
            if instance.class_name in state.protocol_implementations:
                if protocol_name in state.protocol_implementations[instance.class_name]:
                    state.variables[result_var] = 1
                    return 3
        
        # Check structurally (duck typing) - does instance have all required methods?
        if instance.class_name in state.class_defs:
            class_def = state.class_defs[instance.class_name]
            has_all_methods = all(method in class_def.methods for method in protocol.required_methods)
            state.variables[result_var] = 1 if has_all_methods else 0
        else:
            state.variables[result_var] = 0
        
        return 3
    
    @staticmethod
    def _collect_protocol_body(tokens: List[str], start: int) -> tuple:
        """Collect tokens until matching 'end'."""
        body = []
        depth = 1
        i = start
        
        while i < len(tokens):
            token = tokens[i]
            
            if token in ("protocol", "abstract_class", "class", "def", "if", "loop", "while"):
                depth += 1
                body.append(token)
            elif token == "end":
                depth -= 1
                if depth == 0:
                    return body, i
                body.append(token)
            else:
                body.append(token)
            i += 1
        
        return body, i
