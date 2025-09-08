DevaanshPathak: write me | Control Flow | [docs/control-flow.md](docs/control-flow.md) |

GitHub Copilot: Here is the line you requested:

````markdown
| Control Flow | [docs/control-flow.md](docs/control-flow.md) |
````

DevaanshPathak: i mean write me the text to put in control-flow.md

GitHub Copilot: Here’s a starter for your `docs/control-flow.md` file, covering the basics of control flow in TechLang:

````markdown
# Control Flow in TechLang

Control flow statements determine the order in which instructions are executed in a TechLang program. TechLang supports several control flow constructs, including conditional statements, loops, and branching.

## Conditional Statements

Use `if`, `else if`, and `else` to execute code based on conditions:

```techlang
if x > 0 {
    print("Positive")
} else if x == 0 {
    print("Zero")
} else {
    print("Negative")
}
```

## Loops

### While Loop

Repeat a block of code while a condition is true:

```techlang
while count < 10 {
    print(count)
    count = count + 1
}
```

### For Loop

Iterate over a range or collection:

```techlang
for i in 1..5 {
    print(i)
}
```

## Branching

Use `break` to exit a loop early, and `continue` to skip to the next iteration:

```techlang
for i in 1..10 {
    if i == 5 {
        break
    }
    if i % 2 == 0 {
        continue
    }
    print(i)
}
```

## Match Statement

Pattern matching for concise branching:

```techlang
match value {
    1 => print("One"),
    2 => print("Two"),
    _ => print("Other")
}
```

---

See the [Examples Index](examples.md) for runnable code samples.
````

DevaanshPathak: can you create a file and add it?

Workspace: 

DevaanshPathak: now | Data Types | [docs/data-types.md](docs/data-types.md) |


GitHub Copilot: Here’s a new file for `docs/data-types.md` with an overview of data types in TechLang:

````markdown
# Data Types in TechLang

TechLang provides a variety of built-in data types to support different kinds of data and operations. Understanding these types is essential for writing effective programs.

## Primitive Types

- **Integer (`int`)**: Whole numbers, e.g., `42`, `-7`
- **Float (`float`)**: Decimal numbers, e.g., `3.14`, `-0.001`
- **Boolean (`bool`)**: Logical values, `true` or `false`
- **String (`string`)**: Text data, e.g., `"hello world"`

## Composite Types

- **Array**: Ordered collection of elements of the same type.
  ```techlang
  let numbers = [1, 2, 3, 4]
  ```
- **Tuple**: Fixed-size collection of elements of possibly different types.
  ```techlang
  let point = (3, 4)
  ```
- **Map**: Key-value pairs, similar to dictionaries.
  ```techlang
  let capitals = { "France": "Paris", "Japan": "Tokyo" }
  ```

## Special Types

- **Null (`null`)**: Represents the absence of a value.
- **Any (`any`)**: Can hold a value of any type.

## Type Inference and Annotations

TechLang can infer types, but you can also specify them:

```techlang
let age: int = 30
let name: string = "Alice"
```

## Type Conversion

Convert between types using built-in functions:

```techlang
let n = int("42")      // String to int
let s = string(3.14)   // Float to string
```

---

See the [Examples Index](examples.md) for more code samples.
````

DevaanshPathak: now | Math & Science | [docs/math.md](docs/math.md) |


GitHub Copilot: Here’s a new file for math.md with an overview of math and science features in TechLang:

````markdown
# Math & Science in TechLang

TechLang offers a comprehensive set of mathematical and scientific functions for calculations, analysis, and modeling.

## Basic Arithmetic

Standard operators are supported:

```techlang
let sum = 5 + 3
let diff = 10 - 2
let prod = 4 * 7
let quot = 20 / 5
let rem = 17 % 3
```

## Math Functions

Use built-in functions for advanced math:

```techlang
let r = sqrt(16)         // 4
let p = pow(2, 8)        // 256
let abs_val = abs(-42)   // 42
let rounded = round(3.6) // 4
```

## Trigonometry

Trigonometric functions use radians:

```techlang
let s = sin(3.14 / 2)    // ≈1
let c = cos(0)           // 1
let t = tan(0.785)       // ≈1
```

## Scientific Constants

Common constants are available:

```techlang
let pi_val = PI
let e_val = E
```

## Random Numbers

Generate random values:

```techlang
let r = random()         // 0.0 <= r < 1.0
let n = randint(1, 10)   // Integer between 1 and 10
```

## Scientific Utilities

- **Logarithms:** `log(x)`, `log10(x)`
- **Exponentials:** `exp(x)`
- **Statistics:** `mean([1,2,3])`, `median([1,2,3])`, `std([1,2,3])`

---

See the [Examples Index](examples.md) for more code samples.
````

DevaanshPathak: now | File I/O | [docs/file-io.md](docs/file-io.md) |


GitHub Copilot: ````markdown
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

See the [Examples Index](examples.md) for more code samples.
````

DevaanshPathak: now network.md

GitHub Copilot: ````markdown
# Network & Web in TechLang

TechLang includes built-in commands for basic networking and web operations, making it easy to interact with remote resources.

## HTTP Requests

Fetch the contents of a web page:

```techlang
let html = http_get("https://example.com")
print(html)
```

Send data with a POST request:

```techlang
let response = http_post("https://api.example.com/data", "{ \"key\": \"value\" }")
print(response)
```

## Downloading Files

Download a file from the internet:

```techlang
download("https://example.com/file.zip", "file.zip")
```

## Working with Sockets

Create a simple TCP client:

```techlang
let sock = connect("example.com", 80)
sock.write("GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
let resp = sock.read()
print(resp)
sock.close()
```

## Parsing JSON

Parse JSON data from a web API:

```techlang
let data = json_parse(http_get("https://api.example.com/info"))
print(data["name"])
```

---

