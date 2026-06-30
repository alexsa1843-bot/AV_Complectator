import fitz


class PDFEngine:

    def get_info(self, pdf_path):
        doc = fitz.open(pdf_path)

        info = {
            "pages": len(doc),
            "width": doc[0].rect.width,
            "height": doc[0].rect.height
        }

        doc.close()

        return info