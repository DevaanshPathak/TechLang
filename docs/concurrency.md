# Concurrency & Async in TechLang

TechLang offers a lightweight threading model for running interpreter functions concurrently. Threads share the same database, variables, and outputs, so you can coordinate work without complicated plumbing.

## Creating Work

Define the work you want to run in a regular function, then start it with `thread_create <functionName>`. The command returns a numeric thread identifier.

```techlang
def worker
    print "running in thread"
end

thread_create worker   # → 1
print "main keeps going"
```

`async_start` is an alias for `thread_create`, and `async_wait` behaves like `thread_join`.

## Waiting and Sleeping

Use `thread_join <id>` to wait for a thread to finish. Whatever the thread printed is returned as a single string, preserving newlines.

```techlang
def greet
    print "hello from worker"
end

thread_create greet    # → 1
thread_join 1          # prints "hello from worker"
```

If you simply need a delay without blocking other threads, `thread_sleep <milliseconds>` pauses the current interpreter (main or worker) for the requested duration.

## Inspecting Threads

Three utility commands make coordinating work easier:

* `thread_status <id>` — prints `running` while the thread is alive, otherwise `finished`.
* `thread_result <id>` — returns the cached output captured so far (empty until the thread finishes).
* `thread_list` — prints a space-separated list of thread ids that have been created in the current interpreter.

These commands let you poll without blocking:

```techlang
def job
    thread_sleep 50
    print "done"
end

thread_create job      # → 1
thread_status 1        # running
thread_result 1        # (empty line)
thread_join 1          # done
thread_status 1        # finished
```

## Sharing State

Threads run new interpreter instances that inherit the parent's state snapshot. Mutations to variables, strings, arrays, dictionaries, structs, and database connections are shared. If workers should communicate progress, write to shared variables or push structured output to the main thread via `thread_result` and `thread_join`.

TechLang threads are implemented with Python `threading.Thread` and are best suited to I/O bound tasks or simple background automation.

---

See the [Examples Index](examples.md) for runnable examples.