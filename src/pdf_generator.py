
from fpdf import FPDF
import streamlit as st


class PDFGenerator(FPDF):
    def __init__(self, document_title: str, periodo: str):
        super().__init__(orientation="L", format="A4")
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
            self.cell(0, 10, periodo, 0, 1, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def page_title(self, page_num: int, page_title: str):
        self.set_font("Arial", "B", 12)
        # self.cell(0, 10, f"Pagina {page_num}: {page_title}", 0, 1, "L")
        self.ln(10)

    def page_body(self, expenses: list):
        self.set_font("Arial", "B", 8)

        widths = [20, 55, 55, 55, 55]

        headers = ["Fecha", "Detalle de gasto", "Monto", "Pago", ""]

        for width, header in zip(widths, headers):
            self.cell(width, 6, header, border=1, align="C")

        self.ln()

        self.set_font("Arial", "", 7)

        for expense in expenses:
            fecha, Detalle_de_gasto, monto, pago = expense

            values = [fecha, Detalle_de_gasto, str(monto), pago, ""]

            for width, value in zip(widths, values):
                self.cell(width, 5, str(value), border=1)

            self.ln()

    def create_pdf(self, filename: str, pages: list, image_path: str = None):

        for i, expenses in enumerate(pages, start=1):
            self.add_page()

            if image_path:
                self.image(image_path, x=0, y=0, w=self.w, h=self.h)
                self.header()

            self.page_title(i, "Detalle de gastos")
            self.page_body(expenses)

        self.output(filename)


def main():
    st.title("Generador de PDF")

    st.header(
        body="Configuración del PDF",
        anchor="config-pdf",
        help="Configura las opciones del documento",
        icon="📄",
        divider=True,
        width="stretch"
    )

    pages = []

    pages_count = st.number_input(
        "Cantidad de páginas",
        min_value=1,
        max_value=10,
        value=1,
        step=1
    )

    for i in range(pages_count):
        st.subheader(f"Página {i + 1}")

        expenses = []

        for j in range(25):
            st.write(f"Gasto {j + 1}")

            col1, col2, col3, col4, col5 = st.columns(
                [20, 55, 55, 55, 55]
            )

            fecha = col1.text_input(
                "Fecha",
                key=f"fecha_{i}_{j}"
            )

            Detalle_de_gasto = col2.text_input(
                "Detalle de gasto",
                key=f"Detalle_de_gasto_{i}_{j}"
            )

            monto = col3.text_input(
                "Monto",
                key=f"monto_{i}_{j}"
            )

            pago = col4.text_input(
                "Pago",
                key=f"pago_{i}_{j}"
            )

            expenses.append(
                (fecha, Detalle_de_gasto, monto, pago)
            )

        pages.append(expenses)

    document_title = st.text_input(
        "Título del documento",
        placeholder="Escribe el título..."
    )

    upload_image = st.file_uploader(
        "Sube una imagen para el documento",
        type=["jpg", "png"]
    )

    col1, col2 = st.columns(2)

    month = col1.selectbox(
        "Mes",
        ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    )

    year = col2.selectbox(
        "Año",
        list(range(2015, 2061))
    )

    periodo = f"{month} {year}"

    if st.button("Generar PDF"):
        st.write("Generando reporte...")

        image_path = None

        if upload_image:
            image_path = upload_image.name

            with open(image_path, "wb") as f:
                f.write(upload_image.getbuffer())

        pdf = PDFGenerator(document_title, periodo)

        pdf.create_pdf(
            filename="reporte.pdf",
            pages=pages,
            image_path=image_path
        )

        st.success("PDF generado correctamente.")

        with open("reporte.pdf", "rb") as f:
            st.download_button(
                "Descargar PDF",
                data=f,
                file_name="reporte.pdf",
                mime="application/pdf"
            )


if __name__ == "__main__":
    main()
