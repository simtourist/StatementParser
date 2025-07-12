import fitz
import logging

logger = logging.getLogger(__name__)

class PDFParser:
    @staticmethod
    def extract_text(pdf_bytes: bytes) -> str:
        try:
            doc = fitz.open("pdf", pdf_bytes)
            text = "\n".join(page.get_text() for page in doc)
            logger.info(f"📄 Extracted text from {len(doc)} pages")
            return text
        except Exception as e:
            logger.exception("❌ PDF text extraction failed")
            raise