See the [Examples Index](examples.md) for more code samples.
````

DevaanshPathak: graphics.md

GitHub Copilot: ````markdown
# Graphics & Visualization in TechLang

TechLang provides commands for creating graphics, drawing shapes, and visualizing data.

## Drawing Shapes

Draw a window and basic shapes:

```techlang
window("My Drawing", 400, 300)
rect(50, 50, 100, 80, color="blue")
circle(200, 150, 40, color="red")
line(10, 10, 390, 290, color="green")
```

## Working with Images

Load and display an image:

```techlang
img = load_image("picture.png")
draw_image(img, 100, 100)
```

Save the current canvas to a file:

```techlang
save_canvas("output.png")
```

## Data Visualization

Plot a simple chart:

```techlang
plot([1, 3, 2, 5, 4], title="Sample Plot")
```

Create a bar chart:

```techlang
bar_chart(["A", "B", "C"], [5, 2, 7], title="Bar Chart")
```

---

See the [Examples Index](examples.md) for more code samples.
````

DevaanshPathak: now database.md

GitHub Copilot: ````markdown
# Database (SQLite3) in TechLang

TechLang supports SQLite3 databases for lightweight, file-based data storage and querying.

## Connecting to a Database

Open or create a database file:

```techlang
let db = sqlite_open("mydata.db")
```

## Creating Tables

Create a new table:

```techlang
db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INT)")
```

## Inserting Data

Insert a record:

```techlang
db.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
```

## Querying Data

Fetch data from a table:

```techlang
let rows = db.query("SELECT * FROM users")
for row in rows {
    print(row["name"], row["age"])
}
```

## Updating and Deleting Data

Update a record:

```techlang
db.execute("UPDATE users SET age = 31 WHERE name = 'Alice'")
```

Delete a record:

```techlang
db.execute("DELETE FROM users WHERE name = 'Alice'")
```

## Closing the Database

Always close the database when done:

```techlang
db.close()
```

---

See the [Examples Index](examples.md) for more code samples.
````

DevaanshPathak: now memory

GitHub Copilot: ````markdown
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

See the [Examples Index](examples.md) for more code samples.
````

DevaanshPathak: now concurrency.md

GitHub Copilot: ````markdown
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

See the [Examples Index](examples.md) for more code samples.
````

DevaanshPathak: now system

GitHub Copilot: ````markdown
# System & Processes in TechLang

TechLang provides commands for interacting with the operating system, running processes, and accessing environment information.

## Running System Commands

Execute a shell command and capture its output:

```techlang
let result = system("echo Hello, world!")
print(result)
```

## Working with Processes

Start a process and interact with it:

```techlang
let proc = process("python", ["script.py"])
let output = proc.read()
print(output)
proc.close()
```

## Environment Variables

Get and set environment variables:

```techlang
let path = getenv("PATH")
setenv("MY_VAR", "value")
```

## File System Operations

List files in a directory:

```techlang
let files = listdir(".")
for f in files {
    print(f)
}
```

Get the current working directory:

```techlang
let cwd = getcwd()
print(cwd)
```

---

See the [Examples Index](examples.md) for more code samples.
````

DevaanshPathak: now help-cli.md

GitHub Copilot: ````markdown
# Help & CLI in TechLang

TechLang includes a command-line interface (CLI) for running scripts, exploring code interactively, and accessing documentation.

## Running Scripts

Execute a TechLang script file:

```sh
tl path/to/script.tl
```

## Interactive REPL

Start an interactive Read-Eval-Print Loop (REPL) session:

```sh
tl -i
```

Type commands and see results immediately.

## Getting Help

Display built-in help:

```sh
tl --help
```

Show version information:

```sh
tl --version
```

## Command-Line Arguments

Pass arguments to your script:

```sh
tl myscript.tl arg1 arg2
```

Access them in your code:

```techlang
for arg in args {
    print(arg)
}
```

## Script Exit Codes

Set the exit code for your script:

```techlang
exit(0)   // Success
exit(1)   // Error
```

---

See the [Examples Index](examples.md) for more code samples.
````

DevaanshPathak: now examples.md

GitHub Copilot: ````markdown
# TechLang Examples Index

This page provides runnable code samples for each major feature of TechLang. Copy and paste these examples into the REPL (`tl -i`) or a `.tl` file to try them out.

---

## General Rules & Syntax

```techlang
// Variable assignment
let x = 10

// Function definition
fn greet(name) {
    print("Hello, " + name)
}

greet("World")
```

---

## Control Flow

```techlang
let n = 5
if n > 0 {
    print("Positive")
} else {
    print("Non-positive")
}
```

---

## Data Types

```techlang
let nums = [1, 2, 3]
let person = { "name": "Alice", "age": 30 }
let point = (3, 4)
```

---

## Math & Science

```techlang
let area = PI * pow(5, 2)
let r = random()
```

---

## File I/O

```techlang
write("hello.txt", "Hello, file!")
let text = read("hello.txt")
print(text)
```

---

## Network & Web

```techlang
let html = http_get("https://example.com")
print(html)
```

---

## Graphics & Visualization

```techlang
window("Demo", 300, 200)
rect(20, 20, 100, 50, color="blue")
```

---

## Database (SQLite3)

```techlang
let db = sqlite_open("test.db")
db.execute("CREATE TABLE t (id INT)")
db.close()
```

---

## Memory Management

```techlang
let mem = memory_usage()
print(mem)
```

---

## Concurrency & Async

```techlang
thread {
    print("Hello from another thread")
}
```

---

## System & Processes

```techlang
let files = listdir(".")
for f in files {
    print(f)
}
```

---

## Help & CLI

```sh
tl --help
tl -i
```

---
````

DevaanshPathak: examples index is too small way to small

GitHub Copilot: I'll create a more comprehensive examples.md file with more detailed examples for each section:

