import sys
import os
import re
import secrets
import string
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from techlang.interpreter import run

app = Flask(__name__)

if os.environ.get("SECRET_KEY"):
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
else:
    app.config["SECRET_KEY"] = secrets.token_hex(32)

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "uploads"))
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'.tl'}

def is_allowed_file(filename):
    if not filename:
        return False
    
    file_ext = Path(filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        return False
    
    safe_filename = secure_filename(filename)
    if safe_filename != filename:
        return False
    
    # Basic hardening for filenames
    if '..' in filename or '/' in filename or '\\' in filename:
        return False
    
    dangerous_chars = ['<', '>', ':', '"', '|', '?', '*']
    if any(char in filename for char in dangerous_chars):
        return False
    
    if len(filename) > 100:
        return False
    
    return True

def sanitize_filename(filename):
    # Normalize to a safe, unique .tl filename
    safe_name = secure_filename(filename)
    
    if not safe_name.endswith('.tl'):
        safe_name += '.tl'
    
    base_name = safe_name[:-3]  # Remove .tl
    counter = 1
    final_name = safe_name
    
    while os.path.exists(os.path.join(UPLOAD_FOLDER, final_name)):
        final_name = f"{base_name}_{counter}.tl"
        counter += 1
        if counter > 1000:
            raise ValueError("Too many files with similar names")
    
    return final_name


@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    output = ""
    inputs = []
    uploaded_files = []

    if request.method == "POST":
        if "files" in request.files:
            for file in request.files.getlist("files"):
                if file and file.filename:
                    if not is_allowed_file(file.filename):
                        flash(f"Invalid file: {file.filename}. Only .tl files with safe names are allowed.", "error")
                        continue
                    
                    try:
                        safe_filename = sanitize_filename(file.filename)
                        filepath = os.path.join(app.config["UPLOAD_FOLDER"], safe_filename)
                        
                        if not os.path.abspath(filepath).startswith(os.path.abspath(app.config["UPLOAD_FOLDER"])):
                            flash(f"Security violation: Cannot save file outside upload directory", "error")
                            continue
                        
                        file.save(filepath)
                        uploaded_files.append(safe_filename)
                        flash(f"File uploaded successfully: {safe_filename}", "success")
                        
                    except Exception as e:
                        flash(f"Error uploading {file.filename}: {str(e)}", "error")

        code = request.form.get("code", "")

        input_text = request.form.get("inputs", "")
        inputs = input_text.strip().splitlines() if input_text.strip() else []

        if len(code) > 10000:  # 10KB limit
            flash("Code too large. Please keep it under 10KB.", "error")
            code = code[:10000]
        
        if len(input_text) > 1000:  # 1KB limit for inputs
            flash("Input too large. Please keep it under 1KB.", "error")
            inputs = inputs[:50]  # Limit to 50 input lines

        if code.strip():
            try:
                base_dir = app.config["UPLOAD_FOLDER"]
                output = run(code, inputs, base_dir=base_dir)
            except Exception as e:
                output = f"[Runtime error: {str(e)}]"
                flash(f"Execution error: {str(e)}", "error")

    return render_template(
        "index.html",
        code=code,
        inputs="\n".join(inputs),
        output=output,
        uploaded_files=uploaded_files
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
