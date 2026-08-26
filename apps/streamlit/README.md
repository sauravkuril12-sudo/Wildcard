# Mastercard AI Defense Lab: Streamlit App

This directory contains the Python prototype for the closed-loop GenAI fraud engine.

## 🚀 Overview
Traditional rules-based fraud detection systems fail against modern Generative AI threats. The **Mastercard AI Defense Lab** is an end-to-end, closed-loop adversarial security prototype built to detect, simulate, and autonomously defend against advanced GenAI payment fraud vectors.

---

## Components

1. **`threat_profile.json`:** Defines the GenAI threat vectors.
2. **`data_generator.py`:** Generates deterministic payment transaction data.
3. **`defender_model.py`:** Trains the XGBoost classification model.
4. **`closed_loop.py`:** Applies firewall checks and enterprise decisions.
5. **`app.py`:** Provides the interactive Streamlit dashboard.
6. **`data/`:** Stores generated local data used by the dashboard.

## Run

From the repository root:

```text
pip install -r apps/streamlit/requirements.txt
streamlit run apps/streamlit/app.py
```

Run the file through Streamlit, not with `python app.py`. Direct Python execution is bare mode and will produce `missing ScriptRunContext` warnings.

---
*Built for the Mastercard Innovation Challenge @ GFF 2026.*