````markdown
# TechLang Examples Index

This page provides runnable code samples for each major feature of TechLang. Copy and paste these examples into the REPL (`tl -i`) or a `.tl` file to try them out.

---

## General Rules & Syntax

### Basic Syntax

```techlang
// Variable assignment
let x = 10
let y = 20
let sum = x + y

// Constants
const PI_VALUE = 3.14159

// Function definition
fn greet(name) {
    print("Hello, " + name)
}

greet("World")

// Multiple return values
fn divide(a, b) {
    if b == 0 {
        return 0, "Division by zero"
    }
    return a / b, nil
}

let result, error = divide(10, 2)
print(result)  // 5
```

### Comments

```techlang
// This is a single line comment

/*
   This is a
   multi-line comment
*/

// Documentation comments
/// Adds two numbers
fn add(a, b) {
    return a + b
}
```

---

## Control Flow

### Conditionals

```techlang
let n = 5

// Basic if-else
if n > 0 {
    print("Positive")
} else if n < 0 {
    print("Negative")
} else {
    print("Zero")
}

// Conditional expression
let status = n > 0 ? "positive" : "non-positive"
print(status)
```

### Loops

```techlang
// For loop with range
for i in 1..5 {
    print(i)
}

// For loop with array
let fruits = ["apple", "banana", "cherry"]
for fruit in fruits {
    print("I like " + fruit)
}

// While loop
let count = 0
while count < 5 {
    print(count)
    count = count + 1
}

// Loop control
for i in 1..10 {
    if i == 3 {
        continue  // Skip to next iteration
    }
    if i == 8 {
        break     // Exit the loop
    }
    print(i)
}
```

### Match Statements

```techlang
let color = "red"

match color {
    "red" => print("Stop"),
    "yellow" => print("Caution"),
    "green" => print("Go"),
    _ => print("Unknown color")
}
```

---

## Data Types

### Primitive Types

```techlang
// Integers
let age = 30
let negative = -10

// Floats
let pi = 3.14159
let temperature = -2.5

// Booleans
let is_active = true
let is_complete = false

// Strings
let name = "Alice"
let message = 'Hello, ' + name
```

### Collection Types

```techlang
// Arrays
let numbers = [1, 2, 3, 4, 5]
print(numbers[0])       // Access by index
numbers[1] = 20         // Modify element
print(numbers.length)   // Get array length

// Adding elements
numbers.push(6)         // Add to end
numbers.insert(0, 0)    // Insert at index

// Removing elements
let last = numbers.pop()    // Remove and return last element
numbers.remove(2)           // Remove at index

// Slicing
let subset = numbers[1..4]  // Get elements from index 1 to 3

// Maps/Dictionaries
let person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

print(person["name"])       // Access by key
person["job"] = "Engineer"  // Add new key-value pair
delete person["city"]       // Remove key-value pair

// Check if key exists
if "age" in person {
    print("Age is", person["age"])
}

// Tuples
let point = (3, 4)
let (x, y) = point      // Destructuring
print(x, y)
```

### Type Conversion

```techlang
// Converting between types
let num_str = "42"
let num = int(num_str)      // String to int
let pi_str = string(3.14)   // Float to string
let is_true = bool(1)       // Int to bool
let char_code = int("A")    // Character to ASCII value
```

---

## Math & Science

### Basic Math

```techlang
// Arithmetic
let sum = 10 + 5
let difference = 20 - 8
let product = 6 * 7
let quotient = 100 / 5
let remainder = 17 % 3
let power = 2 ** 8  // Or pow(2, 8)

// Increment/decrement
let i = 5
i += 1      // i = i + 1
i -= 2      // i = i - 2
```

### Math Functions

```techlang
// Basic math functions
let s = sqrt(16)            // 4
let p = pow(2, 10)          // 1024
let a = abs(-42)            // 42
let r = round(3.7)          // 4
let f = floor(9.8)          // 9
let c = ceil(9.2)           // 10

// Min/max
let minimum = min(5, 10)    // 5
let maximum = max(5, 10)    // 10

// Constants
let pi_val = PI             // 3.14159...
let e_val = E               // 2.71828...
```

### Trigonometry

```techlang
// All angles are in radians
let sin_val = sin(PI/2)         // 1.0
let cos_val = cos(PI)           // -1.0
let tan_val = tan(PI/4)         // 1.0

// Inverse functions
let asin_val = asin(0.5)        // PI/6
let acos_val = acos(0.5)        // PI/3
let atan_val = atan(1.0)        // PI/4

// Converting between degrees and radians
let angle_deg = 180
let angle_rad = angle_deg * PI / 180
```

### Random Numbers

```techlang
// Random float between 0.0 and 1.0
let r1 = random()

// Random integer between min and max (inclusive)
let dice = randint(1, 6)

// Random choice from array
let colors = ["red", "green", "blue", "yellow"]
let random_color = choice(colors)

// Shuffle an array
shuffle(colors)
print(colors)  // Random order
```

### Statistics

```techlang
let data = [4, 7, 2, 9, 3, 5, 8]

let avg = mean(data)            // 5.429...
let middle = median(data)       // 5
let deviation = std(data)       // Standard deviation
let minimum = min_of(data)      // 2
let maximum = max_of(data)      // 9
let total = sum_of(data)        // 38
```

---

## File I/O

### Basic File Operations

```techlang
// Writing to a file
write("greeting.txt", "Hello, world!")

// Appending to a file
append("greeting.txt", "\nHow are you?")

// Reading a file
let content = read("greeting.txt")
print(content)

// Reading line by line
for line in readlines("greeting.txt") {
    print("Line:", line)
}
```

### File Management

