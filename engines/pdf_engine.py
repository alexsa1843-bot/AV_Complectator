from pathlib import Path
import fitz


class PDFEngine:

    def analyze_pdf(self, pdf_path: str):
        pdf = Path(pdf_path)

        if not pdf.exists():
            raise FileNotFoundError(f"PDF not found: {pdf}")

        document = fitz.open(pdf)

        pages = []

        for page_index in range(document.page_count):
            page = document.load_page(page_index)
            text = page.get_text("text").strip()
            first_line = text.split("\n")[0] if text else "No text found"

            pages.append({
                "number": page_index + 1,
                "first_line": first_line[:120]
            })

        result = {
            "file_name": pdf.name,
            "page_count": document.page_count,
            "pages": pages
        }

        document.close()

        return result