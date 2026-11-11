from fpdf import FPDF
import streamlit as st


class PDFGenerator(FPDF):
    def __init__(self, document_title: str, periodo: str):
        super().__init__()
        self._document_title = document_title
        self._periodo = periodo

    def document_title(self) -> str:
        return self._document_title

    def periodo(self) -> str:
        return self._periodo

    def header(self):
        if hasattr(self, "document_title", "periodo"):
            title = self.document_title()
            periodo = self.periodo()

        if title:
            self.set_font("Arial", "B", 20)
            self.cell(0, 10, title, 0, 1, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def page_title(self, page_num: int, page_title: str):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"Pagina {page_num}: {page_title}", 0, 1, "L")
        self.ln(10)

    def page_body(self, body_text: str):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, body_text)
        self.ln(10)

    def create_pdf(self, filename: str, documente_title: str, pages, image_path = None):
        pdf = PDFGenerator(documente_title)
        pdf._document_title = documente_title
        pdf.add_page()
        if image_path:
            pdf.image(image_path, x=0, y=0, w=pdf.w, h=pdf.h)

        for page in pages:
            title, body, font, size   = page
            pdf.page_title(title, font, size)
            pdf.page_body (body, font, size)

        pdf.output(filename)

def main():
    st.title ("Generador de PDF ")
    st.header(body="Configuración del PDF", anchor="config-pdf", help="Configura las opciones del documento", icon="📄", divider=True, width="stretch")
    pages = []
    pages_count = st.number_input("cantidad de paginas",min_value=1, max_value=10,value=1)
    st.text_input("Titulo Del Documento","Escribe el titulo..")
    st.file_uploader("sube una imagen para el documento",type = ["jpg", "png"])
    col1, col2 = st.columns(2)
    month = col1.selectbox("Mes", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"])
    year = col2.selectbox("Año", list(range(2015, 2061)))
    if st.button("Generar PDF"):
        st.write("Generando reporte...")
    

if __name__ == "__main__":
    main()