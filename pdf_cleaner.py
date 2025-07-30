import fitz
import re

class PDFCleaner:
    def __init__(self, input_pdf_path):
         self.input_pdf_path = input_pdf_path
         self.doc = fitz.open(input_pdf_path)

    def get_page_contents(self, show_texts=True, show_images=True, pages=None):
        """
        Print selected contents of specific pages or all pages in the PDF.

        Args:
            show_texts (bool): Show page text if True.
            show_images (bool): Show image info if True.
            pages (list[int] or None): List of page indices
        Returns:
            dict: A dictionary containing page contents
        """

        if pages is not None:
            target_pages = [p - 1 for p in pages if 1 <= p <= len(self.doc)]
        else:
            target_pages = range(len(self.doc))
        
        pages_data = []

        for page_index in target_pages:

            page = self.doc[page_index]
            page_dict = {"page_number": page_index + 1}

            if show_texts:
                texts = page.get_text("words")
                page_dict["texts"] = [txt[4] for txt in texts] if texts else []
              

            if show_images:
                images = page.get_images(full=True)
                images_info = []
                for img in images:
                    xref = img[0]
                    info = self.doc.extract_image(xref)
                    images_info.append({
                        "xref": xref,
                        "width": info["width"],
                        "height": info["height"]
                    })
                page_dict["images"] = images_info
            
            pages_data.append(page_dict)
        
        return {"data": pages_data}

    def remove_images(self, image_sizes, tolerance=0):
        """
        Remove images that match any of the specified (width, height) pairs across all pages.
        A tolerance value can be set to allow for slight size differences.

        Args:
            image_sizes (list[tuple]): List of (width, height) pairs to remove (in pixels).
            tolerance (int): Acceptable pixel deviation (e.g., 3 = ±3 pixels).
        """
        for page in self.doc:
            images = page.get_images(full=True)
            for img in images:
                xref = img[0]
                pix = fitz.Pixmap(self.doc, xref)
                w, h = pix.width, pix.height
                for tw, th in image_sizes:
                    if abs(w - tw) <= tolerance and abs(h - th) <= tolerance:
                        page.delete_image(xref)


    def remove_texts(self, *texts):
        """
        Remove all occurrences of multiple byte strings from PDF content streams.

        Args:
            *texts: Text strings to remove, e.g. remove_texts("Confidential", "Draft", "Sample")
        """
        for page in self.doc:
            for xref in page.get_contents():
                stream = self.doc.xref_stream(xref)
                new_stream = stream
                for text in texts:
                    byte_string = text.encode('utf-8')
                    new_stream = new_stream.replace(byte_string, b'')
                self.doc.update_stream(xref, new_stream)

    def remove_all_texts(self):
        """
        Remove all text from all pages in the PDF, leaving images and graphics intact.
        """
        for page in self.doc:
            for xref in page.get_contents():
                stream = self.doc.xref_stream(xref)
                new_stream = re.sub(rb"BT.*?ET", b"", stream, flags=re.S)
                self.doc.update_stream(xref, new_stream)

    def remove_last_page(self):
        """
        Remove the last page from the PDF.
        """
        last_page_index = len(self.doc) - 1
        self.doc.delete_page(last_page_index)

    def remove_pages(self, *pages):
        """
        Remove specific pages from the PDF.

        Args:
            *pages: Page numbers (1-based) as separate arguments, e.g. remove_pages(1, 3, 5)
        """
        indexes = [p - 1 for p in pages if 1 <= p <= len(self.doc)]
        if indexes:
            self.doc.delete_pages(indexes)   

    def rotate_pages(self, pages, angle=180):
        """
        Rotate specific pages in the PDF by a given angle.

        Args:
            pages (list[int]): List of 1-based page numbers to rotate.
            angle (int): Rotation angle. Must be one of 0, 90, 180, 270.
        Raises:
            ValueError: If an invalid angle is provided.
        """
        if angle not in [0, 90, 180, 270]:
            raise ValueError("Angle must be 0, 90, 180, or 270 degrees.")

        target_pages = [p - 1 for p in pages if 1 <= p <= len(self.doc)]

        for page_index in target_pages:
            page = self.doc[page_index]
            page.set_rotation(angle)
              
    def save(self, output_pdf_path):
        """
        Save the modified PDF document to a new file.

        Args:
            output_pdf_path (str): Path where the output PDF file will be saved.
        """
        self.doc.save(output_pdf_path)

    def close(self):
        """
        Close the PDF document to release file handles and free memory.

        This should be called after all processing is complete,
        especially if working with large PDFs or in long-running applications.
        """
        self.doc.close()