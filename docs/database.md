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

See the [Examples Index](examples.md) for more