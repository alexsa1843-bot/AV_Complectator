import tkinter as tk
from tkinter import filedialog, messagebox
from engines.template_engine import TemplateEngine
from engines.pdf_engine import PDFEngine


class MainWindow:

    def __init__(self, root):
        self.root = root
        self.root.title("AV Complectator")
        self.root.geometry("900x760")

        self.template_path = ""
        self.pdf_path = ""
        self.output_folder = ""

        self.language = tk.StringVar(value="English")
        self.strict_mode = tk.BooleanVar(value=True)

        self.build()

    def build(self):
        tk.Label(self.root, text="AV Complectator", font=("Arial", 28, "bold")).pack(pady=25)

        settings = tk.LabelFrame(self.root, text="Settings", padx=20, pady=15)
        settings.pack(fill="x", padx=30, pady=10)

        tk.Label(settings, text="Language:").grid(row=0, column=0, sticky="w")
        tk.Radiobutton(settings, text="English", variable=self.language, value="English").grid(row=0, column=1, padx=10)
        tk.Radiobutton(settings, text="Русский", variable=self.language, value="Russian").grid(row=0, column=2, padx=10)

        tk.Checkbutton(
            settings,
            text="Strict mode: do not translate or invent text",
            variable=self.strict_mode
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=10)

        files = tk.LabelFrame(self.root, text="Files", padx=20, pady=15)
        files.pack(fill="x", padx=30, pady=10)

        tk.Button(files, text="Select Excel Template", width=30, command=self.select_template).pack(pady=8)
        self.template_label = tk.Label(files, text="Template: not selected", wraplength=760)
        self.template_label.pack()

        tk.Button(files, text="Select Project PDF", width=30, command=self.select_pdf).pack(pady=8)
        self.pdf_label = tk.Label(files, text="PDF: not selected", wraplength=760)
        self.pdf_label.pack()

        tk.Button(files, text="Select Output Folder", width=30, command=self.select_output_folder).pack(pady=8)
        self.output_label = tk.Label(files, text="Output: not selected", wraplength=760)
        self.output_label.pack()

        tk.Button(
            self.root,
            text="Generate Specification",
            width=32,
            height=2,
            command=self.generate
        ).pack(pady=20)

        self.status_label = tk.Label(self.root, text="Status: ready", fg="gray")
        self.status_label.pack()

        self.log = tk.Text(self.root, height=8, bg="#2b2b2b", fg="white", font=("Menlo", 11))
        self.log.pack(fill="both", padx=30, pady=10)

        self.write_log("AV Complectator started")

    def write_log(self, text):
        self.log.insert("end", text + "\n")
        self.log.see("end")

    def select_template(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            self.template_path = path
            self.template_label.config(text=f"Template: {path}")
            self.write_log(f"Template selected: {path}")

    def select_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.pdf_path = path
            self.pdf_label.config(text=f"PDF: {path}")
            self.write_log(f"PDF selected: {path}")

    def select_output_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.output_folder = path
            self.output_label.config(text=f"Output: {path}")
            self.write_log(f"Output folder selected: {path}")

    def generate(self):
        if not self.template_path:
            messagebox.showwarning("Warning", "Select Excel template first.")
            self.write_log("Error: Excel template not selected")
            return

        if not self.pdf_path:
            messagebox.showwarning("Warning", "Select Project PDF first.")
            self.write_log("Error: PDF not selected")
            return

        if not self.output_folder:
            messagebox.showwarning("Warning", "Select output folder first.")
            self.write_log("Error: output folder not selected")
            return

        self.write_log("PDF Engine started")
        pdf_engine = PDFEngine()
        pdf_info = pdf_engine.analyze_pdf(self.pdf_path)

        self.write_log(f"PDF loaded: {pdf_info['file_name']}")
        self.write_log(f"Pages found: {pdf_info['page_count']}")

        for page in pdf_info["pages"][:10]:
            self.write_log(f"Page {page['number']}: {page['first_line']}")

        if pdf_info["page_count"] > 10:
            self.write_log("Only first 10 pages shown in log")

        self.write_log("Template Engine started")
        engine = TemplateEngine()
        result_path = engine.copy_template(self.template_path, self.output_folder)

        self.write_log(f"Template copied: {result_path}")
        self.status_label.config(text="Status: PDF analyzed + template copied")

        messagebox.showinfo(
            "AV Complectator",
            f"PDF analyzed successfully.\n\nPages: {pdf_info['page_count']}\n\nTemplate copied:\n{result_path}"
        )