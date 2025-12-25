"""
Async/Await Event Loop support for TechLang.

This module implements a proper async/await system with:
- async def for defining coroutines
- await for waiting on async operations
- Event loop for scheduling and running coroutines
- Async utilities: gather, sleep, timeout

The event loop is cooperative - coroutines yield control at await points.
"""

from typing import Dict, List, Optional, Any, Callable, Set
from .core import InterpreterState
import threading
import time
import queue
import concurrent.futures
from dataclasses import dataclass, field
from enum import Enum


class TaskState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class AsyncTask:
    """Represents an async task (coroutine instance)."""
    task_id: int
    name: str
    body: List[str]  # The coroutine body tokens
    state: TaskState = TaskState.PENDING
    result: Any = None
    error: Optional[str] = None
    awaiting_task: Optional[int] = None  # Task we're waiting on
    callbacks: List[Callable] = field(default_factory=list)
    
    def __repr__(self):
        return f"<Task {self.task_id}: {self.name} ({self.state.value})>"


@dataclass
class AsyncCoroutine:
    """Represents an async function definition (not yet called)."""
    name: str
    params: List[str]
    body: List[str]
    
    def __repr__(self):
        return f"<async {self.name}({', '.join(self.params)})>"


class EventLoop:
    """Simple cooperative event loop for async operations."""
    
    def __init__(self):
        self.tasks: Dict[int, AsyncTask] = {}
        self.ready_queue: queue.Queue = queue.Queue()
        self.next_task_id: int = 1
        self.running: bool = False
        self.current_task: Optional[AsyncTask] = None
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    
    def create_task(self, name: str, body: List[str]) -> AsyncTask:
        """Create a new task from a coroutine body."""
        task = AsyncTask(
            task_id=self.next_task_id,
            name=name,
            body=body
        )
        self.next_task_id += 1
        self.tasks[task.task_id] = task
        self.ready_queue.put(task.task_id)
        return task
    
    def get_task(self, task_id: int) -> Optional[AsyncTask]:
        """Get a task by ID."""
        return self.tasks.get(task_id)
    
    def complete_task(self, task_id: int, result: Any = None, error: str = None):
        """Mark a task as completed."""
        task = self.tasks.get(task_id)
        if task:
            if error:
                task.state = TaskState.FAILED
                task.error = error
            else:
                task.state = TaskState.COMPLETED
                task.result = result
            
            # Wake up tasks waiting on this one
            for tid, t in self.tasks.items():
                if t.awaiting_task == task_id:
                    t.awaiting_task = None
                    self.ready_queue.put(tid)
            
            # Run callbacks
            for cb in task.callbacks:
                try:
                    cb(result, error)
                except Exception:
                    pass
    
    def cancel_task(self, task_id: int):
        """Cancel a task."""
        task = self.tasks.get(task_id)
        if task and task.state == TaskState.PENDING:
            task.state = TaskState.CANCELLED
    
    def shutdown(self):
        """Shutdown the executor."""
        self._executor.shutdown(wait=False)


