from datetime import datetime
from pdf_parser import PDFParser
from utils import normalize_spaces, extract_field, detect_language_and_name, split_full_name, extract_dates, extract_transactions
import logging

logger = logging.getLogger(__name__)


class KaspiParser:
    def __init__(self, pdf_bytes: bytes):
        self.pdf_bytes = pdf_bytes
        self.raw_text = None
        self.data = {}

    def parse(self) -> dict:
        self.raw_text = PDFParser.extract_text(self.pdf_bytes)
        language, name_lines = detect_language_and_name(self.raw_text)
        full_name, surname, name, patronymic = split_full_name(language, name_lines)
        from_date, to_date = extract_dates(self.raw_text)
        card_number = extract_field(self.raw_text, [
            r"Card number:\s*\*?(\d+)",
            r"Номер карты:\s*\*?(\d+)",
            r"Карта нөмірі:\s*\*?(\d+)"
        ])
        acc_number = extract_field(self.raw_text, [
            r"Account number:([A-Z0-9]+)",
            r"Номер счета:\s*([A-Z0-9]+)",
            r"Шот нөмірі:\s*([A-Z0-9]+)"
        ])

        transactions = extract_transactions(self.raw_text)

        avg_incoming = [t["amount"] for t in transactions if t["amount"] > 0]
        avg_sum = sum(avg_incoming) / len(avg_incoming) if avg_incoming else 0

        self.data = {
            "financialInstitutionName": "Kaspi",
            "cardNumber": card_number,
            "fromDate": from_date.strftime("%d.%m.%Y"),
            "toDate": to_date.strftime("%d.%m.%Y"),
            "details": transactions,
            "metrics": {
                "from_date": from_date.isoformat(),
                "to_date": to_date.isoformat(),
                "statement_language": language,
                "name": name,
                "surname": surname,
                "patronymic": patronymic,
                "full_name": full_name,
                "fin_institut": "Kaspi",
                "card_number": f"*{card_number[-4:]}",
                "number_account": acc_number,
                "avg_sum": round(avg_sum, 2)
            },
            "statementLanguage": language,
            "fullName": full_name
        }

        return {
            "success": True,
            "msg": None,
            "msgType": None,
            "data": self.data
        }
