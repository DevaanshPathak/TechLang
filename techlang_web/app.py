import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template, request
from techlang.interpreter import run


app = Flask(__name__)
UPLOAD_FOLDER = os.path.abspath(".")  # Same dir where Flask runs
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    output = ""
    inputs = []

    if request.method == "POST":
        # Save all uploaded .tl files
        if "files" in request.files:
            for file in request.files.getlist("files"):
                if file and file.filename.endswith(".tl"):
                    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                    file.save(filepath)

        # Read code from textarea
        code = request.form.get("code", "")

        # Read inputs (one per line)
        input_text = request.form.get("inputs", "")
        inputs = input_text.strip().splitlines() if input_text.strip() else []

        # Run interpreter
        if code.strip():
            try:
                output = run(code, inputs)
            except Exception as e:
                output = f"[Runtime error: {e}]"

    return render_template("index.html", code=code, inputs="\n".join(inputs), output=output)


if __name__ == "__main__":
    app.run(port=8080)
