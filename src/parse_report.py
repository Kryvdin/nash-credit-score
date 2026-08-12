import json
import sys

from pypdf import PdfReader

BUREAUS = {"EXPERIAN", "TRANSUNION", "EQUIFAX"}
SECTION_END_MARKER = "Note for testers"
HEADER_ROW = ["Creditor", "Item Type", "Opened", "Balance", "Status"]


def parse_negative_items(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    result = {}
    bureau = None
    i = 0
    while i < len(lines):
        line = lines[i]

        if line in BUREAUS:
            bureau = line
            result[bureau] = []
            i += 1
            continue

        if line.startswith(SECTION_END_MARKER):
            bureau = None
            i += 1
            continue

        if bureau is None:
            i += 1
            continue

        if lines[i:i + 5] == HEADER_ROW:
            i += 5
            continue

        if i + 5 <= len(lines):
            creditor, item_type, opened, balance, status = lines[i:i + 5]
            result[bureau].append({
                "creditor": creditor,
                "item_type": item_type,
                "opened": opened,
                "balance": balance,
                "status": status,
            })
            i += 5
        else:
            break

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
