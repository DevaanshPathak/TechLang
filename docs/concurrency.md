# Concurrency & Async in TechLang

TechLang provides features for concurrent and asynchronous programming, allowing you to write efficient programs that perform multiple tasks at once.

## Spawning Threads

Run code in parallel using threads:

```techlang
thread {
    print("Running in a separate thread")
}
print("Main thread continues")
```

## Async Functions

Define and run asynchronous functions:

```techlang
async fn fetch_data() {
    let data = http_get("https://example.com")
    print(data)
}

await fetch_data()
```

## Channels for Communication

Use channels to safely communicate between threads:

```techlang
let ch = channel()
thread {
    ch.send("Hello from thread")
}
let msg = ch.recv()
print(msg)
```

## Synchronization

Use locks to protect shared data:

```techlang
let lock = mutex(0)
thread {
    lock.with(|v| {
        *v = *v + 1
    })
}
```

---

See the [Examples Index](examples.md) for more