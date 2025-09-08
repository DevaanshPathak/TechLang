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

See the [Examples Index](examples.md) for