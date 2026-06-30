import tkinter as tk
from tkinter import filedialog, messagebox


class AVComplectatorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("AV Complectator")
        self.root.geometry("760x620")

        self.template_path = ""
        self.pdf_path = ""

        self.language = tk.StringVar(value="English")
        self.strict_mode = tk.BooleanVar(value=True)

        self.use_manufacturer_photos = tk.BooleanVar(value=True)
        self.use_project_drawings = tk.BooleanVar(value=True)
        self.use_project_renders = tk.BooleanVar(value=True)
        self.use_material_samples = tk.BooleanVar(value=False)

        self.build_ui()

    def build_ui(self):
        tk.Label(
            self.root,
            text="AV Complectator",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        tk.Label(
            self.root,
            text="Automatic Interior Specification Generator",
            font=("Arial", 12)
        ).pack(pady=(0, 15))

        settings_frame = tk.LabelFrame(
            self.root,
            text="Settings",
            padx=20,
            pady=15
        )
        settings_frame.pack(fill="x", padx=30, pady=10)

        tk.Label(settings_frame, text="Language:").grid(row=0, column=0, sticky="w")

        tk.Radiobutton(
            settings_frame,
            text="English",
            variable=self.language,
            value="English"
        ).grid(row=0, column=1, sticky="w", padx=10)

        tk.Radiobutton(
            settings_frame,
            text="Русский",
            variable=self.language,
            value="Russian"
        ).grid(row=0, column=2, sticky="w", padx=10)

        tk.Checkbutton(
            settings_frame,
            text="Strict mode: do not translate or invent text",
            variable=self.strict_mode
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=8)

        images_frame = tk.LabelFrame(
            self.root,
            text="Images",
            padx=20,
            pady=15
        )
        images_frame.pack(fill="x", padx=30, pady=10)

        tk.Checkbutton(
            images_frame,
            text="Manufacturer photos for ready-made items",
            variable=self.use_manufacturer_photos
        ).pack(anchor="w")

        tk.Checkbutton(
            images_frame,
            text="Project drawings",
            variable=self.use_project_drawings
        ).pack(anchor="w")

        tk.Checkbutton(
            images_frame,
            text="Project renders",
            variable=self.use_project_renders
        ).pack(anchor="w")

        tk.Checkbutton(
            images_frame,
            text="Material samples only if available in project",
            variable=self.use_material_samples
        ).pack(anchor="w")

        files_frame = tk.LabelFrame(
            self.root,
            text="Files",
            padx=20,
            pady=15
        )
        files_frame.pack(fill="x", padx=30, pady=10)

        tk.Button(
            files_frame,
            text="Select Excel Template",
            width=30,
            command=self.select_template
        ).pack(pady=8)

        self.template_label = tk.Label(
            files_frame,
            text="Template: not selected",
            wraplength=650
        )
        self.template_label.pack()

        tk.Button(
            files_frame,
            text="Select Project PDF",
            width=30,
            command=self.select_pdf
        ).pack(pady=8)

        self.pdf_label = tk.Label(
            files_frame,
            text="PDF: not selected",
            wraplength=650
        )
        self.pdf_label.pack()

        tk.Button(
            self.root,
            text="Generate Specification",
            width=32,
            height=2,
            command=self.generate
        ).pack(pady=25)

        self.status_label = tk.Label(
            self.root,
            text="Status: ready",
            fg="gray"
        )
        self.status_label.pack()

    def select_template(self):
        path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx")]
        )
        if path:
            self.template_path = path
            self.template_label.config(text=f"Template: {path}")

    def select_pdf(self):
        path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")]
        )
        if path:
            self.pdf_path = path
            self.pdf_label.config(text=f"PDF: {path}")

    def generate(self):
        if not self.template_path:
            messagebox.showwarning("Warning", "Select Excel template first.")
            return

        if not self.pdf_path:
            messagebox.showwarning("Warning", "Select Project PDF first.")
            return

        settings = (
            f"Language: {self.language.get()}\n"
            f"Strict mode: {self.strict_mode.get()}\n"
            f"Manufacturer photos: {self.use_manufacturer_photos.get()}\n"
            f"Project drawings: {self.use_project_drawings.get()}\n"
            f"Project renders: {self.use_project_renders.get()}\n"
            f"Material samples: {self.use_material_samples.get()}"
        )

        self.status_label.config(text="Status: settings checked")

        messagebox.showinfo(
            "AV Complectator",
            "Settings accepted.\n\n"
            "Next step: connect Template Engine.\n\n"
            + settings
        )


root = tk.Tk()
app = AVComplectatorApp(root)
root.mainloop()