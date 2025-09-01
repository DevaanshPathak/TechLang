import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template, request
from techlang.interpreter import run

app = Flask(__name__)

# Ensure a SECRET_KEY is set for session safety (required for production)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev_secret_key")
UPLOAD_FOLDER = os.path.abspath(".")  # Upload files to current directory
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    output = ""
    inputs = []

    if request.method == "POST":
        # Save uploaded .tl files safely
        if "files" in request.files:
            for file in request.files.getlist("files"):
                if file and file.filename.endswith(".tl"):
                    filename = os.path.basename(file.filename)  # Prevent directory traversal
                    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                    file.save(filepath)

        # Get code from textarea
        code = request.form.get("code", "")

        # Get input values (one per line)
        input_text = request.form.get("inputs", "")
        inputs = input_text.strip().splitlines() if input_text.strip() else []

        # Run TechLang interpreter
        if code.strip():
            try:
                output = run(code, inputs)
            except Exception as e:
                output = f"[Runtime error: {e}]"

    return render_template(
        "index.html",
        code=code,
        inputs="\n".join(inputs),
        output=output
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
