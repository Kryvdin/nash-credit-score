# Nash Credit Score

Nash Credit Score parses PDF credit reports and extracts negative items
(charge-offs, collections, delinquencies, etc.) grouped by bureau
(Experian, TransUnion, Equifax). It ships as both a command-line script
and a Streamlit web app.

## Installation

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Web app (Streamlit)

Launch the app:

```bash
streamlit run app.py
```

This opens the app in your browser (default: http://localhost:8501).
Upload a PDF credit report, or click "Load demo report" to try it with the
bundled synthetic fixture, then click "Analyze Report" to see the summary,
the negative items table, and download the results as CSV or JSON.

Uploaded PDFs are processed in memory only — they are never written to disk
and are discarded once analysis is complete.

### Command line

```bash
python src/parse_report.py path/to/report.pdf
```

This prints the raw extracted text followed by a formatted negative-item
report grouped by bureau.

## Project structure

- `src/parse_report.py` — PDF text extraction and negative-item parsing
  (shared by the CLI and the web app), plus the CLI entry point.
- `app.py` — Streamlit web app entry point.
- `fixtures/synthetic-credit-report.pdf` — synthetic (fake) sample report
  safe for demos and testing.
