# TechLang Examples Index

This page provides runnable code samples for each major feature of TechLang. Copy and paste these examples into the REPL (`tl -i`) or a `.tl` file to try them out.

---

## GUI (Tkinter)

Runnable examples (recommended):

- `examples/gui_ttk_demo.tl` — ttk widgets (Notebook, styles) + dialog from click handler
- `examples/gui_text_canvas_demo.tl` — Text insert/tags + Canvas line items

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