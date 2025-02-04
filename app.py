import tkinter as tk
from tkinter import filedialog, messagebox
import markdown
import os
from fpdf import FPDF
import pandas as pd
from bs4 import BeautifulSoup
import json
import xml.etree.ElementTree as ET
from json2xml import json2xml
from json2xml.utils import readfromstring

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

def convert_html_to_md(html_file_path, md_file_path):
    try:
        with open(html_file_path, 'r', encoding='utf-8') as html_file:
            html_text = html_file.read()
    except FileNotFoundError:
        return "Error: The file does not exist."

    soup = BeautifulSoup(html_text, 'html.parser')
    md_text = soup.get_text()

    try:
        with open(md_file_path, 'w', encoding='utf-8') as md_file:
            md_file.write(md_text)
    except IOError:
        return "Error: Could not write to file."

    return md_file_path

def convert_txt_to_pdf(txt_file_path, pdf_file_path):
    try:
        with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
            txt_text = txt_file.read()
    except FileNotFoundError:
        return "Error: The file does not exist."

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt_text)

    try:
        pdf.output(pdf_file_path)
    except IOError:
        return "Error: Could not write to file."

    return pdf_file_path

def convert_csv_to_excel(csv_file_path, excel_file_path):
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        return "Error: The file does not exist."

    try:
        df.to_excel(excel_file_path, index=False)
    except IOError:
        return "Error: Could not write to file."

    return excel_file_path

def convert_json_to_csv(json_file_path, csv_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
    except FileNotFoundError:
        return "Error: The file does not exist."

    df = pd.json_normalize(json_data)

    try:
        df.to_csv(csv_file_path, index=False)
    except IOError:
        return "Error: Could not write to file."

    return csv_file_path

def convert_xml_to_json(xml_file_path, json_file_path):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
    except FileNotFoundError:
        return "Error: The file does not exist."

    json_data = json2xml.Json2xml(readfromstring(ET.tostring(root, encoding='utf-8').decode('utf-8'))).to_json()

    try:
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json_file.write(json_data)
    except IOError:
        return "Error: Could not write to file."

    return json_file_path

def select_file():
    file_path = filedialog.askopenfilename()
    input_file_var.set(file_path)

def convert_file():
    input_file_path = input_file_var.get()
    input_type = input_type_var.get()
    output_type = output_type_var.get()
    css_file_path = css_file_var.get() if include_css_var.get() else None

    if not input_file_path:
        messagebox.showerror("Error", "Please select a file.")
        return

    if input_type == "Markdown" and output_type == "HTML":
        output_file_path = os.path.splitext(input_file_path)[0] + ".html"
        result = convert_md_to_html(input_file_path, output_file_path, css_file_path)
    elif input_type == "HTML" and output_type == "Markdown":
        output_file_path = os.path.splitext(input_file_path)[0] + ".md"
        result = convert_html_to_md(input_file_path, output_file_path)
    elif input_type == "TXT" and output_type == "PDF":
        output_file_path = os.path.splitext(input_file_path)[0] + ".pdf"
        result = convert_txt_to_pdf(input_file_path, output_file_path)
    elif input_type == "CSV" and output_type == "Excel":
        output_file_path = os.path.splitext(input_file_path)[0] + ".xlsx"
        result = convert_csv_to_excel(input_file_path, output_file_path)
    elif input_type == "JSON" and output_type == "CSV":
        output_file_path = os.path.splitext(input_file_path)[0] + ".csv"
        result = convert_json_to_csv(input_file_path, output_file_path)
    elif input_type == "XML" and output_type == "JSON":
        output_file_path = os.path.splitext(input_file_path)[0] + ".json"
        result = convert_xml_to_json(input_file_path, output_file_path)
    else:
        messagebox.showerror("Error", "Unsupported conversion type.")
        return

    if result.startswith("Error"):
        messagebox.showerror("Error", result)
    else:
        messagebox.showinfo("Success", f"Converted {input_file_path} to {output_file_path}")

# Create the main window
root = tk.Tk()
root.title("File Converter")

# Create and place widgets
input_file_var = tk.StringVar()
css_file_var = tk.StringVar()
include_css_var = tk.BooleanVar()
input_type_var = tk.StringVar(value="Markdown")
output_type_var = tk.StringVar(value="HTML")

tk.Label(root, text="Select file:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=input_file_var, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Input type:").grid(row=1, column=0, padx=10, pady=10)
tk.OptionMenu(root, input_type_var, "Markdown", "HTML", "TXT", "CSV", "JSON", "XML").grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Output type:").grid(row=2, column=0, padx=10, pady=10)
tk.OptionMenu(root, output_type_var, "HTML", "Markdown", "PDF", "Excel", "CSV", "JSON").grid(row=2, column=1, padx=10, pady=10)

tk.Checkbutton(root, text="Include CSS", variable=include_css_var).grid(row=3, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=css_file_var, width=50).grid(row=3, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=lambda: css_file_var.set(filedialog.askopenfilename(filetypes=[("CSS files", "*.css")]))).grid(row=3, column=2, padx=10, pady=10)

tk.Button(root, text="Convert", command=convert_file).grid(row=4, column=0, columnspan=3, padx=10, pady=20)

# Run the application
root.mainloop()