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
        title = self.document_title()
        periodo = self.periodo()

        if title:
            self.set_font("Arial", "B", 20)
            self.cell(0, 10, title, 0, 1, align="C")

        if periodo:
            self.set_font("Arial", "", 12)
            self.cell(0, 10, periodo, align="C")
     

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

    def create_pdf(self, filename: str, pages: list, image_path: str = None):
        self.add_page()

        if image_path:
          self.image(image_path, x=0, y=0, w=self.w, h=self.h)

        for page in range(pages):
            title, body, font, size = page
            self.page_title(title, font, size)
            self.page_body(body, font, size)

        self.output(filename)


def main():
    st.title("Generador de PDF")

    st.header(body="Configuración del PDF", anchor="config-pdf", help="Configura las opciones del documento", icon="📄", divider=True, width="stretch")

    pages_count = st.number_input("Cantidad de páginas", min_value=1, max_value=10, value=1)

    document_title = st.text_input("Título del documento", placeholder="Escribe el título...")

    upload_image = st.file_uploader("Sube una imagen para el documento", type=["jpg", "png"])

    col1, col2 = st.columns(2)
    month = col1.selectbox("Mes", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"])
    year = col2.selectbox("Año", list(range(2015, 2061)))

    periodo = f"{month} {year}"

    if st.button("Generar PDF"):
        st.write("Generando reporte...")

        image_path = None

        if upload_image:
            image_path = upload_image.name
            with open(image_path, "wb") as f:
                f.write(upload_image.getbuffer())

        pdf = PDFGenerator(document_title, periodo)

        pdf.create_pdf(filename="reporte.pdf", pages=pages_count, image_path=image_path)

if __name__ == "__main__":
    main()