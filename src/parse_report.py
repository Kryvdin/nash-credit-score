import sys

import pdfplumber


def main():
    pdf_path = sys.argv[1]

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            print(text)


if __name__ == "__main__":
    main()
