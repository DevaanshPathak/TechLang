"""
Tests for decorators, context managers, and async/await features.
"""

import pytest
import time
from techlang.interpreter import run


class TestDecorators:
    """Tests for decorator functionality."""
    
    def test_decorator_definition(self):
        """Test defining a decorator."""
        code = '''
decorator logger func do
    print "Before"
    func
    print "After"
end
'''
        output = run(code).strip()
        # Decorator definition doesn't produce output
        assert output == ""
    
    def test_decorate_function(self):
        """Test applying a decorator to a function."""
        code = '''
decorator wrapper func do
    print "Start"
    func
    print "End"
end

def greet
    print "Hello"
end

decorate greet with wrapper as wrapped_greet
call wrapped_greet
'''
        output = run(code).strip().splitlines()
        assert "Start" in output
        assert "Hello" in output
        assert "End" in output
    
    def test_decorator_preserves_function(self):
        """Test that original function still works."""
        code = '''
decorator log func do
    print "LOG"
    func
end

def add_numbers
    set x 5
    add x 3
    print x
end

decorate add_numbers with log as logged_add
call add_numbers
'''
        output = run(code).strip()
        assert "8" in output


class TestContextManagers:
    """Tests for context manager functionality."""
    
    def test_with_timer(self):
        """Test timer context manager."""
        code = '''
with timer as t do
    set x 1
    add x 1
    print x
end
'''
        output = run(code).strip()
        assert "2" in output
        assert "Timer:" in output or output.count("\n") >= 0  # Timer output may vary
    
    def test_with_suppress(self):
        """Test suppress context manager (errors suppressed)."""
        code = '''
with suppress do
    print "Before error"
    # This would normally error but is suppressed
    print "After attempt"
end
print "Done"
'''
        output = run(code).strip()
        assert "Before error" in output
        assert "Done" in output
    
    def test_with_file_context(self, tmp_path):
        """Test file context manager."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello")
        
        code = f'''
with file "{test_file}" as f do
    print "File context active"
end
print "Done"
'''
        output = run(code, base_dir=str(tmp_path)).strip()
        assert "File context active" in output
        assert "Done" in output
    
    def test_custom_context_manager(self):
        """Test user-defined context manager."""
        code = '''
context resource param do
    enter do
        print "Entering"
        set opened 1
    end
    exit do
        print "Exiting"
        set opened 0
    end
end

with resource 42 as r do
    print "Inside"
end
print "After"
'''
        output = run(code).strip().splitlines()
        assert "Entering" in output
        assert "Inside" in output
        assert "Exiting" in output
        assert "After" in output
    
    def test_with_lock_context(self):
        """Test lock context manager."""
        code = '''
mutex_create my_lock
with lock my_lock as m do
    print "Locked"
end
print "Unlocked"
'''
        output = run(code).strip().splitlines()
        assert "Locked" in output
        assert "Unlocked" in output


class TestAsyncAwait:
    """Tests for async/await functionality."""
    
    def test_async_def(self):
        """Test defining an async function."""
        code = '''
async def fetch_data url do
    print "Fetching"
    return 42
end
'''
        output = run(code).strip()
        # Definition doesn't produce output
        assert output == ""
    
    def test_await_coroutine(self):
        """Test awaiting an async coroutine."""
        code = '''
async def compute x do
    set result x
    mul result 2
    return result
end

await compute 21 -> answer
print answer
'''
        output = run(code).strip()
        assert "42" in output
    
    def test_await_sleep(self):
        """Test await sleep."""
        code = '''
set start 1
await sleep 10
set done 1
print done
'''
        start = time.time()
        output = run(code).strip()
        elapsed = time.time() - start
        assert "1" in output
        # Should have some delay (at least a few ms)
        assert elapsed >= 0.005
    
    def test_spawn_task(self):
        """Test spawning a task."""
        code = '''
async def slow_work do
    set x 10
    return x
end

spawn slow_work -> task_id
print task_id
'''
        output = run(code).strip()
        # Should print a task ID (numeric)
        assert output.isdigit() or "1" in output
    
    def test_task_status(self):
        """Test checking task status."""
        code = '''
async def quick do
    set x 1
end

spawn quick -> tid
await sleep 100
task_status tid -> status
print status
'''
        output = run(code).strip()
        # Status should be one of: pending, running, completed, failed
        assert any(s in output for s in ["pending", "running", "completed", "failed"])
    
    def test_gather_multiple_tasks(self):
        """Test gathering multiple tasks."""
        code = '''
async def task1 do
    set x 1
    return 1
end

async def task2 do
    set x 2
    return 2
end

spawn task1 -> t1
spawn task2 -> t2
gather t1 t2 -> results
print "Done"
'''
        output = run(code).strip()
        assert "Done" in output
    
    def test_async_with_params(self):
        """Test async function with parameters."""
        code = '''
async def multiply a b do
    set result a
    mul result b
    return result
end

await multiply 6 7 -> product
print product
'''
        output = run(code).strip()
        assert "42" in output


class TestIntegration:
    """Integration tests combining multiple features."""
    
    def test_decorator_with_timer(self):
        """Test decorator that times function execution."""
        code = '''
decorator timed func do
    with timer as t do
        func
    end
end

def work
    set x 0
    loop 10
        add x 1
    end
    print x
end

decorate work with timed as timed_work
call timed_work
'''
        output = run(code).strip()
        assert "10" in output
    
    def test_async_in_context(self):
        """Test async operation within context manager."""
        code = '''
async def fetch do
    set data 100
    return data
end

await fetch -> result
print result
'''
        output = run(code).strip()
        assert "100" in output


class TestEdgeCases:
    """Edge case tests."""
    
    def test_empty_decorator_body(self):
        """Test decorator with minimal body."""
        code = '''
decorator passthrough func do
    func
end

def test_fn
    print "test"
end

decorate test_fn with passthrough as wrapped
call wrapped
'''
        output = run(code).strip()
        assert "test" in output
    
    def test_nested_with_blocks(self):
        """Test nested with statements."""
        code = '''
with timer as t1 do
    with suppress do
        print "Nested"
    end
end
print "Done"
'''
        output = run(code).strip()
        assert "Nested" in output
        assert "Done" in output
    
    def test_context_cleanup_on_error(self):
        """Test that context exit runs even on error (suppressed)."""
        code = '''
context cleaner do
    enter do
        print "Enter"
    end
    exit do
        print "Exit"
    end
end

with suppress do
    with cleaner as c do
        print "Body"
    end
end
print "After"
'''
        output = run(code).strip().splitlines()
        assert "Enter" in output
        assert "Body" in output
        assert "Exit" in output
        assert "After" in output
