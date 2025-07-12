# utils.py

import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def normalize_spaces(text: str) -> str:
    """Removes multiple spaces and trims leading/trailing whitespace."""
    return re.sub(r"[ ]{2,}", " ", text).strip()


def extract_field(text: str, patterns: list[str], fallback: str = "") -> str:
    """
    Try to extract a field using multiple regex patterns.
    Returns first match found, or fallback.
    """
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            for group in match.groups():
                if group:
                    return group.strip()
    return fallback


def detect_language_and_name(text: str) -> tuple[str, list[str]]:
    """Detects the statement language and returns full name components."""
    match_en = re.search(r"Kaspi Gold.*?\n(.*?)\nCard number", text, re.DOTALL)
    if match_en:
        logger.info("✅ English format detected")
        lines = match_en.group(1).splitlines()
        return "eng", [normalize_spaces(line) for line in lines if line.strip()]

    if "по Kaspi Gold" in text and "Номер карты" in text:
        logger.info("✅ Russian format detected")
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if "Номер карты" in line:
                if i >= 1 and i + 2 < len(lines):
                    surname = lines[i - 1].strip()
                    name_patronymic = lines[i + 2].strip()
                    return "rus", [normalize_spaces(surname), normalize_spaces(name_patronymic)]

    if "Kaspi Gold бойынша" in text and "Карта нөмірі" in text:
        logger.info("✅ Kazakh format detected")
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if "Карта нөмірі" in line:
                if i >= 1 and i + 2 < len(lines):
                    surname = lines[i - 1].strip()
                    name_patronymic = lines[i + 2].strip()
                    return "kaz", [normalize_spaces(surname), normalize_spaces(name_patronymic)]

    logger.warning("❌ Language could not be detected")
    return "unknown", ["Unknown"]


def split_full_name(language: str, name_lines: list[str]) -> tuple[str, str, str, str]:
    """
    Splits full name into components: full_name, surname, name, patronymic
    """
    if language == "eng":
        parts = name_lines[-1].split()
        if len(parts) == 2:
            name, surname = parts
            return f"{surname} {name}", surname, name, ""
        return name_lines[-1], "", "", ""

    elif language in {"rus", "kaz"}:
        if len(name_lines) >= 2:
            surname = name_lines[0]
            name_parts = name_lines[1].split()
            name = name_parts[0] if len(name_parts) >= 1 else ""
            patronymic = name_parts[1] if len(name_parts) >= 2 else ""
            return f"{surname} {name} {patronymic}".strip(), surname, name, patronymic
        return name_lines[0], name_lines[0], "", ""

    return name_lines[0], "", "", ""


def extract_dates(text: str) -> tuple[datetime, datetime]:
    """
    Extracts the statement period (from_date, to_date) from the text.
    Supports English, Russian, and Kazakh.
    """
    match = re.search(
        r"period from (\d{2}\.\d{2}\.\d{2}) to (\d{2}\.\d{2}\.\d{2})"
        r"|с (\d{2}\.\d{2}\.\d{2}) по (\d{2}\.\d{2}\.\d{2})"
        r"|(\d{2}\.\d{2}\.\d{2})ж\. бастап (\d{2}\.\d{2}\.\d{2})ж",
        text
    )
    if not match:
        raise ValueError("❌ Couldn't find statement period in PDF text")

    dates = [d for d in match.groups() if d]
    return datetime.strptime(dates[0], "%d.%m.%y"), datetime.strptime(dates[1], "%d.%m.%y")


def find_transaction_start_index(lines: list[str]) -> int:
    """
    Heuristically finds where transaction records start by locating table headers.
    """
    headers = ["Дата", "Сумма", "Күні", "Сомасы", "Date", "Amount"]
    for i, line in enumerate(lines):
        if any(header in line for header in headers):
            return i + 1
    return 0


def extract_transactions(text: str) -> list[dict]:
    """
    Parses all transactions from the text and returns them as a list of dicts.
    Each transaction includes amount, operationDate, transactionType, and details.
    """
    lines = text.splitlines()
    start_idx = find_transaction_start_index(lines)
    transactions = []
    i = start_idx

    while i < len(lines) - 2:
        date_line = lines[i].strip()
        amount_line = lines[i + 1].strip()
        info_line = lines[i + 2].strip()

        if re.match(r"\d{2}\.\d{2}\.\d{2}", date_line[:8]):
            try:
                date_obj = datetime.strptime(date_line[:8], "%d.%m.%y").strftime("%Y-%m-%d")

                amount_match = re.match(r"([−\-+]?\s?[\d\s,]+)\s₸", amount_line)
                if not amount_match:
                    i += 1
                    continue

                raw_amount = amount_match.group(1)
                clean_amount = (
                    raw_amount.replace("−", "-")
                    .replace("–", "-")
                    .replace("+", "")
                    .replace(" ", "")
                    .replace(",", ".")
                )
                amount = float(clean_amount)
                signed_amount = amount if "-" not in raw_amount else -abs(amount)

                info_parts = re.sub(r"\s{2,}|\t+", "\t", info_line).split("\t")
                transaction_type = info_parts[0].strip() if len(info_parts) > 0 else ""
                details = info_parts[1].strip() if len(info_parts) > 1 else ""

                transactions.append({
                    "amount": signed_amount,
                    "operationDate": date_obj,
                    "transactionType": transaction_type,
                    "details": details
                })

                i += 3
            except Exception as e:
                logger.warning(f"⚠️ Failed block: {date_line} + {amount_line} → {e}")
                i += 1
        else:
            i += 1

    return transactions