class AsyncOpsHandler:
    """Handles async/await operations in TechLang."""
    
    # Global event loop
    _event_loop: Optional[EventLoop] = None
    
    @classmethod
    def get_event_loop(cls) -> EventLoop:
        """Get or create the global event loop."""
        if cls._event_loop is None:
            cls._event_loop = EventLoop()
        return cls._event_loop
    
    @staticmethod
    def handle_async_def(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Define an async function (coroutine):
        async def <name> [params...] do ... end
        """
        if index + 2 >= len(tokens):
            state.add_error("Invalid async def. Use: async def <name> [params...] do ... end")
            return 0
        
        # Skip 'async' - next should be 'def'
        if tokens[index + 1] != "def":
            state.add_error("Expected 'def' after 'async'")
            return 0
        
        func_name = tokens[index + 2]
        cursor = index + 3
        
        # Collect parameters until 'do'
        params = []
        while cursor < len(tokens) and tokens[cursor] != "do":
            params.append(tokens[cursor])
            cursor += 1
        
        if cursor >= len(tokens) or tokens[cursor] != "do":
            state.add_error("Expected 'do' in async function definition")
            return cursor - index
        
        cursor += 1  # Skip 'do'
        
        # Find matching 'end'
        body_start = cursor
        depth = 1
        while cursor < len(tokens):
            t = tokens[cursor]
            if t in {"def", "fn", "if", "loop", "while", "switch", "try", "match", "do", "async", "class"}:
                depth += 1
            elif t == "end":
                depth -= 1
                if depth == 0:
                    break
            cursor += 1
        
        if cursor >= len(tokens):
            state.add_error("async function missing 'end'")
            return cursor - index
        
        body = tokens[body_start:cursor]
        
        # Store as async coroutine
        if not hasattr(state, 'async_coroutines') or state.async_coroutines is None:
            state.async_coroutines = {}
        
        coro = AsyncCoroutine(func_name, params, body)
        state.async_coroutines[func_name] = coro
        
        return cursor - index
    
    @staticmethod
    def handle_await(state: InterpreterState, tokens: List[str], index: int,
                    execute_block: Callable) -> int:
        """
        Await an async operation:
        await <async_call_or_task> [-> result_var]
        
        Examples:
        await async_fetch url -> response
        await task_id -> result
        await sleep 1000
        """
        if index + 1 >= len(tokens):
            state.add_error("await requires an expression")
            return 0
        
        what = tokens[index + 1]
        cursor = index + 2
        result_var = None
        
        # DON'T check for result variable early - each branch handles it
        
        # Handle different await types
        if what == "sleep":
            # await sleep <ms>
            if cursor > index + 2:
                # Already parsed ->
                ms = int(tokens[index + 2]) if index + 2 < len(tokens) else 0
            else:
                ms = int(tokens[cursor]) if cursor < len(tokens) else 0
                cursor += 1
            
            time.sleep(ms / 1000.0)
            if result_var:
                state.variables[result_var] = ms
            return cursor - index - 1
        
        elif what.isdigit():
            # await <task_id> - wait for task to complete
            task_id = int(what)
            loop = AsyncOpsHandler.get_event_loop()
            task = loop.get_task(task_id)
            
            if task is None:
                state.add_error(f"Task {task_id} not found")
                return cursor - index - 1
            
            # Simple blocking wait (in real impl would be cooperative)
            timeout = 30  # 30 second timeout
            start = time.time()
            while task.state in (TaskState.PENDING, TaskState.RUNNING):
                if time.time() - start > timeout:
                    state.add_error(f"Task {task_id} timed out")
                    return cursor - index - 1
                time.sleep(0.01)
            
            if task.state == TaskState.COMPLETED:
                if result_var:
                    if isinstance(task.result, (int, float)):
                        state.variables[result_var] = int(task.result)
                    elif isinstance(task.result, str):
                        state.strings[result_var] = task.result
                    else:
                        state.variables[result_var] = 1
            elif task.state == TaskState.FAILED:
                state.add_error(f"Task {task_id} failed: {task.error}")
            
            return cursor - index - 1
        
        else:
            # await <coroutine_name> [args...] -> result
            # Check if it's an async coroutine
            if hasattr(state, 'async_coroutines') and what in state.async_coroutines:
                coro = state.async_coroutines[what]
                
                # Collect arguments
                args = []
                while cursor < len(tokens) and tokens[cursor] != "->" and tokens[cursor] != "end":
                    args.append(tokens[cursor])
                    cursor += 1
                
                # Check for result var again
                if cursor + 1 < len(tokens) and tokens[cursor] == "->":
                    cursor += 1
                    result_var = tokens[cursor]
                    cursor += 1
                
                # Execute coroutine body with args
                # Set up parameters
                for i, param in enumerate(coro.params):
                    if i < len(args):
                        arg = args[i]
                        # Resolve argument value
                        if arg in state.variables:
                            state.variables[param] = state.variables[arg]
                        elif arg in state.strings:
                            state.strings[param] = state.strings[arg]
                        else:
                            try:
                                state.variables[param] = int(arg)
                            except ValueError:
                                state.strings[param] = arg.strip('"')
                
                # Clear return values and should_return flag before execution
                state.return_values.clear()
                state.should_return = False
                
                # Execute body
                execute_block(coro.body)
                
                # Get return value if any
                if result_var:
                    if state.return_values:
                        ret = state.return_values[-1]  # Get last return value
                        if isinstance(ret, (int, float)):
                            state.variables[result_var] = int(ret)
                        else:
                            state.strings[result_var] = str(ret)
                    else:
                        # Check if 'result' variable was set
                        if 'result' in state.variables:
                            state.variables[result_var] = state.variables['result']
                        elif 'result' in state.strings:
                            state.strings[result_var] = state.strings['result']
                
                # Reset should_return flag so execution continues
                state.should_return = False
                
                return cursor - index - 1
            
            state.add_error(f"Cannot await '{what}'")
            return cursor - index - 1
    
    @staticmethod
    def handle_spawn_task(state: InterpreterState, tokens: List[str], index: int,
                         execute_block: Callable, base_dir: str) -> int:
        """
        Spawn an async task (non-blocking):
        spawn <coroutine_name> [args...] -> task_id
        
        Returns immediately with a task ID that can be awaited later.
        """
        if index + 1 >= len(tokens):
            state.add_error("spawn requires a coroutine name")
            return 0
        
        coro_name = tokens[index + 1]
        cursor = index + 2
        
        # Check for async coroutine
        if not hasattr(state, 'async_coroutines') or coro_name not in state.async_coroutines:
            state.add_error(f"Async coroutine '{coro_name}' not defined")
            return 1
        
        coro = state.async_coroutines[coro_name]
        
        # Collect arguments
        args = []
        while cursor < len(tokens) and tokens[cursor] != "->" and tokens[cursor] not in {"end", "await", "spawn"}:
            if tokens[cursor] not in state.async_coroutines:  # Don't consume next command
                args.append(tokens[cursor])
                cursor += 1
            else:
                break
        
        result_var = None
        if cursor + 1 < len(tokens) and tokens[cursor] == "->":
            cursor += 1
            result_var = tokens[cursor]
            cursor += 1
        
        loop = AsyncOpsHandler.get_event_loop()
        task = loop.create_task(coro_name, coro.body)
        
        # Run task in thread pool
        def run_task():
            try:
                # Create isolated state for task
                from .interpreter import run as run_code
                
                # Build code with arguments
                code_parts = []
                for i, param in enumerate(coro.params):
                    if i < len(args):
                        arg = args[i]
                        if arg in state.variables:
                            code_parts.append(f"set {param} {state.variables[arg]}")
                        elif arg in state.strings:
                            code_parts.append(f'str_create {param} "{state.strings[arg]}"')
                        else:
                            try:
                                int(arg)
                                code_parts.append(f"set {param} {arg}")
                            except ValueError:
                                code_parts.append(f'str_create {param} {arg}')
                
                code_parts.append(' '.join(coro.body))
                code = '\n'.join(code_parts)
                
                result = run_code(code, base_dir=base_dir)
                loop.complete_task(task.task_id, result)
            except Exception as e:
                loop.complete_task(task.task_id, error=str(e))
        
        loop._executor.submit(run_task)
        task.state = TaskState.RUNNING
        
        # Return task ID
        if result_var:
            state.variables[result_var] = task.task_id
        else:
            state.add_output(str(task.task_id))
        
        return cursor - index - 1
    
    @staticmethod
    def handle_gather(state: InterpreterState, tokens: List[str], index: int,
                     execute_block: Callable) -> int:
        """
        Wait for multiple tasks to complete:
        gather task1 task2 task3 -> results_array
        
        Waits for all tasks and collects results.
        """
        if index + 1 >= len(tokens):
            state.add_error("gather requires at least one task ID")
            return 0
        
        cursor = index + 1
        task_ids = []
        
        # Collect task IDs until -> or end
        while cursor < len(tokens) and tokens[cursor] != "->" and tokens[cursor] != "end":
            try:
                tid = int(tokens[cursor])
                task_ids.append(tid)
            except ValueError:
                # Try to resolve variable
                if tokens[cursor] in state.variables:
                    task_ids.append(int(state.variables[tokens[cursor]]))
                else:
                    break
            cursor += 1
        
        result_var = None
        if cursor + 1 < len(tokens) and tokens[cursor] == "->":
            cursor += 1
            result_var = tokens[cursor]
            cursor += 1
        
        if not task_ids:
            state.add_error("gather requires task IDs")
            return cursor - index - 1
        
        loop = AsyncOpsHandler.get_event_loop()
        results = []
        
        # Wait for all tasks
        timeout = 30
        start = time.time()
        for tid in task_ids:
            task = loop.get_task(tid)
            if task is None:
                results.append(f"[Task {tid} not found]")
                continue
            
            while task.state in (TaskState.PENDING, TaskState.RUNNING):
                if time.time() - start > timeout:
                    results.append(f"[Task {tid} timed out]")
                    break
                time.sleep(0.01)
            
            if task.state == TaskState.COMPLETED:
                results.append(str(task.result) if task.result else "")
            elif task.state == TaskState.FAILED:
                results.append(f"[Error: {task.error}]")
            else:
                results.append(f"[{task.state.value}]")
        
        # Store results in array
        if result_var:
            state.arrays[result_var] = results
        else:
            for r in results:
                state.add_output(str(r))
        
        return cursor - index - 1
    
    @staticmethod
    def handle_task_status(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Get task status:
        task_status <task_id> -> status_var
        """
        if index + 1 >= len(tokens):
            state.add_error("task_status requires a task ID")
            return 0
        
        try:
            task_id = int(tokens[index + 1])
        except ValueError:
            if tokens[index + 1] in state.variables:
                task_id = int(state.variables[tokens[index + 1]])
            else:
                state.add_error("task_status requires a numeric task ID")
                return 1
        
        cursor = index + 2
        result_var = None
        
        if cursor + 1 < len(tokens) and tokens[cursor] == "->":
            cursor += 1
            result_var = tokens[cursor]
            cursor += 1
        
        loop = AsyncOpsHandler.get_event_loop()
        task = loop.get_task(task_id)
        
        if task is None:
            status = "not_found"
        else:
            status = task.state.value
        
        if result_var:
            state.strings[result_var] = status
        else:
            state.add_output(status)
        
        return cursor - index - 1
    
    @staticmethod
    def handle_task_cancel(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Cancel a task:
        task_cancel <task_id>
        """
        if index + 1 >= len(tokens):
            state.add_error("task_cancel requires a task ID")
            return 0
        
        try:
            task_id = int(tokens[index + 1])
        except ValueError:
            if tokens[index + 1] in state.variables:
                task_id = int(state.variables[tokens[index + 1]])
            else:
                state.add_error("task_cancel requires a numeric task ID")
                return 1
        
        loop = AsyncOpsHandler.get_event_loop()
        loop.cancel_task(task_id)
        
        return 1
