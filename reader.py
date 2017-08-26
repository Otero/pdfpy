from io import StringIO

from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.converter import TextConverter


class PDF:

    def __init__(self, metadata=None):
        self._pages = []
        self._metadata = metadata

    @property
    def number_of_pages(self):
        """
        Calculates the number of pages inside the PDF file.

        :return: number of pages in the PDF file
        :rtype: int
        """
        return len(self._pages)

    @property
    def metada(self):
        """
        Returns metadata related with the PDF file
        """
        return self._metadata

    @property
    def pages(self):
        """
        Returns all the pages inside the PDF document
        """
        return self._pages

    def append_page(self, page):
        """
        Appends a new page at the end of the PDF object.

        :page: Page object which is expected to be appended to the PDF file
        """
        self._pages.append(page)


class PDFReader(object):
    def __init__(self, file_object, password=''):
        self.pdf_document = PDFDocument()

        self.parser = PDFParser(file_object)
        self.parser.set_document(self.pdf_document)

        self.pdf_document.set_parser(self.parser)
        self.pdf_document.initialize(password)

        if self.pdf_document.is_extractable:

            self.resource_manager = PDFResourceManager()
            self.text_converter = TextConverter(
                self.resource_manager,
                outfp=StringIO()
            )
            self.interpreter = PDFPageInterpreter(
                self.resource_manager,
                self.text_converter
            )
            self.pdf = PDF(metadata=self.pdf_document.info)

            for page in self.pdf_document.get_pages():
                self.pdf.append_page(self.interpreter.process_page(page))

    def get_text(self):
        """
        Returns the text of the PDF as a single string
        """
        return ''.join(self.pdf.pages)