```techlang
// Check if a file exists
if exists("data.txt") {
    print("File exists")
} else {
    print("File doesn't exist")
}

// Copy a file
copy_file("source.txt", "destination.txt")

// Delete a file
if exists("temp.txt") {
    remove("temp.txt")
}

// Get file information
let info = file_info("document.txt")
print("Size:", info.size)
print("Last modified:", info.modified)
```

### Working with Paths

```techlang
// Join paths
let path = path_join("documents", "reports", "annual.txt")

// Get file name from path
let filename = path_basename("/home/user/data.txt")  // "data.txt"

// Get directory name from path
let dir = path_dirname("/home/user/data.txt")  // "/home/user"

// Get file extension
let ext = path_extension("report.pdf")  // "pdf"
```

### CSV Files

```techlang
// Reading CSV
let data = read_csv("data.csv")
for row in data {
    print(row[0], row[1], row[2])
}

// Writing CSV
let records = [
    ["Name", "Age", "City"],
    ["Alice", "30", "New York"],
    ["Bob", "25", "Chicago"]
]
write_csv("people.csv", records)
```

---

## Network & Web

### HTTP Requests

```techlang
// GET request
let response = http_get("https://api.example.com/data")
print(response)

// POST request with JSON data
let post_data = {
    "name": "John",
    "age": 30
}
let json_str = json_stringify(post_data)
let response = http_post("https://api.example.com/users", json_str)

// Using headers
let headers = {
    "Authorization": "Bearer token123",
    "Content-Type": "application/json"
}
let response = http_get("https://api.example.com/protected", headers)
```

### Working with JSON

```techlang
// Parse JSON string
let json_str = '{"name": "Alice", "age": 30, "skills": ["Python", "JavaScript"]}'
let data = json_parse(json_str)

print(data["name"])
print(data["skills"][0])

// Convert object to JSON string
let person = {
    "name": "Bob",
    "age": 25,
    "is_active": true
}
let json = json_stringify(person)
print(json)
```

### API Interaction

```techlang
// Get weather data from API
let api_key = "your_api_key"
let city = "New York"
let url = "https://api.example.com/weather?city=" + city + "&apikey=" + api_key

let response = http_get(url)
let weather_data = json_parse(response)

print("Temperature:", weather_data["temperature"])
print("Conditions:", weather_data["conditions"])
```

### Web Scraping

```techlang
// Get HTML content
let html = http_get("https://example.com")

// Extract all links (simple approach)
let start_idx = 0
while true {
    let href_start = html.find('href="', start_idx)
    if href_start == -1 {
        break
    }
    href_start += 6  // Length of 'href="'
    let href_end = html.find('"', href_start)
    let link = html.substring(href_start, href_end)
    print(link)
    start_idx = href_end
}
```

---

## Graphics & Visualization

### Basic Drawing

```techlang
// Create a window
window("My Drawing", 500, 400)

// Basic shapes
rect(50, 50, 100, 80, color="blue")
circle(250, 200, 60, color="red")
line(10, 10, 490, 390, color="green", width=2)
oval(350, 150, 80, 40, color="purple")
polygon([100, 300, 150, 350, 50, 350], color="orange")

// Text
text("Hello, TechLang!", 200, 30, size=20, color="black")
```

### Colors and Styles

```techlang
// RGB colors
rect(50, 50, 100, 100, color=[255, 0, 0])  // Red
rect(200, 50, 100, 100, color=[0, 255, 0])  // Green
rect(350, 50, 100, 100, color=[0, 0, 255])  // Blue

// Opacity (RGBA)
circle(100, 250, 60, color=[255, 0, 0, 128])  // Semi-transparent red
circle(150, 300, 60, color=[0, 255, 0, 128])  // Semi-transparent green
circle(200, 250, 60, color=[0, 0, 255, 128])  // Semi-transparent blue

// Fill and outline
rect(300, 200, 100, 100, fill="yellow", outline="black", outline_width=3)
```

### Animation

```techlang
window("Animation", 400, 300)
let x = 50
let y = 150
let dx = 5

// Animation loop
while true {
    clear()
    circle(x, y, 30, color="blue")
    x += dx
    
    // Bounce at edges
    if x > 370 || x < 30 {
        dx = -dx
    }
    
    refresh(30)  // 30 FPS
    
    // Exit condition
    if key_pressed("escape") {
        break
    }
}
```

### Charts and Plots

```techlang
// Line chart
let data = [5, 8, 12, 7, 9, 15, 6, 11]
plot(data, title="Sample Data", x_label="Time", y_label="Value")

// Bar chart
let categories = ["A", "B", "C", "D", "E"]
let values = [12, 19, 7, 15, 10]
bar_chart(categories, values, title="Results by Category")

// Pie chart
let labels = ["Product A", "Product B", "Product C"]
let sizes = [45, 30, 25]
pie_chart(labels, sizes, title="Market Share")

// Scatter plot
let x_coords = [1, 2, 3, 4, 5, 6, 7, 8]
let y_coords = [5, 7, 6, 8, 9, 12, 10, 11]
scatter_plot(x_coords, y_coords, title="Correlation")
```

---

## Database (SQLite3)

### Basic Database Operations

```techlang
// Open/create database
let db = sqlite_open("mydata.db")

// Create a table
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")

// Insert data
db.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
db.execute("INSERT INTO users (name, age) VALUES ('Bob', 25)")
db.execute("INSERT INTO users (name, age) VALUES ('Charlie', 35)")

// Query data
let results = db.query("SELECT * FROM users")
for row in results {
    print(row["id"], row["name"], row["age"])
}

// Close database
db.close()
```

### Using Parameters

```techlang
// Open database
let db = sqlite_open("mydata.db")

// Insert with parameters
let name = "David"
let age = 28
db.execute("INSERT INTO users (name, age) VALUES (?, ?)", name, age)

// Query with parameters
let min_age = 25
let results = db.query("SELECT * FROM users WHERE age > ?", min_age)
for row in results {
    print(row["name"], "is", row["age"], "years old")
}

db.close()
```

