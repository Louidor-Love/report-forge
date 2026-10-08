from fpdf import FPDF


class PDFGenerator(FPDF):
    def __init__(self, document_title: str):
        super().__init__()
        self._document_title = document_title

    def document_title(self) -> str:
        return self._document_title

    def header(self):
        if hasattr(self, "document_title"):
            title = self.document_title()

        if title:
            self.set_font("Arial", "B", 20)
            self.cell(0, 10, title, 0, 1, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def chapter_title(self, chapter_num: int, chapter_title: str):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"Chapter {chapter_num}: {chapter_title}", 0, 1, "L")
        self.ln(10)

    def chapter_body(self, body_text: str):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, body_text)
        self.ln(10)

    def create_pdf(self, filename: str, documente_title: str, image_path = None):
        pdf = PDFGenerator(documente_title)
        pdf._document_title = documente_title
        pdf.add_page()
        if image_path:
            pdf.image(image_path, x=0, y=0, w=pdf.w, h=pdf.h)
        pdf.output(filename)