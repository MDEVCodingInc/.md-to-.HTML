import tkinter as tk
from tkinter import filedialog, messagebox
import markdown
import os

def convert_md_to_html(md_file_path, html_file_path, css_path=None):
    try:
        with open(md_file_path, 'r', encoding='utf-8') as md_file:
            md_text = md_file.read()
    except FileNotFoundError:
        return "Error: The file does not exist."

    html_text = markdown.markdown(md_text)

    if css_path:
        html_text = f'<link rel="stylesheet" type="text/css" href="{css_path}">\n' + html_text

    try:
        with open(html_file_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_text)
    except IOError:
        return "Error: Could not write to file."

    return html_file_path

def select_md_file():
    file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md")])
    md_file_var.set(file_path)

def select_css_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSS files", "*.css")])
    css_file_var.set(file_path)

def convert_file():
    md_file_path = md_file_var.get()
    css_file_path = css_file_var.get() if include_css_var.get() else None
    if not md_file_path:
        messagebox.showerror("Error", "Please select a Markdown file.")
        return

    html_file_path = os.path.splitext(md_file_path)[0] + ".html"
    result = convert_md_to_html(md_file_path, html_file_path, css_file_path)
    if result.startswith("Error"):
        messagebox.showerror("Error", result)
    else:
        messagebox.showinfo("Success", f"Converted {md_file_path} to {html_file_path}")

# Create the main window
root = tk.Tk()
root.title("Markdown to HTML Converter")

# Create and place widgets
md_file_var = tk.StringVar()
css_file_var = tk.StringVar()
include_css_var = tk.BooleanVar()

tk.Label(root, text="Select Markdown file:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=md_file_var, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_md_file).grid(row=0, column=2, padx=10, pady=10)

tk.Checkbutton(root, text="Include CSS", variable=include_css_var).grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=css_file_var, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_css_file).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="Convert", command=convert_file).grid(row=2, column=0, columnspan=3, padx=10, pady=20)

# Run the application
root.mainloop()