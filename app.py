import io
import json
from pathlib import Path

import pandas as pd
import streamlit as st

from src.parse_report import extract_text_from_pdf, parse_negative_items

BUREAUS = ["EXPERIAN", "TRANSUNION", "EQUIFAX"]
TABLE_COLUMNS = ["Bureau", "Creditor", "Item Type", "Opened", "Balance", "Status"]
FIXTURE_PATH = Path(__file__).parent / "fixtures" / "synthetic-credit-report.pdf"

st.set_page_config(page_title="Nash Credit Score", page_icon="📄", layout="wide")


def items_to_dataframe(negative_items):
    rows = [
        {
            "Bureau": bureau.title(),
            "Creditor": item["creditor"],
            "Item Type": item["item_type"],
            "Opened": item["opened"],
            "Balance": item["balance"],
            "Status": item["status"],
        }
        for bureau in BUREAUS
        for item in negative_items.get(bureau, [])
    ]
    return pd.DataFrame(rows, columns=TABLE_COLUMNS)


def render_summary(negative_items):
    total = sum(len(items) for items in negative_items.values())
    columns = st.columns(4)
    columns[0].metric("Total Negative Items", total)
    for column, bureau in zip(columns[1:], BUREAUS):
        column.metric(bureau.title(), len(negative_items.get(bureau, [])))


def init_session_state():
    st.session_state.setdefault("negative_items", None)
    st.session_state.setdefault("source_label", None)
    st.session_state.setdefault("use_demo", False)


def main():
    init_session_state()

    st.title("Nash Credit Score")
    st.caption(
        "Upload a credit report PDF to extract and review negative items "
        "across Experian, TransUnion, and Equifax."
    )

    uploaded_file = st.file_uploader("Upload credit report (PDF)", type=["pdf"])
    demo_clicked = st.button("Load demo report (synthetic fixture)")

    if uploaded_file is not None:
        st.session_state.use_demo = False
    if demo_clicked:
        st.session_state.use_demo = True

    pdf_bytes = None
    source_label = None

    if uploaded_file is not None:
        pdf_bytes = uploaded_file.getvalue()
        source_label = uploaded_file.name
    elif st.session_state.use_demo:
        if FIXTURE_PATH.exists():
            pdf_bytes = FIXTURE_PATH.read_bytes()
            source_label = FIXTURE_PATH.name
        else:
            st.error("Demo fixture not found at fixtures/synthetic-credit-report.pdf.")

    if source_label:
        st.caption(f"Selected file: **{source_label}**")

    analyze_clicked = st.button("Analyze Report", type="primary", disabled=pdf_bytes is None)

    if analyze_clicked and pdf_bytes is not None:
        if len(pdf_bytes) == 0:
            st.error("The selected file is empty.")
        else:
            try:
                text = extract_text_from_pdf(io.BytesIO(pdf_bytes))
            except Exception as exc:
                st.error(f"Could not read this file as a PDF: {exc}")
                st.session_state.negative_items = None
            else:
                if not text.strip():
                    st.warning(
                        "No extractable text was found in this PDF. "
                        "It may be a scanned image without a text layer."
                    )
                    st.session_state.negative_items = None
                else:
                    negative_items = parse_negative_items(text)
                    if not negative_items:
                        st.warning(
                            "No Experian, TransUnion, or Equifax sections were "
                            "recognized in this report."
                        )
                    st.session_state.negative_items = negative_items
                    st.session_state.source_label = source_label
            # pdf_bytes and text are local to this run and are never persisted,
            # written to disk, or stored in session state.

    negative_items = st.session_state.negative_items
    if negative_items is not None:
        st.divider()
        st.subheader("Summary")
        render_summary(negative_items)

        st.subheader("Negative Items")
        df = items_to_dataframe(negative_items)
        if df.empty:
            st.info("No negative items to display.")
        else:
            st.dataframe(df, width="stretch", hide_index=True)

            csv_bytes = df.to_csv(index=False).encode("utf-8")
            json_bytes = json.dumps(negative_items, indent=2).encode("utf-8")

            col1, col2 = st.columns(2)
            col1.download_button(
                "Download CSV",
                data=csv_bytes,
                file_name="negative_items.csv",
                mime="text/csv",
            )
            col2.download_button(
                "Download JSON",
                data=json_bytes,
                file_name="negative_items.json",
                mime="application/json",
            )

    st.divider()
    st.caption(
        "Privacy: uploaded PDFs are processed in memory only. They are never "
        "written to disk and are discarded once analysis is complete."
    )


if __name__ == "__main__":
    main()