### Transactions

```techlang
let db = sqlite_open("mydata.db")

// Start a transaction
db.execute("BEGIN TRANSACTION")

try {
    db.execute("INSERT INTO users (name, age) VALUES ('Eva', 33)")
    db.execute("INSERT INTO users (name, age) VALUES ('Frank', 29)")
    
    // Commit if all operations succeed
    db.execute("COMMIT")
} catch {
    // Rollback on error
    db.execute("ROLLBACK")
    print("Transaction failed")
}

db.close()
```

### Database Schema

```techlang
let db = sqlite_open("library.db")

// Create a more complex schema
db.execute("CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER,
    isbn TEXT UNIQUE
)")

db.execute("CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY,
    book_id INTEGER,
    borrower TEXT NOT NULL,
    loan_date TEXT,
    return_date TEXT,
    FOREIGN KEY (book_id) REFERENCES books(id)
)")

// Add an index
db.execute("CREATE INDEX IF NOT EXISTS idx_author ON books(author)")

db.close()
```

---

## Memory Management

### Resource Cleanup

```techlang
// File resource cleanup
let f = open("data.txt", "w")
try {
    f.write("Some data")
} finally {
    f.close()
}

// Database resource cleanup
let db = sqlite_open("test.db")
try {
    db.execute("CREATE TABLE test (id INT)")
} finally {
    db.close()
}
```

### Memory Usage Analysis

```techlang
// Track memory before operation
let mem_before = memory_usage()

// Perform operation
let big_array = []
for i in 1..100000 {
    big_array.push(i)
}

// Check memory after operation
let mem_after = memory_usage()
let diff = mem_after - mem_before

print("Memory used by operation:", diff, "bytes")
```

### Garbage Collection

```techlang
// Create some objects
for i in 1..1000 {
    let obj = { "data": "x" * 1000 }
}

// Check memory
print("Before GC:", memory_usage())

// Request garbage collection
gc_collect()

// Check memory again
print("After GC:", memory_usage())
```

---

## Concurrency & Async

### Basic Threading

```techlang
// Start a thread
thread {
    for i in 1..5 {
        print("Thread A:", i)
        sleep(0.5)
    }
}

// Main thread continues
for i in 1..5 {
    print("Main thread:", i)
    sleep(0.3)
}

// Wait for all threads to complete
thread_join_all()
```

### Thread Communication with Channels

```techlang
// Create a channel
let ch = channel()

// Producer thread
thread {
    for i in 1..5 {
        print("Producing:", i)
        ch.send(i)
        sleep(0.5)
    }
    ch.close()  // Signal that no more data will be sent
}

// Consumer - main thread
while true {
    let val, ok = ch.recv()
    if !ok {
        break  // Channel is closed
    }
    print("Consumed:", val)
}
```

### Async/Await

```techlang
// Define an async function
async fn fetch_data(url) {
    print("Fetching from", url)
    sleep(1)  // Simulate network delay
    return "Data from " + url
}

// Use await to wait for the result
async fn main() {
    print("Starting...")
    
    // Start multiple async operations
    let future1 = fetch_data("api.example.com/users")
    let future2 = fetch_data("api.example.com/products")
    
    // Wait for results
    let data1 = await future1
    let data2 = await future2
    
    print(data1)
    print(data2)
    print("Done!")
}

// Run the async main function
await main()
```

### Parallel Processing

```techlang
// Function to calculate sum of a subarray
fn partial_sum(array, start, end) {
    let sum = 0
    for i in start..end {
        sum += array[i]
    }
    return sum
}

// Process a large array in parallel
let data = []
for i in 1..1000000 {
    data.push(i)
}

let ch = channel()
let num_threads = 4
let chunk_size = data.length / num_threads

// Split work among threads
for t in 0..num_threads {
    let start = t * chunk_size
    let end = (t == num_threads - 1) ? data.length : (t + 1) * chunk_size
    
    thread {
        let result = partial_sum(data, start, end)
        ch.send(result)
    }
}

// Collect results
let total = 0
for i in 0..num_threads {
    let partial = ch.recv()
    total += partial
}

print("Sum:", total)
```

---

## System & Processes

### File System Operations

```techlang
// List files
let files = listdir(".")
for file in files {
    print(file)
}

// Create directory
mkdir("new_folder")

// Create nested directories
mkdir("path/to/new/folder", true)  // recursive=true

// Remove directory
rmdir("old_folder")

// Get current working directory
let cwd = getcwd()
print("Current directory:", cwd)

// Change directory
chdir("new_folder")
```

### Running System Commands

```techlang
// Simple command execution
let result = system("echo Hello from system")
print(result)

// Command with error handling
let exit_code, output = system_with_status("some_command")
if exit_code != 0 {
    print("Command failed with code", exit_code)
    print("Output:", output)
}
```

### Process Management

```techlang
// Start a process and capture output
let proc = process("ls", ["-la"])
let output = proc.read()
print(output)

// Interactive process
let p = process("python", ["-i"])
p.write("print('Hello from Python')\n")
let response = p.read_line()
print("Python says:", response)
p.write("exit()\n")
p.close()
```

### Environment Variables

```techlang
// Get environment variable
let path = getenv("PATH")
print("PATH:", path)

// Set environment variable
setenv("MY_VARIABLE", "my_value")

// Get all environment variables
let env = get_env()
for key, value in env {
    print(key, "=", value)
}
```

### System Information

```techlang
// Get system information
let sys_info = system_info()
print("OS:", sys_info.os)
print("Architecture:", sys_info.arch)
print("CPU Cores:", sys_info.cpu_count)
print("Hostname:", sys_info.hostname)

// Memory information
let mem = memory_info()
print("Total memory:", mem.total, "bytes")
print("Free memory:", mem.free, "bytes")
print("Used memory:", mem.used, "bytes")
```

