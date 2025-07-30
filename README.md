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

# Get contents from specific pages (e.g., pages 1, 3, and 5)
contents = cleaner.get_page_contents(1, 3, 5, show_texts=True, show_images=True)

# Or get contents from all pages
contents = cleaner.get_page_contents(show_texts=True, show_images=True)

# Remove images by size
cleaner.remove_images((100, 100), [250, 250], tolerance=2)

# Remove specific texts
cleaner.remove_texts("Confidential", "Sample")

# Remove all texts
cleaner.remove_texts()

# Remove last page
cleaner.remove_last_page()

# Remove specific pages (e.g., pages 2 and 4)
cleaner.remove_pages(2, 4)

# Rotate selected pages (e.g., pages 1 and 3) by 180 degrees
cleaner.rotate_pages(1, 3, angle=180)

# Save output
cleaner.save("output.pdf")

# Close file
cleaner.close()
```

## License

MIT License
