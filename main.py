import re
import tkinter as tk
from tkinter import ttk, scrolledtext
import arxiv
import threading
import sys
import os

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
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
                sort_by=arxiv.SortCriterion.Relevance
            )

            # Display the results
            for idx, result in enumerate(search.results(), start=1):
                title = result.title
                url = result.entry_id
                doi = result.doi if result.doi else "DOI not available"
                sci_hub_url = f"https://sci-hub.se/{result.doi}" if result.doi else "Sci-Hub link not available"

                result_field.insert(tk.END, f"{idx}. {title}")
                result_field.insert(tk.END, f"DOI: {doi}\n")
                result_field.insert(tk.END, f"{url}\n", ("link", url))
                result_field.insert(tk.END, f"{sci_hub_url}\n\n", ("link", sci_hub_url))

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
    
    
# Function to clean input
# i.e. Remove non-alphanumeric characters (except spaces)
def clean_input():
    query = search_entry.get(1.0, tk.END).strip()
    cleaned_query = re.sub(r'[^a-zA-Z0-9\s]', '', query)
    search_entry.delete(1.0, tk.END)
    search_entry.insert(tk.END, cleaned_query)


# Create the main window
root = tk.Tk()
root.iconbitmap(resource_path("icon.ico"))
root.title("Search Research")
root.geometry(f"750x600")

# Set background color
root.configure(bg="#FEF9E1")

# Add title and subtitle
title_label = tk.Label(root, text="Search Research", font=("Arial", 32, "bold"), bg="#FEF9E1", fg="#6D2323")
title_label.pack(pady=(35, 1))
subtitle_label = tk.Label(root, text="Search for research papers with ease", font=("Arial", 12), bg="#FEF9E1", fg="#000")
subtitle_label.pack(pady=(1, 15))

# Create the multi-line text entry field
search_label = tk.Label(root, text="Enter your search query:", bg="#FEF9E1", fg="#000")
search_label.pack(pady=5)
search_entry = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=5, width=70, bg="#E5D0AC")
search_entry.pack(pady=5)

# Create the buttons and result limit input in a row
style = ttk.Style()
style.configure("Custom.TFrame", background="#FEF9E1")
button_frame = ttk.Frame(root, style="Custom.TFrame")
button_frame.pack(pady=10)

clear_input_button = tk.Button(button_frame, text="Clear Input", command=lambda: search_entry.delete(1.0, tk.END), bg="#6D2323", fg="#FEF9E1", font=("Arial", 10, "bold"))
clear_input_button.grid(row=0, column=0, padx=5)

clear_output_button = tk.Button(button_frame, text="Clear Output", command=lambda: result_field.delete(1.0, tk.END), bg="#6D2323", fg="#FEF9E1", font=("Arial", 10, "bold"))
clear_output_button.grid(row=0, column=1, padx=5)

result_limit_label = tk.Label(button_frame, text="Results Limit:", bg="#FEF9E1", fg="#000")
result_limit_label.grid(row=0, column=2, padx=5)
result_limit_entry = tk.Entry(button_frame, width=5, bg="#E5D0AC")
result_limit_entry.grid(row=0, column=3, padx=5)
result_limit_entry.insert(0, "30")

search_button = tk.Button(button_frame, text="Search", command=search_papers, bg="#6D2323", fg="#FEF9E1", font=("Arial", 10, "bold"))
search_button.grid(row=0, column=4, padx=5)

clean_input_button = tk.Button(button_frame, text="Clean", command=clean_input, bg="#6D2323", fg="#FEF9E1", font=("Arial", 10, "bold"))
clean_input_button.grid(row=0, column=5, padx=5)

# Create the result field (a scrolled text widget)
result_label = tk.Label(root, text="Search Results:", bg="#FEF9E1", fg="#000")
result_label.pack(pady=5)
result_field = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=70, bg="#E5D0AC")
result_field.pack(pady=5)


# Run the application
root.mainloop()