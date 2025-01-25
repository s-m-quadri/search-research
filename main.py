import tkinter as tk
from tkinter import ttk, scrolledtext
import arxiv

# Function to perform the search
def search_papers():
    # Clear the results field
    result_field.delete(1.0, tk.END)

    # Get the query from the text field
    query = search_entry.get(1.0, tk.END).strip()

    if not query:
        result_field.insert(tk.END, "Please enter a search term.")
        return

    try:
        # Query arXiv for research papers
        search = arxiv.Search(
            query=query,
            max_results=30,
            sort_by=arxiv.SortCriterion.Relevance
        )

        # Display the results
        for result in search.results():
            title = result.title
            url = result.entry_id
            doi = result.doi if result.doi else "DOI not available"
            sci_hub_url = f"https://sci-hub.se/{result.doi}" if result.doi else "Sci-Hub link not available"

            result_field.insert(tk.END, f"Title: {title}\n")
            result_field.insert(tk.END, f"DOI: {doi}\n")
            result_field.insert(tk.END, f"{url}\n", ("link", url))
            result_field.insert(tk.END, f"{sci_hub_url}\n\n", ("link", sci_hub_url))

        # Make links clickable
        result_field.tag_configure("link", foreground="blue", underline=True)
        result_field.tag_bind("link", "<Button-1>", lambda e: open_link(e))
    except Exception as e:
        result_field.insert(tk.END, f"An error occurred: {str(e)}")

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

# Create the main window
root = tk.Tk()
root.title("Research Paper Search")
root.geometry("600x400")

# Create the multi-line text entry field
search_label = ttk.Label(root, text="Enter your search query:")
search_label.pack(pady=5)
search_entry = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=5, width=70)
search_entry.pack(pady=5)

# Create the Search button
search_button = ttk.Button(root, text="Search", command=search_papers)
search_button.pack(pady=5)

# Create the result field (a scrolled text widget)
result_label = ttk.Label(root, text="Search Results:")
result_label.pack(pady=5)
result_field = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=70)
result_field.pack(pady=5)

# Run the application
root.mainloop()
