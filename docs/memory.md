# Memory Management in TechLang

TechLang manages memory automatically, but also provides commands for advanced control and inspection.

## Automatic Memory Management

Most objects are managed automatically. Unused memory is reclaimed by the garbage collector.

## Manual Resource Management

For resources like files or sockets, always close them when done:

```techlang
let f = open("file.txt")
... // use the file
f.close()
```

## Inspecting Memory Usage

Check current memory usage:

```techlang
let mem = memory_usage()
print("Memory used:", mem, "bytes")
```

## Freeing Unused Memory

Request a manual garbage collection (optional):

```techlang
gc_collect()
```

## Working with Large Data

When handling large datasets, process data in chunks to reduce memory usage:

```techlang
for line in readlines("largefile.txt") {
    process(line)
}
```

---

See the