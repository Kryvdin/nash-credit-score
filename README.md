# Nash Credit Score

Nash Credit Score parses PDF credit reports and extracts negative items
(charge-offs, collections, delinquencies, etc.) grouped by bureau
(Experian, TransUnion, Equifax). It ships as both a command-line script
and a Streamlit web app.

## Live Demo

Try it now: [https://nash-credit-score.streamlit.app](https://nash-credit-score.streamlit.app)

Upload your own PDF credit report, or click "Load demo report" to try it
instantly with the bundled synthetic fixture — no installation required.

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

This opens the app in your browser at [http://localhost:8501](http://localhost:8501).

Upload a PDF credit report, or click "Load demo report" to try the bundled
synthetic fixture. Click "Analyze Report" to view the summary and negative
items table and download the results as CSV or JSON.

Uploaded PDFs are processed in memory only. They are never written to disk
and are discarded once analysis is complete.

### Command line

```bash
python src/parse_report.py path/to/report.pdf
```

This prints the extracted text followed by a formatted negative-item report
grouped by bureau.

## Project structure

- `src/parse_report.py` — PDF extraction and negative-item parsing shared by
  the CLI and web app.
- `app.py` — Streamlit web app entry point.
- `fixtures/synthetic-credit-report.pdf` — synthetic sample report for demos
  and testing.

## Built with Agent Orchestrator

This project was built using [Agent Orchestrator](https://aoagents.dev/) with
Claude Code agents for The Orchestra hackathon. AO was used to:

- Scaffold the Python project
- Build and debug the PDF parser
- Test parsing against the synthetic credit report
- Build and test the Streamlit web app
- Manage development through AO sessions, isolated Git worktrees, and the
  AO Kanban board
