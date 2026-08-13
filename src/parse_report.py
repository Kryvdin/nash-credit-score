import sys

from pypdf import PdfReader

BUREAUS = {"EXPERIAN", "TRANSUNION", "EQUIFAX"}
SECTION_END_MARKER = "Note for testers"
HEADER_ROW = ["Creditor", "Item Type", "Opened", "Balance", "Status"]


def extract_text_from_pdf(source):
    """Extract raw text from a PDF. `source` may be a file path or a file-like object."""
    reader = PdfReader(source)
    page_texts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            page_texts.append(text)
    return "\n".join(page_texts)


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


def print_report(negative_items):
    total = sum(len(items) for items in negative_items.values())
    print("=" * 60)
    print("NASH CREDIT SCORE — Negative Item Report")
    print(f"{total} negative item(s) found across 3 bureaus")
    print("=" * 60)

    for bureau in ("EXPERIAN", "TRANSUNION", "EQUIFAX"):
        items = negative_items.get(bureau, [])
        label = "item" if len(items) == 1 else "items"
        print(f"\n{bureau} ({len(items)} {label})")
        print("-" * 60)
        if not items:
            print("  No negative items found.")
            continue
        for item in items:
            print(f"  * {item['creditor']}")
            print(f"    Type: {item['item_type']}  |  Opened: {item['opened']}  |  Balance: {item['balance']}")
            print(f"    Status: {item['status']}")
    print()


def main():
    pdf_path = sys.argv[1]

    text = extract_text_from_pdf(pdf_path)
    negative_items = parse_negative_items(text)
    print_report(negative_items)


if __name__ == "__main__":
    main()
