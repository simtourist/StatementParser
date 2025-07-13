# 🧾 Kaspi Bank Statement Parser

A Python tool for parsing **Kaspi Bank PDF statements** and converting them into structured **JSON** and **Excel (.xlsx)** files.  
Supports **Kazakh**, **Russian**, and **English** languages, and works with both raw `.pdf` and base64-encoded `.txt` inputs.


## 📦 Features

- 🧠 Auto-detects statement language (`KAZ`, `RUS`, `ENG`)
- 👤 Extracts full name, card number, and statement date range
- 💳 Parses detailed transactions: amount, type, date, and details
- 📄 Converts into:
  - Clean **JSON** structure
  - Structured **Excel file** ready for reporting or import

---

## 🗂 Project Structure

```

├── main.py             # CLI entrypoint
├── parser.py           # Core parsing logic
├── pdf\_to\_base64.py    # Utility: convert PDF → base64
├── excel\_writer.py     # Excel writing logic
├── utils.py            # Reusable helpers
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation

````

---

## 🚀 Quick Start (Local)

### 1. Install dependencies

```bash
pip install -r requirements.txt
````

### 2. Run with PDF:

```bash
python main.py --input ex.pdf
```

### 3. Run with base64 `.txt`:

```bash
python main.py --input sample_base64.txt
```

### Output files:

* `result.json` → contains parsed data
* `statementoutput.xlsx` → Excel summary of all transactions

---

## 🛠 Utility Script

### Convert a PDF to base64 `.txt`:

```bash
python pdf_to_base64.py /path/to/ex.pdf
```

Use this if you want to send the file in base64.

---

## 📑 Excel Output Columns

| Column                 | Description                               |
| ---------------------- | ----------------------------------------- |
| FROM\_DATE             | Start date of the statement               |
| TO\_DATE               | End date of the statement                 |
| STATEMENT\_LANGUAGE    | Statement language: KAZ / RUS / ENG       |
| FULL\_NAME             | Cardholder full name                      |
| FINANSIAL\_INSTITUTION | Always "Kaspi"                            |
| AMOUNT                 | Transaction amount (positive or negative) |
| DETAILS                | Transaction description/details           |
| OPERATION\_DATE        | Date of transaction                       |
| TRANSACTION\_TYPE      | Transaction category/type                 |
| CARD\_NUMBER           | Last 4 digits of card                     |
| INSERT\_DATE, etc.     | System metadata timestamps                |

---

## 📄 Sample JSON Output

```json
{
  "success": true,
  "data": {
    "financialInstitutionName": "Kaspi",
    "cardNumber": "7820",
    "fromDate": "12.06.2025",
    "toDate": "12.07.2025",
    "statementLanguage": "kaz",
    "fullName": "Asanov ...",
    "details": [
      {
        "amount": -10000.0,
        "operationDate": "2025-06-25",
        "transactionType": "Purchase",
        "details": "MEGA Shopping Mall"
      }
    ]
  }
}
```

---

## 📚 Dependencies

All dependencies are in `requirements.txt`:

* [`PyMuPDF`](https://pymupdf.readthedocs.io/) — PDF parsing engine
* [`openpyxl`](https://openpyxl.readthedocs.io/) — Excel export

Install with:

```bash
pip install -r requirements.txt
```

---

## 📥 Input Formats

| Format | Description                          |
| ------ | ------------------------------------ |
| `.pdf` | Raw Kaspi bank statement export      |
| `.txt` | Base64-encoded PDF (useful for APIs) |

---

## 💡 Further Suggestions

* ✅ Add unit tests (`unittest` or `pytest`) for `utils.py` and `parser.py`
* 🚀 Wrap into a **FastAPI** microservice with file upload
* 🧪 Add CI pipeline to auto-validate parser on new statements
* 🌐 Build a small web UI for drag & drop parsing

---
