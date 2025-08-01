import customtkinter as ctk
import tkinter as tk

from pdf_cleaner import PDFCleaner
from gui import (
    RemoveTextFrame,
    RemoveImageFrame,
    RotatePdfFrame,
    RemovePageFrame,
    RemoveLastPageFrame,
    GetContentFrame,
)
import json
from lang import LanguageManager
import os


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        metadata_path = os.path.join(os.path.dirname(__file__), "metadata.json")
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        self.lang_mgr = LanguageManager()

        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        self.lang_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.lang_menu.add_command(
            label="English", command=lambda: self.switch_language("en")
        )
        self.lang_menu.add_command(
            label="ภาษาไทย", command=lambda: self.switch_language("th")
        )
        self.menu_bar.add_cascade(label="Language", menu=self.lang_menu)

        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.title("PDF Cleaner")
        self.geometry("800x850")
        self.minsize(800,850)
        self.grid_columnconfigure((0, 1), weight=1)
        self.file_path = None
        self.cleaner = None

        # ===== Widgets: Select PDF =====
        self.file_label = ctk.CTkLabel(self, text=self.lang_mgr.get("no_file_selected"))
        self.file_label.grid(row=0, column=0, columnspan=2, pady=10)
        self.select_pdf_btn = ctk.CTkButton(
            self,
            text=self.lang_mgr.get("select_pdf"),
            command=self.import_file,
            text_color="#ffffff",
        )
        self.select_pdf_btn.grid(row=1, column=0, columnspan=2, pady=10)

        # ===== Frame: Remove Text =====
        self.remove_text_frame = RemoveTextFrame(self, self.lang_mgr)
        self.remove_text_frame.grid(
            row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=5
        )

        # ===== Frame: Remove Image =====
        self.remove_img_frame = RemoveImageFrame(self, self.lang_mgr)
        self.remove_img_frame.grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=5
        )

        # ===== Frame: Rotate Pages =====
        self.rotate_frame = RotatePdfFrame(self, self.lang_mgr)
        self.rotate_frame.grid(
            row=4, column=0, columnspan=2, sticky="ew", padx=20, pady=5
        )

        # ===== Frame: Remove Pages =====
        self.remove_page_frame = RemovePageFrame(self, self.lang_mgr)
        self.remove_page_frame.grid(
            row=5, column=0, columnspan=2, sticky="ew", padx=20, pady=5
        )

        # ===== Frame: Remove Last Page =====
        self.remove_last_page_frame = RemoveLastPageFrame(self, self.lang_mgr)
        self.remove_last_page_frame.grid(
            row=6, column=0, columnspan=2, sticky="ew", padx=20, pady=5
        )

        # ===== Frame: Get Page Contents =====
        self.page_content_frame = GetContentFrame(
            self, self.lang_mgr, callback=self.run_callback
        )
        self.page_content_frame.grid(
            row=7, column=0, columnspan=2, sticky="ew", padx=20, pady=5
        )

        # ===== Widgets: Buttons =====
        self.clean_btn = ctk.CTkButton(
            self,
            text=self.lang_mgr.get("clean_pdf"),
            command=self.clean_callback,
            text_color="#ffffff",
            state=ctk.DISABLED,
        )
        self.clean_btn.grid(row=8, column=0, sticky="e", padx=20, pady=5)

        self.save_btn = ctk.CTkButton(
            self,
            text=self.lang_mgr.get("save_pdf"),
            command=self.save_callback,
            text_color="#ffffff",
            state=ctk.DISABLED,
        )
        self.save_btn.grid(row=8, column=1, sticky="w", padx=20, pady=5)

        # ===== Widgets: Logs Area =====
        self.logs_txtbox = ctk.CTkTextbox(
            self,
            width=600,
            height=200,
            corner_radius=10,
            text_color="#2c2c2c",
            fg_color="#D3D3D3",
        )
        self.logs_txtbox.insert("0.0", "Logs go here.")
        self.logs_txtbox.configure(state=ctk.DISABLED)
        self.logs_txtbox.grid(row=9, column=0, columnspan=2, padx=20, pady=10)

    def insert_log(self, *args, **kwargs):
        self.logs_txtbox.configure(state=ctk.NORMAL)
        self.logs_txtbox.insert(*args, **kwargs)
        self.logs_txtbox.see(ctk.END)
        self.logs_txtbox.configure(state=ctk.DISABLED)

    def clean_callback(self):
        is_remove_text = self.remove_text_frame.is_checked()
        is_remove_image = self.remove_img_frame.is_checked()
        is_rotate_page = self.rotate_frame.is_checked()
        is_remove_page = self.remove_page_frame.is_checked()
        is_remove_last_page = self.remove_last_page_frame.is_checked()

        self.insert_log(ctk.END, "Checking...\n")

        self.insert_log(ctk.END, f"Remove Text: {'✓' if is_remove_text else '✗'}\n")
        self.insert_log(ctk.END, f"Remove Image: {'✓' if is_remove_image else '✗'}\n")
        self.insert_log(ctk.END, f"Rotate Page: {'✓' if is_rotate_page else '✗'}\n")
        self.insert_log(ctk.END, f"Remove Page: {'✓' if is_remove_page else '✗'}\n")
        self.insert_log(
            ctk.END, f"Remove Last Page: {'✓' if is_remove_last_page else '✗'}\n"
        )
        self.insert_log(ctk.END, "Check Complate! \n")

        self.cleaner = PDFCleaner(self.file_path)

        self.insert_log(ctk.END, "Start cleaning process... \n")
        if is_remove_text:
            self.insert_log(ctk.END, "Removing text... \n")
            rs = self.remove_text_frame.get_value()
            if rs:
                value = [str(i) for i in rs.split(",")]
                self.cleaner.remove_texts(*value)
            else:
                self.cleaner.remove_texts()
            self.insert_log(ctk.END, "Remove texts complete. \n")
        if is_remove_image:
            self.insert_log(ctk.END, "Removing images... \n")
            rs = self.remove_img_frame.get_value()
            if rs:
                value = [str(i) for i in rs.split(",")]
                self.cleaner.remove_images(*value)
            else:
                pass
            self.insert_log(ctk.END, "Remove images complete. \n")
        if is_rotate_page:
            self.insert_log(ctk.END, "Rotating pages... \n")
            rs = self.rotate_frame.get_value()
            angle = int(self.rotate_frame.get_angle())
            if rs:
                value = [int(i) for i in rs.split(",")]
                self.cleaner.rotate_pages(*value, angle=angle)
            else:
                pass
            self.insert_log(ctk.END, "Rotate pages complete. \n")
        if is_remove_page:
            self.insert_log(ctk.END, "Removing pages... \n")
            rs = self.remove_page_frame.get_value()
            if rs:
                value = [int(i) for i in rs.split(",")]
                self.cleaner.remove_pages(*value)
            else:
                pass
            self.insert_log(ctk.END, "Remove page complete. \n")
        if is_remove_last_page:
            self.insert_log(ctk.END, "Removing last page... \n")
            self.cleaner.remove_last_page()
            self.insert_log(ctk.END, "Remove last page complete. \n")
        self.insert_log(ctk.END, "Cleaning process finished. \n")
        self.save_btn.configure(state=ctk.NORMAL)

    def run_callback(self):
        if not self.cleaner:
            self.cleaner = PDFCleaner(self.file_path)

        self.logs_txtbox.configure(state=ctk.NORMAL)
        rs = self.page_content_frame.get_value()
        is_show_img = self.page_content_frame.is_show_image()
        is_show_text = self.page_content_frame.is_show_text()
        if rs:
            value = [int(i) for i in rs.split(",")]
            page_contents = self.cleaner.get_page_contents(
                *value, show_images=is_show_img, show_texts=is_show_text
            )
        else:
            page_contents = self.cleaner.get_page_contents(
                show_images=is_show_img, show_texts=is_show_text
            )

        json_str = json.dumps(page_contents, indent=4)
        self.logs_txtbox.insert(ctk.END, f"{json_str}\n")
        self.logs_txtbox.see(ctk.END)
        self.logs_txtbox.configure(state=ctk.DISABLED)

    def save_callback(self):
        output_path = ctk.filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )
        self.logs_txtbox.insert(ctk.END, "Saving...\n")
        self.cleaner.save(output_path)
        self.logs_txtbox.insert(ctk.END, "Save Complete!\n")
        self.logs_txtbox.see(ctk.END)

    def import_file(self):
        self.file_path = ctk.filedialog.askopenfilename(
            title="Select a file", filetypes=[("PDF files", "*.pdf")]
        )
        if self.cleaner:
            self.cleaner.close()
            self.cleaner = None
        if self.file_path:
            self.file_label.configure(
                text=f"{self.lang_mgr.get('select')}: {self.file_path}"
            )
            self.page_content_frame.btn.configure(state=ctk.NORMAL)
            self.clean_btn.configure(state=ctk.NORMAL)

    def switch_language(self, lang_code):
        self.lang_mgr.load_language(lang_code)
        self.remove_text_frame.update_text()
        self.remove_img_frame.update_text()
        self.remove_page_frame.update_text()
        self.remove_last_page_frame.update_text()
        self.rotate_frame.update_text()
        self.page_content_frame.update_text()
        if self.file_path:
            self.file_label.configure(
                text=f"{self.lang_mgr.get('select')}: {self.file_path}"
            )
        else:
            self.file_label.configure(text=self.lang_mgr.get("no_file_selected"))
        self.select_pdf_btn.configure(text=self.lang_mgr.get("select_pdf"))
        self.clean_btn.configure(text=self.lang_mgr.get("clean_pdf"))
        self.save_btn.configure(text=self.lang_mgr.get("save_pdf"))

    def show_about(self):
        tk.messagebox.showinfo(
            "About",
            f"This application was created by {self.metadata['author']}.\n"
            f"Version: {self.metadata['version']}\n\n"
            f"GitHub: {self.metadata['github']}\n\n"
            f"License: {self.metadata['license']}\n\n"
            f"{self.metadata['copyright']}",
        )


app = App()
app.mainloop()
