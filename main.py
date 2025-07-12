import argparse
import base64
import json
import logging
from pathlib import Path

from kaspi_parser import KaspiParser
from excel_writer import KaspiReportGenerator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    parser = argparse.ArgumentParser(description="📊 Kaspi Bank PDF Parser")
    parser.add_argument("--input", "-i", required=True, help="Input file (.pdf or .txt)")
    parser.add_argument("--output-excel", "-x", default="statementoutput.xlsx")
    parser.add_argument("--output-json", "-j", default="result.json")
    args = parser.parse_args()

    path = Path(args.input)
    if not path.exists():
        logging.error("❌ Input file does not exist.")
        return

    try:
        if path.suffix.lower() == ".pdf":
            pdf_bytes = path.read_bytes()
        elif path.suffix.lower() == ".txt":
            pdf_bytes = base64.b64decode(path.read_text(encoding="utf-8"))
        else:
            logging.error("❌ Invalid file type. Use .pdf or .txt")
            return

        parser = KaspiParser(pdf_bytes)
        result = parser.parse()

        if not result["success"]:
            logging.error(f"❌ Parsing failed: {result['msgType']}: {result['msg']}")
            return


        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        # Save Excel
        KaspiReportGenerator(result["data"]).write_excel(args.output_excel)

        logging.info(f"✅ JSON → {args.output_json}")
        logging.info(f"✅ Excel → {args.output_excel}")
        logging.info(f"📊 {len(result['data']['details'])} transactions extracted")

    except Exception as e:
        logging.exception("❌ Unexpected error")

if __name__ == "__main__":
    main()
