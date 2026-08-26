# Mastercard AI Defense Lab

Python/Streamlit dashboard for closed-loop GenAI payment-fraud defense.

## Run

```text
pip install -r apps/streamlit/requirements.txt
streamlit run apps/streamlit/app.py
```

Run the Streamlit file with `streamlit run`; do not launch it with `python app.py`, because direct Python execution runs outside Streamlit's script context and produces `missing ScriptRunContext` warnings.

The app stores its generated CSV and local inspection-history database in `apps/streamlit/data/`. These are local runtime files, not source code.