---

## Help & CLI

### Command-Line Interface

```sh
# Run a script
tl myscript.tl

# Run with arguments
tl myscript.tl arg1 arg2

# Start interactive REPL
tl -i

# Get help
tl --help

# Show version
tl --version

# Run a single expression
tl -e "print('Hello, world!')"
```

### Accessing Command-Line Arguments

```techlang
// Print all arguments
print("Arguments:", args)

// Process individual arguments
if args.length > 0 {
    print("First argument:", args[0])
}

// Parse flags
let verbose = false
for arg in args {
    if arg == "--verbose" || arg == "-v" {
        verbose = true
    }
}

if verbose {
    print("Running in verbose mode")
}
```

### Custom REPL

```techlang
// Simple custom REPL
print("Custom REPL - Type 'exit' to quit")

while true {
    print("> ", end="")
    let input = readline()
    
    if input == "exit" {
        break
    }
    
    if input == "help" {
        print("Available commands: help, time, exit")
        continue
    }
    
    if input == "time" {
        print("Current time:", time())
        continue
    }
    
    print("Unknown command:", input)
}
```

---
````

DevaanshPathak: can we have a more detailed core.md?

GitHub Copilot: Here's a more detailed version of the core.md file:

````markdown
# Core Commands in TechLang

This document covers the fundamental commands that form the backbone of TechLang programming. These core commands provide essential functionality for variable manipulation, arithmetic operations, input/output, and program flow.

## Command Reference

