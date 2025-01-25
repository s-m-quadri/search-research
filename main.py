import tkinter as tk
from tkinter import ttk, scrolledtext
import arxiv

# Function to perform the search
def search_papers():
    # Clear the results field
    result_field.delete(1.0, tk.END)

    # Get the query from the text field
    query = search_entry.get()

    if not query.strip():
        result_field.insert(tk.END, "Please enter a search term.")
        return

    try:
        # Query arXiv for research papers
        search = arxiv.Search(
            query=query,
            max_results=10,  # Limit the number of results to 10
            sort_by=arxiv.SortCriterion.Relevance
        )

        # Display the results
        for result in search.results():
            title = result.title
            url = result.entry_id
            result_field.insert(tk.END, f"Title: {title}\nLink: {url}\n\n")
    except Exception as e:
        result_field.insert(tk.END, f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Research Paper Search")
root.geometry("600x400")

# Create the text entry field
search_label = ttk.Label(root, text="Enter your search query:")
search_label.pack(pady=5)
search_entry = ttk.Entry(root, width=50)
search_entry.pack(pady=5)

# Create the Search button
search_button = ttk.Button(root, text="Search", command=search_papers)
search_button.pack(pady=5)

# Create the result field (a scrolled text widget)
result_label = ttk.Label(root, text="Search Results:")
result_label.pack(pady=5)
result_field = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, width=70)
result_field.pack(pady=5)

# Run the application
root.mainloop()