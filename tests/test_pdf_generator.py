import unittest
from src.pdf_generator import PDFGenerator

class TestPDFGenerator(unittest.TestCase):
    def test_generate_pdf(self):
        pdf_generator = PDFGenerator("Sample Title")
        title = "Sample Title"
        title2 = "Sample Titl"
        self.assertIsInstance(pdf_generator, PDFGenerator)
        self.assertEqual(pdf_generator.document_title(), title)
        self.assertNotEqual(pdf_generator.document_title(), title2)
    