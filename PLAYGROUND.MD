# 🧪 TechLang Playground

This guide explains how to **run the Flask-based web playground** for [TechLang](https://github.com/DevaanshPathak/TechLang) — a toy hacker-themed language interpreter. The playground lets you paste or upload `.tl` files and run them in your browser. Perfect for quick testing or demos!

---

## 🚀 Clone the Repository

```bash
git clone https://github.com/DevaanshPathak/TechLang.git
cd TechLang
````

---

## 🧰 Setup Environment

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the environment

* **Linux/macOS:**

  ```bash
  source .venv/bin/activate
  ```

* **Windows (PowerShell):**

  ```powershell
  .venv\Scripts\Activate.ps1
  ```

---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` doesn't exist, manually install Flask:

```bash
pip install flask
```

---

## ▶️ Run the Web Playground

```bash
cd techlang_web
python app.py
```

* Visit the site at: [http://localhost:8080](http://localhost:8080)

---

## 🖼️ Interface Overview

The page will let you:

* 💻 **Paste .tl Code** - Write TechLang programs directly in the browser
* 🔢 **Enter inputs** (one per line) - Provide input values for `input` commands
* 📂 **Upload `.tl` files** for `import` statements - Import external TechLang modules
* 🗄️ **Database operations** - Full SQLite3 integration with CRUD operations
* ▶️ **Run** the program and see output immediately - Real-time execution results

---

## 📂 Uploaded Files

Uploaded `.tl` files are saved in:

```
techlang_web/uploads/
```

They're accessible to the interpreter if you use the `import filename` command in your `.tl` code.

**Database files** created by `db_*` commands are saved in the current working directory as `techlang.db`.

### Database Features in Playground

* **Create Tables**: Use `db_create` to define table schemas
* **Insert Data**: Use `db_insert` to add records
* **Query Data**: Use `db_select` to retrieve and display results
* **Update Records**: Use `db_update` to modify existing data
* **Delete Records**: Use `db_delete` to remove data
* **Execute SQL**: Use `db_execute` for custom SQL statements
* **Connection Management**: Use `db_close` to clean up connections

### Example Database Code

```bash
# Create a simple user table
db_create users "id INTEGER PRIMARY KEY, name TEXT, age INTEGER"

# Add some users
db_insert users "1, Alice, 25"
db_insert users "2, Bob, 30"

# Query all users
db_select "SELECT * FROM users"

# Update a user's age
db_update "UPDATE users SET age = 26 WHERE name = 'Alice'"

# Close database connections
db_close
```

---

## 🛠️ Dev Mode (Optional)

Enable Flask debug mode by editing `techlang_web/app.py`:

```python
app.run(host="0.0.0.0", port=8080, debug=True)
```

This reloads the app automatically on code changes and shows detailed errors.

---

## 🌐 Hosting Externally

To host on your local network:

```bash
python app.py
```

Then visit from another device using your IP (shown in the terminal, e.g. `http://192.168.1.5:8080`).

For public hosting, use a production WSGI server like Gunicorn or set up Nginx + Flask.

---

## 🧼 Cleanup

To remove uploaded files after use:

```bash
cd techlang_web/uploads
rm *.tl  # or del *.tl on Windows
```

---

## 🧪 Need Help?

If something doesn't work, double-check:

* Python version is 3.10+
* Flask is installed (`pip install flask`)
* No syntax error in your `.tl` file
* Database files are properly closed with `db_close`
* SQL syntax is correct for database operations

---

## 📬 Feedback or Contributions?

Open an issue or PR at:
👉 [github.com/DevaanshPathak/TechLang](https://github.com/DevaanshPathak/TechLang)
