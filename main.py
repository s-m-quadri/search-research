import tkinter as tk
from tkinter import ttk, scrolledtext
import arxiv
import threading

# Function to perform the search
def search_papers():
    # Disable the search button and show status
    search_button.config(state=tk.DISABLED)
    status_label.config(text="Searching...")
    
    def perform_search():
        # Clear the results field
        result_field.delete(1.0, tk.END)

        # Get the query from the text field
        query = search_entry.get(1.0, tk.END).strip()

        if not query:
            result_field.insert(tk.END, "Please enter a search term.")
            status_label.config(text="Idle")
            search_button.config(state=tk.NORMAL)
            return

        try:
            # Query arXiv for research papers
            search = arxiv.Search(
                query=query,
                max_results=30,
                sort_by=arxiv.SortCriterion.Relevance
            )

            # Display the results
            for idx, result in enumerate(search.results(), start=1):
                title = result.title
                url = result.entry_id
                doi = result.doi if result.doi else "DOI not available"
                sci_hub_url = f"https://sci-hub.se/{result.doi}" if result.doi else "Sci-Hub link not available"

                result_field.insert(tk.END, f"{idx}.\n")
                result_field.insert(tk.END, f"Title: {title}\n")
                result_field.insert(tk.END, f"DOI: {doi}\n")
                result_field.insert(tk.END, f"Link: {url}\n", ("link", url))
                result_field.insert(tk.END, f"Sci-Hub: {sci_hub_url}\n\n", ("link", sci_hub_url))

            # Make links clickable
            result_field.tag_configure("link", foreground="blue", underline=True)
            result_field.tag_bind("link", "<Button-1>", lambda e: open_link(e))
        except Exception as e:
            result_field.insert(tk.END, f"An error occurred: {str(e)}")
        finally:
            # Re-enable the search button and update status
            search_button.config(state=tk.NORMAL)
            status_label.config(text="Idle")

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

# Create the main window
root = tk.Tk()
root.title("Research Paper Search")
root.geometry(f"750x600")

# Add title and subtitle
title_label = tk.Label(root, text="Research Paper Search", font=("Arial", 32, "bold")).pack(pady=(15,1))
subtitle_label = tk.Label(root, text="Search for research papers with ease", font=("Arial", 12)).pack(pady=(1, 15))

# Create the multi-line text entry field
search_label = ttk.Label(root, text="Enter your search query:")
search_label.pack(pady=5)
search_entry = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=5, width=70)
search_entry.pack(pady=5)

# Create the buttons (Search, Clear Input, Clear Output) in a row
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

search_button = ttk.Button(button_frame, text="Search", command=search_papers)
search_button.grid(row=0, column=0, padx=5)

clear_input_button = ttk.Button(button_frame, text="Clear Input", command=lambda: search_entry.delete(1.0, tk.END))
clear_input_button.grid(row=0, column=1, padx=5)

clear_output_button = ttk.Button(button_frame, text="Clear Output", command=lambda: result_field.delete(1.0, tk.END))
clear_output_button.grid(row=0, column=2, padx=5)

# Add a status label
status_label = tk.Label(root, text="Idle", font=("Arial", 10), fg="green")
status_label.pack(pady=5)

# Create the result field (a scrolled text widget)
result_label = ttk.Label(root, text="Search Results:")
result_label.pack(pady=5)
result_field = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=70)
result_field.pack(pady=5)

# Run the application
root.mainloop()