| Command | Syntax | Description | Example |
|--------|--------|-------------|---------|
| boot | `boot` | Reset the current value to 0. This is often used to initialize a calculation or reset the program state. | `boot print  # 0` |
| ping | `ping` | Increment current value by 1. This command adds 1 to the implicit current value maintained by the interpreter. | `boot ping ping print  # 2` |
| crash | `crash` | Decrement current value by 1. This command subtracts 1 from the implicit current value. | `boot ping crash print  # 0` |
| print | `print [arg]` | Print the current value, variable, or quoted text to the console. If no argument is provided, it prints the current value. | `print "Hello, TechLang!"` → Hello, TechLang! |
| set | `set <var> <int>` | Assign an integer value to a variable. Creates the variable if it doesn't exist, or updates it if it does. | `set counter 5` |
| add | `add <var> <int\|var>` | Add a value (integer or another variable's value) to a variable. | `set x 10 add x 5 print x  # 15` |
| sub | `sub <var> <int\|var>` | Subtract a value from a variable. | `set x 10 sub x 3 print x  # 7` |
| mul | `mul <var> <int\|var>` | Multiply a variable by a value. | `set x 4 mul x 6 print x  # 24` |
| div | `div <var> <int\|var>` | Divide a variable by a value using integer division. Automatically handles division by zero by producing an error. | `set x 9 div x 2 print x  # 4` |
| input | `input <var>` | Read the next input from the user and store it in a variable. In non-interactive mode, reads from predefined inputs. | `input name print "Hello, " print name` |
| upload | `upload` | Push the current value onto the stack for later retrieval. The stack can store multiple values in LIFO (Last In, First Out) order. | `boot ping upload boot ping ping download print  # 1` |
| download | `download` | Pop the top value from the stack and set it as the current value. Produces an error if the stack is empty. | `boot ping upload boot download print  # 1` |
| debug | `debug` | Print the current state of the program, including stack contents, variable values, and data types. Useful for troubleshooting. | `set x 5 set y 10 debug` |
| alias | `alias <short> <command>` | Create a shorthand name for a command. Useful for creating custom commands or simplifying repetitive operations. | `alias inc ping alias dec crash inc inc print  # 2` |
| import | `import <name>` | Load and execute a TechLang file (`name.tl`). Each file is imported only once, even if the command is called multiple times. | `import math_utils` |

## Detailed Examples

### Value Manipulation

```techlang
# Basic value manipulation
boot             # Reset to 0
ping ping ping   # Increment three times (value is now 3)
print            # Output: 3

# Using crash to decrement
boot ping ping ping   # Value is 3
crash crash           # Decrement twice (value is now 1)
print                 # Output: 1
```

### Variable Operations

```techlang
# Setting and manipulating variables
set counter 10
print counter         # Output: 10
add counter 5
print counter         # Output: 15
sub counter 3
print counter         # Output: 12
mul counter 2
print counter         # Output: 24
div counter 6
print counter         # Output: 4

# Using variables with other variables
set x 5
set y 3
add x y               # x = x + y
print x               # Output: 8
```

### Input and Output

```techlang
# Basic input and output
print "What is your name?"
input user_name
print "Hello, "
print user_name

# Combining input with arithmetic
print "Enter a number:"
input num
set num int(num)      # Convert string input to integer
mul num 2
print "Double your number is: "
print num
```

### Stack Operations

```techlang
# Using the stack to save and restore values
boot ping ping        # Value is 2
upload                # Save 2 to the stack
boot                  # Reset to 0
ping ping ping ping   # Value is 4
upload                # Save 4 to the stack
boot                  # Reset to 0
download              # Pop 4 from stack, value is now 4
print                 # Output: 4
download              # Pop 2 from stack, value is now 2
print                 # Output: 2
```

### Creating Aliases

```techlang
# Define custom commands with alias
alias increment ping
alias decrement crash
alias double "mul current 2"

set current 5
increment
increment
print current         # Output: 7
double
print current         # Output: 14
decrement
print current         # Output: 13
```

### Importing Files

```techlang
# main.tl
import utils          # Loads utils.tl
print "Main program"
print counter         # Uses variable defined in utils.tl

# utils.tl
set counter 0
alias increment "add counter 1"
print "Utils loaded"
```

## Common Patterns and Techniques

### Counter Pattern

```techlang
# Initialize counter
set counter 0

# Increment in a loop
set i 0
while i < 10 {
    add counter 1
    add i 1
}
print counter    # Output: 10
```

### Accumulator Pattern

```techlang
# Sum a list of numbers
set sum 0
set numbers [5, 10, 15, 20, 25]

for num in numbers {
    add sum num
}
print "The sum is: "
print sum        # Output: 75
```

### Value Swapping

```techlang
# Swap two variables using the stack
set x 10
set y 20

# Traditional swap
set temp x
set x y
set y temp

print x          # Output: 20
print y          # Output: 10

# Swap using stack
set x 10
set y 20
boot
set current x
upload
set current y
set x current
download
set y current
print x          # Output: 20
print y          # Output: 10
```

## Tips and Best Practices

1. **Initialize Variables**: Always initialize variables before using them with the `set` command.

2. **Use Aliases for Clarity**: Create meaningful aliases for common operations to make your code more readable.

3. **Stack Management**: Be careful with stack operations - always ensure you download the same number of values that you upload.

4. **Error Handling**: Prevent division by zero errors by checking values before using the `div` command.

5. **Modularity**: Use `import` to organize your code into reusable modules.

## Advanced Usage

### Custom Function Simulation

```techlang
# Define a "function" using aliases
alias start_square "set temp current upload"
alias end_square "download mul temp temp set current temp"

# Usage
set current 5
start_square
# Do other operations...
end_square
print current    # Output: 25
```

### Debug-Driven Development

```techlang
# Use debug to inspect program state
set counter 0
add counter 5
debug            # Shows all variables and their values
mul counter 2
debug            # Check the result of multiplication
```

---

See the [Examples Index](examples.md) for more code samples.
````

DevaanshPathak: and a detailed general.md?

GitHub Copilot: Here's a detailed version of the general.md file:

````markdown
# General Rules & Syntax in TechLang

This document outlines the fundamental syntax rules and conventions that govern the TechLang programming language.

## Basic Syntax Rules

| Topic | Details |
|------|---------|
| Case Sensitivity | Commands are lowercase (`print`, `set`, `add`); variables are case-sensitive (`counter` and `Counter` are different variables) |
| Statement Termination | One command per line; no semicolons required |
| Strings | Double quotes only: `"text"` (single quotes are not supported) |
| Comments | Use `#` for single-line comments; no multi-line comment syntax |
| Blocks | Begin with a keyword (`loop`, `if`, `def`, `while`, `switch`, `try`) and end with `end` |
| Whitespace | Whitespace is used for separation but is otherwise ignored |
| Errors | Printed as `[Error: message]` (non-fatal); execution continues |
| Inputs | `input <var>` reads queued inputs (CLI/tests) or prompts user in interactive mode |

## Variables and Data Types

### Variable Naming

Variables in TechLang:
- Must start with a letter or underscore
- Can contain letters, numbers, and underscores
- Are case-sensitive
- Cannot use reserved keywords

```techlang
set counter 1      # Valid
set Counter 2      # Different from 'counter'
set _temp 3        # Valid
set 1st_value 4    # Invalid - cannot start with a number
```

### Data Types

TechLang supports these basic data types:

- **Integers**: Whole numbers (`42`, `-7`)
- **Strings**: Text data (`"Hello, world!"`)
- **Floats**: Decimal numbers (`3.14`, `-0.5`)
- **Booleans**: `true` or `false`
- **Arrays**: Ordered collections (`[1, 2, 3]`)
- **Maps**: Key-value pairs (`{"name": "Alice", "age": 30}`)

```techlang
set age 30                     # Integer
set name "Alice"               # String
set pi 3.14159                 # Float
set is_active true             # Boolean
set numbers [1, 2, 3, 4, 5]    # Array
set person {"name": "Bob", "age": 25}  # Map
```

## Code Blocks and Structure

### Block Structure

All blocks in TechLang follow this pattern:
```techlang
keyword [condition] {
    # code inside block
}
```

Examples of different blocks:

```techlang
# If block
if x > 5 {
    print "x is greater than 5"
}

# While loop
while counter < 10 {
    add counter 1
    print counter
}

# Function definition
fn greet(name) {
    print "Hello, " + name
}
```

### Nesting Blocks

Blocks can be nested within other blocks:

```techlang
if x > 0 {
    print "Positive"
    if x > 10 {
        print "Greater than 10"
    } else {
        print "Not greater than 10"
    }
} else {
    print "Non-positive"
}
```

## Error Handling

Errors in TechLang are non-fatal by default:

```techlang
print 10 / 0  # [Error: Division by zero]
print "Program continues"  # This still executes
```

Use try-catch blocks for explicit error handling:

```techlang
try {
    print 10 / 0
} catch error {
    print "Caught error: " + error
}
```

## Input and Output

### Basic Input

```techlang
print "What is your name?"
input name
print "Hello, " + name
```

### Input Modes

- **Interactive Mode**: Prompts the user for input
- **Script Mode**: Reads from predefined inputs provided at runtime
- **Test Mode**: Uses inputs specified in test cases

### Output Formatting

```techlang
set name "Alice"
set age 30
print name + " is " + string(age) + " years old"

# Format strings
print "Name: ${name}, Age: ${age}"
```

## Comments and Documentation

### Single-line Comments

```techlang
# This is a comment
print "Hello"  # This is an end-of-line comment
```

### Documentation Style

Good practice for documenting functions:

```techlang
# Calculate the factorial of a number
# Params:
#   n: The number to calculate factorial for
# Returns:
#   The factorial of n
fn factorial(n) {
    if n <= 1 {
        return 1
    }
    return n * factorial(n - 1)
}
```

## Advanced Syntax Features

### One-liners

For simple conditions and loops, you can use one-line syntax:

```techlang
if x > 10 { print "Greater than 10" }
for i in 1..5 { print i }
```

### Chained Commands

Some commands can be chained for conciseness:

```techlang
# Instead of:
set x 5
add x 3
print x

# You can write:
set x 5 add x 3 print x  # Output: 8
```

### Implicit Value Usage

Some commands operate on an implicit current value:

```techlang
boot ping ping print   # Output: 2
```

## Best Practices

1. **Consistent Indentation**: Use 2 or 4 spaces for indentation inside blocks
2. **Meaningful Variable Names**: Use descriptive names that indicate purpose
3. **Comment Complex Logic**: Add comments to explain non-obvious code
4. **Modular Structure**: Break large programs into smaller, reusable functions
5. **Error Checking**: Validate inputs and handle potential errors gracefully

## Complete Example

```techlang
# Simple temperature converter program

print "Temperature Converter"
print "---------------------"
print "1. Celsius to Fahrenheit"
print "2. Fahrenheit to Celsius"
print "Enter your choice (1 or 2):"

input choice
set choice int(choice)

if choice == 1 {
    print "Enter temperature in Celsius:"
    input celsius
    set celsius float(celsius)
    set fahrenheit (celsius * 9/5) + 32
    print string(celsius) + "°C = " + string(fahrenheit) + "°F"
} else if choice == 2 {
    print "Enter temperature in Fahrenheit:"
    input fahrenheit
    set fahrenheit float(fahrenheit)
    set celsius (fahrenheit - 32) * 5/9
    print string(fahrenheit) + "°F = " + string(celsius) + "°C"
} else {
    print "Invalid choice!"
}
```

---

See the [Examples Index](examples.md) for more code samples.
````

DevaanshPathak: can you write a good playground.md

GitHub Copilot: # TechLang Web Playground

This guide explains how to set up and use the TechLang web playground - an interactive browser-based environment for writing, testing, and running TechLang code.

## Features

- 💻 Write and edit TechLang code directly in your browser
- ▶️ Execute code with immediate results
- 📄 Upload and import external `.tl` files
- 🔢 Provide inputs for interactive programs
- 🗄️ Full SQLite database integration
- 🔄 Real-time execution feedback

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Git

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/DevaanshPathak/TechLang.git
   cd TechLang
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   ```

3. **Activate the environment**

   - **Linux/macOS:**
     ```bash
     source .venv/bin/activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt):**
     ```cmd
     .venv\Scripts\activate.bat
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   If requirements.txt is missing, install Flask directly:

   ```bash
   pip install flask
   ```

## Running the Playground

1. **Start the Flask server**

   ```bash
   cd techlang_web
   python app.py
   ```

2. **Access the playground**

   Open your browser and visit [http://localhost:8080](http://localhost:8080)

## Using the Playground

### Code Editor

- Type or paste TechLang code in the editor area
- Use syntax highlighting to identify different parts of your code
- Save snippets for future use

### Input Section

- Enter values one per line
- These values will be used when your code calls the `input` command
- Values are consumed in order

### File Uploads

- Upload `.tl` files to use with `import` statements
- Files are stored in uploads
- Imported files must be uploaded before running code that imports them

### Running Code

1. Click the "Run" button to execute your code
2. View results in the output panel
3. Check for errors or execution feedback

## Database Features

TechLang includes SQLite database functionality that's fully accessible in the playground:

### Database Commands

| Command | Description | Example |
|---------|-------------|---------|
| `db_create` | Create a new table | `db_create users "id INTEGER PRIMARY KEY, name TEXT, age INTEGER"` |
| `db_insert` | Insert data | `db_insert users "1, 'Alice', 25"` |
| `db_select` | Query data | `db_select "SELECT * FROM users"` |
| `db_update` | Update records | `db_update "UPDATE users SET age = 26 WHERE name = 'Alice'"` |
| `db_delete` | Delete records | `db_delete "DELETE FROM users WHERE age < 18"` |
| `db_execute` | Run custom SQL | `db_execute "DROP TABLE IF EXISTS temp"` |
| `db_close` | Close connection | `db_close` |

### Database Example

```techlang
# Create a simple table
db_create users "id INTEGER PRIMARY KEY, name TEXT, age INTEGER"

