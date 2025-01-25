
[![sr](https://github.com/user-attachments/assets/d200809c-68ef-4b08-b1b6-ab38fb7bd1e2)
](https://s-m-quadri.gitlab.io/projects/search-research/)

# Search Research [v1.1.0](https://s-m-quadri.gitlab.io/projects/search-research/)

A lightweight and user-friendly application to search for research papers from the **arXiv** repository with ease.  

## 📌 Features  

- **Quick Search**: Query research papers from **arXiv** with a customizable result limit.  
- **Utilities**: Cleanup of input data, from non-alpha-numeric characters, customizable search limits, and more. 
- **Enhanced Accessibility**: Links to papers, DOI, and Sci-Hub (if available) are clickable directly from the results.  
- **Interactive GUI and theme**: Built with Python's [`tkinter`](https://docs.python.org/3/library/tkinter.html) for simplicity and ease of use; better readability and aesthetics.  

## Tech Stack  

- **Programming Language**: Python  
- **Libraries Used**:  
  - [`tkinter`](https://docs.python.org/3/library/tkinter.html) for GUI development  
  - [`arXiv`](https://pypi.org/project/arxiv/) for querying research papers  

## About arXiv  

[arXiv](https://arxiv.org/) is a project by the Cornell University Library, providing open access to over **1,000,000+** articles in diverse fields such as:  

- Physics  
- Mathematics  
- Computer Science  
- Quantitative Biology  
- Quantitative Finance  
- Statistics  

This application leverages the [arXiv Python wrapper](https://pypi.org/project/arxiv/) for seamless integration with their API.  

## Theming  

This application uses a carefully chosen color palette for a professional yet visually appealing design:  

- **Palette**: `#FEF9E1`, `#E5D0AC`, `#A31D1D`, and `#6D2323`  
- Sourced from [colorhunt.co](https://colorhunt.co/palette/fef9e1e5d0aca31d1d6d2323).  

## How to Run  

1. **Prerequisites**:  
   - Python 3.12.6  
   
2. **Install Dependencies**:  
   ```bash  
   pip install -r requirements.txt  
   ```  

> [!IMPORTANT]
> Non-windows users must remove this line before execution from `main.py`, since it's only compatible with Windows operating system
> ```
> root.iconbitmap(resource_path("icon.ico"))
> ```
> **Tl'dr:** Comment or remove above line before run!

3. **Run the Application**:  
   ```bash  
   python main.py  
   ```  

## Build  

To create an executable file:  

1. Install `pyinstaller`:  
   ```bash  
   pip install pyinstaller  
   ```  

2. Create the `.exe` file:  
   ```bash  
   pyinstaller search-research.spec --clean  
   ```  

The `.exe` file will be located in the `dist` folder.  

## Contribution  

Contributions are welcome! If you have suggestions for new features, improvements, or bug fixes, feel free to open an issue or submit a pull request.

## Credits

This project is contributed by https://github.com/SuyashAtkane

## License  

This project is licensed under the **GPL-3.0 License**. For more details, see the [LICENSE](LICENSE) file.  
