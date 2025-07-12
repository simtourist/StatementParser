import base64
import sys
import os

def convert_pdf_to_base64(pdf_path: str, output_path: str = "sample_base64.txt"):
    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return

    with open(pdf_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    with open(output_path, "w", encoding="utf-8") as out:
        out.write(encoded)

    print(f"✅ Base64 saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_base64.py yourfile.pdf [output.txt]")
    else:
        pdf_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else "sample_base64.txt"
        convert_pdf_to_base64(pdf_path, output_path)
