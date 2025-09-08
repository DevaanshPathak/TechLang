# File I/O in TechLang

TechLang provides simple and flexible commands for reading from and writing to files.

## Reading Files

Read the entire contents of a file as a string:

```techlang
let text = read("data.txt")
print(text)
```

Read a file line by line:

```techlang
for line in readlines("data.txt") {
    print(line)
}
```

## Writing Files

Write text to a file (overwrites if the file exists):

```techlang
write("output.txt", "Hello, world!")
```

Append text to a file:

```techlang
append("output.txt", "More text\n")
```

## Working with Binary Files

Read and write binary data:

```techlang
let bytes = readbytes("image.png")
writebytes("copy.png", bytes)
```

## File Existence and Deletion

Check if a file exists:

```techlang
if exists("data.txt") {
    print("File found!")
}
```

Delete a file:

```techlang
remove("output.txt")
```

---

See the [Examples Index](examples.md) for more