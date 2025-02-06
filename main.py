import re
import tkinter as tk
from tkinter import ttk, scrolledtext, Frame, Canvas
import arxiv
import threading
import sys
import os
from PIL import Image, ImageTk


def resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller creates a temp folder and stores files there
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# Function to perform the search
def search_papers():
    # Disable the search button and show status
    search_button.config(state=tk.DISABLED, text="Searching...")

    def perform_search():
        # Clear the results field
        result_field.delete(1.0, tk.END)

        # Get the query and result limit from the fields
        query = search_entry.get(1.0, tk.END).strip()

        try:
            result_limit = int(result_limit_entry.get().strip())
        except ValueError:
            result_field.insert(tk.END, "Please enter a valid number for result limit.")
            search_button.config(state=tk.NORMAL, text="Search")
            return

        if not query:
            result_field.insert(tk.END, "Please enter a search term.")
            search_button.config(state=tk.NORMAL, text="Search")
            return

        try:
            # Query arXiv for research papers
            search = arxiv.Search(
                query=query,
                max_results=result_limit,
                sort_by=arxiv.SortCriterion.Relevance,
            )

            # Display the results
            for idx, result in enumerate(search.results(), start=1):
                title = result.title
                url = result.entry_id
                doi = result.doi if result.doi else None
                sci_hub_url = f"https://sci-hub.se/{result.doi}" if result.doi else None

                result_field.insert(tk.END, f"{idx}. {title}\n")
                if doi:
                    result_field.insert(tk.END, f"DOI: {doi}\n")
                    result_field.insert(
                        tk.END, f"{sci_hub_url}\n", ("link", sci_hub_url)
                    )
                result_field.insert(tk.END, f"{url}\n\n", ("link", url))

            # Make links clickable
            result_field.tag_configure("link", foreground="#6D2323", underline=True)
            result_field.tag_bind("link", "<Button-1>", lambda e: open_link(e))
        except Exception as e:
            result_field.insert(tk.END, f"An error occurred: {str(e)}")
        finally:
            # Re-enable the search button
            search_button.config(state=tk.NORMAL, text="Search")

    threading.Thread(target=perform_search).start()


# Function to open links
def open_link(event):
    import webbrowser

    widget = event.widget
    index = widget.index("@%s,%s" % (event.x, event.y))
    tags = widget.tag_names(index)
    for tag in tags:
        if tag == "link":
            url = widget.get("%s linestart" % index, "%s lineend" % index).strip()
            webbrowser.open(url)


# Function to clear input and output fields
def clear_fields():
    search_entry.delete(1.0, tk.END)
    result_field.delete(1.0, tk.END)


# Function to clean input from special characters
def clean_input():
    query = search_entry.get(1.0, tk.END).strip()
    cleaned_query = re.sub(r"[^a-zA-Z0-9\s]", "", query)
    search_entry.delete(1.0, tk.END)
    search_entry.insert(tk.END, cleaned_query)


# Function to clean input from numbers as well
def deep_clean_input():
    query = search_entry.get(1.0, tk.END).strip()
    cleaned_query = re.sub(r"[^a-zA-Z ]", "", query)
    cleaned_query = re.sub(r"\s+", " ", cleaned_query)
    cleaned_query = cleaned_query.strip().upper()
    search_entry.delete(1.0, tk.END)
    search_entry.insert(tk.END, cleaned_query)


# Initialize the Tkinter application
root = tk.Tk()
root.iconbitmap(resource_path("icon.ico"))
root.title("Search Research")
root.geometry(f"800x500")


# main
main_frame = Frame(root)
main_frame.pack(fill="both", expand=1)

# canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side="left", fill="both", expand=1)

# scrollbar
my_scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=my_canvas.yview)
my_scrollbar.pack(side="right", fill="y")

# configure the canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind(
    "<Configure>", lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all"))
)

second_frame = Frame(my_canvas, width=1000, height=100)

# Style the application
second_frame.configure(bg="#FEF9E1")
style = ttk.Style()
style.configure("Custom.TFrame", background="#FEF9E1")
image = ImageTk.PhotoImage(Image.open(resource_path("icon.ico")).resize((128, 128)))

# Add title and subtitle
tk.Label(second_frame, image=image, bg="#FEF9E1").pack(pady=(30, 0))

