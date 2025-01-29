import markdown
import argparse
import os

def convert_md_to_html(md_file_path, html_file_path, css_path=None):
    try:
        with open(md_file_path, 'r', encoding='utf-8') as md_file:
            md_text = md_file.read()
    except FileNotFoundError:
        print(f"Error: The file {md_file_path} does not exist.")
        return

    html_text = markdown.markdown(md_text)

    if css_path:
        html_text = f'<link rel="stylesheet" type="text/css" href="{css_path}">\n' + html_text

    try:
        with open(html_file_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_text)
    except IOError:
        print(f"Error: Could not write to file {html_file_path}.")
        return

    print(f"Converted {md_file_path} to {html_file_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown files to HTML.")
    parser.add_argument('input', help="Path to the input Markdown file.")
    parser.add_argument('output', help="Path to the output HTML file.")
    parser.add_argument('--css', help="Path to a CSS file to include in the HTML.", default=None)
    args = parser.parse_args()

    convert_md_to_html(args.input, args.output, args.css)

if __name__ == "__main__":
    main()