# Add records
db_insert users "1, 'Alice', 25"
db_insert users "2, 'Bob', 30"
db_insert users "3, 'Charlie', 22"

# Query data
db_select "SELECT * FROM users WHERE age > 23"

# Always close the connection
db_close
```

## Advanced Usage

### Development Mode

For developers who want to modify the playground:

1. Edit app.py
2. Enable debug mode:
   ```python
   app.run(host="0.0.0.0", port=8080, debug=True)
   ```
3. Restart the server to apply changes

### Network Access

To allow access from other devices on your network:

1. Find your local IP address (`ipconfig` on Windows, `ifconfig` on Linux/Mac)
2. Run the Flask app (it should already be configured to listen on all interfaces)
3. Other devices can access using `http://YOUR_IP_ADDRESS:8080`

### Cleanup

To remove uploaded files after use:

```bash
cd techlang_web/uploads
rm *.tl  # Linux/macOS
# OR
del *.tl  # Windows
```

## Troubleshooting

If you encounter issues with the playground:

- **Server won't start**: Check Python version (3.10+) and Flask installation
- **Upload errors**: Verify the uploads directory exists and is writable
- **Database errors**: Ensure correct SQL syntax and check `db_close` is called
- **Import failures**: Confirm that imported files were uploaded first
- **Execution timeout**: Simplify code or check for infinite loops

## Contributing

We welcome contributions to improve the TechLang playground!

- Report bugs or suggest features in the [GitHub repository](https://github.com/DevaanshPathak/TechLang)
- Submit pull requests with improvements
- Share interesting TechLang examples with the community

---

Enjoy experimenting with TechLang in the web playground!