title_label = tk.Label(
    second_frame,
    text="Search Research",
    font=("Arial", 32, "bold"),
    bg="#FEF9E1",
    fg="#6D2323",
)
title_label.pack(pady=(0, 0))
subtitle_label = tk.Label(
    second_frame,
    text="Search for research papers with ease",
    font=("Arial", 12),
    bg="#FEF9E1",
    fg="#000",
)
subtitle_label.pack(pady=(1, 10))
ttk.Separator(second_frame, orient="horizontal").pack(fill="x", padx=50, pady=(0, 10))

# Search Actions and Label
input_action_bar = ttk.Frame(second_frame, style="Custom.TFrame")
input_action_bar.pack(pady=(0, 10))
tk.Label(
    input_action_bar,
    text="Enter your search query:",
    bg="#FEF9E1",
    fg="#6D2323",
    font=("Arial", 12),
).grid(row=0, column=1, padx=5)
tk.Button(
    input_action_bar,
    text="Clear Input",
    command=lambda: search_entry.delete(1.0, tk.END),
    bg="#FEF9E1",
    fg="#6D2323",
    font=("Arial", 10, "bold"),
).grid(row=0, column=0, padx=5)

# Search Entry
search_entry = scrolledtext.ScrolledText(
    second_frame, wrap=tk.WORD, height=5, width=70, bg="#E5D0AC"
)
search_entry.pack(pady=5)

# Action Bar
action_bar = ttk.Frame(second_frame, style="Custom.TFrame")
action_bar.pack(pady=10)
tk.Button(
    action_bar,
    text="Clean",
    command=clean_input,
    bg="#6D2323",
    fg="#FEF9E1",
    font=("Arial", 10, "bold"),
).grid(row=0, column=0, padx=5)
tk.Button(
    action_bar,
    text="Deep Clean",
    command=deep_clean_input,
    bg="#6D2323",
    fg="#FEF9E1",
    font=("Arial", 10, "bold"),
).grid(row=0, column=1, padx=5)
result_limit_label = tk.Label(
    action_bar, text="Results Limit:", bg="#FEF9E1", fg="#000"
).grid(row=0, column=2, padx=5)
result_limit_entry = tk.Entry(action_bar, width=5, bg="#E5D0AC")
result_limit_entry.grid(row=0, column=3, padx=5)
result_limit_entry.insert(0, "30")
search_button = tk.Button(
    action_bar,
    text="Search",
    command=search_papers,
    bg="#6D2323",
    fg="#FEF9E1",
    font=("Arial", 10, "bold"),
)
search_button.grid(row=0, column=4, padx=5)

# Description
tk.Label(
    second_frame,
    text='"Clean" Removes special characters from the search query.',
    font=("Arial", 10),
    bg="#FEF9E1",
    fg="#000",
).pack(pady=(1, 5))
tk.Label(
    second_frame,
    text='"Deep Clean" Removes special characters, numbers, and multiple spaces from the search query.',
    font=("Arial", 10),
    bg="#FEF9E1",
    fg="#000",
).pack(pady=(1, 10))
ttk.Separator(second_frame, orient="horizontal").pack(fill="x", padx=50, pady=(0, 10))

# Output Actions and Label
output_action_bar = ttk.Frame(second_frame, style="Custom.TFrame")
output_action_bar.pack(pady=(0, 10))
tk.Label(
    output_action_bar,
    text="Search Results:",
    bg="#FEF9E1",
    fg="#6D2323",
    font=("Arial", 12),
).grid(row=0, column=1, padx=5)
tk.Button(
    output_action_bar,
    text="Clear Output",
    command=lambda: result_field.delete(1.0, tk.END),
    bg="#FEF9E1",
    fg="#6D2323",
    font=("Arial", 10, "bold"),
).grid(row=0, column=0, padx=5)


result_field = scrolledtext.ScrolledText(
    second_frame, wrap=tk.WORD, height=10, width=70, bg="#E5D0AC"
)
result_field.pack(pady=(5, 0))
tk.Label(
    second_frame,
    text="Note: Click on the DOI or arXiv link to open the paper in your browser.",
    font=("Arial", 10),
    bg="#FEF9E1",
    fg="#000",
).pack(pady=(3, 0))
ttk.Separator(second_frame, orient="horizontal").pack(fill="x", padx=50, pady=(10, 20))
tk.Label(
    second_frame,
    text="Version 1.2.0 | Last Updated on February 2025",
    font=("Arial", 10),
    bg="#FEF9E1",
    fg="#000",
).pack(pady=(0, 30))


# Run the application
my_canvas.create_window((0, 0), window=second_frame, anchor="nw", width=800)
root.mainloop()
