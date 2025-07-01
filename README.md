# PDF Cleaner

A Python tool for analyzing and cleaning PDF files using [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/).

## Features

- List text and image contents of PDF pages.
- Remove images by size (with optional tolerance).
- Remove specific text strings from all pages.
- Remove the last page of the PDF.
- Save the cleaned PDF to a new file.

## Requirements

- Python 3.7+
- [PyMuPDF (fitz)](https://pypi.org/project/PyMuPDF/)

Install dependencies:

```bash
pip install pymupdf
```

## Usage

Import and use the `PDFCleaner` class in your Python scripts:

```python
from pdf_cleaner import PDFCleaner

# Open PDF
cleaner = PDFCleaner("input.pdf")

# Get contents
contents = cleaner.get_page_contents(show_texts=True, show_images=True)

# Remove images by size
cleaner.remove_images([(100, 100), (250,250)], tolerance=2)

# Remove specific texts
cleaner.remove_texts(["Confidential", "Sample"])

# Remove last page
cleaner.remove_last_page()

# Save output
cleaner.save("output.pdf")

# Close file
cleaner.close()
```

## License

MIT License
