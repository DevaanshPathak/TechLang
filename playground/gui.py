import tkinter as tk
from tkinter import scrolledtext
from techlang.interpreter import run

def run_code():
    code = input_box.get("1.0", tk.END)
    result = run(code)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result)

# Minimal local playground for quick manual testing
app = tk.Tk()
app.title("💻 TechLang Playground")

tk.Label(app, text="Write TechLang code:").pack()

input_box = scrolledtext.ScrolledText(app, width=60, height=10)
input_box.pack(padx=10, pady=5)

tk.Button(app, text="▶ Run", command=run_code).pack(pady=5)

tk.Label(app, text="Output:").pack()

output_box = scrolledtext.ScrolledText(app, width=60, height=10)
output_box.pack(padx=10, pady=5)

app.mainloop()
