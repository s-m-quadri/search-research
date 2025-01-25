
![sr](https://github.com/user-attachments/assets/d200809c-68ef-4b08-b1b6-ab38fb7bd1e2)


# Search Research  

A lightweight and user-friendly application to search for research papers from the **arXiv** repository with ease.  

## 📌 Features  

- **Dynamic Search**: Query research papers from **arXiv** with a customizable result limit.  
- **Interactive GUI**: Built with Python's [`tkinter`](https://docs.python.org/3/library/tkinter.html) for simplicity and ease of use.  
- **Enhanced Accessibility**: Links to papers, DOI, and Sci-Hub (if available) are clickable directly from the results.  
- **Customizable Theme**: A clean and vibrant color palette for better readability and aesthetics.  

## 📌 Tech Stack  

- **Programming Language**: Python  
- **Libraries Used**:  
  - [`tkinter`](https://docs.python.org/3/library/tkinter.html) for GUI development  
  - [`arXiv`](https://pypi.org/project/arxiv/) for querying research papers  

## 📌 About arXiv  

[arXiv](https://arxiv.org/) is a project by the Cornell University Library, providing open access to over **1,000,000+** articles in diverse fields such as:  

- Physics  
- Mathematics  
- Computer Science  
- Quantitative Biology  
- Quantitative Finance  
- Statistics  

This application leverages the [arXiv Python wrapper](https://pypi.org/project/arxiv/) for seamless integration with their API.  

## 📌 Theming  

This application uses a carefully chosen color palette for a professional yet visually appealing design:  

- **Palette**: `#FEF9E1`, `#E5D0AC`, `#A31D1D`, and `#6D2323`  
- Sourced from [colorhunt.co](https://colorhunt.co/palette/fef9e1e5d0aca31d1d6d2323).  

## 📌 How to Run  

1. **Prerequisites**:  
   - Python 3.7 or above  
   - Required libraries: `arxiv`, `tkinter` (pre-installed with Python)  

2. **Install Dependencies**:  
   ```bash  
   pip install arxiv  
   ```  

3. **Run the Application**:  
   ```bash  
   python app.py  
   ```  

## 📌 Distribution  

To create an executable file:  

1. Install `pyinstaller`:  
   ```bash  
   pip install pyinstaller  
   ```  

2. Create the `.exe` file:  
   ```bash  
   pyinstaller --onefile --windowed app.py  
   ```  

The `.exe` file will be located in the `dist` folder.  

## 📌 Contribution  

Contributions are welcome! If you have suggestions for new features, improvements, or bug fixes, feel free to open an issue or submit a pull request.  

## 📌 License  

This project is licensed under the **GPL-3.0 License**. For more details, see the [LICENSE](LICENSE) file.  
