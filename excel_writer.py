from openpyxl import Workbook
from datetime import datetime

class KaspiReportGenerator:
    def __init__(self, data: dict):
        self.data = data

    def write_excel(self, filename: str):
        wb = Workbook()
        ws = wb.active
        ws.title = "KaspiStatement"

        headers = [
            "FROM_DATE", "TO_DATE", "STATEMENT_LANGUAGE", "FULL_NAME", "FINANSIAL_INSTITUTION",
            "AMOUNT", "DETAILS", "OPERATION_DATE", "TRANSACTION_TYPE", "INSERT_DATE",
            "CARD_NUMBER", "ST_CREATION_DATE", "ST_MODIFIED_DATE", "ST_SUBJECT", "ST_AUTHOR",
            "ST_TITLE", "ST_PRODUCER"
        ]
        ws.append(headers)

        now = datetime.now().isoformat()

        for trx in self.data["details"]:
            ws.append([
                self.data["fromDate"],
                self.data["toDate"],
                self.data["statementLanguage"].upper(),
                self.data["fullName"],
                self.data["financialInstitutionName"],
                trx["amount"],
                trx["details"],
                trx["operationDate"],
                trx["transactionType"],
                now,
                self.data["cardNumber"],
                now,
                now,
                "Kaspi Bank Statement",
                self.data["fullName"],
                f"Kaspi statement from {self.data['fromDate']} to {self.data['toDate']}",
                "KaspiBank"
            ])

        wb.save(filename)
