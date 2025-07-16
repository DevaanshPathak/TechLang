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

* 💻 **Paste .tl Code**
* 🔢 **Enter inputs** (one per line)
* 📂 **Upload `.tl` files** for `import` statements
* ▶️ **Run** the program and see output immediately

---

## 📂 Uploaded Files

Uploaded `.tl` files are saved in:

```
techlang_web/uploads/
```

They're accessible to the interpreter if you use the `import filename` command in your `.tl` code.

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

---

## 📬 Feedback or Contributions?

Open an issue or PR at:
👉 [github.com/DevaanshPathak/TechLang](https://github.com/DevaanshPathak/TechLang)
