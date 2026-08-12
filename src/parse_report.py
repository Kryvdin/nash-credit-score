import json
import re
import sys

from pypdf import PdfReader

BUREAUS = {"EXPERIAN", "TRANSUNION", "EQUIFAX"}
SECTION_END_MARKER = "Note for testers"
HEADER_LABELS = "Creditor Item Type Opened Balance Status"

ITEM_TYPES = ["Closed Account", "Charge-Off", "Collection", "Delinquent"]

ROW_RE = re.compile(
    r"^(?P<prefix>.+?)\s+(?P<opened>\d{2}/\d{4})\s+(?P<balance>\$[\d,]+)\s+(?P<status>.+)$"
)


def split_creditor_and_item_type(prefix):
    for item_type in ITEM_TYPES:
        if prefix.endswith(item_type):
            return prefix[: -len(item_type)].strip(), item_type
    return prefix.strip(), ""


def parse_negative_items(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    result = {}
    bureau = None
    for line in lines:
        if line in BUREAUS:
            bureau = line
            result[bureau] = []
            continue

        if line.startswith(SECTION_END_MARKER):
            bureau = None
            continue

        if bureau is None or line == HEADER_LABELS:
            continue

        match = ROW_RE.match(line)
        if not match:
            continue

        creditor, item_type = split_creditor_and_item_type(match.group("prefix"))
        result[bureau].append({
            "creditor": creditor,
            "item_type": item_type,
            "opened": match.group("opened"),
            "balance": match.group("balance"),
            "status": match.group("status"),
        })

    return result


def main():
    pdf_path = sys.argv[1]

    page_texts = []
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text = page.extract_text()
        print(text)
        if text:
            page_texts.append(text)

    negative_items = parse_negative_items("\n".join(page_texts))
    print(json.dumps(negative_items, indent=2))


if __name__ == "__main__":
    main()
