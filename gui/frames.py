import customtkinter as ctk


class BaseFrame(ctk.CTkFrame):
    def __init__(
        self,
        master,
        lang_mgr,
        checkbox_text_key,
        entry_placeholder_key=None,
        entry_label_key=None,
    ):
        super().__init__(master)
        self.grid_columnconfigure(1, weight=1)

        self.lang_mgr = lang_mgr
        self.checkbox_text_key = checkbox_text_key
        self.entry_placeholder_key = entry_placeholder_key
        self.entry_label_key = entry_label_key
        self.checkbox_text = self.lang_mgr.get(self.checkbox_text_key)

        self.chkbox = ctk.CTkCheckBox(
            self, width=150, text=self.checkbox_text, command=self.toggle_entry
        )
        self.chkbox.grid(row=0, column=0, sticky="w", padx=10, pady=(8, 0))
        if self.entry_placeholder_key:
            self.entry_placeholder_key = entry_placeholder_key
            self.entry_label_key = entry_label_key

            self.entry_placeholder = self.lang_mgr.get(self.entry_placeholder_key)
            self.entry_label = self.lang_mgr.get(self.entry_label_key)

            self.entry = ctk.CTkEntry(
                self, placeholder_text=self.entry_placeholder, fg_color="#cccccc"
            )
            self.entry.grid(row=0, column=1, sticky="ew", padx=10, pady=(8, 0))
            self.entry.configure(state=ctk.DISABLED)
            self.info_label = ctk.CTkLabel(
                self,
                text=self.entry_label,
                font=ctk.CTkFont(size=10),
                text_color="gray",
            )
            self.info_label.grid(row=1, column=1, sticky="w", padx=14)
        else:
            self.entry = None

    def toggle_entry(self):
        if self.entry:
            if self.chkbox.get():
                self.entry.configure(state=ctk.NORMAL, fg_color="#ffffff")
            else:
                self.entry.delete(0, ctk.END)
                self.entry._activate_placeholder()  # https://github.com/TomSchimansky/CustomTkinter/issues/2257
                self.entry.master.focus()
                self.entry.configure(state=ctk.DISABLED, fg_color="#cccccc")

    def get_value(self):
        return self.entry.get() if self.is_checked() else None

    def is_checked(self):
        return self.chkbox.get()

    def update_text(self):
        if self.checkbox_text_key:
            self.chkbox.configure(text=self.lang_mgr.get(self.checkbox_text_key))
        if self.entry_placeholder_key:
            self.entry.configure(state=ctk.NORMAL)
            self.entry.configure(
                placeholder_text=self.lang_mgr.get(self.entry_placeholder_key)
            )
            self.entry.configure(state=ctk.DISABLED)
        if self.entry_label_key:
            self.info_label.configure(text=self.lang_mgr.get(self.entry_label_key))


class RemoveTextFrame(BaseFrame):
    def __init__(self, master, lang_mgr):
        super().__init__(
            master,
            lang_mgr,
            checkbox_text_key="remove_texts",
            entry_placeholder_key="placeholder_texts",
            entry_label_key="info_texts",
        )


class RemoveImageFrame(BaseFrame):
    def __init__(self, master, lang_mgr):
        super().__init__(
            master,
            lang_mgr,
            checkbox_text_key="remove_images",
            entry_placeholder_key="placeholder_images",
            entry_label_key="info_required",
        )


class RotatePdfFrame(BaseFrame):
    def __init__(self, master, lang_mgr):
        super().__init__(
            master,
            lang_mgr,
            checkbox_text_key="rotate_pages",
            entry_placeholder_key="placeholder_texts",
            entry_label_key="info_required",
        )
        self.angle_label = ctk.CTkLabel(self, text=self.lang_mgr.get("angle"))
        self.angle_label.grid(row=0, column=2, sticky="w", pady=(8, 0))

        self.angle_option = ctk.CTkOptionMenu(
            self,
            values=["0", "90", "180", "270"],
            width=70,
            text_color="#ffffff",
            state=ctk.DISABLED,
        )
        self.angle_option.set("180")
        self.angle_option.grid(row=0, column=3, sticky="w", padx=10, pady=(8, 0))

    def toggle_entry(self):
        super().toggle_entry()

        if self.chkbox.get():
            self.angle_option.configure(state=ctk.NORMAL)
        else:
            self.angle_option.configure(state=ctk.DISABLED)

    def get_angle(self):
        return self.angle_option.get() if self.chkbox.get() else None

    def update_text(self):
        super().update_text()

        self.angle_label.configure(text=self.lang_mgr.get("angle"))


class RemovePageFrame(BaseFrame):
    def __init__(self, master, lang_mgr):
        super().__init__(
            master,
            lang_mgr,
            checkbox_text_key="remove_pages",
            entry_placeholder_key="placeholder_pages",
            entry_label_key="info_required",
        )


class RemoveLastPageFrame(BaseFrame):
    def __init__(self, master, lang_mgr):
        super().__init__(master, lang_mgr, checkbox_text_key="remove_last")
        
        self.chkbox.grid_forget()
        self.chkbox.grid(row=0, column=0, sticky="w", padx=10, pady=10)


class GetContentFrame(ctk.CTkFrame):
    def __init__(self, master, lang_mgr, callback=None):
        super().__init__(master)
        self.lang_mgr = lang_mgr
        self.grid_columnconfigure(1, weight=1)
        self.label = ctk.CTkLabel(
            self, width=150, text=self.lang_mgr.get("get_contents")
        )
        self.label.grid(row=0, column=0, sticky="w", padx=10, pady=(8, 0))
        self.entry = ctk.CTkEntry(
            self, placeholder_text=self.lang_mgr.get("placeholder_pages")
        )
        self.entry.grid(row=0, column=1, sticky="ew", padx=10, pady=(8, 0))
        self.info_label = ctk.CTkLabel(
            self,
            text=self.lang_mgr.get("info_get_content"),
            font=ctk.CTkFont(size=10),
            text_color="gray",
        )
        self.info_label.grid(row=1, column=1, sticky="w", padx=14, columnspan=3)
        self.chkbox1 = ctk.CTkCheckBox(self, text=self.lang_mgr.get("show_images"))
        self.chkbox1.grid(row=0, column=2, sticky="w", padx=(10, 5), pady=(8, 0))
        self.chkbox1.select()
        self.chkbox2 = ctk.CTkCheckBox(self, text=self.lang_mgr.get("show_texts"))
        self.chkbox2.grid(row=0, column=3, sticky="w", padx=(5, 5), pady=(8, 0))
        self.chkbox2.select()
        self.btn = ctk.CTkButton(
            self,
            text=self.lang_mgr.get("run"),
            width=50,
            text_color="#ffffff",
            state=ctk.DISABLED,
            command=callback,
        )
        self.btn.grid(row=0, column=4, padx=(5, 10), pady=(8, 0))

    def is_show_image(self):
        return self.chkbox1.get()

    def is_show_text(self):
        return self.chkbox2.get()

    def get_value(self):
        return self.entry.get() or None

    def update_text(self):
        self.label.configure(text=self.lang_mgr.get("get_contents"))
        self.entry.configure(placeholder_text=self.lang_mgr.get("placeholder_pages"))
        self.info_label.configure(text=self.lang_mgr.get("info_get_content"))
        self.chkbox1.configure(text=self.lang_mgr.get("show_images"))
        self.chkbox2.configure(text=self.lang_mgr.get("show_texts"))
        self.btn.configure(text=self.lang_mgr.get("run"))
