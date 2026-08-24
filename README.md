# Mastercard AI Defense Lab: Closed-Loop GenAI Fraud Engine
**Mastercard Innovation Challenge 2026**

## 🚀 Overview
Traditional rules-based fraud detection systems fail against modern Generative AI threats. The **Mastercard AI Defense Lab** is an end-to-end, closed-loop adversarial security prototype built to detect, simulate, and autonomously defend against advanced GenAI payment fraud vectors.

---

## 🛠️ Project Architecture & Components
1. **`threat_profile.json` (Identify):** Codifies advanced GenAI threat vectors.
2. **`data_generator.py` (Generate):** Simulates 20,000 realistic payment transaction records (`master_payment_simulation.csv`).
3. **`defender_model.py` (Defend):** Optimized XGBoost classification engine achieving 1.0000 ROC-AUC.
4. **`closed_loop.py` (Adapt):** Automated adversarial feedback loop and self-hardening engine.
5. **`app.py`:** Interactive Streamlit UI Dashboard for live evaluation.

---
*Built for the Mastercard Innovation Challenge @ GFF 2026.*